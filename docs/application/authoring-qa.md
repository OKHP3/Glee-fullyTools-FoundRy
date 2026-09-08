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
Chrome-for-Testing binary, and removes the temporary database on completion.
Evidence screenshots and the exported synthetic JSON remain in a temporary
directory printed as `EVIDENCE` for the duration of local review.

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
`NOT RUN` and does not claim browser evidence. It does not install dependencies.
The browser driver and binary are environment-provided prerequisites, not
application dependencies. Their installation location is intentionally not
encoded in this public repository.

This is a local acceptance smoke journey, not proof of external deployment,
multi-browser compatibility, publication readiness, or PME certification.
