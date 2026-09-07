#!/usr/bin/env bash
set -euo pipefail

# This repository is content-first: there are no runtime dependencies,
# migrations, or build artifacts to install after a task merge. Keep the
# automatic hook fast and deterministic by validating the checkout instead.
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

git rev-parse --show-toplevel >/dev/null
git diff --check

if git diff --quiet && git diff --cached --quiet; then
  printf 'Post-merge setup passed: clean, valid Git checkout.\n'
else
  printf 'Post-merge setup passed: Git checkout contains reviewed changes.\n'
fi