---
name: GitHub sync authentication
description: Local Git can use the Replit secret helper when the authorized GitHub connection cannot be bound to this Repl.
---

When the GitHub connection is authorized but cannot be assigned to the current Repl, local Git remains the reliable sync path: keep `origin` credential-free and use a temporary secret-backed credential helper for each network command.

**Why:** The connector may return a permission-denied assignment error even though the repository credential is valid; persisting a token in `.git/config` creates unnecessary exposure.

**How to apply:** Verify the repository owner and default branch, sanitize the remote URL, use a non-persisting helper for pull/fetch/push, and verify `HEAD...origin/main` after each operation. Never print or commit the credential.