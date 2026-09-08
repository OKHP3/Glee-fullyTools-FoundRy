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
            (root / "docs/guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "[local](docs/guide.md)",
                        "[with anchor](docs/guide.md#heading)",
                        "[anchor](#heading)",
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


if __name__ == "__main__":
    unittest.main()