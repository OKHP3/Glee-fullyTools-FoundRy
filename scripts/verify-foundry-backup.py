#!/usr/bin/env python3
"""Rehearse a private FoundRy SQLite backup and restore with synthetic data."""

from __future__ import annotations

import argparse
import copy
import http.client
import json
import shutil
import sys
import tempfile
import threading
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from app.server import FoundryServer, Store


class RecoveryError(RuntimeError):
    """Raised when restored project or history data does not match the source."""


def synthetic_project(name: str, kind: str = "workflow") -> dict:
    return {
        "name": name,
        "kind": kind,
        "description": "Synthetic backup rehearsal project",
        "audience": "Recovery test",
        "inputs": "Synthetic input",
        "outputs": "Synthetic output",
        "constraints": "Temporary data only",
        "instructions": "Verify that this project survives a folder backup.",
        "components": [{"id": "core", "name": "Core", "purpose": "Exercise persistence", "dependsOn": []}],
        "tests": [{"id": "round-trip", "name": "Round trip", "expected": "Project is readable after restore", "actual": "Observed in rehearsal", "status": "pass"}],
        "skillIds": [],
    }


def request(port: int, method: str, path: str, body: dict | None = None) -> tuple[int, dict | bytes]:
    headers = {}
    payload = None
    if body is not None:
        payload = json.dumps(body).encode()
        headers = {"Content-Type": "application/json", "X-Foundry-Request": "1"}
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        connection.request(method, path, payload, headers)
        response = connection.getresponse()
        raw = response.read()
        if response.getheader("Content-Type", "").startswith("application/json"):
            return response.status, json.loads(raw)
        return response.status, raw
    finally:
        connection.close()


def start_server(root: Path, data_dir: Path) -> tuple[FoundryServer, threading.Thread]:
    server = FoundryServer(("127.0.0.1", 0), root, data_dir)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def close_server(server: FoundryServer, thread: threading.Thread) -> None:
    server.shutdown()
    server.server_close()
    thread.join(timeout=10)
    if thread.is_alive():
        raise RecoveryError("server did not stop before backup")


def create_expected_state(root: Path, data_dir: Path) -> tuple[list[dict], dict[str, list[dict]]]:
    server, thread = start_server(root, data_dir)
    try:
        created = []
        for project in (synthetic_project("F05 primary"), synthetic_project("F05 companion", "web-tool")):
            status, value = request(server.server_address[1], "POST", "/api/projects", project)
            if status != 201:
                raise RecoveryError(f"synthetic project creation failed: HTTP {status}: {value}")
            created.append(value)
        update = copy.deepcopy(created[0])
        update = {key: update[key] for key in ("name", "kind", "description", "audience", "inputs", "outputs", "constraints", "instructions", "components", "tests", "skillIds", "status")}
        update["revision"] = created[0]["revision"]
        update["description"] = "Synthetic backup rehearsal project, revised"
        status, value = request(server.server_address[1], "PUT", f"/api/projects/{created[0]['id']}", update)
        if status != 200:
            raise RecoveryError(f"synthetic history creation failed: HTTP {status}: {value}")
        status, projects = request(server.server_address[1], "GET", "/api/projects")
        if status != 200:
            raise RecoveryError(f"source project readback failed: HTTP {status}: {projects}")
        histories = {}
        for project in projects["projects"]:
            status, history = request(server.server_address[1], "GET", f"/api/projects/{project['id']}/history")
            if status != 200:
                raise RecoveryError(f"source history readback failed: HTTP {status}: {history}")
            histories[project["id"]] = history["history"]
        return projects["projects"], histories
    finally:
        close_server(server, thread)


def verify_recovery(data_dir: Path, expected_projects: list[dict], expected_histories: dict[str, list[dict]]) -> None:
    """Check restored project records and complete revision history."""
    store = Store(data_dir)
    try:
        actual_projects = {project["id"]: project for project in store.list()}
        expected = {project["id"]: project for project in expected_projects}
        if actual_projects != expected:
            raise RecoveryError("restored project readback does not match the source")
        for project_id, expected_history in expected_histories.items():
            if store.history(project_id) != expected_history:
                raise RecoveryError(f"restored history readback does not match project {project_id}")
    finally:
        store.conn.close()


def rehearse(root: Path | None = None) -> dict:
    """Run the complete synthetic backup, close, copy, restore and readback flow."""
    repository_root = (root or Path(__file__).resolve().parents[1]).resolve()
    with tempfile.TemporaryDirectory(prefix="foundry-f05-") as workspace:
        workspace_path = Path(workspace)
        source = workspace_path / "source-data"
        backup = workspace_path / "backup-copy"
        restored = workspace_path / "restored-data"
        expected_projects, expected_histories = create_expected_state(repository_root, source)
        shutil.copytree(source, backup)
        shutil.copytree(backup, restored)
        verify_recovery(restored, expected_projects, expected_histories)
        return {"projects": len(expected_projects), "history_entries": sum(map(len, expected_histories.values()))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None, help="repository root, default: inferred from this script")
    args = parser.parse_args()
    result = rehearse(args.root)
    print(json.dumps({"status": "passed", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
