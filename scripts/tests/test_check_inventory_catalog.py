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
\ufeff# TOOLBOX 🧰 (Trunk🌳) \\#00 – Example Toolbox

### Full Description:
An example toolbox used by the regression check.

### Primary Functions:
🧰FUNCTION⚙️ (🌳Branch): Perform the example action

### Elevator Pitch:
📒 A complete example toolbox for exercising catalog imports.
"""

EXECUTED_LEDGER = """\
| ID | Legacy path | Signals | Classification | Candidate target | Disposition |
|---|---|---|---|---|---|
| X-01 | `legacy/example.md` | underscore | ordinary documentation | `docs/example.md` | **Executed 2026-09-09** |
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

    def _set_ledger(self, directory: Path, text: str = EXECUTED_LEDGER) -> None:
        ledger = directory / CHECKER.MIGRATION_LEDGER_PATH
        ledger.parent.mkdir(parents=True, exist_ok=True)
        ledger.write_text(text, encoding="utf-8")

    def test_current_contract_passes(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)

        self.assertEqual([], CHECKER.check(directory))

    def test_toolbox_entry_imports_by_id_with_leading_bom(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)

        scaffold = CHECKER._load_scaffold(directory / CHECKER.SCAFFOLD_PATH)
        entry = scaffold.parse_inventory(
            directory / CHECKER.CATALOG_PATH,
            target_id="00",
        )

        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual("00", entry.entity_id)
        self.assertEqual("Example Toolbox", entry.name)

    def test_scaffold_defaults_to_catalog_in_its_repository(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)

        scaffold = CHECKER._load_scaffold(directory / CHECKER.SCAFFOLD_PATH)

        self.assertEqual(
            directory / CHECKER.CATALOG_PATH,
            scaffold.default_inventory_path(),
        )

    def test_explicit_inventory_path_overrides_catalog_default(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)
        explicit = directory / "alternate-catalog.md"
        explicit.write_text(CATALOG_TEXT, encoding="utf-8")

        scaffold = CHECKER._load_scaffold(directory / CHECKER.SCAFFOLD_PATH)

        self.assertEqual(explicit, scaffold.resolve_inventory_path(str(explicit)))

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

    def test_executed_move_passes_when_target_exists_and_legacy_is_absent(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)
        self._set_ledger(directory)
        (directory / "docs/example.md").parent.mkdir(parents=True, exist_ok=True)
        (directory / "docs/example.md").write_text("moved\n", encoding="utf-8")

        self.assertEqual([], CHECKER.check_filename_migration_ledger(directory))

    def test_executed_move_reports_missing_candidate(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)
        self._set_ledger(directory)

        issues = CHECKER.check_filename_migration_ledger(directory)

        self.assertTrue(any("candidate path to exist" in issue for issue in issues))

    def test_executed_move_reports_legacy_path_that_remains(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)
        self._set_ledger(directory)
        (directory / "docs/example.md").parent.mkdir(parents=True, exist_ok=True)
        (directory / "docs/example.md").write_text("moved\n", encoding="utf-8")
        (directory / "legacy/example.md").parent.mkdir(parents=True)
        (directory / "legacy/example.md").write_text("old\n", encoding="utf-8")

        issues = CHECKER.check_filename_migration_ledger(directory)

        self.assertTrue(any("still has the legacy path" in issue for issue in issues))

    def test_intentional_legacy_retention_is_allowed(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)
        self._set_ledger(
            directory,
            EXECUTED_LEDGER.replace(
                "**Executed 2026-09-09**",
                "**Executed 2026-09-09** — intentional retention",
            ),
        )
        (directory / "docs/example.md").parent.mkdir(parents=True, exist_ok=True)
        (directory / "docs/example.md").write_text("moved\n", encoding="utf-8")
        (directory / "legacy/example.md").parent.mkdir(parents=True)
        (directory / "legacy/example.md").write_text("retained source\n", encoding="utf-8")

        self.assertEqual([], CHECKER.check_filename_migration_ledger(directory))

    def test_non_executed_source_retention_is_ignored(self):
        directory = self._make_repository()
        self.addCleanup(shutil.rmtree, directory)
        self._set_ledger(
            directory,
            EXECUTED_LEDGER.replace(
                "`legacy/example.md`",
                "`docs/source-material/original.md`",
            ).replace(
                "`docs/example.md`",
                "`docs/source-material/renamed.md`",
            ).replace(
                "**Executed 2026-09-09**",
                "**Retain by default** — provenance rename requires approval",
            ),
        )
        (directory / "docs/source-material/original.md").parent.mkdir(
            parents=True
        )
        (directory / "docs/source-material/original.md").write_text(
            "source\n", encoding="utf-8"
        )

        self.assertEqual([], CHECKER.check_filename_migration_ledger(directory))


if __name__ == "__main__":
    unittest.main()