from __future__ import annotations

import tempfile
import threading
import unittest
from pathlib import Path

from app.server import Store


class ConcurrentStoreTests(unittest.TestCase):
    def project_fields(self, **overrides):
        fields = {
            "name": "Concurrency garden",
            "kind": "workflow",
            "description": "Exercise revisioned writes",
            "audience": "Test readers",
            "inputs": "A stale revision",
            "outputs": "One winning write",
            "constraints": "Temporary data only",
            "instructions": "Keep the revision history coherent",
            "components": [{"id": "core", "name": "Core", "purpose": "Write", "dependsOn": []}],
            "tests": [],
            "skillIds": [],
            "status": "draft",
        }
        fields.update(overrides)
        return fields

    def test_simultaneous_revisioned_writes_have_one_winner_and_coherent_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory))
            project = store.create(self.project_fields())
            start = threading.Barrier(4, timeout=2)
            outcomes = []
            observations = []
            failures = []
            lock = threading.Lock()

            def writer(name):
                try:
                    stale_revision = store.get(project["id"])["revision"]
                    start.wait()
                    saved = store.update(
                        project["id"],
                        self.project_fields(name=name),
                        stale_revision,
                    )
                    with lock:
                        outcomes.append(("won", saved["revision"], saved["name"]))
                except RuntimeError as error:
                    with lock:
                        outcomes.append(("conflict", str(error), name))
                except BaseException as error:  # surfaced below instead of hanging the test
                    with lock:
                        failures.append(error)

            def reader():
                try:
                    start.wait()
                    for _ in range(40):
                        current = store.get(project["id"])
                        listed = store.list()
                        history = store.history(project["id"])
                        with lock:
                            observations.append(
                                (
                                    current["revision"],
                                    listed[0]["revision"],
                                    tuple(item["revision"] for item in history),
                                )
                            )
                        if [item["revision"] for item in history] not in ([1], [1, 2]):
                            raise AssertionError("reader saw a non-contiguous history")
                        if current["revision"] not in (1, 2) or listed[0]["revision"] not in (1, 2):
                            raise AssertionError("reader saw an invalid project revision")
                except BaseException as error:  # surfaced below instead of hanging the test
                    with lock:
                        failures.append(error)

            threads = [
                threading.Thread(target=writer, args=("Candidate A",)),
                threading.Thread(target=writer, args=("Candidate B",)),
                threading.Thread(target=reader),
                threading.Thread(target=reader),
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=5)

            all_stopped = all(not thread.is_alive() for thread in threads)
            self.assertTrue(all_stopped, "concurrency workers exceeded bounded join")
            try:
                self.assertEqual(failures, [])
                self.assertGreater(len(observations), 0)
                self.assertEqual([outcome[0] for outcome in outcomes].count("won"), 1)
                self.assertEqual([outcome[0] for outcome in outcomes].count("conflict"), 1)
                winner = next(outcome for outcome in outcomes if outcome[0] == "won")
                conflict = next(outcome for outcome in outcomes if outcome[0] == "conflict")
                self.assertEqual(winner[1], 2)
                self.assertEqual(conflict[1], "revision conflict")
                self.assertNotEqual(winner[2], conflict[2])

                final = store.get(project["id"])
                history = store.history(project["id"])
                self.assertEqual(final["revision"], 2)
                self.assertEqual(final["name"], winner[2])
                self.assertEqual([item["revision"] for item in history], [1, 2])
                self.assertEqual(history[0]["action"], "created")
                self.assertEqual(history[1]["action"], "updated")
            finally:
                store.conn.close()


if __name__ == "__main__":
    unittest.main()
