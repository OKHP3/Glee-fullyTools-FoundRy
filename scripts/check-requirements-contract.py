#!/usr/bin/env python3
"""Check the manifest validator requirements contract without third-party imports."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REQUIREMENTS = ROOT / "requirements.txt"
MANIFEST_VALIDATOR_DEPENDENCIES = {"pyyaml", "jsonschema"}
# Import names do not always match their distribution names. Keep these
# exceptions next to the requirement-name normalization used by all checks.
IMPORT_TO_DISTRIBUTION_ALIASES = {"yaml": "pyyaml"}
REQUIREMENT_LINE = re.compile(
    r"^(?P<name>[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)"
    r"(?=(?:\[|\s|[<>=!~]|$))"
    r"(?:\[(?P<extras>[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?"
    r"(?:\s*,\s*[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)*)\]|(?!\[))"
    r"(?P<specifier>.*)$"
)
EXACT_PIN = re.compile(r"^==\s*(?![=<>!~])[^;\s]+(?:\s*;\s*.+)?$")
HASH_OPTIONS = re.compile(r"\s+--hash=\S+")


def canonical_requirement_name(name: str) -> str:
    """Return the normalized name used for requirement duplicate checks."""

    return re.sub(r"[-_.]+", "-", name).lower()


def requirement_name_for_import(import_name: str) -> str:
    """Return the canonical requirement name for an import's distribution."""

    distribution_name = IMPORT_TO_DISTRIBUTION_ALIASES.get(import_name, import_name)
    return canonical_requirement_name(distribution_name)


def parse_requirement_entries(
    path: Path,
) -> tuple[list[tuple[int, str, str]], list[str]]:
    """Parse package entries and report malformed requirement lines."""

    entries: list[tuple[int, str, str]] = []
    errors: list[str] = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue

        match = REQUIREMENT_LINE.fullmatch(HASH_OPTIONS.sub("", line).strip())
        if match is None:
            errors.append(
                f"line {line_number} is not a supported package requirement: {line}; "
                "use a package name with an exact == version pin"
            )
            continue

        entries.append(
            (
                line_number,
                canonical_requirement_name(match.group("name")),
                match.group("specifier").strip(),
            )
        )

    return entries, errors


def requirements_contract_errors(path: Path) -> list[str]:
    """Report requirement entries that break the manifest validator contract."""

    entries, errors = parse_requirement_entries(path)
    names = [name for _, name, _ in entries]
    for name in sorted(set(names)):
        if names.count(name) > 1:
            errors.append(f"duplicate requirement name: {name}")

    for dependency in sorted(MANIFEST_VALIDATOR_DEPENDENCIES):
        matching_entries = [
            (line_number, specifier)
            for line_number, name, specifier in entries
            if name == dependency
        ]
        if not matching_entries:
            errors.append(f"missing manifest validator dependency: {dependency}")
            continue
        for line_number, specifier in matching_entries:
            if not EXACT_PIN.fullmatch(specifier):
                errors.append(
                    f"{dependency} on line {line_number} must use an exact == pin"
                )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check requirements.txt before installing manifest validator dependencies."
    )
    parser.add_argument("--requirements", type=Path, default=DEFAULT_REQUIREMENTS)
    args = parser.parse_args(argv)

    try:
        errors = requirements_contract_errors(args.requirements)
    except OSError as error:
        print(f"FAIL unable to read requirements contract: {error}")
        return 1

    if errors:
        print("FAIL manifest validator requirements contract:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK manifest validator requirements contract: {args.requirements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())