# Coop-pertition integration review

Date: September 7, 2026. Takeover coordinator: Codex thread
`01a07e88-5641-7df1-8d13-4ce8402c56de`.

## FoundRy batch one

Accepted from the workers' committed tips: F01, F02, F03, F04, F05, F06, F08,
F09, F10, F15, F16, F18, F19, and F20. Their assigned additions were
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
- F11, F12, F14: the initial pilot fixtures were raw project objects. The actual
  `/api/import` contract requires a `{ "project": ... }` envelope, so these drafts
  are preserved on their worker branches and excluded pending corrected fixtures
  with temporary import/export proof.
- F17: correction requested to remove a machine-specific path from the proposal.

All pilot fixtures are synthetic and are not production, canon, PME, or external
platform evidence. F15, F16, and F17 remain proposals only; no runtime/schema
design has been adopted.
