"""Regression tests for the repository manifest validators.

Run from the repository root with:

    python3 -m unittest discover -s scripts/tests -v
"""

from __future__ import annotations

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