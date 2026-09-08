#!/usr/bin/env python3
"""Validate the pinned Skillz shelf used by app/data/skills.json.

Checks the shelf records for:
- the expected object-list schema
- unique, safe identifiers
- HTTPS source URLs
- pinned full-length Git revisions

Exit status:
- 0 when the shelf is valid
- 1 when any problem is found
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


EXPECTED_KEYS = {"id", "name", "description", "url", "sourcePath", "revision"}
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
FULL_REVISION_RE = re.compile(r"^[0-9a-f]{40}$")


class ValidationError:
    def __init__(self, path: str, message: str):
        self.path = path
        self.message = message

    def format(self) -> str:
        return f"[{self.path}] {self.message}"


def load_shelf(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_shelf(shelf) -> list[ValidationError]:
    errors: list[ValidationError] = []

    if not isinstance(shelf, list):
        return [ValidationError("(root)", "expected a list of skill records")]

    seen_ids: set[str] = set()
    for index, item in enumerate(shelf):
        path = f"[{index}]"
        if not isinstance(item, dict):
            errors.append(ValidationError(path, "expected an object record"))
            continue

        keys = set(item)
        missing = EXPECTED_KEYS - keys
        extra = keys - EXPECTED_KEYS
        if missing:
            errors.append(ValidationError(path, f"missing keys: {', '.join(sorted(missing))}"))
        if extra:
            errors.append(ValidationError(path, f"unexpected keys: {', '.join(sorted(extra))}"))

        if not missing:
            skill_id = item["id"]
            name = item["name"]
            description = item["description"]
            url = item["url"]
            source_path = item["sourcePath"]
            revision = item["revision"]

            if not isinstance(skill_id, str) or not skill_id:
                errors.append(ValidationError(f"{path}.id", "must be a non-empty string"))
            elif not SAFE_ID_RE.fullmatch(skill_id):
                errors.append(ValidationError(f"{path}.id", "must be a safe string using letters, digits, dot, underscore, colon or hyphen"))
            elif skill_id in seen_ids:
                errors.append(ValidationError(f"{path}.id", f"duplicate shelf id {skill_id!r}"))
            else:
                seen_ids.add(skill_id)

            if not isinstance(name, str) or not name.strip():
                errors.append(ValidationError(f"{path}.name", "must be a non-empty string"))
            if not isinstance(description, str) or not description.strip():
                errors.append(ValidationError(f"{path}.description", "must be a non-empty string"))
            if not isinstance(url, str) or not url.strip():
                errors.append(ValidationError(f"{path}.url", "must be a non-empty string"))
            else:
                parsed = urlparse(url)
                if parsed.scheme != "https" or not parsed.netloc:
                    errors.append(ValidationError(f"{path}.url", "must use https:// with a hostname"))

            if not isinstance(source_path, str) or not source_path.strip():
                errors.append(ValidationError(f"{path}.sourcePath", "must be a non-empty string"))
            elif source_path.startswith(("/", "\\")) or ".." in source_path.split("/"):
                errors.append(ValidationError(f"{path}.sourcePath", "must be a safe relative path"))

            if not isinstance(revision, str) or not FULL_REVISION_RE.fullmatch(revision):
                errors.append(ValidationError(f"{path}.revision", "must be a pinned 40-character lowercase Git revision"))

    return errors


def run(path: Path) -> int:
    try:
        shelf = load_shelf(path)
    except FileNotFoundError:
        print(f"ERROR: shelf file not found: {path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {path}: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: could not read {path}: {exc}", file=sys.stderr)
        return 1

    errors = validate_shelf(shelf)
    if errors:
        print(f"ERROR: {path} has {len(errors)} problem(s)", file=sys.stderr)
        for error in errors:
            print(f"  - {error.format()}", file=sys.stderr)
        return 1

    print(f"OK: {path} passed skill shelf validation")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the pinned Skillz shelf used by app/data/skills.json.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="app/data/skills.json",
        help="Path to the shelf JSON file (default: app/data/skills.json)",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    return run(Path(args.path))


if __name__ == "__main__":
    raise SystemExit(main())
