# Error recovery browser QA

This is a focused regression runner for the application states most likely to
lose a person's work: a failed save, a stale revision conflict, invalid JSON
import and attempted navigation with unsaved edits.

Run it from the repository root:

```bash
node scripts/foundry-error-recovery-qa.mjs
```

The runner creates a temporary SQLite data directory, starts the Python service
on an ephemeral loopback port, places a small loopback proxy in front of it to
inject one failed save, and removes the temporary data when it exits. It uses
the installed Playwright Chromium driver when available. If the driver cannot
be imported, it reports `NOT RUN` and exits successfully so a missing tool is
not mistaken for a passing browser check.

The browser assertions verify that:

- a failed save shows the truthful service error, keeps the edited text and
  re-enables the controls;
- a stale revision shows the explicit conflict, keeps the local edit and
  re-enables the controls;
- malformed import JSON reports the parse error without replacing the current
  draft and recovers from busy state;
- navigation while dirty opens the warning, and choosing “Keep editing” keeps
  the unsaved text.

The runner does not modify `app/static/app.js`. A `FINDING` is a reproducible
browser defect and exits non-zero. Existing API tests remain separate from this
installed-driver check.
