"""Tests for generated Agent Skills catalog link validation."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "gen-skills-readme.py"
SPEC = importlib.util.spec_from_file_location("gen_skills_readme", SCRIPT)
CATALOGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CATALOGER)


class CatalogLinkValidationTests(unittest.TestCase):
    def test_existing_relative_catalog_link_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "skill" / "SKILL.md").parent.mkdir()
            (root / "skill" / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
            content = (
                f"{CATALOGER.START_MARKER}\n"
                "[skill](skill/SKILL.md)\n"
                f"{CATALOGER.END_MARKER}\n"
            )

            self.assertEqual([], CATALOGER.validate_catalog_links(root / "README.md", content))

    def test_missing_relative_catalog_link_reports_source_and_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = (
                "# Skills\n"
                f"{CATALOGER.START_MARKER}\n"
                "[missing](missing/SKILL.md)\n"
                f"{CATALOGER.END_MARKER}\n"
            )

            errors = CATALOGER.validate_catalog_links(root / "README.md", content)

            self.assertEqual(1, len(errors))
            self.assertIn("README.md:3", errors[0])
            self.assertIn("missing/SKILL.md", errors[0])
            self.assertIn("targets missing path", errors[0])

    def test_external_and_anchor_links_are_not_filesystem_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = (
                f"{CATALOGER.START_MARKER}\n"
                "[external](https://example.invalid/skill)\n"
                "[anchor](#skills)\n"
                f"{CATALOGER.END_MARKER}\n"
            )

            self.assertEqual([], CATALOGER.validate_catalog_links(root / "README.md", content))

    def test_catalog_link_cannot_escape_catalog_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = (
                f"{CATALOGER.START_MARKER}\n"
                "[outside](../outside/SKILL.md)\n"
                f"{CATALOGER.END_MARKER}\n"
            )

            errors = CATALOGER.validate_catalog_links(root / "README.md", content)

            self.assertEqual(1, len(errors))
            self.assertIn("escapes catalog directory", errors[0])

    def test_existing_family_file_link_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "family" / "FAMILY.md").parent.mkdir()
            (root / "family" / "FAMILY.md").write_text("# Family\n", encoding="utf-8")
            content = (
                f"{CATALOGER.FAMILIES_TABLE_START}\n"
                "[family](family/FAMILY.md)\n"
                f"{CATALOGER.FAMILIES_TABLE_END}\n"
            )

            self.assertEqual([], CATALOGER.validate_family_links(root / "README.md", content))

    def test_missing_family_targets_report_source_line_and_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = (
                "# Families\n"
                f"{CATALOGER.FAMILIES_TABLE_START}\n"
                "[missing family file](family/FAMILY.md)\n"
                "[missing family readme](readme-family/README.md)\n"
                "[missing family directory](missing-family/)\n"
                f"{CATALOGER.FAMILIES_TABLE_END}\n"
            )

            errors = CATALOGER.validate_family_links(root / "README.md", content)

            self.assertEqual(3, len(errors))
            self.assertIn("README.md:3", errors[0])
            self.assertIn("family/FAMILY.md", errors[0])
            self.assertIn("README.md:4", errors[1])
            self.assertIn("readme-family/README.md", errors[1])
            self.assertIn("README.md:5", errors[2])
            self.assertIn("missing-family/", errors[2])
            self.assertTrue(all("generated family link" in error for error in errors))

    def test_family_link_cannot_escape_index_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = (
                f"{CATALOGER.FAMILIES_TABLE_START}\n"
                "[outside](../outside/FAMILY.md)\n"
                f"{CATALOGER.FAMILIES_TABLE_END}\n"
            )

            errors = CATALOGER.validate_family_links(root / "README.md", content)

            self.assertEqual(1, len(errors))
            self.assertIn("escapes index directory", errors[0])

    def test_full_check_reports_missing_family_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Distribution\n"
                f"{CATALOGER.FAMILIES_TABLE_START}\n"
                "| Family | Skills | What it covers |\n"
                "|---|---|---|\n"
                "| [`missing/`](missing/FAMILY.md) | 1 | Missing family |\n"
                f"{CATALOGER.FAMILIES_TABLE_END}\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--full", "--check"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("README.md:5", result.stderr)
            self.assertIn("generated family link", result.stderr)
            self.assertIn("missing/FAMILY.md", result.stderr)