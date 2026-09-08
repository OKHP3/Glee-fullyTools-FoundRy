#!/usr/bin/env node
import assert from 'node:assert/strict';
import { execFileSync, spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { mkdtemp, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import net from 'node:net';

const root = resolve(join(fileURLToPath(import.meta.url), '..', '..'));
const chromeCandidates = process.env.CHROME_BIN
  ? [process.env.CHROME_BIN]
  : ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'];
const chrome = chromeCandidates.find((candidate) => existsSync(candidate));
const waitMs = 5000;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function freePort() {
  const server = net.createServer();
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const port = server.address().port;
  await new Promise((resolve) => server.close(resolve));
  return port;
}
async function waitFor(url, predicate = (response) => response.ok, method = 'GET') {
  const deadline = Date.now() + waitMs;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(url, { method });
      if (predicate(response)) return response;
    } catch (_) { /* The loopback service may still be starting. */ }
    await sleep(100);
  }
  throw new Error(`Timed out waiting for ${url}`);
}
function stop(child) {
  if (child && child.exitCode === null) child.kill('SIGTERM');
}
async function cdp(wsUrl) {
  const socket = new WebSocket(wsUrl);
  const pending = new Map();
  let nextId = 0;
  socket.addEventListener('message', (event) => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) reject(new Error(JSON.stringify(message.error))); else resolve(message.result);
    }
  });
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve, { once: true });
    socket.addEventListener('error', reject, { once: true });
  });
  const call = (method, params = {}) => new Promise((resolve, reject) => {
    const id = ++nextId;
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
  const evaluate = async (expression) => (await call('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true, userGesture: true })).result?.value;
  return { call, evaluate, close: () => socket.close() };
}
async function browserPage(staticUrl, profile, sourceScript) {
  const debugPort = await freePort();
  const browser = spawn(chrome, ['--headless=new', '--no-sandbox', '--disable-gpu', '--no-first-run', '--no-default-browser-check', `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`], { stdio: 'ignore' });
  try {
    const targetResponse = await waitFor(`http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent(staticUrl)}`, (response) => response.ok, 'PUT');
    const { webSocketDebuggerUrl } = await targetResponse.json();
    const page = await cdp(webSocketDebuggerUrl);
    await page.call('Page.enable');
    await page.call('Runtime.enable');
    if (sourceScript) await page.call('Page.addScriptToEvaluateOnNewDocument', { source: sourceScript });
    await page.call('Page.navigate', { url: staticUrl });
    await page.evaluate(`new Promise((resolve) => { const ready = () => document.readyState === 'complete' ? resolve(true) : setTimeout(ready, 20); ready(); })`);
    return { browser, page };
  } catch (error) {
    stop(browser);
    throw error;
  }
}
function expect(value, message) {
  assert.equal(value, true, message);
}
async function run() {
  if (!chrome) {
    console.log('NOT RUN browser assertions: no Chromium/Chrome binary found; set CHROME_BIN to run them');
    process.exitCode = 2;
    return;
  }
  const temp = await mkdtemp(join(tmpdir(), 'foundry-starter-qa-'));
  const dataDir = join(temp, 'data');
  const appPort = await freePort();
  const app = spawn('python3', ['-m', 'app.server', '--port', String(appPort), '--data-dir', dataDir], { cwd: root, stdio: 'ignore' });
  let staticServer;
  let browser;
  try {
    await waitFor(`http://127.0.0.1:${appPort}/api/health`);
    const project = { name: 'F10 synthetic garden notes', kind: 'web-tool', description: 'Synthetic browser QA only', audience: 'QA', inputs: 'Notes', outputs: 'Records', constraints: 'Temporary', instructions: 'Exercise the starter.', components: [{ id: 'core', name: 'Records', purpose: 'Keep records', dependsOn: [] }], tests: [{ id: 'browser', name: 'Browser flow', expected: 'Records can be managed', actual: '', status: 'not-run' }], skillIds: [] };
    const created = await (await fetch(`http://127.0.0.1:${appPort}/api/projects`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Foundry-Request': '1' }, body: JSON.stringify(project) })).json();
    const zip = await (await fetch(`http://127.0.0.1:${appPort}/api/projects/${created.id}/export?format=zip`)).arrayBuffer();
    const zipPath = join(temp, 'starter.zip');
    await writeFile(zipPath, Buffer.from(zip));
    execFileSync('unzip', ['-q', zipPath, '-d', join(temp, 'package')]);
    const staticPort = await freePort();
    staticServer = spawn('python3', ['-m', 'http.server', String(staticPort), '--bind', '127.0.0.1'], { cwd: join(temp, 'package'), stdio: 'ignore' });
    const staticUrl = `http://127.0.0.1:${staticPort}/index.html`;
    await waitFor(staticUrl);

    const normal = await browserPage(staticUrl, join(temp, 'normal'));
    browser = normal.browser;
    const page = normal.page;
    expect(await page.evaluate(`document.title === 'F10 synthetic garden notes'`), 'exported HTML should load');
    await page.evaluate(`(() => { const input = document.querySelector('#record-text'); input.value = 'Compost checklist'; document.querySelector('#record-form').requestSubmit(); })()`);
    expect(await page.evaluate(`document.querySelectorAll('#records li').length === 1 && document.querySelector('#records li').textContent.includes('Compost checklist')`), 'add should render a record');
    await page.evaluate(`document.querySelector('#records button').click()`);
    expect(await page.evaluate(`document.querySelector('#records li').className === 'done' && document.querySelector('#records button').textContent === 'Reopen'`), 'complete should mark the record done');
    await page.evaluate(`document.querySelector('#filter-open').click()`);
    expect(await page.evaluate(`document.querySelectorAll('#records li').length === 0`), 'open filter should hide completed records');
    await page.evaluate(`document.querySelector('#filter-done').click()`);
    expect(await page.evaluate(`document.querySelectorAll('#records li').length === 1`), 'completed filter should show completed records');
    await page.evaluate(`document.querySelector('#records button').click()`);
    await page.evaluate(`document.querySelector('#filter-all').click()`);
    expect(await page.evaluate(`document.querySelector('#records li').className === '' && document.querySelector('#records button').textContent === 'Complete'`), 'reopen should restore an open record');
    await page.call('Page.reload');
    await sleep(100);
    expect(await page.evaluate(`document.querySelectorAll('#records li').length === 1 && document.querySelector('#records li').textContent.includes('Compost checklist')`), 'reload should preserve records');
    page.close();
    stop(browser); browser = null;

    const malformed = await browserPage(staticUrl, join(temp, 'malformed'));
    browser = malformed.browser;
    await malformed.page.evaluate(`localStorage.setItem('foundry-records-${created.id}', '{not-json')`);
    await malformed.page.call('Page.reload');
    await sleep(100);
    expect(await malformed.page.evaluate(`document.querySelector('#message').textContent === 'Saved records were unreadable; a new list is ready.'`), 'malformed storage should produce the documented recovery message');
    malformed.page.close();
    stop(browser); browser = null;

    const unavailable = await browserPage(staticUrl, join(temp, 'unavailable'), `Object.defineProperty(window, 'localStorage', { configurable: true, get() { throw new Error('storage unavailable'); } });`);
    browser = unavailable.browser;
    expect(await unavailable.page.evaluate(`document.querySelector('#message').textContent === 'Saved records were unreadable; a new list is ready.'`), 'unavailable storage should produce the documented recovery message');
    unavailable.page.close();
    stop(browser); browser = null;
    console.log('PASS exported ZIP browser flow: add, complete, open filter, completed filter, reopen, reload');
    console.log('PASS malformed localStorage recovery message');
    console.log('PASS unavailable localStorage recovery message');
  } finally {
    stop(browser); stop(staticServer); stop(app);
  }
}
run().catch((error) => { console.error(`FAIL ${error.message}`); process.exitCode = 1; });
