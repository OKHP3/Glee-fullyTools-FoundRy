# Coop-pertition integration review

Date: September 7, 2026. Takeover coordinator: Codex thread
`01a07e88-5641-7df1-8d13-4ce8402c56de`.

## FoundRy batch one

Accepted from the workers' committed tips: F01, F02, F03, F04, F05, F06, F08,
F09, F10, F11, F12, F14, F15, F16, F17, F18, F19, and F20. Their assigned additions were
cherry-picked onto `codex/coop-pertition-integration`; the stale worker bases
were not allowed to replace the program register.

Checks on that source revision:

- `python3 -m unittest discover -s app/tests -v`: 69 tests passed.
- `python3 scripts/verify-foundry-backup.py`: completed successfully.
- `python3 scripts/validate-skills-shelf.py app/data/skills.json`: completed
  successfully.
- `git diff --check origin/main...HEAD`: clean.

The suite emitted one `ResourceWarning` for an unclosed SQLite connection in
the F08 boundary test. The assertions passed, but that warning is a follow-up
test-hygiene finding, not evidence of an application defect.

## Pending or excluded FoundRy work

- F07: correction requested for an EOF whitespace failure from `git diff --check`.
- F09: correction requested to remove host-specific driver paths.
- F10: correction requested so unavailable browsers report `NOT RUN` and the
  temporary fixture does not claim a pass.
- F13: no committed deliverable at review time.
- F13: no committed deliverable was available at the initial review point. Its
  worker source evidence must be reconciled before assigning a final disposition.
- F17: correction requested to remove a machine-specific path from the proposal.

## Addendum: pilot import review correction

The initial exclusion of F11, F12, and F14 was incorrect. The UI deliberately
wraps a raw imported project as `{ "project": imported.project || imported }`
before it calls `/api/import`. Re-testing each raw fixture with that same request
shape created all three temporary projects successfully and retained every
acceptance case as `not-run`. The drafts are accepted as synthetic pilot kits.

All pilot fixtures are synthetic and are not production, canon, PME, or external
platform evidence. F15, F16, and F17 remain proposals only; no runtime/schema
design has been adopted.

## Final disposition, September 8, 2026

The earlier pending notes above are preserved as review history. This table is
the final disposition and supersedes those intermediate states.

| Tasks | Disposition | Integrated evidence |
| --- | --- | --- |
| F01-F08 | Accepted regression and validation coverage | FoundRy PR #9, merged `53caa7e8`; local application suite: 71 tests passed. F08 also emitted one SQLite `ResourceWarning`, retained as test-hygiene follow-up. |
| F09-F10 | Accepted browser journeys | F09 portability correction `392ccc4`; F10 missing-browser path reports `NOT RUN`, exit 0, rather than a pass. Neither is external-browser or deployment proof. |
| F11-F14 | Accepted synthetic pilot kits | UI-equivalent temporary imports using `{ "project": raw }` succeeded; all acceptance observations remain `not-run`. F13 was recovered from its task evidence as the workflow pilot, merged in FoundRy PR #10. |
| F15-F18 | Accepted documentation proposals and mentoring packet | Proposal-only material; it does not alter canon, schema, runtime, or readiness. F17 correction `1dfc574` removed a machine-specific path. |
| F19-F20 | Accepted handoff and recovery QA material | F20 is a browser runner whose unavailable-driver result is `NOT RUN`; it is not a browser pass. |
| W01-W05 | Accepted website tests and documentation | Website PR #35, merged `c89d6ee2`; local focused page and universe tests plus site validation and link checks passed. |
| W06 | Accepted diagnostic regression runner, not a green accessibility result | Reclassified to `scripts/tests/foundry-accessibility-qa.mjs` so it is a test rather than a top-level script. Bundled Playwright ran: 10 checks passed and focus visibility failed at 320px and 390px for the “WHY GLEE-FULLY” navigation link. The finding is documented for `assets/css/theme.css`; no production CSS changed. Missing-runtime and loopback-unavailable paths emit structured `NOT RUN` with exit status 2. |

### Publication and cleanup

- FoundRy PR #9 merged `53caa7e8c1114c98481d1521086aa60846990dbc` and PR #10
  merged `2f9ca53df464310c655fa060e843483d05e61320`.
- Website PR #35 merged `c89d6ee29562682c9abfb36448d20c5d87f09efe` after site
  validation, i18n, sparkle, resilience, and viewport checks passed.
- The owner main checkouts were fast-forwarded and verified clean by the parent
  coordinator. This record does not claim Replit receipt or external deployment
  parity.
- The original W06 top-level-runner commit is retained as lineage. The W03 worker
  worktree's unrelated generated audit mutation is deliberately preserved, not
  staged or deleted. No claim is made that every worker branch or worktree was
  removed.

### Reviewed worker tips and integrated heads

Worker tips are provenance. “Integrated head” names a corrective integration
commit where a worker tip was absent or could not be used unchanged.

| ID | Reviewed tip or integrated head | Final location |
| --- | --- | --- |
| F01-F06 | `e8cb590`, `974d8f5`, `9041bea`, `791346f`, `e8696d0`, `0cf9551` | FoundRy PR #9 |
| F07-F10 | `042f2f9`, `4bd2f9b`, `392ccc4`, `3d57f19` | FoundRy PR #9 |
| F11-F14 | `adad252`, `ba63e8b`, integrated `8b4cdf3`, `9aac639` with fixture lineage `1a98a3b` | FoundRy PR #10 |
| F15-F20 | `422b030`, `48f73b5`, `1dfc574`, `7def02e`, `1d59080`, `816f460` | FoundRy PR #9 |
| W01-W05 | `449b047`, `dbfcccff`, `c6a1228` plus `8f5fdcf`, `8256e8c`, `51444d0` | Website PR #35 |
| W06 | Original `647af1f` preserved; reclassified runner integrated on Website PR #35 | Website PR #35 |
