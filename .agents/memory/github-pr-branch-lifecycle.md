---
name: GitHub PR branch lifecycle
description: A merged pull request may have its head branch deleted automatically, so refresh the default branch before trying to recover the feature ref.
---

A missing remote feature branch after a pull request closes is not evidence that its commits were lost. First inspect the pull request's merged state and refresh `origin/main`; the integrated commit may already be the current default-branch tip.

**Why:** GitHub can delete a pull request's head branch after merge, while a stale local remote-tracking ref still makes the old branch appear expected.

**How to apply:** Do not recreate or force-push a deleted branch until the PR state and default-branch SHA are verified. If the PR is merged, use a fast-forward-only pull of the default branch and continue from there.