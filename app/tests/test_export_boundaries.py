from __future__ import annotations

import json
import unittest
import zipfile
from io import BytesIO

from app.tests.test_server import ServiceTests


class ExportBoundaryTests(ServiceTests):
    def test_unicode_long_text_and_archive_paths_survive_export(self):
        name = "Glee Δossier ../unsafe/🪴✨"
        long_description = "".join([
            "Line one with unicode: café, naïve, 影, and 🧪.\n",
            "Line two stays readable even when it is deliberately long: " + ("彩" * 120) + "\n",
            "Line three keeps punctuation intact: —but we do not rely on em dashes here—\n",
        ])
        hostile = "Folder-ish name ../nested/..\\escape? <record>"
        item = self.create(
            kind="web-tool",
            name=name,
            description=long_description,
            audience="Unicode-sensitive reviewers",
            inputs=hostile,
            outputs=long_description,
            constraints="No path traversal, no lossy encoding.",
            instructions=long_description,
            components=[{
                "id": "entry",
                "name": hostile,
                "purpose": long_description,
                "dependsOn": [],
            }],
            tests=[{
                "id": "case",
                "name": hostile,
                "expected": long_description,
                "actual": long_description,
                "status": "pass",
            }],
        )

        status, headers, raw = self.request("GET", f"/api/projects/{item['id']}/export?format=json")
        self.assertEqual(status, 200)
        self.assertIn("attachment", headers["Content-Disposition"])
        exported = raw
        self.assertEqual(exported["name"], name)
        self.assertEqual(exported["description"], long_description)
        self.assertEqual(exported["components"][0]["name"], hostile)

        status, _, markdown = self.request("GET", f"/api/projects/{item['id']}/export?format=markdown")
        self.assertEqual(status, 200)
        markdown_text = markdown.decode()
        self.assertIn(name, markdown_text)
        self.assertIn("café", markdown_text)
        self.assertIn("彩" * 40, markdown_text)
        self.assertIn("Folder-ish name ../nested/..\\escape? &lt;record&gt;", markdown_text)

        status, _, zipped = self.request("GET", f"/api/projects/{item['id']}/export?format=zip")
        self.assertEqual(status, 200)
        with zipfile.ZipFile(BytesIO(zipped)) as bundle:
            members = set(bundle.namelist())
            self.assertEqual(members & {"../x", "..\\x", "/x", "C:/x"}, set())
            self.assertTrue(all(".." not in member and not member.startswith("/") for member in members))
            self.assertIn("café", bundle.read("README.md").decode())
            self.assertIn(name, bundle.read("README.md").decode())
            self.assertIn("Folder-ish name ../nested/..\\escape? &lt;record&gt;", bundle.read("specification.md").decode())
            self.assertIn("彩" * 40, bundle.read("evaluation.md").decode())
            self.assertEqual(json.loads(bundle.read("project.json")), item)
            self.assertIn("Continue from here", bundle.read("handoff.md").decode())
