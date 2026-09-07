"""Loopback-only, standard-library FoundRy application service."""
from __future__ import annotations

import argparse
import html
import io
import json
import re
import sqlite3
import threading
import uuid
import zipfile
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

MAX_BODY = 1024 * 1024
MAX_TEXT = 100_000
KINDS = {"custom-gpt", "agent-skill", "workflow", "web-tool"}
STATUSES = {"draft", "archived"}
TEST_STATUSES = {"not-run", "pass", "fail"}
EDITABLE = {"name", "kind", "description", "audience", "inputs", "outputs",
            "constraints", "instructions", "components", "tests", "skillIds", "status"}
TEXT_FIELDS = EDITABLE - {"components", "tests", "skillIds", "kind", "status"}
SAFE_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")

SOURCES = {
    "promptchain": ("Builder-Ready PromptChain", "prompts/glee-fully-builder-ready-promptchain-v2-0.md"),
    "gpt-scaffold": ("Custom GPT scaffold", "prompts/custom_gpt_scaffold.md"),
    "pulsebook": ("GPT PulseBook v1.7", "evaluation/gpt-pulsebook-evaluation-v1-7.md"),
    "vernacular": ("Glee-fully vernacular", "vernacular/glee-fully-vernacular-lite.md"),
    "canon-overview": ("Canon overview", "canon/README.md"),
}
UNIVERSE = [
    {"id": "askjamie", "name": "AskJamie", "region": "left", "role": "Personal guidance", "url": "https://askjamie.ai", "shared": False},
    {"id": "overkill", "name": "OverKill Hill", "region": "center", "role": "Connective center", "url": "https://overkillhill.com", "shared": False},
    {"id": "gleefully", "name": "Glee-fully", "region": "right", "role": "Personalizable tools", "url": "https://glee-fully.tools", "shared": False},
    {"id": "skillz", "name": "Skillz", "region": "shared", "role": "Shared skills", "url": "https://github.com/OKHP3/skillz", "shared": True},
    {"id": "foundry", "name": "OverKill Found-Ry", "region": "center", "role": "OverKill-only foundry", "url": "https://overkillhill.com", "shared": False},
    {"id": "toolbox", "name": "Toolbox", "region": "right", "role": "Glee-fully trunk", "url": "https://glee-fully.tools", "shared": False},
    {"id": "foundry-relay", "name": "Glee-fully FoundRy", "region": "right", "role": "Tool-building workspace", "url": "https://glee-fully.tools", "shared": False},
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def template(kind: str, name: str, description: str) -> dict:
    return {"id": kind, "name": name, "description": description,
            "project": {"name": "Untitled " + name, "kind": kind,
                        "description": "", "audience": "", "inputs": "", "outputs": "",
                        "constraints": "", "instructions": "", "components": [], "tests": [], "skillIds": []}}


TEMPLATES = [
    template("custom-gpt", "Custom GPT", "A conversational tool specification."),
    template("agent-skill", "Agent Skill", "A portable, reviewable skill specification."),
    template("workflow", "Workflow", "A repeatable process with evidence and checks."),
    template("web-tool", "Web tool", "A local record-management web-tool starter."),
]


class ValidationError(ValueError):
    pass


def validate_project(payload: object, *, creating: bool = False, importing: bool = False) -> dict:
    if not isinstance(payload, dict):
        raise ValidationError("project must be an object")
    allowed = EDITABLE | ({"revision"} if not creating else set())
    if importing:
        allowed |= {"id", "schemaVersion", "createdAt", "updatedAt"}
    unknown = set(payload) - allowed
    if unknown:
        raise ValidationError("unknown project fields: " + ", ".join(sorted(unknown)))
    result = {key: payload.get(key, "" if key in TEXT_FIELDS else []) for key in EDITABLE}
    if not isinstance(result["name"], str) or not result["name"].strip():
        raise ValidationError("name is required")
    if not isinstance(result["kind"], str) or result["kind"] not in KINDS:
        raise ValidationError("kind is invalid")
    if result["status"] in ([], ""):
        result["status"] = "draft"
    if result["status"] not in STATUSES:
        raise ValidationError("status is invalid")
    for field in TEXT_FIELDS:
        if not isinstance(result[field], str) or len(result[field]) > MAX_TEXT:
            raise ValidationError(field + " must be text no longer than 100000 characters")
    if not isinstance(result["skillIds"], list) or any(not isinstance(x, str) or not SAFE_ID.fullmatch(x) for x in result["skillIds"]):
        raise ValidationError("skillIds must be safe string identifiers")
    if len(set(result["skillIds"])) != len(result["skillIds"]):
        raise ValidationError("skillIds must be unique")
    components = result["components"]
    if not isinstance(components, list):
        raise ValidationError("components must be a list")
    ids = set()
    for component in components:
        if not isinstance(component, dict) or set(component) != {"id", "name", "purpose", "dependsOn"}:
            raise ValidationError("components must contain id, name, purpose, dependsOn only")
        if not isinstance(component["id"], str) or not SAFE_ID.fullmatch(component["id"]) or component["id"] in ids:
            raise ValidationError("component IDs must be unique safe identifiers")
        ids.add(component["id"])
        if any(not isinstance(component[x], str) or len(component[x]) > MAX_TEXT for x in ("name", "purpose")):
            raise ValidationError("component name and purpose must be text")
        if not isinstance(component["dependsOn"], list) or any(not isinstance(x, str) for x in component["dependsOn"]):
            raise ValidationError("component dependsOn must be a string list")
    for component in components:
        if any(dep not in ids for dep in component["dependsOn"]):
            raise ValidationError("component dependency does not exist")
    graph = {c["id"]: c["dependsOn"] for c in components}
    visiting, visited = set(), set()
    def visit(node: str):
        if node in visiting: raise ValidationError("component dependencies contain a cycle")
        if node not in visited:
            visiting.add(node)
            for dep in graph[node]: visit(dep)
            visiting.remove(node); visited.add(node)
    for item in graph: visit(item)
    tests = result["tests"]
    if not isinstance(tests, list): raise ValidationError("tests must be a list")
    test_ids = set()
    for case in tests:
        if not isinstance(case, dict) or set(case) != {"id", "name", "expected", "actual", "status"}:
            raise ValidationError("tests must contain id, name, expected, actual, status only")
        if not isinstance(case["id"], str) or not SAFE_ID.fullmatch(case["id"]) or case["id"] in test_ids:
            raise ValidationError("test IDs must be unique safe identifiers")
        test_ids.add(case["id"])
        if any(not isinstance(case[x], str) or len(case[x]) > MAX_TEXT for x in ("name", "expected", "actual")):
            raise ValidationError("test fields must be text")
        if case["status"] not in TEST_STATUSES: raise ValidationError("test status is invalid")
        if case["status"] == "pass" and not case["actual"].strip():
            raise ValidationError("a passing test requires actual evidence")
    return result


class Store:
    def __init__(self, directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(directory / "foundry.sqlite3", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        with self.conn:
            self.conn.execute("CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, revision INTEGER NOT NULL, data TEXT NOT NULL)")
            self.conn.execute("CREATE TABLE IF NOT EXISTS history (project_id TEXT NOT NULL, revision INTEGER NOT NULL, at TEXT NOT NULL, action TEXT NOT NULL, summary TEXT NOT NULL, PRIMARY KEY(project_id, revision))")
    def list(self):
        with self.lock: return [json.loads(r["data"]) for r in self.conn.execute("SELECT data FROM projects ORDER BY json_extract(data, '$.updatedAt') DESC")]
    def get(self, project_id):
        with self.lock:
            row = self.conn.execute("SELECT data FROM projects WHERE id=?", (project_id,)).fetchone()
        return json.loads(row["data"]) if row else None
    def create(self, editable, action="created", summary=None):
        stamp = now(); project = {"id": str(uuid.uuid4()), "schemaVersion": 1, "revision": 1, **editable, "createdAt": stamp, "updatedAt": stamp}
        self._insert(project, action, summary or "Project created")
        return project
    def _insert(self, project, action, summary):
        with self.lock, self.conn:
            self.conn.execute("INSERT INTO projects(id,revision,data) VALUES(?,?,?)", (project["id"], project["revision"], json.dumps(project, separators=(",", ":"))))
            self.conn.execute("INSERT INTO history VALUES(?,?,?,?,?)", (project["id"], project["revision"], project["updatedAt"], action, summary))
    def update(self, project_id, editable, revision):
        with self.lock, self.conn:
            row = self.conn.execute("SELECT data,revision FROM projects WHERE id=?", (project_id,)).fetchone()
            if not row: return None
            if row["revision"] != revision: raise RuntimeError("revision conflict")
            old = json.loads(row["data"]); project = {**old, **editable, "revision": revision + 1, "updatedAt": now()}
            self.conn.execute("UPDATE projects SET revision=?,data=? WHERE id=?", (project["revision"], json.dumps(project, separators=(",", ":")), project_id))
            self.conn.execute("INSERT INTO history VALUES(?,?,?,?,?)", (project_id, project["revision"], project["updatedAt"], "updated", "Project updated"))
        return project
    def history(self, project_id):
        with self.lock: rows = self.conn.execute("SELECT revision,at,action,summary FROM history WHERE project_id=? ORDER BY revision", (project_id,)).fetchall()
        return [dict(r) for r in rows]


def readiness(project: dict, skills: list[dict]) -> dict:
    checks = []
    def required(id, label, value): checks.append({"id": id, "label": label, "status": "pass" if value.strip() else "fail", "detail": "Recorded." if value.strip() else "Add this before review."})
    required("purpose", "Purpose", project["description"]); required("audience", "Audience", project["audience"])
    required("interface", "Inputs and outputs", project["inputs"] + project["outputs"]); required("constraints", "Constraints", project["constraints"]); required("instructions", "Instructions", project["instructions"])
    checks.append({"id":"components", "label":"Components and dependencies", "status":"pass" if project["components"] else "warning", "detail":"Recorded." if project["components"] else "No components recorded."})
    evidence = [x for x in project["tests"] if x["status"] == "pass" and x["actual"].strip()]
    checks.append({"id":"evidence", "label":"Acceptance evidence", "status":"pass" if evidence else "fail", "detail":"Observed evidence recorded." if evidence else "Record actual evaluation evidence."})
    ids = {x.get("id") for x in skills}; attached = project["skillIds"]
    checks.append({"id":"skills", "label":"Attached skill provenance", "status":"pass" if attached and all(x in ids for x in attached) else ("warning" if not attached else "fail"), "detail":"Pinned skill references recorded." if attached and all(x in ids for x in attached) else "Attach allowlisted Skillz references."})
    ready = all(c["status"] == "pass" for c in checks)
    return {"readyForReview": ready, "checks": checks, "summary": "Ready for review; this is not PME or publication certification." if ready else "Complete failed checks and address warnings before review."}


def markdown(project: dict) -> str:
    # Keep exported Markdown inert when opened by a permissive renderer.
    esc = lambda value: html.escape(value.replace("\r", "").strip(), quote=False)
    lines = [f"# {esc(project['name'])}", "", f"Status: `{project['status']}`", "", "## Description", esc(project["description"]), "", "## Audience", esc(project["audience"]), "", "## Instructions", esc(project["instructions"]), "", "## Constraints", esc(project["constraints"])]
    return "\n".join(lines) + "\n"


def web_starter(project: dict) -> dict[str, str]:
    title = html.escape(project["name"], quote=True)
    # No project field is interpolated into executable JavaScript.
    return {"index.html": f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="style.css"><main><h1>{title}</h1><form id="form"><input id="text" required placeholder="New record"><button>Add</button></form><p><button id="all">All</button> <button id="open">Open</button> <button id="done">Completed</button></p><ul id="records"></ul></main><script src="app.js"></script>',
            "style.css": "body{font:16px system-ui;max-width:42rem;margin:2rem auto;padding:0 1rem}li{margin:.5rem 0}.done{text-decoration:line-through}",
            "app.js": "const k='foundry-records';let items=JSON.parse(localStorage.getItem(k)||'[]'),mode='all';const save=()=>localStorage.setItem(k,JSON.stringify(items));function draw(){records.innerHTML='';items.filter(x=>mode==='all'||(mode==='done'?x.done:!x.done)).forEach(x=>{let l=document.createElement('li'),b=document.createElement('button');b.textContent=x.done?'Reopen':'Complete';b.onclick=()=>{x.done=!x.done;save();draw()};l.textContent=x.text+' ';l.className=x.done?'done':'';l.append(b);records.append(l)})}form.onsubmit=e=>{e.preventDefault();items.push({text:text.value,done:false});text.value='';save();draw()};all.onclick=()=>{mode='all';draw()};open.onclick=()=>{mode='open';draw()};done.onclick=()=>{mode='done';draw()};draw();"}


class Handler(SimpleHTTPRequestHandler):
    server_version = "FoundRy/1"
    def end_headers(self):
        self.send_header("Content-Security-Policy", "default-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()
    def log_message(self, format, *args): pass
    @property
    def app(self): return self.server
    def json(self, status, value):
        raw=json.dumps(value).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def error_json(self, status, error): self.json(status, {"error": error})
    def valid_request(self):
        host=self.headers.get("Host", "").split(":")[0].lower()
        if host not in {"127.0.0.1", "localhost", "[::1]"}: return False
        origin=self.headers.get("Origin")
        if origin:
            parsed=urlparse(origin)
            if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}: return False
        return True
    def body(self):
        if self.headers.get("Content-Type", "").split(";",1)[0].lower() != "application/json": raise ValidationError("Content-Type must be application/json")
        if self.headers.get("X-Foundry-Request") != "1": raise ValidationError("X-Foundry-Request: 1 is required")
        try: length=int(self.headers.get("Content-Length", "-1"))
        except ValueError: raise ValidationError("invalid Content-Length")
        if length < 0 or length > MAX_BODY: raise ValidationError("JSON body exceeds 1 MB")
        try: return json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError): raise ValidationError("invalid JSON")
    def do_GET(self):
        if not self.valid_request(): return self.error_json(HTTPStatus.FORBIDDEN, "foreign Host or Origin")
        path=urlparse(self.path).path
        if path == "/api/health": return self.json(200,{"status":"ok"})
        if path == "/api/bootstrap": return self.json(200,{"templates":TEMPLATES,"skills":self.app.skills(),"sources":[{"id":k,"title":v[0],"path":v[1],"url":None,"description":"Local read-only reference."} for k,v in SOURCES.items()],"universe":UNIVERSE})
        if path == "/api/projects": return self.json(200,{"projects":self.app.store.list()})
        if path.startswith("/api/sources/"):
            key=path.rsplit("/",1)[1]; source=SOURCES.get(key)
            if not source: return self.error_json(404,"source not found")
            file=(self.app.root/source[1]).resolve()
            if self.app.root not in file.parents or not file.is_file(): return self.error_json(404,"source unavailable")
            return self.json(200,{"id":key,"title":source[0],"content":file.read_text(encoding="utf-8"),"path":source[1],"url":None})
        match=re.fullmatch(r"/api/projects/([0-9a-f-]{36})(?:/(validation|history|export))?", path)
        if match:
            project=self.app.store.get(match.group(1))
            if not project: return self.error_json(404,"project not found")
            suffix=match.group(2)
            if suffix is None: return self.json(200,project)
            if suffix == "validation": return self.json(200,readiness(project,self.app.skills()))
            if suffix == "history": return self.json(200,{"history":self.app.store.history(project["id"])})
            return self.export(project, parse_qs(urlparse(self.path).query).get("format",[""])[0])
        return self.static(path)
    def static(self,path):
        if path not in {"/", "/index.html", "/app.js", "/styles.css"}: return self.error_json(404,"not found")
        filename="index.html" if path in {"/","/index.html"} else path[1:]; target=self.app.static/filename
        if not target.is_file(): return self.error_json(404,"static resource unavailable")
        raw=target.read_bytes(); content="text/html; charset=utf-8" if filename.endswith("html") else ("application/javascript; charset=utf-8" if filename.endswith("js") else "text/css; charset=utf-8")
        self.send_response(200);self.send_header("Content-Type",content);self.send_header("Content-Length",str(len(raw)));self.end_headers();self.wfile.write(raw)
    def export(self, project, fmt):
        if fmt == "json": return self.download("project.json","application/json",json.dumps(project,indent=2).encode())
        if fmt == "markdown": return self.download("README.md","text/markdown; charset=utf-8",markdown(project).encode())
        if fmt != "zip": return self.error_json(400,"format must be json, markdown, or zip")
        contents={"project.json":json.dumps(project,indent=2),"README.md":markdown(project),"specification.md":markdown(project),"evaluation.md":"# Evaluation\n\nDraft status. Observed evidence only.\n", "skill-references.md":"# Skill references\n\n"+"\n".join(project["skillIds"]), "handoff.md":"# Handoff\n\nThis is a draft package, not certification or deployment.\n"}
        if project["kind"] == "custom-gpt": contents.update({"instructions.md":project["instructions"],"starters.md":"# Conversation starters\n"})
        elif project["kind"] == "agent-skill": contents["SKILL.md"]="---\nname: exported-draft\ndescription: Draft FoundRy skill.\n---\n\n# Draft skill\n\n"+project["instructions"]
        elif project["kind"] == "workflow": contents.update({"workflow.md":markdown(project),"workflow.json":json.dumps({"name":project["name"],"components":project["components"]},indent=2)})
        elif project["kind"] == "web-tool": contents.update(web_starter(project))
        out=io.BytesIO()
        with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
            for name,data in contents.items(): z.writestr(name,data)
        return self.download("foundry-project.zip","application/zip",out.getvalue())
    def download(self,name,content_type,raw):
        self.send_response(200);self.send_header("Content-Type",content_type);self.send_header("Content-Disposition",f'attachment; filename="{name}"');self.send_header("Content-Length",str(len(raw)));self.end_headers();self.wfile.write(raw)
    def do_POST(self):
        if not self.valid_request(): return self.error_json(403,"foreign Host or Origin")
        try: payload=self.body()
        except ValidationError as err: return self.error_json(400,str(err))
        path=urlparse(self.path).path
        try:
            if path == "/api/projects": return self.json(201,self.app.store.create(validate_project(payload,creating=True)))
            if path == "/api/import":
                if not isinstance(payload,dict) or set(payload)!={"project"}: raise ValidationError("import requires project only")
                source=payload["project"]
                if not isinstance(source,dict) or source.get("schemaVersion") != 1: raise ValidationError("unsupported project schemaVersion")
                editable=validate_project(source,importing=True)
                editable["tests"]=[{**case,"actual":"","status":"not-run"} for case in editable["tests"]]
                origin = source.get("id", "unidentified source") if isinstance(source.get("id"), str) else "unidentified source"
                return self.json(201,self.app.store.create(editable,"imported",f"Imported from {origin} with fresh identity and reset evidence"))
            return self.error_json(404,"not found")
        except ValidationError as err: return self.error_json(400,str(err))
    def do_PUT(self):
        if not self.valid_request(): return self.error_json(403,"foreign Host or Origin")
        match=re.fullmatch(r"/api/projects/([0-9a-f-]{36})",urlparse(self.path).path)
        if not match:return self.error_json(404,"not found")
        try:
            payload=self.body()
            if not isinstance(payload,dict) or not isinstance(payload.get("revision"),int): raise ValidationError("current revision is required")
            editable=validate_project(payload); project=self.app.store.update(match.group(1),editable,payload["revision"])
            if not project:return self.error_json(404,"project not found")
            return self.json(200,project)
        except RuntimeError: return self.error_json(409,"revision conflict")
        except ValidationError as err:return self.error_json(400,str(err))


class FoundryServer(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,address,root,data_dir):
        super().__init__(address,Handler); self.root=Path(root).resolve();self.static=self.root/"app"/"static";self.data_dir=Path(data_dir);self.store=Store(self.data_dir)
    def skills(self):
        file=self.root/"app"/"data"/"skills.json"
        if not file.is_file(): return []
        try:
            result=json.loads(file.read_text(encoding="utf-8"))
            if not isinstance(result,list): return []
            required={"id","name","description","url","sourcePath","revision"}
            return [x for x in result if isinstance(x,dict) and set(x)==required and all(isinstance(x[k],str) for k in required) and x["url"].startswith("https://")]
        except (OSError,json.JSONDecodeError): return []


def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument("--port",type=int,default=8765);parser.add_argument("--data-dir",default=None);args=parser.parse_args(argv)
    if not 1 <= args.port <= 65535: parser.error("port must be between 1 and 65535")
    root=Path(__file__).resolve().parents[1]; data=Path(args.data_dir) if args.data_dir else root/"app"/"data"
    server=FoundryServer(("127.0.0.1",args.port),root,data)
    print(f"FoundRy serving http://127.0.0.1:{args.port}")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__ == "__main__": main()
