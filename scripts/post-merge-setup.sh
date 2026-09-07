#!/usr/bin/env bash
set -euo pipefail

# The owner-local application uses the Python standard library; no package
# installation or build is required after merging. Keep this hook limited to
# checkout validation. Run application tests explicitly per AGENTS.md.
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

git rev-parse --show-toplevel >/dev/null
git diff --check

if git diff --quiet && git diff --cached --quiet; then
  printf 'Post-merge setup passed: clean, valid Git checkout.\n'
else
  printf 'Post-merge setup passed: Git checkout contains reviewed changes.\n'
fi