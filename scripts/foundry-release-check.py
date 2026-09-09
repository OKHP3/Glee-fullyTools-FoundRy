#!/usr/bin/env python3
"""Run the owner-local FoundRy release gate without publishing anything."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(label: str, command: list[str]) -> bool:
    print(f"CHECK {label}")
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode:
        print(f"FAIL  {label} (exit {result.returncode})")
        return False
    print(f"PASS  {label}")
    return True


def main() -> int:
    checks = [
        ("Python API and boundary suite", [sys.executable, "-m", "unittest", "discover", "-s", "app/tests"]),
        ("Python syntax", [sys.executable, "-m", "py_compile", "app/server.py"]),
        ("Browser JavaScript syntax", ["node", "--check", "app/static/app.js"]),
        ("Browser acceptance runner syntax", ["node", "--check", "scripts/foundry-authoring-qa.mjs"]),
        ("Whitespace", ["git", "diff", "--check"]),
    ]
    passed = all(run(label, command) for label, command in checks)
    if passed:
        print("RELEASE GATE PASSED: local checks only; no deployment or publication was performed.")
        return 0
    print("RELEASE GATE FAILED: fix the checks above before treating this workbench change as releasable.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())