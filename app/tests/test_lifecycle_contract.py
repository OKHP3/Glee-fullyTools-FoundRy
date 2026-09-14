from __future__ import annotations

import json
import unittest

from app.tests.test_server import ServiceTests


class LifecycleContractTests(ServiceTests):
    def test_legacy_record_save_defaults_metadata_without_resetting_evidence(self):
        item = self.create(tests=[{"id": "case", "name": "Case", "expected": "Result",
                                  "actual": "Observed", "status": "pass"}])
        legacy = {key: value for key, value in item.items()
                  if key not in {"owner", "version", "purpose"}}
        with self.server.store.lock, self.server.store.conn:
            self.server.store.conn.execute("UPDATE projects SET data=? WHERE id=?",
                                           (json.dumps(legacy), item["id"]))
        payload = self.project(revision=1, tests=item["tests"])
        status, _, saved = self.request("PUT", f"/api/projects/{item['id']}", payload)
        self.assertEqual(status, 200)
        self.assertEqual(saved["revision"], 2)
        self.assertEqual(saved["tests"], item["tests"])
        for key in ("owner", "version", "purpose"):
            self.assertEqual(saved[key], "")

    def test_restore_accepts_backup_larger_than_regular_request_limit(self):
        for index in range(12):
            self.create(name=f"Project {index}", instructions="x" * 100_000)
        status, _, backup = self.request("GET", "/api/workspace/backup")
        self.assertEqual(status, 200)
        self.assertGreater(len(json.dumps(backup).encode()), 1024 * 1024)
        status, _, result = self.request("POST", "/api/workspace/restore",
                                        {"backup": backup, "confirm": True, "mode": "replace"})
        self.assertEqual(status, 200)
        self.assertEqual(result["restored"], 12)
        status, _, error = self.request("POST", "/api/projects", {"padding": "x" * (1024 * 1024)})
        self.assertEqual(status, 400)
        self.assertIn("1 MB", error["error"])

    def test_restore_rejects_backup_above_ten_megabytes(self):
        status, _, error = self.request("POST", "/api/workspace/restore",
                                        {"backup": "x" * (10 * 1024 * 1024),
                                         "confirm": True, "mode": "replace"})
        self.assertEqual(status, 400)
        self.assertIn("10 MB", error["error"])

    def test_metadata_duplicate_delete_and_package_inspection(self):
        original = self.create(
            kind="custom-gpt",
            owner="Glee-fully owner",
            version="1.2.3",
            purpose="Turn a useful idea into a reviewable conversation tool.",
            tests=[{
                "id": "case",
                "name": "Useful response",
                "expected": "The declared output is returned",
                "actual": "Observed locally",
                "status": "pass",
            }],
        )
        self.assertEqual(original["owner"], "Glee-fully owner")
        self.assertEqual(original["version"], "1.2.3")
        self.assertEqual(original["purpose"], "Turn a useful idea into a reviewable conversation tool.")

        status, _, package = self.request("GET", f"/api/projects/{original['id']}/package")
        self.assertEqual(status, 200)
        self.assertEqual(package["manifest"]["projectId"], original["id"])
        self.assertEqual(package["manifest"]["version"], "1.2.3")
        self.assertIn("manifest.json", [item["name"] for item in package["files"]])
        self.assertIn("instructions.md", [item["name"] for item in package["files"]])
        manifest = next(item for item in package["files"] if item["name"] == "manifest.json")
        self.assertEqual(json.loads(manifest["content"])["kind"], "custom-gpt")

        status, _, duplicate = self.request(
            "POST",
            f"/api/projects/{original['id']}/duplicate",
            {"revision": original["revision"]},
        )
        self.assertEqual(status, 201)
        self.assertNotEqual(duplicate["id"], original["id"])
        self.assertEqual(duplicate["revision"], 1)
        self.assertEqual(duplicate["tests"][0]["status"], "not-run")
        self.assertEqual(duplicate["tests"][0]["actual"], "")

        status, _, response = self.request(
            "DELETE",
            f"/api/projects/{duplicate['id']}",
            {"confirm": False, "revision": duplicate["revision"]},
        )
        self.assertEqual(status, 400)
        self.assertIsNotNone(self.server.store.get(duplicate["id"]))
        status, _, response = self.request(
            "DELETE",
            f"/api/projects/{duplicate['id']}",
            {"confirm": True, "revision": duplicate["revision"]},
        )
        self.assertEqual(status, 200)
        self.assertEqual(response["deleted"], True)
        self.assertIsNone(self.server.store.get(duplicate["id"]))

    def test_workspace_backup_restore_validates_before_replacement(self):
        original = self.create(name="Restorable primary")
        update = self.project(revision=original["revision"], name="Restorable revision")
        status, _, revised = self.request("PUT", f"/api/projects/{original['id']}", update)
        self.assertEqual(status, 200)
        status, _, raw = self.request("GET", "/api/workspace/backup")
        self.assertEqual(status, 200)
        backup = raw
        self.assertEqual(backup["format"], "glee-fully-foundry-workspace")
        self.assertEqual(len(backup["history"][revised["id"]]), 2)

        newer = self.create(name="Newer edit that must survive rejection")
        before = self.request("GET", "/api/projects")[2]["projects"]
        malformed = json.loads(json.dumps(backup))
        malformed["history"][revised["id"]].pop()
        status, _, error = self.request(
            "POST",
            "/api/workspace/restore",
            {"backup": malformed, "confirm": True, "mode": "replace"},
        )
        self.assertEqual(status, 400)
        self.assertIn("history", error["error"])
        self.assertEqual(self.request("GET", "/api/projects")[2]["projects"], before)
        self.assertIsNotNone(self.server.store.get(newer["id"]))

        status, _, result = self.request(
            "POST",
            "/api/workspace/restore",
            {"backup": backup, "confirm": True, "mode": "replace"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(result["restored"], 1)
        restored = self.server.store.get(revised["id"])
        self.assertEqual(restored, revised)
        self.assertEqual([item["revision"] for item in self.server.store.history(revised["id"])], [1, 2])
        self.assertIsNone(self.server.store.get(newer["id"]))

    def test_revision_snapshots_restore_append_only_and_reset_evidence(self):
        original = self.create(
            status="archived",
            tests=[{
                "id": "case",
                "name": "Useful case",
                "expected": "It works",
                "actual": "Observed before restore",
                "status": "pass",
            }],
        )
        status, _, revised = self.request(
            "PUT",
            f"/api/projects/{original['id']}",
            self.project(revision=original["revision"], name="Changed name", status="archived",
                         tests=original["tests"]),
        )
        self.assertEqual(status, 200)
        status, _, history = self.request("GET", f"/api/projects/{original['id']}/history")
        self.assertEqual(status, 200)
        self.assertTrue(all(entry["restorable"] for entry in history["history"]))
        self.assertFalse(any(entry["baseline"] for entry in history["history"]))

        status, _, restored = self.request(
            "POST",
            f"/api/projects/{original['id']}/restore",
            {"sourceRevision": original["revision"], "currentRevision": revised["revision"]},
        )
        self.assertEqual(status, 200)
        self.assertEqual(restored["id"], original["id"])
        self.assertEqual(restored["createdAt"], original["createdAt"])
        self.assertEqual(restored["revision"], 3)
        self.assertEqual(restored["name"], original["name"])
        self.assertEqual(restored["status"], "draft")
        self.assertEqual(restored["tests"][0]["status"], "not-run")
        self.assertEqual(restored["tests"][0]["actual"], "")

        with self.server.store.lock:
            source = self.server.store.conn.execute(
                "SELECT data FROM project_revisions WHERE project_id=? AND revision=?",
                (original["id"], original["revision"]),
            ).fetchone()
            snapshot_count = self.server.store.conn.execute(
                "SELECT COUNT(*) FROM project_revisions WHERE project_id=?",
                (original["id"],),
            ).fetchone()[0]
        self.assertEqual(json.loads(source["data"]), original)
        self.assertEqual(snapshot_count, 3)
        history = self.request("GET", f"/api/projects/{original['id']}/history")[2]["history"]
        self.assertEqual([entry["revision"] for entry in history], [1, 2, 3])
        self.assertEqual(history[-1]["action"], "restored")
        self.assertTrue(history[-1]["restorable"])
        self.assertIn("evidence reset", history[-1]["summary"])

    def test_restore_rejects_stale_or_corrupt_source_without_writing(self):
        original = self.create(name="Original")
        status, _, revised = self.request(
            "PUT",
            f"/api/projects/{original['id']}",
            self.project(revision=original["revision"], name="Revised"),
        )
        self.assertEqual(status, 200)
        status, _, error = self.request(
            "POST",
            f"/api/projects/{original['id']}/restore",
            {"sourceRevision": 1, "currentRevision": 1},
        )
        self.assertEqual(status, 409)
        self.assertEqual(self.server.store.get(original["id"]), revised)
        self.assertEqual(len(self.server.store.history(original["id"])), 2)

        with self.server.store.lock, self.server.store.conn:
            self.server.store.conn.execute(
                "UPDATE project_revisions SET sha256=? WHERE project_id=? AND revision=?",
                ("0" * 64, original["id"], original["revision"]),
            )
        status, _, error = self.request(
            "POST",
            f"/api/projects/{original['id']}/restore",
            {"sourceRevision": original["revision"], "currentRevision": revised["revision"]},
        )
        self.assertEqual(status, 400)
        self.assertIn("unavailable", error["error"])
        self.assertEqual(self.server.store.get(original["id"]), revised)
        self.assertEqual(len(self.server.store.history(original["id"])), 2)
        history = self.request("GET", f"/api/projects/{original['id']}/history")[2]["history"]
        self.assertFalse(history[0]["restorable"])

    def test_pre_snapshot_database_gets_only_current_baseline(self):
        original = self.create(name="Before snapshots")
        status, _, revised = self.request(
            "PUT",
            f"/api/projects/{original['id']}",
            self.project(revision=original["revision"], name="Current state"),
        )
        self.assertEqual(status, 200)
        with self.server.store.lock, self.server.store.conn:
            self.server.store.conn.execute("DELETE FROM project_revisions WHERE project_id=?", (original["id"],))
            self.server.store._migrate_current_baselines_locked()
        history = self.request("GET", f"/api/projects/{original['id']}/history")[2]["history"]
        self.assertFalse(history[0]["restorable"])
        self.assertTrue(history[1]["restorable"])
        self.assertTrue(history[1]["baseline"])
        self.assertFalse(history[1]["action"] == "migration-baseline")
        status, _, error = self.request(
            "POST",
            f"/api/projects/{original['id']}/restore",
            {"sourceRevision": original["revision"], "currentRevision": revised["revision"]},
        )
        self.assertEqual(status, 400)
        self.assertIn("unavailable", error["error"])
        self.assertEqual(self.server.store.get(original["id"]), revised)

    def test_package_contract_has_target_file_for_each_kind(self):
        expected = {
            "custom-gpt": "instructions.md",
            "agent-skill": "SKILL.md",
            "workflow": "workflow.json",
            "web-tool": "index.html",
        }
        for kind, target in expected.items():
            with self.subTest(kind=kind):
                item = self.create(kind=kind)
                status, _, package = self.request("GET", f"/api/projects/{item['id']}/package")
                self.assertEqual(status, 200)
                names = {file["name"] for file in package["files"]}
                self.assertTrue({"manifest.json", "README.md", "build.md", "evaluation.md", "handoff.md", "skill-references.md"} <= names)
                self.assertIn(target, names)


if __name__ == "__main__":
    unittest.main()
