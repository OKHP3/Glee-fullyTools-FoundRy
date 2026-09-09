import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "check-markdown-links.py"
SPEC = importlib.util.spec_from_file_location("check_markdown_links", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class CheckMarkdownLinksTests(unittest.TestCase):
    def test_supported_non_repository_links_are_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/guide.md").write_text("# Heading\n", encoding="utf-8")
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Index",
                        "[local](docs/guide.md)",
                        "[with anchor](docs/guide.md#heading)",
                        "[anchor](#index)",
                        "[external](https://example.invalid/missing)",
                        "[template]({{generated-path}})",
                        "[environment](${generated_path})",
                        "```markdown",
                        "[example](missing.md)",
                        "```",
                    ]
                ),
                encoding="utf-8",
            )

            result = CHECKER.scan(root, ("README.md",))

            self.assertEqual([], result.issues)
            self.assertEqual(6, result.links)
            self.assertEqual(1, result.external)
            self.assertEqual(1, result.anchors)
            self.assertEqual(2, result.placeholders)

    def test_missing_relative_link_is_reported_with_line_number(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Index\n\n[missing](docs/not-here.md)\n",
                encoding="utf-8",
            )

            result = CHECKER.scan(root, ("README.md",))

            self.assertEqual(1, len(result.issues))
            self.assertEqual(Path("README.md"), result.issues[0].source)
            self.assertEqual(3, result.issues[0].line)
            self.assertEqual("target does not exist", result.issues[0].reason)

    def test_missing_heading_fragment_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Index\n\n[missing](README.md#not-there)\n",
                encoding="utf-8",
            )

            result = CHECKER.scan(root, ("README.md",))

            self.assertEqual(1, len(result.issues))
            self.assertEqual(3, result.issues[0].line)
            self.assertEqual("heading does not exist", result.issues[0].reason)

    def test_heading_fragments_use_github_normalization_and_duplicate_suffixes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Repeated Heading",
                        "# Repeated Heading",
                        "# Punctuation: and `markup`",
                        "Setext Heading",
                        "----------------",
                        "[first](README.md#repeated-heading)",
                        "[second](README.md#repeated-heading-1)",
                        "[punctuation](README.md#punctuation-and-markup)",
                        "[setext](#setext-heading)",
                    ]
                ),
                encoding="utf-8",
            )

            result = CHECKER.scan(root, ("README.md",))

            self.assertEqual([], result.issues)

    def test_percent_encoded_fragment_is_decoded_before_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/guide.md").write_text("# A Heading\n", encoding="utf-8")
            (root / "README.md").write_text(
                "[guide](docs/guide.md#a%2Dheading)\n",
                encoding="utf-8",
            )

            result = CHECKER.scan(root, ("README.md",))

            self.assertEqual([], result.issues)

    def test_external_fragment_is_not_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "[external](https://example.invalid/missing#not-there)\n",
                encoding="utf-8",
            )

            result = CHECKER.scan(root, ("README.md",))

            self.assertEqual([], result.issues)
            self.assertEqual(1, result.external)


if __name__ == "__main__":
    unittest.main()