---
name: Fail-closed CLI status
description: Preserve process failure status for command-line validators and import checks
---

Command-line validators that return a failure status must propagate it through the
process exit code; printing an error while calling `main()` directly can make a
failed check appear successful to automation.

**Why:** Automated checks use the process status, not stderr content, to decide
whether a fail-closed validation step passed.

**How to apply:** Use an entry-point wrapper that exits with the return value of
the command dispatcher whenever a validation or import failure is expected to
stop the command.