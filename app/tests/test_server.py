from __future__ import annotations

import http.client
import json
import tempfile
import threading
import unittest
import zipfile
from io import BytesIO
from pathlib import Path

from app.server import FoundryServer, readiness


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(__file__).resolve().parents[2]
        self.server = FoundryServer(("127.0.0.1", 0), self.root, Path(self.tmp.name))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(); self.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        headers = headers or {}
        if body is not None:
            body = json.dumps(body).encode()
            headers = {"Content-Type":"application/json", "X-Foundry-Request":"1", **headers}
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request(method, path, body, headers)
        response = conn.getresponse(); raw = response.read(); conn.close()
        return response.status, dict(response.getheaders()), json.loads(raw) if response.getheader("Content-Type", "").startswith("application/json") else raw

    def project(self, **overrides):
        value = {"name":"Garden planner", "kind":"web-tool", "description":"Plan plants", "audience":"Home gardeners", "inputs":"Beds", "outputs":"Tasks", "constraints":"Offline", "instructions":"Record work", "components":[], "tests":[], "skillIds":[]}
        value.update(overrides); return value

    def create(self, **overrides):
        status, _, item = self.request("POST", "/api/projects", self.project(**overrides))
        self.assertEqual(status, 201); return item

    def test_health_and_bootstrap_have_bounded_shape(self):
        self.assertEqual(self.request("GET", "/api/health")[2], {"status":"ok"})
        status, _, data = self.request("GET", "/api/bootstrap")
        self.assertEqual(status, 200); self.assertEqual([x["id"] for x in data["templates"]], ["custom-gpt","agent-skill","workflow","web-tool"])
        self.assertEqual(len(data["universe"]), 7); self.assertEqual(data["universe"][0]["url"], "https://askjamie.bot")
        self.assertEqual({x["id"] for x in data["universe"]}, {"askjamie","overkill","gleefully","skillz","askjamie-foundry","overkill-foundry","gleefully-foundry"})

    def test_mutation_security_and_content_type(self):
        status, _, _ = self.request("POST", "/api/projects", self.project(), {"Host":"evil.example"})
        self.assertEqual(status, 403)
        status, _, _ = self.request("POST", "/api/projects", self.project(), {"Origin":"https://evil.example"})
        self.assertEqual(status, 403)
        conn=http.client.HTTPConnection("127.0.0.1",self.port); conn.request("POST","/api/projects",b"{}",{"Content-Type":"text/plain","X-Foundry-Request":"1"}); self.assertEqual(conn.getresponse().status,400); conn.close()
        status, _, _ = self.request("POST", "/api/projects", self.project(), {"X-Foundry-Request":"0"})
        self.assertEqual(status, 400)
        status, _, _ = self.request("POST", "/api/projects", self.project(), {"Origin":f"http://127.0.0.1:{self.port + 1}"})
        self.assertEqual(status, 403)
        self.assertEqual(self.request("HEAD", "/app/server.py")[0], 405)
        self.assertEqual(self.request("OPTIONS", "/api/projects")[0], 405)

    def test_invalid_schema_and_cycle_rejected(self):
        status, _, data = self.request("POST", "/api/projects", {"name":"x","kind":"web-tool","surprise":True})
        self.assertEqual(status,400); self.assertIn("unknown",data["error"])
        components=[{"id":"a","name":"A","purpose":"A","dependsOn":["b"]},{"id":"b","name":"B","purpose":"B","dependsOn":["a"]}]
        status, _, data = self.request("POST", "/api/projects", self.project(components=components))
        self.assertEqual(status,400); self.assertIn("cycle",data["error"])
        status, _, data = self.request("POST", "/api/projects", self.project(tests=[{"id":"t","name":"t","expected":"x","actual":"","status":"pass"}]))
        self.assertEqual(status,400); self.assertIn("evidence",data["error"])
        status, _, data=self.request("POST", "/api/projects", self.project(status={"bad":"type"}))
        self.assertEqual(status,400); self.assertIn("status",data["error"])
        status, _, data=self.request("POST", "/api/projects", self.project(tests=[{"id":"t","name":"","expected":"","actual":"","status":[]}]))
        self.assertEqual(status,400)
        status, _, data=self.request("POST", "/api/projects", self.project(skillIds=["not-registered"]))
        self.assertEqual(status,400); self.assertIn("unknown registered",data["error"])

    def test_revision_conflict_and_immutable_history(self):
        created=self.create(); update=self.project(name="Renamed", revision=created["revision"])
        status, _, saved=self.request("PUT", f"/api/projects/{created['id']}", update); self.assertEqual(status,200); self.assertEqual(saved["revision"],2)
        status, _, _=self.request("PUT",f"/api/projects/{created['id']}",update); self.assertEqual(status,409)
        status, _, history=self.request("GET",f"/api/projects/{created['id']}/history"); self.assertEqual(status,200); self.assertEqual([x["revision"] for x in history["history"]],[1,2])

    def test_material_change_resets_stale_evidence(self):
        item=self.create(tests=[{"id":"case","name":"Checks plan","expected":"Works","actual":"Observed", "status":"pass"}])
        update=self.project(revision=item["revision"], instructions="Changed behavior", tests=item["tests"])
        status, _, saved=self.request("PUT",f"/api/projects/{item['id']}",update)
        self.assertEqual(status,200); self.assertEqual(saved["tests"][0]["status"],"not-run"); self.assertEqual(saved["tests"][0]["actual"],"")

    def test_persistence_and_archiving(self):
        item=self.create(status="archived")
        # Database is durable and can be reopened by a new service object.
        second=FoundryServer(("127.0.0.1",0),self.root,Path(self.tmp.name)); self.assertEqual(second.store.get(item["id"])["status"],"archived"); second.server_close()

    def test_import_fresh_identity_resets_evidence(self):
        original=self.create(tests=[{"id":"e1","name":"Check","expected":"Works","actual":"Observed locally","status":"pass"}])
        status, _, imported=self.request("POST","/api/import",{"project":original}); self.assertEqual(status,201)
        self.assertNotEqual(imported["id"],original["id"]); self.assertEqual(imported["revision"],1); self.assertEqual(imported["tests"][0]["status"],"not-run"); self.assertEqual(imported["tests"][0]["actual"],"")
        self.assertIn(original["id"], self.request("GET", f"/api/projects/{imported['id']}/history")[2]["history"][0]["summary"])

    def test_readiness_is_honest(self):
        item=self.create(); status, _, report=self.request("GET",f"/api/projects/{item['id']}/validation")
        self.assertEqual(status,200); self.assertFalse(report["readyForReview"]); self.assertIn("evidence", " ".join(x["id"] for x in report["checks"]))
        direct=readiness(item,[]); self.assertFalse(direct["readyForReview"])
        incomplete=self.create(inputs="", tests=[{"id":"case","name":"Check","expected":"Works","actual":"Observed","status":"pass"}])
        report=self.request("GET",f"/api/projects/{incomplete['id']}/validation")[2]
        self.assertFalse(report["readyForReview"]); self.assertEqual(next(x for x in report["checks"] if x["id"] == "inputs")["status"], "fail")

    def test_fixed_source_allowlist_blocks_traversal(self):
        self.assertEqual(self.request("GET","/api/sources/promptchain")[0],200)
        self.assertEqual(self.request("GET","/api/sources/..%2Fmanifest.yaml")[0],404)
        self.assertEqual(self.request("GET","/api/sources/unknown")[0],404)

    def test_export_json_markdown_and_safe_web_zip(self):
        hostile='<img src=x onerror=alert(1)>'
        item=self.create(name=hostile, instructions=hostile)
        status, headers, raw=self.request("GET",f"/api/projects/{item['id']}/export?format=json"); self.assertEqual(status,200); self.assertIn("attachment",headers["Content-Disposition"]); self.assertEqual(raw["name"],hostile)
        status, _, raw=self.request("GET",f"/api/projects/{item['id']}/export?format=zip"); self.assertEqual(status,200)
        package=zipfile.ZipFile(BytesIO(raw)); self.assertEqual(set(package.namelist()) & {"../x"},set()); html=package.read("index.html").decode(); js=package.read("app.js").decode(); self.assertNotIn(hostile,js); self.assertIn("&lt;img",html); self.assertIn("localStorage",js)
        self.assertIn('lang="en"', html); self.assertNotIn("open.onclick",js); self.assertIn("try",js); self.assertIn(item["id"],js)
        self.assertIn("## Inputs", package.read("specification.md").decode()); self.assertIn("## Observed acceptance evidence", package.read("evaluation.md").decode()); self.assertIn("Continue from here", package.read("handoff.md").decode())
        status, _, exported=self.request("GET",f"/api/projects/{item['id']}/export?format=markdown"); self.assertEqual(status,200); self.assertIn("&lt;img",exported.decode())

    def test_body_limit_and_csp(self):
        conn=http.client.HTTPConnection("127.0.0.1",self.port); conn.request("POST","/api/projects",b"{}",{"Content-Type":"application/json","X-Foundry-Request":"1","Content-Length":str(1024*1024+1)}); response=conn.getresponse(); self.assertEqual(response.status,400); response.read();conn.close()
        status, headers, _ = self.request("GET","/api/health"); self.assertEqual(status,200); self.assertIn("default-src 'self'",headers["Content-Security-Policy"])


if __name__ == "__main__": unittest.main()
