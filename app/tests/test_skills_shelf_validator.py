from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_validator():
    path = Path(__file__).resolve().parents[2] / "scripts" / "validate-skills-shelf.py"
    spec = importlib.util.spec_from_file_location("validate_skills_shelf", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


class SkillShelfValidatorTests(unittest.TestCase):
    def test_current_shelf_is_valid(self):
        shelf = VALIDATOR.load_shelf(Path(__file__).resolve().parents[1] / "data" / "skills.json")
        self.assertEqual(VALIDATOR.validate_shelf(shelf), [])

    def test_rejects_duplicate_ids(self):
        shelf = [
            {"id": "alpha", "name": "Alpha", "description": "One", "url": "https://example.com/a", "sourcePath": "a/SKILL.md", "revision": "a" * 40},
            {"id": "alpha", "name": "Alpha 2", "description": "Two", "url": "https://example.com/b", "sourcePath": "b/SKILL.md", "revision": "b" * 40},
        ]
        errors = VALIDATOR.validate_shelf(shelf)
        self.assertTrue(any("duplicate shelf id" in error.message for error in errors))

    def test_accepts_mixed_case_and_punctuation_safe_ids(self):
        shelf = [{
            "id": "Glee.Skill:Alpha_1",
            "name": "Mixed ID",
            "description": "Allowed shelf ID shape",
            "url": "https://example.com/skill.md",
            "sourcePath": "mixed/SKILL.md",
            "revision": "c" * 40,
        }]
        self.assertEqual(VALIDATOR.validate_shelf(shelf), [])

    def test_rejects_non_https_url_and_short_revision(self):
        shelf = [{
            "id": "bad-entry",
            "name": "Bad Entry",
            "description": "Broken record",
            "url": "http://example.com/skill.md",
            "sourcePath": "bad/SKILL.md",
            "revision": "1234abcd",
        }]
        errors = VALIDATOR.validate_shelf(shelf)
        self.assertTrue(any(".url" in error.path for error in errors))
        self.assertTrue(any(".revision" in error.path for error in errors))

    def test_rejects_unknown_shape(self):
        errors = VALIDATOR.validate_shelf({"id": "not-a-list"})
        self.assertEqual(errors[0].path, "(root)")

    def test_cli_reports_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "skills.json"
            path.write_text('[{"id":"bad id","name":"X","description":"Y","url":"ftp://example.com","sourcePath":"../skill.md","revision":"short"}]', encoding="utf-8")
            exit_code = VALIDATOR.main([str(path)])
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
