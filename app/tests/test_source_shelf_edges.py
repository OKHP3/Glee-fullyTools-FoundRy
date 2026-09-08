from __future__ import annotations

import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from app.server import FoundryServer, SOURCES


class SourceShelfEdgeTests(unittest.TestCase):
    def setUp(self):
        self.data_tmp = tempfile.TemporaryDirectory()
        self.root_tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.root_tmp.name)
        self.server = FoundryServer(("127.0.0.1", 0), self.root, Path(self.data_tmp.name))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.root_tmp.cleanup()
        self.data_tmp.cleanup()

    def request(self, path: str):
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request("GET", path)
        response = conn.getresponse()
        raw = response.read()
        conn.close()
        body = json.loads(raw) if response.getheader("Content-Type", "").startswith("application/json") else raw
        return response.status, body

    def write_source_tree(self, *, missing: str | None = None, symlinked: bool = False):
        outside = Path(self.data_tmp.name) / "outside"
        outside.mkdir(exist_ok=True)
        for source_id, (_, relative_path) in SOURCES.items():
            target = self.root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            if source_id == missing:
                continue
            if symlinked:
                outside_file = outside / f"{source_id}.md"
                outside_file.write_text(f"# {source_id}\n")
                target.symlink_to(outside_file)
            else:
                target.write_text(f"# {source_id}\n")

    def test_missing_file_returns_source_unavailable_for_every_allowlisted_reference(self):
        for source_id in SOURCES:
            with self.subTest(source_id=source_id):
                self.write_source_tree(missing=source_id)
                status, body = self.request(f"/api/sources/{source_id}")
                self.assertEqual(status, 404)
                self.assertEqual(body["error"], "source unavailable")
                for path in self.root.rglob("*"):
                    if path.is_file() or path.is_symlink():
                        path.unlink()

    def test_symlink_traversal_and_encoded_path_boundaries_stay_blocked(self):
        self.write_source_tree(symlinked=True)
        for source_id in SOURCES:
            with self.subTest(source_id=source_id):
                status, body = self.request(f"/api/sources/{source_id}")
                self.assertEqual(status, 404)
                self.assertEqual(body["error"], "source unavailable")
                encoded_status, encoded_body = self.request(f"/api/sources/%2e%2e%2f{source_id}")
                self.assertEqual(encoded_status, 404)
                self.assertEqual(encoded_body["error"], "source not found")

