#!/usr/bin/env python3
"""Audit a FoundRy manifest.yaml for required governance fields."""
from __future__ import annotations
import pathlib
import re
import sys

REQUIRED_TOKENS = [
    "schema_version:",
    "repo:",
    "name:",
    "display_name:",
    "type:",
    "lifecycle_status:",
    "visibility:",
    "brand:",
    "author:",
]
VALID_STATUSES = {"spark", "research", "concept", "prototype", "capability", "productizing", "product", "active", "archived", "deprecated"}

def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def value(text: str, key: str) -> str:
    m = re.search(rf"^\s*{re.escape(key)}:\s*\"?([^\n\"]*)\"?\s*$", text, re.M)
    return m.group(1).strip() if m else ""


def nested_value(text: str, parent: str, child: str) -> str:
    """Read a simple child key without requiring a YAML runtime dependency."""
    lines = text.splitlines()
    parent_pattern = re.compile(rf"^(\s*){re.escape(parent)}:\s*(?:#.*)?$")
    child_pattern = re.compile(rf"^\s+{re.escape(child)}:\s*\"?([^\n\"]*)\"?\s*$")
    for index, line in enumerate(lines):
        match = parent_pattern.match(line)
        if not match:
            continue
        parent_indent = len(match.group(1).expandtabs(2))
        for candidate in lines[index + 1:]:
            if candidate.strip() and len(candidate) - len(candidate.lstrip()) <= parent_indent:
                break
            child_match = child_pattern.match(candidate)
            if child_match:
                return child_match.group(1).strip()
    return ""


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    path = root / "manifest.yaml"
    if not path.exists():
        print("FAIL manifest.yaml missing")
        return 1
    text = read(path)
    missing = [t for t in REQUIRED_TOKENS if t not in text]
    if missing:
        print("FAIL missing required manifest tokens:")
        for item in missing:
            print(f"  - {item}")
        return 1
    if not nested_value(text, "brand", "domain"):
        print("FAIL missing required manifest field: brand.domain")
        return 1
    status = value(text, "lifecycle_status")
    if status and status not in VALID_STATUSES:
        print(f"WARN lifecycle_status not in known set: {status}")
    print("OK manifest.yaml baseline fields present")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
