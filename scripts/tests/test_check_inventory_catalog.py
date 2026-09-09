import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
SCRIPT = ROOT / "scripts" / "check-inventory-catalog.py"
SPEC = importlib.util.spec_from_file_location("check_inventory_catalog", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECKER)


CATALOG_TEXT = """\
# TOOL-ETTE 🔩 (Twig🌿): \\#01a – Example Tool-ette

### Full Description:
An example tool-ette used by the regression check.

### Primary Functions:
🔩FUNCTION⚙️ (🍃Leaf): Perform the example action

### Elevator Pitch:
📒 A complete example tool-ette for exercising catalog imports.
"""


class CheckInventoryCatalogTests(unittest.TestCase):
    def _make_repository(self) -> Path:
        directory = Path(tempfile.mkdtemp())
        catalog = directory / CHECKER.CATALOG_PATH
        catalog.parent.mkdir(parents=True)
        catalog.write_text(CATALOG_TEXT, encoding="utf-8")

        for relative_path, count in CHECKER.DOCUMENTED_REFERENCES.items():
            document = directory / relative_path
            document.parent.mkdir(parents=True, exist_ok=True)
            document.write_text(
                "\n".join([count[0]] * count[1]),
                encoding="utf-8",
            )

        scaffold = directory / CHECKER.SCAFFOLD_PATH
        scaffold.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            ROOT
            / ".agents/skills/glee-fully-repo-standardizer/scripts/scaffold.py",
            scaffold,
        )
        return directory

    def test_current_contract_passes(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)

        self.assertEqual([], CHECKER.check(directory))

    def test_missing_documented_reference_is_reported(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)
        document = directory / "prompts/README.md"
        document.write_text("the catalog moved\n", encoding="utf-8")

        issues = CHECKER.check(directory)

        self.assertTrue(any("prompts/README.md" in issue for issue in issues))

    def test_importer_without_catalog_data_is_reported(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)
        (directory / CHECKER.CATALOG_PATH).write_text(
            "# TOOLBOX 🧰 #00 – Example Toolbox\n", encoding="utf-8"
        )

        issues = CHECKER.check(directory)

        self.assertTrue(any("pre-populate" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()