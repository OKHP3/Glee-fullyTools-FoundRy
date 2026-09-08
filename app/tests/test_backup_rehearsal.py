from __future__ import annotations

import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "verify-foundry-backup.py"
SPEC = importlib.util.spec_from_file_location("verify_foundry_backup", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class BackupRehearsalTests(unittest.TestCase):
    def test_synthetic_backup_restore_reads_projects_and_history(self):
        result = MODULE.rehearse(Path(__file__).resolve().parents[2])
        self.assertEqual(result, {"projects": 2, "history_entries": 3})

    def test_verifier_rejects_missing_history(self):
        with tempfile.TemporaryDirectory() as temporary:
            data_dir = Path(temporary) / "data"
            expected_projects, expected_histories = MODULE.create_expected_state(Path(__file__).resolve().parents[2], data_dir)
            database = data_dir / "foundry.sqlite3"
            connection = sqlite3.connect(database)
            try:
                connection.execute("DELETE FROM history WHERE revision = 2")
                connection.commit()
            finally:
                connection.close()
            with self.assertRaises(MODULE.RecoveryError):
                MODULE.verify_recovery(data_dir, expected_projects, expected_histories)


if __name__ == "__main__":
    unittest.main()
