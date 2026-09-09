"""Regression tests for the repository manifest validators.

Run from the repository root with:

    python3 -m unittest discover -s scripts/tests -v
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Callable

import yaml


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "manifest.yaml"
VALIDATOR = ROOT / "scripts" / "validate-manifest.py"
AUDIT = ROOT / "scripts" / "manifest-audit.py"
REQUIREMENTS = ROOT / "requirements.txt"
MANIFEST_VALIDATOR_DEPENDENCIES = {"pyyaml", "jsonschema"}
REQUIREMENT_LINE = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]+\])?(?P<specifier>.*)$"
)
EXACT_PIN = re.compile(r"^==\s*(?![=<>!~])[^;\s]+(?:\s*;\s*.+)?$")


def canonical_requirement_name(name: str) -> str:
    """Return the normalized name used for requirement duplicate checks."""

    return re.sub(r"[-_.]+", "-", name).lower()


def requirements_contract_errors(path: Path) -> list[str]:
    """Report requirement entries that break the manifest validator contract."""

    entries: list[tuple[int, str, str]] = []
    errors: list[str] = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue

        match = REQUIREMENT_LINE.fullmatch(line)
        if match is None:
            errors.append(f"line {line_number} is not a package requirement: {line}")
            continue

        entries.append(
            (
                line_number,
                canonical_requirement_name(match.group("name")),
                match.group("specifier").strip(),
            )
        )

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


class ManifestValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tracked_manifest_before = MANIFEST.read_bytes()

    def tearDown(self) -> None:
        self.assertEqual(
            self.tracked_manifest_before,
            MANIFEST.read_bytes(),
            "manifest validator tests must not modify the tracked manifest",
        )

    def run_validator(self, manifest_path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(manifest_path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_audit(self, manifest_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(AUDIT), str(manifest_root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def write_requirements_variant(self, directory: Path, contents: str) -> Path:
        path = directory / "requirements.txt"
        path.write_text(contents, encoding="utf-8")
        return path

    def write_manifest_variant(
        self,
        directory: Path,
        mutate: Callable[[dict], None] | None = None,
    ) -> Path:
        manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        if mutate is not None:
            mutate(manifest)
        path = directory / "manifest.yaml"
        path.write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )
        return path

    def test_manifest_validator_requirements_are_unique_and_exactly_pinned(self) -> None:
        self.assertEqual([], requirements_contract_errors(REQUIREMENTS))

    def test_duplicate_requirement_names_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_requirements_variant(
                Path(directory),
                "PyYAML==6.0.3\npyyaml==6.0.3\njsonschema==4.26.0\n",
            )

            errors = requirements_contract_errors(path)

        self.assertIn("duplicate requirement name: pyyaml", errors)

    def test_non_exact_manifest_validator_pins_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_requirements_variant(
                Path(directory),
                "PyYAML>=6.0,<7\njsonschema==4.26.0\n",
            )

            errors = requirements_contract_errors(path)

        self.assertIn(
            "pyyaml on line 1 must use an exact == pin",
            errors,
        )

    def test_current_manifest_passes_strict_validator_and_legacy_audit(self) -> None:
        validator_result = self.run_validator(MANIFEST)
        self.assertEqual(0, validator_result.returncode, validator_result.stdout)
        self.assertIn("PASS", validator_result.stdout)

        audit_result = self.run_audit(ROOT)
        self.assertEqual(0, audit_result.returncode, audit_result.stdout)
        self.assertIn("OK manifest.yaml baseline fields present", audit_result.stdout)

    def test_missing_top_level_section_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_manifest_variant(
                Path(directory),
                lambda manifest: manifest.pop("application"),
            )

            result = self.run_validator(path)

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("'application' is a required property", result.stdout)

    def test_missing_brand_domain_is_rejected_by_both_audits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self.write_manifest_variant(
                root,
                lambda manifest: manifest["brand"].pop("domain"),
            )

            validator_result = self.run_validator(path)
            audit_result = self.run_audit(root)

        self.assertNotEqual(0, validator_result.returncode, validator_result.stdout)
        self.assertIn("'domain' is a required property", validator_result.stdout)
        self.assertNotEqual(0, audit_result.returncode, audit_result.stdout)
        self.assertIn("missing required manifest field: brand.domain", audit_result.stdout)

    def test_invalid_lifecycle_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_manifest_variant(
                Path(directory),
                lambda manifest: manifest["repo"].update(
                    lifecycle_status="not-a-real-status"
                ),
            )

            result = self.run_validator(path)

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("not-a-real-status", result.stdout)
        self.assertIn("is not one of", result.stdout)


if __name__ == "__main__":
    unittest.main()