# Main protection audit

The scheduled Monday and manual `Main protection audit` workflow reads the live
GitHub settings for `OKHP3/Glee-fullyTools-FoundRy` on `main`. It fails if the
classic branch rule no longer requires at least one approval, stops dismissing
stale reviews, loses the `Validate manifest` check or its up-to-date requirement,
stops enforcing admins, or permits force pushes or deletion. It also checks
that the `github-pages` environment retains deployment branch restrictions and
that a custom branch policy, when used, permits `main`. An unreadable API
response fails the job as **incomplete**, not as a pass. No settings are changed.

**Activation:** This workflow runs after it is merged into the default branch.
The built-in `GITHUB_TOKEN` is tried, but it may not have permission to read
branch protection. If the job reports HTTP 403, configure a repository Actions
secret named `REPO_SETTINGS_READ_TOKEN` with a fine-grained, repository-scoped
credential with **Administration: read** permission (and the required
Metadata: read access). Do not paste tokens into code, logs, or issue comments.
The secret is available only to the scheduled/manual job, never to PR code.
The separate PR job runs offline tests without an audit credential.

An older settings receipt in `docs/repo-settings-review/protection-receipt.json`
records **zero** required approvals, and `docs/repo-settings-recap.md` explains
the earlier solo-owner choice. This new task specifies **at least one**: the
audit will fail until that policy is explicitly approved and applied by the
repository owner. This change does **not** update the live rule. Failures
appear in GitHub Actions and are subject to the repository owner's Actions
notification preferences. Run `workflow_dispatch` after configuring access
to confirm that the scheduled job can read settings and alerts as expected.

This is a periodic check of the classic branch rule and one deployment
environment, not a complete audit of inherited rulesets or all environments.
It does not attest to delivery of email notifications. If `main` is renamed
or the required check/environment changes intentionally, update the checker
and its tests together.