#!/usr/bin/env python3
"""Check the canonical inventory catalog path and scaffold integration."""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path


CATALOG_PATH = Path("inventory/inventory-of-toolbox-tools-and-tool-ettes.md")
MIGRATION_LEDGER_PATH = Path("docs/filename-migration-ledger.md")
SCAFFOLD_PATH = Path(
    ".agents/skills/glee-fully-repo-standardizer/scripts/scaffold.py"
)

# These are the seven maintained documentation references created by the catalog
# rename. Keep the expected counts explicit so a moved catalog cannot silently
# lose one of its indexes.
DOCUMENTED_REFERENCES = {
    Path("README.md"): (CATALOG_PATH.name, 1),
    Path("docs/agent-skill-conversion-strategy.md"): (CATALOG_PATH.as_posix(), 1),
    Path("docs/filename-migration-ledger.md"): (CATALOG_PATH.as_posix(), 1),
    Path("inventory/README.md"): (CATALOG_PATH.name, 2),
    Path("prompts/README.md"): (CATALOG_PATH.as_posix(), 1),
    Path("web-templates/README.md"): (CATALOG_PATH.as_posix(), 1),
}
DOCUMENTED_REFERENCE_COUNT = sum(
    expected_count for _, expected_count in DOCUMENTED_REFERENCES.values()
)
EXECUTED_MARKER = re.compile(r"\bexecuted\b", re.IGNORECASE)
INTENTIONAL_RETENTION_MARKERS = (
    "intentional retention",
    "intentionally retained",
    "legacy path retained",
    "old path retained",
    "retain legacy path",
    "retain the legacy path",
    "source-material retention",
)


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _load_scaffold(path: Path):
    module_name = "glee_fully_catalog_scaffold_check"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _backtick_path(cell: str) -> str | None:
    match = re.fullmatch(r"\s*`([^`]+)`\s*", cell)
    return match.group(1) if match else None


def check_filename_migration_ledger(root: Path) -> list[str]:
    """Verify filesystem state for rows marked Executed in the migration ledger."""
    ledger = root / MIGRATION_LEDGER_PATH
    ledger_text = _read_text(ledger)
    if ledger_text is None:
        return []

    issues: list[str] = []
    for line_number, line in enumerate(ledger_text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0].lower() in {"id", "---"}:
            continue

        disposition = cells[5]
        if not EXECUTED_MARKER.search(disposition):
            continue

        row_id = cells[0] or f"line {line_number}"
        legacy_path = _backtick_path(cells[1])
        candidate_path = _backtick_path(cells[4])
        if legacy_path is None or candidate_path is None:
            issues.append(
                f"{MIGRATION_LEDGER_PATH} row {row_id} has an Executed "
                "mapping without a parseable legacy and candidate path"
            )
            continue

        candidate = root / candidate_path
        if not candidate.is_file():
            issues.append(
                f"{MIGRATION_LEDGER_PATH} row {row_id} expected candidate "
                f"path to exist: {candidate_path}"
            )

        retains_legacy = any(
            marker in disposition.lower()
            for marker in INTENTIONAL_RETENTION_MARKERS
        )
        legacy = root / legacy_path
        if legacy.exists() and not retains_legacy:
            issues.append(
                f"{MIGRATION_LEDGER_PATH} row {row_id} still has the legacy "
                f"path after execution: {legacy_path}"
            )

    return issues


def check(root: Path) -> list[str]:
    """Return actionable failures for the catalog/scaffold contract."""
    root = root.resolve()
    issues: list[str] = []
    catalog = root / CATALOG_PATH
    scaffold = root / SCAFFOLD_PATH
    catalog_text = _read_text(catalog)

    if catalog_text is None:
        issues.append(f"missing canonical catalog: {CATALOG_PATH}")

    for relative_path, (reference, expected_count) in DOCUMENTED_REFERENCES.items():
        document = root / relative_path
        text = _read_text(document)
        actual_count = (
            sum(reference in line for line in text.splitlines())
            if text is not None
            else 0
        )
        if text is None:
            issues.append(f"missing documented reference file: {relative_path}")
        elif actual_count != expected_count:
            issues.append(
                f"{relative_path} contains {actual_count} references to "
                f"{reference}; expected {expected_count}"
            )

    issues.extend(check_filename_migration_ledger(root))

    scaffold_text = _read_text(scaffold)
    if scaffold_text is None:
        issues.append(f"missing scaffold tooling: {SCAFFOLD_PATH}")
        return issues

    canonical_path = CATALOG_PATH.as_posix()
    if canonical_path not in scaffold_text:
        issues.append(
            f"{SCAFFOLD_PATH} no longer documents the canonical inventory "
            f"path {CATALOG_PATH}"
        )

    try:
        help_result = subprocess.run(
            [sys.executable, str(scaffold), "--help"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        issues.append(f"could not execute scaffold help: {exc}")
    else:
        help_text = help_result.stdout + help_result.stderr
        normalized_help = "".join(help_text.split())
        if help_result.returncode != 0:
            issues.append(
                f"scaffold --help failed with exit code {help_result.returncode}"
            )
        if "--inventory" not in help_text or CATALOG_PATH.name not in normalized_help:
            issues.append(
                "scaffold --help no longer exposes the canonical inventory "
                f"path {CATALOG_PATH}"
            )

    if catalog_text is None:
        return issues

    try:
        scaffold_module = _load_scaffold(scaffold)
        parse_inventory = scaffold_module.parse_inventory
        entry = parse_inventory(catalog, target_id="00")
    except (AttributeError, ImportError, OSError, SyntaxError, TypeError, ValueError) as exc:
        issues.append(f"scaffold inventory importer could not be exercised: {exc}")
        return issues

    if entry is None:
        issues.append(
            "scaffold inventory importer could not pre-populate catalog entity #00"
        )
    else:
        missing_fields = [
            field
            for field, value in (
                ("name", entry.name),
                ("full_description", entry.full_description),
                ("primary_functions", entry.primary_functions),
                ("elevator_pitch", entry.elevator_pitch),
            )
            if not value
        ]
        if missing_fields:
            issues.append(
                "scaffold inventory importer did not pre-populate entity #00 "
                f"fields: {', '.join(missing_fields)}"
            )

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the inventory catalog path and scaffold integration."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="repository root (default: current directory)",
    )
    args = parser.parse_args(argv)

    issues = check(Path(args.root))
    if issues:
        print("FAIL inventory catalog contract:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print(
        "OK inventory catalog contract: "
        f"{DOCUMENTED_REFERENCE_COUNT} documented references and scaffold "
        "pre-population verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())