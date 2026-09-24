from __future__ import annotations

import json
import sqlite3
import unittest

from app.tests.test_server import ServiceTests


class LifecycleContractTests(ServiceTests):
    def revision_state(self, project_id=None):
        with self.server.store.lock:
            if project_id is None:
                projects = [
                    dict(row) for row in self.server.store.conn.execute(
                        "SELECT id, revision, data FROM projects ORDER BY id"
                    )
                ]
                history = [
                    dict(row) for row in self.server.store.conn.execute(
                        "SELECT project_id, revision, at, action, summary FROM history ORDER BY project_id, revision"
                    )
                ]
                snapshots = [
                    dict(row) for row in self.server.store.conn.execute(
                        """SELECT project_id, revision, captured_at, action,
                                  schema_version, data, sha256
                           FROM project_revisions
                           ORDER BY project_id, revision"""
                    )
                ]
                return projects, history, snapshots
            project = self.server.store.conn.execute(
                "SELECT id, revision, data FROM projects WHERE id=?", (project_id,)
            ).fetchone()
            history = [
                dict(row) for row in self.server.store.conn.execute(
                    "SELECT project_id, revision, at, action, summary FROM history WHERE project_id=? ORDER BY revision",
                    (project_id,),
                )
            ]
            snapshots = [
                dict(row) for row in self.server.store.conn.execute(
                    """SELECT project_id, revision, captured_at, action,
                              schema_version, data, sha256
                       FROM project_revisions
                       WHERE project_id=? ORDER BY revision""",
                    (project_id,),
                )
            ]
            return (dict(project) if project else None), history, snapshots

    def fail_sqlite_write_at(self, write_number):
        writes = 0

        def authorizer(action, *_):
            nonlocal writes
            if action in (sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE):
                writes += 1
                if writes == write_number:
                    return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK

        self.server.store.conn.set_authorizer(authorizer)

    def assert_revision_write_rolls_back(self, request, project_id=None):
        before = self.revision_state(project_id)
        before_all = self.revision_state()
        self.fail_sqlite_write_at(request["fail_at"])
        try:
            status, _, error = self.request(request["method"], request["path"], request["body"])
        finally:
            self.server.store.conn.set_authorizer(None)
        self.assertEqual(status, 500)
        self.assertEqual(error, {"error": "database write failed"})
        self.assertEqual(self.revision_state(project_id), before)
        self.assertEqual(self.revision_state(), before_all)

        reopened = type(self.server.store)(self.server.data_dir)
        try:
            with reopened.lock:
                current = [
                    dict(row) for row in reopened.conn.execute(
                        "SELECT id, revision, data FROM projects ORDER BY id"
                    )
                ]
                history = [
                    dict(row) for row in reopened.conn.execute(
                        "SELECT project_id, revision, at, action, summary FROM history ORDER BY project_id, revision"
                    )
                ]
                snapshots = [
                    dict(row) for row in reopened.conn.execute(
                        """SELECT project_id, revision, captured_at, action,
                                  schema_version, data, sha256
                           FROM project_revisions
                           ORDER BY project_id, revision"""
                    )
                ]
            self.assertEqual((current, history, snapshots), before_all)
        finally:
            reopened.conn.close()

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
        # The ordinary endpoint rejects oversized headers before reading a body.
        # Keep the body small so socket closure cannot race a large client upload.
        status, _, error = self.request(
            "POST", "/api/projects", {}, {"Content-Length": str(1024 * 1024 + 1)}
        )
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
        self.assertEqual([item["revision"] for item in backup["snapshots"][revised["id"]]], [1, 2])
        self.assertEqual(
            set(backup["snapshots"][revised["id"]][0]),
            {"revision", "capturedAt", "action", "schemaVersion", "data", "sha256"},
        )

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
        self.assertTrue(all(item["restorable"] for item in self.server.store.history(revised["id"])))

    def test_workspace_backup_round_trip_preserves_snapshot_bodies(self):
        original = self.create(name="First revision")
        status, _, revised = self.request(
            "PUT",
            f"/api/projects/{original['id']}",
            self.project(revision=original["revision"], name="Second revision"),
        )
        self.assertEqual(status, 200)
        backup = self.request("GET", "/api/workspace/backup")[2]
        expected_snapshots = backup["snapshots"][original["id"]]

        self.request(
            "PUT",
            f"/api/projects/{original['id']}",
            self.project(revision=revised["revision"], name="Third revision"),
        )
        status, _, result = self.request(
            "POST",
            "/api/workspace/restore",
            {"backup": backup, "confirm": True, "mode": "replace"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(result["restored"], 1)
        with self.server.store.lock:
            actual_snapshots = [
                dict(row) for row in self.server.store.conn.execute(
                    """SELECT revision, captured_at AS capturedAt, action,
                              schema_version AS schemaVersion, data, sha256
                       FROM project_revisions WHERE project_id=? ORDER BY revision""",
                    (original["id"],),
                )
            ]
        self.assertEqual(actual_snapshots, expected_snapshots)
        history = self.request("GET", f"/api/projects/{original['id']}/history")[2]["history"]
        self.assertEqual([item["revision"] for item in history], [1, 2])
        self.assertTrue(all(item["restorable"] for item in history))

    def test_workspace_restore_rejects_invalid_snapshot_without_replacement(self):
        original = self.create(name="Keep this project")
        backup = self.request("GET", "/api/workspace/backup")[2]
        backup["snapshots"][original["id"]][0]["sha256"] = "0" * 64
        newer = self.create(name="Must survive rejection")
        before = self.request("GET", "/api/projects")[2]["projects"]

        status, _, error = self.request(
            "POST",
            "/api/workspace/restore",
            {"backup": backup, "confirm": True, "mode": "replace"},
        )
        self.assertEqual(status, 400)
        self.assertIn("digest", error["error"])
        self.assertEqual(self.request("GET", "/api/projects")[2]["projects"], before)
        self.assertIsNotNone(self.server.store.get(newer["id"]))

    def test_legacy_workspace_backup_does_not_invent_historical_snapshots(self):
        original = self.create(name="Legacy backup revision one")
        status, _, revised = self.request(
            "PUT",
            f"/api/projects/{original['id']}",
            self.project(revision=original["revision"], name="Legacy backup current state"),
        )
        self.assertEqual(status, 200)
        backup = self.request("GET", "/api/workspace/backup")[2]
        legacy_backup = {key: value for key, value in backup.items() if key != "snapshots"}

        self.create(name="Discarded newer project")
        status, _, result = self.request(
            "POST",
            "/api/workspace/restore",
            {"backup": legacy_backup, "confirm": True, "mode": "replace"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(result["restored"], 1)
        history = self.request("GET", f"/api/projects/{original['id']}/history")[2]["history"]
        self.assertFalse(history[0]["restorable"])
        self.assertTrue(history[1]["restorable"])
        self.assertTrue(history[1]["baseline"])
        self.assertEqual(self.server.store.get(original["id"]), revised)

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

    def test_revision_writes_roll_back_when_sqlite_fails_at_each_write_boundary(self):
        operations = []

        for write_number in range(1, 4):
            with self.subTest(operation="create", write_number=write_number):
                protected = self.create(owner="Protected owner")
                operations.append({
                    "fail_at": write_number,
                    "method": "POST",
                    "path": "/api/projects",
                    "body": self.project(name="Failed create", owner="Other owner"),
                })
                self.assert_revision_write_rolls_back(operations.pop(), protected["id"])

        for write_number in range(1, 4):
            with self.subTest(operation="update", write_number=write_number):
                original = self.create(owner="Protected owner")
                self.assert_revision_write_rolls_back({
                    "fail_at": write_number,
                    "method": "PUT",
                    "path": f"/api/projects/{original['id']}",
                    "body": self.project(
                        revision=original["revision"],
                        name="Failed update",
                        owner="Other owner",
                    ),
                }, original["id"])

        for write_number in range(1, 4):
            with self.subTest(operation="duplicate", write_number=write_number):
                original = self.create(owner="Protected owner")
                self.assert_revision_write_rolls_back({
                    "fail_at": write_number,
                    "method": "POST",
                    "path": f"/api/projects/{original['id']}/duplicate",
                    "body": {"revision": original["revision"]},
                }, original["id"])

        for write_number in range(1, 4):
            with self.subTest(operation="archive", write_number=write_number):
                original = self.create(owner="Protected owner")
                self.assert_revision_write_rolls_back({
                    "fail_at": write_number,
                    "method": "PUT",
                    "path": f"/api/projects/{original['id']}",
                    "body": self.project(
                        revision=original["revision"],
                        status="archived",
                        owner="Other owner",
                    ),
                }, original["id"])

        for write_number in range(1, 4):
            with self.subTest(operation="version restore", write_number=write_number):
                original = self.create(owner="Protected owner", name="Original")
                status, _, revised = self.request(
                    "PUT",
                    f"/api/projects/{original['id']}",
                    self.project(revision=original["revision"], name="Revised"),
                )
                self.assertEqual(status, 200)
                self.assert_revision_write_rolls_back({
                    "fail_at": write_number,
                    "method": "POST",
                    "path": f"/api/projects/{original['id']}/restore",
                    "body": {
                        "sourceRevision": original["revision"],
                        "currentRevision": revised["revision"],
                    },
                }, original["id"])

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
