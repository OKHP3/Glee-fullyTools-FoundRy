---
name: Python package installation
description: The Replit shell's system Python is externally managed under PEP 668.
---

Use the package-management tooling for local Python dependencies instead of invoking
pip directly against the system interpreter. GitHub Actions runners remain
responsible for installing repository requirements in CI workflows.

**Why:** Direct pip installation is rejected by the managed system environment before
the command can run, while the repository's CI commands are intended for a disposable
runner.

**How to apply:** For local validation, first use the package-management skill and
reuse already-installed modules when available. Keep CI dependency installation
explicit in the workflow with `python -m pip install -r requirements.txt`.