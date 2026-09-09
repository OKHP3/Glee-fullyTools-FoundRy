"""Tests for generated Agent Skills catalog link validation."""

import importlib.util
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