# Repeatable browser authoring QA

This is the F09 smoke journey for the owner-local application. It uses synthetic
temporary data and a temporary loopback server. It does not write `.foundry-data/`
or any repository-tracked application data.

## Run

From the repository root:

```bash
FOUNDRY_SOURCE_SHA="$(git rev-parse HEAD)" node scripts/foundry-authoring-qa.mjs
```

The runner first uses normal Node module resolution. If the already-installed
driver is outside the module search path, provide its module path explicitly:

```bash
PLAYWRIGHT_CORE_PATH="/path/to/already-installed/playwright-core" \
  FOUNDRY_SOURCE_SHA="$(git rev-parse HEAD)" node scripts/foundry-authoring-qa.mjs
```

The runner selects a free loopback port, starts `python3 -m app.server` with a
temporary SQLite directory, launches an already-installed Playwright-compatible
Chrome-for-Testing binary, and removes the temporary database on completion. Set
`CHROME_BIN` when the environment provides Chromium separately from the
Playwright driver, for example:

```bash
CHROME_BIN="/repl/tools/bin/chromium" \
  FOUNDRY_SOURCE_SHA="$(git rev-parse HEAD)" node scripts/foundry-authoring-qa.mjs
```
Evidence screenshots and the exported synthetic JSON remain in a temporary
directory printed as `EVIDENCE` for the duration of local review.

## Opt-in GitHub Actions run

In the repository's Actions tab, start **FoundRy browser journey (opt-in)** via
**Run workflow**. This job is separate from the application API and structural
checks; it does not run on pushes or pull requests. On a GitHub-hosted Ubuntu
runner, it installs an isolated, pinned Playwright driver (`1.55.0`) and its
matching Chromium with system libraries. The runner uses a temporary SQLite
directory, which it deletes afterward. No browser dependency is added to the
application.

The job summary reports `PASS`, `NOT RUN`, or `FAIL`. Download the
`foundry-browser-evidence` artifact from the workflow run for `result.txt`,
`journey.log` and, when the browser started, a `foundry-f09-evidence-*`
directory containing screenshots, exported synthetic JSON, and `result.json`
on success. The log prints the temporary `EVIDENCE` path, and `result.json`
includes the checked-out source SHA. If the driver or Chromium cannot be
installed or the script exits 2, the job reports `NOT RUN` without claiming
browser proof. If prerequisites are available but a browser assertion fails,
the job reports `FAIL` and fails the opt-in workflow only.

## Journey and assertions

The actual browser flow is:

`app loads -> create Custom GPT from template -> edit visible fields -> save ->
reload and reopen -> export JSON -> import JSON -> reload and reopen imported draft`

The runner asserts the page title, meaningful initial content, local-service
status, visible revision changes, dirty-state feedback, saved field values after
reopen, JSON export contents, fresh imported revision identity, two persisted
library entries after import, reload persistence, and browser console health.
All interactions use real browser locators and downloads. There is no substitute
DOM simulation or direct API-only claim.

## Availability boundary

If `playwright-core` or its browser binary is not installed, the runner reports
`NOT RUN`, exits with status 2, and does not claim browser evidence. It does not
install dependencies.
The browser driver and binary are environment-provided prerequisites for local
runs, not application dependencies. The CI job installs its own isolated pair.

This is a local acceptance smoke journey, not proof of external deployment,
multi-browser compatibility, publication readiness, or PME certification.
