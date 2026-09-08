#!/usr/bin/env node
/* Focused browser regression runner for error and recovery states. */
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { once } from 'node:events';

const results = [];
const record = (name, status, detail) => { results.push({ name, status, detail }); console.log(`${status.padEnd(8)} ${name}${detail ? `: ${detail}` : ''}`); };
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const waitFor = async (fn, timeout = 5000, interval = 50) => {
  const end = Date.now() + timeout;
  while (Date.now() < end) { try { const value = await fn(); if (value) return value; } catch (_) {} await new Promise(resolve => setTimeout(resolve, interval)); }
  throw new Error('timed out waiting for expected state');
};
const listen = server => new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', () => resolve(server.address().port)); });

let playwright;
try { playwright = await import('playwright'); }
catch (_) { console.log('NOT RUN  Browser driver unavailable: install/use an installed Playwright driver to execute browser assertions.'); process.exitCode = 2; }

if (playwright) {
  const executablePath = playwright.chromium.executablePath();
  if (!existsSync(executablePath)) {
    console.log(`NOT RUN  Browser executable unavailable at ${executablePath}; install/use an installed Playwright browser to execute browser assertions.`);
    process.exitCode = 2;
  } else {
  const root = fileURLToPath(new URL('..', import.meta.url));
  const dataDir = await mkdtemp(join(tmpdir(), 'foundry-error-recovery-'));
  const appPortServer = createServer();
  const appPort = await listen(appPortServer); appPortServer.close();
  const app = spawn('python3', ['-m', 'app.server', '--port', String(appPort), '--data-dir', dataDir], { cwd: root, stdio: ['ignore', 'pipe', 'pipe'] });
  const { request: httpRequest } = await import('node:http');
  const proxy = createServer();
  proxy.on('request', (req, res) => {
    if (req.url === '/__qa__/fail-next-save') { proxy.failNextSave = true; res.writeHead(204); return res.end(); }
    const headers = { ...req.headers, host: `127.0.0.1:${appPort}` };
    if (proxy.failNextSave && req.method === 'PUT' && req.url.startsWith('/api/projects/')) { proxy.failNextSave = false; res.writeHead(503, { 'content-type': 'application/json' }); return res.end(JSON.stringify({ error: 'synthetic save outage' })); }
    const upstream = httpRequest({ hostname: '127.0.0.1', port: appPort, path: req.url, method: req.method, headers }, response => { res.writeHead(response.statusCode, response.headers); response.pipe(res); });
    upstream.on('error', error => { res.writeHead(502); res.end(String(error)); }); req.pipe(upstream);
  });
  const proxyPort = await listen(proxy);
  const browser = await playwright.chromium.launch({ headless: true });
  const page = await browser.newPage();
  try {
    await page.goto(`http://127.0.0.1:${proxyPort}/`, { waitUntil: 'domcontentloaded' });
    await waitFor(() => page.locator('#connection').textContent().then(text => text.includes('ready')));
    assert((await page.title()) === 'Glee-fully FoundRy', 'unexpected page title');
    assert((await page.locator('body').innerText()).includes('Make room for the next useful thing.'), 'page is blank');

    await page.locator('#new-button').click(); await page.locator('[data-template="custom-gpt"]').first().click();
    await waitFor(() => page.locator('#editor').isVisible());
    const name = page.locator('[name="name"]'); await name.fill('Recovery draft');
    await page.request.get(`http://127.0.0.1:${proxyPort}/__qa__/fail-next-save`);
    await page.locator('#save-button').click();
    await waitFor(() => page.locator('#message').isVisible() && page.locator('#message').textContent().then(t => t.includes('synthetic save outage')));
    assert(await name.inputValue() === 'Recovery draft', 'failed save discarded draft text');
    assert(await page.locator('#save-button').isEnabled(), 'busy state did not recover after failed save');
    record('failed save preserves draft and recovers busy state', 'PASS');

    await page.locator('#save-button').click(); await waitFor(() => page.locator('#message').textContent().then(t => t.includes('Saved locally')));
    const projectId = await page.locator('.project-card').first().getAttribute('data-id');
    const current = await page.evaluate(async id => (await fetch(`/api/projects/${id}`)).json(), projectId);
    const changed = { ...current, name: 'Changed elsewhere' }; delete changed.id; delete changed.schemaVersion; delete changed.createdAt; delete changed.updatedAt;
    await page.evaluate(async ({ id, payload }) => fetch(`/api/projects/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json', 'X-Foundry-Request': '1' }, body: JSON.stringify(payload) }), { id: projectId, payload: changed });
    await name.fill('Stale local edit'); await page.locator('#save-button').click();
    await waitFor(() => page.locator('#message').textContent().then(t => t.includes('revision conflict')));
    assert(await name.inputValue() === 'Stale local edit', 'revision conflict discarded local edit');
    assert(await page.locator('#save-button').isEnabled(), 'busy state did not recover after conflict');
    record('stale revision keeps local edit and shows explicit conflict', 'PASS');

    const invalid = join(dataDir, 'invalid-project.json'); await writeFile(invalid, '{ not project json');
    await page.locator('#import-button').click();
    await page.locator('#import-file').setInputFiles(invalid);
    await waitFor(() => page.locator('#message').textContent().then(t => t.includes('Unexpected token')));
    assert(await name.inputValue() === 'Stale local edit', 'invalid import replaced current draft');
    assert(await page.locator('#save-button').isEnabled(), 'busy state did not recover after invalid import');
    record('invalid import preserves current draft and recovers busy state', 'PASS');

    await name.fill('Unsaved navigation check'); await page.locator('#new-button').click();
    await waitFor(() => page.locator('#confirm-dialog').isVisible());
    assert((await page.locator('#confirm-dialog').innerText()).includes('Leave this draft?'), 'navigation warning did not appear');
    await page.locator('#confirm-dialog [value="cancel"]').click();
    assert(await name.inputValue() === 'Unsaved navigation check', 'cancel navigation discarded edits');
    record('unsaved navigation warns and cancel preserves edits', 'PASS');
  } catch (error) {
    record('browser recovery assertions', 'FINDING', error.message);
    process.exitCode = 1;
  } finally {
    await browser.close(); proxy.close(); app.kill('SIGTERM'); await rm(dataDir, { recursive: true, force: true });
  }
  }
}
