#!/usr/bin/env node
/**
 * Repeatable browser smoke journey for the owner-local FoundRy application.
 * Uses only an already-installed playwright-core and browser binary.
 */
import { createRequire } from "node:module";
import { mkdtemp, rm, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawn } from "node:child_process";
import net from "node:net";

const require = createRequire(import.meta.url);
const root = new URL("..", import.meta.url).pathname;
const projectName = "F09 synthetic authoring draft";

function loadPlaywright() {
  const candidates = [process.env.PLAYWRIGHT_CORE_PATH, "playwright-core"].filter(Boolean);
  for (const candidate of candidates) {
    try { return require(candidate); } catch (_) { /* try the next installed location */ }
  }
  return null;
}

function assert(condition, message) {
  if (!condition) throw new Error(`ASSERTION FAILED: ${message}`);
}

async function freePort() {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.once("error", reject);
    probe.listen(0, "127.0.0.1", () => {
      const port = probe.address().port;
      probe.close(() => resolve(port));
    });
  });
}

async function waitForServer(page, url) {
  for (let attempt = 0; attempt < 30; attempt += 1) {
    try {
      await page.goto(url, { waitUntil: "load", timeout: 2000 });
      return;
    } catch (error) {
      if (attempt === 29) throw error;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
}

async function main() {
  const playwright = loadPlaywright();
  if (!playwright) {
    console.log("NOT RUN: installed playwright-core driver was not found; no browser proof claimed.");
    return;
  }
  const executablePath = playwright.chromium.executablePath();
  const { access } = await import("node:fs/promises");
  try { await access(executablePath); } catch (_) {
    console.log(`NOT RUN: browser binary was not found at ${executablePath}; no browser proof claimed.`);
    return;
  }

  const dataDir = await mkdtemp(join(tmpdir(), "foundry-f09-data-"));
  const evidenceDir = await mkdtemp(join(tmpdir(), "foundry-f09-evidence-"));
  const port = await freePort();
  const server = spawn("python3", ["-m", "app.server", "--port", String(port), "--data-dir", dataDir], {
    cwd: root,
    stdio: ["ignore", "pipe", "pipe"],
  });
  const serverErrors = [];
  server.stderr.on("data", chunk => serverErrors.push(String(chunk)));
  let browser;
  try {
    browser = await playwright.chromium.launch({ executablePath, headless: true });
    const context = await browser.newContext({ acceptDownloads: true, viewport: { width: 1280, height: 900 } });
    const page = await context.newPage();
    const browserErrors = [];
    page.on("console", message => {
      // The source intentionally has no favicon route. Ignore that browser-generated
      // noise while retaining application console errors and warnings.
      if (message.text() === "Failed to load resource: the server responded with a status of 404 (Not Found)") return;
      if (["error", "warning"].includes(message.type())) browserErrors.push(`${message.type()}: ${message.text()}`);
    });
    page.on("pageerror", error => browserErrors.push(`pageerror: ${error.message}`));
    const url = `http://127.0.0.1:${port}/`;
    await waitForServer(page, url);

    assert(await page.title() === "Glee-fully FoundRy", "page identity has the FoundRy title");
    assert((await page.locator("body").innerText()).includes("Make room for the next useful thing."), "initial screen is not blank");
    assert(await page.locator("#connection").innerText() === "Local service ready", "loopback service reports ready");
    await page.screenshot({ path: join(evidenceDir, "01-initial.png"), fullPage: false });

    await page.locator("#new-button").click();
    await page.locator("#template-dialog").waitFor({ state: "visible" });
    await page.locator('#template-dialog [data-template="custom-gpt"]').click();
    await page.locator("#editor").waitFor({ state: "visible" });
    assert((await page.locator("#project-title").innerText()) === "Untitled Custom GPT", "template creates an editable project");

    await page.locator('[name="name"]').fill(projectName);
    await page.locator('[name="description"]').fill("Synthetic browser journey for repeatable authoring evidence.");
    await page.locator('[name="audience"]').fill("Synthetic QA reviewer");
    await page.locator('[name="inputs"]').fill("A temporary browser journey");
    await page.locator('[name="outputs"]').fill("A saved and portable draft");
    await page.locator('[name="constraints"]').fill("Loopback only; synthetic data; no external calls.");
    await page.locator('[name="instructions"]').fill("Create, edit, save, reopen, export and import this draft.");
    assert((await page.locator("#save-button").innerText()).includes("changes"), "editing marks the draft dirty");
    await page.locator("#save-button").click();
    await page.getByRole("status").filter({ hasText: "Saved locally." }).waitFor({ state: "visible" });
    assert((await page.locator("#project-meta").innerText()).includes("Revision 2"), "save advances the visible revision");
    await page.screenshot({ path: join(evidenceDir, "02-saved.png"), fullPage: false });

    await page.reload({ waitUntil: "load" });
    await page.locator(`.project-card:has-text("${projectName}")`).first().click();
    await page.locator('[name="name"]').waitFor({ state: "visible" });
    assert(await page.locator('[name="name"]').inputValue() === projectName, "reopen restores the saved name");
    assert(await page.locator('[name="description"]').inputValue() === "Synthetic browser journey for repeatable authoring evidence.", "reopen restores the saved description");
    assert((await page.locator("#project-meta").innerText()).includes("Revision 2"), "reopen restores the saved revision");

    await page.getByRole("button", { name: "Review" }).click();
    const downloadPromise = page.waitForEvent("download");
    await page.getByRole("button", { name: "JSON", exact: true }).click();
    const download = await downloadPromise;
    const exportPath = join(evidenceDir, "exported-project.json");
    await download.saveAs(exportPath);
    const exported = JSON.parse(await readFile(exportPath, "utf8"));
    assert(exported.name === projectName, "JSON export preserves the saved project name");
    assert(exported.revision === 2, "JSON export preserves the saved revision");
    await page.getByRole("status").filter({ hasText: "JSON download prepared" }).waitFor({ state: "visible" });

    await page.locator("#import-file").setInputFiles(exportPath);
    await page.getByRole("status").filter({ hasText: "Imported as a fresh draft" }).waitFor({ state: "visible" });
    assert(await page.locator('[name="name"]').inputValue() === projectName, "import displays the exported project values");
    assert((await page.locator("#project-meta").innerText()).includes("Revision 1"), "import creates a fresh revision identity");
    assert(await page.locator(".project-card").count() === 2, "import persists a second project in the visible library");
    await page.screenshot({ path: join(evidenceDir, "03-imported.png"), fullPage: false });

    await page.reload({ waitUntil: "load" });
    assert(await page.locator(".project-card").count() === 2, "reload preserves both created and imported projects");
    await page.locator(`.project-card:has-text("${projectName}")`).first().click();
    await page.waitForFunction(name => document.querySelector('[name="name"]')?.value === name, projectName);
    assert(await page.locator('[name="name"]').inputValue() === projectName, "reopen after reload preserves imported values");
    assert((await page.locator("#project-meta").innerText()).includes("Revision 1"), "reopen after reload preserves imported revision");
    assert(browserErrors.length === 0, `browser console is clean (${browserErrors.join(" | ")})`);
    await writeFile(join(evidenceDir, "result.json"), JSON.stringify({
      status: "PASS", sourceSha: process.env.FOUNDRY_SOURCE_SHA || "not-provided", url,
      evidenceDir, checks: ["create", "edit", "save", "reopen", "export", "import", "reload persistence", "console health"],
    }, null, 2));
    console.log(`PASS: browser authoring journey completed against ${url}`);
    console.log(`EVIDENCE: ${evidenceDir}`);
  } catch (error) {
    console.error(`FAIL: ${error.message}`);
    if (serverErrors.length) console.error(`SERVER: ${serverErrors.join("").trim()}`);
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close().catch(() => {});
    server.kill("SIGTERM");
    await new Promise(resolve => server.once("exit", resolve));
    await rm(dataDir, { recursive: true, force: true });
    // Keep evidence local for review. It is intentionally outside the repository.
  }
}

main().catch(error => { console.error(`FAIL: ${error.stack || error}`); process.exitCode = 1; });
