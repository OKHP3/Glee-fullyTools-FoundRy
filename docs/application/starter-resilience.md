# Exported web-tool starter resilience

## Purpose

This record covers the exported web-tool starter only. It uses a synthetic
temporary project, exports the actual ZIP from the FoundRy application, serves
the extracted package on loopback, and checks the rendered package in Chromium.
It does not modify `app/server.py` or claim that a domain-specific web tool is
implemented by the generic starter.

## Reusable check

From the repository root, run:

```bash
node scripts/foundry-starter-qa.mjs
```

The runner uses Node's built-in WebSocket support and an installed Chromium or
Chrome binary. Set `CHROME_BIN` when the browser is installed at another path.
If no browser is available, it reports `NOT RUN` and exits with status 2. It
creates temporary data, uses ephemeral loopback ports, and does not add
dependencies or retain the exported package.

## Evidence

Run on 2026-09-07 from base `32b89159293bba2edc0c9b308b716ab20e234b5d`:

- PASS: the actual exported ZIP loaded in Chromium.
- PASS: add rendered one record.
- PASS: complete changed the action to `Reopen` and applied the done state.
- PASS: open and completed filters returned the expected records.
- PASS: reopen restored the open state.
- PASS: reload preserved the record through browser storage.
- PASS: malformed storage showed the documented recovery message.
- PASS: unavailable storage showed the same documented recovery message.

These checks distinguish supported behavior from defects. No shared-runtime
defect was reproduced, so no fix location or out-of-scope runtime patch is
proposed. Server-level export coverage remains in `app/tests/test_server.py`.

## Boundaries

This is browser behavior evidence for the generic starter, not production
readiness, accessibility certification, cross-browser coverage, or proof of a
published web tool. Browser-unavailable environments should be reported as
NOT RUN rather than treated as a pass.
