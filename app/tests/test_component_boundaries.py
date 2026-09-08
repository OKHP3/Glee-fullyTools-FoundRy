from __future__ import annotations

import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from app.server import MAX_DEPENDENCIES, MAX_ITEMS, FoundryServer, validate_project


class ComponentBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(__file__).resolve().parents[2]
        self.server = FoundryServer(("127.0.0.1", 0), self.root, Path(self.tmp.name))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        headers = headers or {}
        if body is not None:
            body = json.dumps(body).encode()
            headers = {"Content-Type": "application/json", "X-Foundry-Request": "1", **headers}
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request(method, path, body, headers)
        response = conn.getresponse()
        raw = response.read()
        conn.close()
        payload = json.loads(raw) if response.getheader("Content-Type", "").startswith("application/json") else raw
        return response.status, dict(response.getheaders()), payload

    def project(self, **overrides):
        value = {
            "name": "Boundary graph",
            "kind": "workflow",
            "description": "Check component boundaries",
            "audience": "Owners",
            "inputs": "Inputs",
            "outputs": "Outputs",
            "constraints": "Constraints",
            "instructions": "Instructions",
            "components": [],
            "tests": [],
            "skillIds": [],
        }
        value.update(overrides)
        return value

    def create(self, **overrides):
        status, _, item = self.request("POST", "/api/projects", self.project(**overrides))
        self.assertEqual(status, 201)
        return item

    def test_deep_branched_graph_and_dependency_edges(self):
        components = [
            {"id": "root", "name": "Root", "purpose": "Anchor the graph", "dependsOn": []},
            {"id": "ingest", "name": "Ingest", "purpose": "Collect inputs", "dependsOn": ["root"]},
            {"id": "shape", "name": "Shape", "purpose": "Normalize inputs", "dependsOn": ["root"]},
            {"id": "review", "name": "Review", "purpose": "Check output", "dependsOn": ["ingest", "shape"]},
            {"id": "publish", "name": "Publish", "purpose": "Release the result", "dependsOn": ["review"]},
        ]
        item = self.create(components=components)
        self.assertEqual([component["id"] for component in item["components"]], [component["id"] for component in components])
        self.assertEqual(self.request("GET", f"/api/projects/{item['id']}/validation")[2]["readyForReview"], False)
        direct = validate_project(self.project(components=components))
        self.assertEqual([component["dependsOn"] for component in direct["components"]], [component["dependsOn"] for component in components])

    def test_unknown_self_and_cycle_dependencies_are_rejected(self):
        unknown = self.project(components=[{"id": "root", "name": "Root", "purpose": "A", "dependsOn": ["missing"]}])
        self.assertEqual(self.request("POST", "/api/projects", unknown)[0], 400)

        self_ref = self.project(components=[{"id": "root", "name": "Root", "purpose": "A", "dependsOn": ["root"]}])
        self.assertEqual(self.request("POST", "/api/projects", self_ref)[0], 400)

        cycle = self.project(components=[
            {"id": "a", "name": "A", "purpose": "A", "dependsOn": ["b"]},
            {"id": "b", "name": "B", "purpose": "B", "dependsOn": ["c"]},
            {"id": "c", "name": "C", "purpose": "C", "dependsOn": ["a"]},
        ])
        status, _, data = self.request("POST", "/api/projects", cycle)
        self.assertEqual(status, 400)
        self.assertIn("cycle", data["error"])

    def test_component_collection_and_dependency_list_bounds(self):
        too_many_components = [{"id": f"c{i}", "name": f"C{i}", "purpose": "Leaf", "dependsOn": []} for i in range(MAX_ITEMS + 1)]
        status, _, data = self.request("POST", "/api/projects", self.project(components=too_many_components))
        self.assertEqual(status, 400)
        self.assertIn("components", data["error"])

        deps = [f"d{i}" for i in range(MAX_DEPENDENCIES + 1)]
        components = [{"id": dep, "name": dep.upper(), "purpose": "Leaf", "dependsOn": []} for dep in deps]
        components.append({"id": "hub", "name": "Hub", "purpose": "Collects leaves", "dependsOn": deps})
        status, _, data = self.request("POST", "/api/projects", self.project(components=components))
        self.assertEqual(status, 400)
        self.assertIn("dependsOn", data["error"])


if __name__ == "__main__":
    unittest.main()
