# FoundRy application contract v1

The owner-authorized application lives under `app/`. Python 3.11+ standard library, SQLite durable working records, vanilla JS/CSS frontend. Start from root with `python3 -m app.server`; default bind 127.0.0.1:8765, `--port` supports another local port, `--data-dir` supports a test/private data directory. No runtime package installation required. Draft projects do not write canon. All existing canon and seals are preserved unchanged. The service exposes only its static frontend and explicitly allowlisted research/resources, never the repository root.

## JSON project schema

```
{id: UUID, schemaVersion: 1, revision: integer, name: string,
 kind: "custom-gpt"|"agent-skill"|"workflow"|"web-tool",
 description: string, audience: string, inputs: string, outputs: string,
 constraints: string, instructions: string,
 components: [{id: string, name: string, purpose: string, dependsOn: [component id]}],
 tests: [{id: string, name: string, expected: string, actual: string,
          status: "not-run"|"pass"|"fail"}],
 skillIds: [string], status: "draft"|"archived",
 createdAt: ISO timestamp, updatedAt: ISO timestamp}
```

Server assigns IDs, revisions and timestamps. PUT requires current `revision`, returns 409 on conflict. Imports get a fresh ID and reset evaluation evidence to not-run, keeping source identity in history. Unknown keys, malformed nested objects, oversized text, invalid enum values and missing references are rejected. `name` and `kind` required to create; other fields can be empty while drafting. All user text is untrusted and rendered as text. Component IDs unique, dependencies must exist, and cycles are flagged by validation. A pass without actual evidence is never a pass. No claim of automatic behavioral validation.

## Endpoints

All JSON errors: `{error: string}` with correct 4xx/5xx. JSON body <= 1 MB. Mutations require `Content-Type: application/json`, header `X-Foundry-Request: 1`, validated Host and same Origin if present. Bind only loopback. No CORS. Foreign hosts/origins rejected. HTML CSP restricts all requests/assets to self and outbound links use safe HTTPS URLs.

- GET `/api/bootstrap`: `{templates: [{id, name, description, project: partialProject}], skills: [{id,name,description,url,sourcePath,revision}], sources: [{id,title,path,url,description}], universe: [{id,name,region,role,url,shared: boolean}]}`. Templates exactly four kinds. Coordinator supplies optional `app/data/skills.json`; engine handles its absence as an empty list during development. Sources allowlist includes PromptChain, GPT scaffold, PulseBook current, brand vernacular and canon overview. These are local read-only reference text, no automatic execution/adoption.
- GET `/api/projects`: `{projects: [project]}` includes archives.
- POST `/api/projects`: partial project, returns complete project, 201.
- GET `/api/projects/{id}`: complete project.
- PUT `/api/projects/{id}`: editable project plus revision, returns complete updated project.
- GET `/api/projects/{id}/validation`: `{readyForReview: boolean, checks: [{id,label,status: "pass"|"fail"|"warning",detail}], summary: string}`. Check purpose, audience, interface, constraints, instructions, components/dependencies, acceptance evidence, and attached skill provenance. Review-ready does not imply PME or publication-ready.
- GET `/api/projects/{id}/history`: `{history:[{revision,at,action,summary}]}`.
- GET `/api/projects/{id}/export?format=json|markdown|zip`: attachment. JSON is complete project. ZIP contains project.json, README.md, specification.md, evaluation.md, skill-references.md, handoff.md and type-specific files. Custom GPT: instructions.md/starters.md; agent skill: a structurally valid SKILL.md; workflow: workflow.md and workflow.json; web tool: runnable HTML/CSS/JS starter with persisted record entry, completion, filtering and its own README. User fields must be safely encoded and cannot inject executable HTML/JS. Packages contain draft status and observed validation results, never fabricated certification, secrets, copied canon or claims of deployment.
- POST `/api/import`: `{project: object}` returns new project, 201. Invalid version rejects without changing existing projects.
- GET `/api/sources/{id}`: `{id,title,content,path,url}` from fixed allowlist; no arbitrary path or network fetching.
- GET `/api/health`: `{status:"ok"}`.

## Frontend ownership and behavior

Frontend task owns only `app/static/index.html`, `app/static/app.js`, `app/static/styles.css` and optional frontend-only local assets. Engine owns Python and tests. Coordinator owns `app/data/skills.json`, documentation and repository metadata. Project navigation must warn before discarding unsaved edits, preserve text on errors, and display conflict errors explicitly. Save before validation/export if edited, or clearly explain that actions use the saved revision. Empty states provide useful next actions; seed examples only on explicit user action. JSON import is visible, archives recoverable, external skill links optional. UI must support editing components and acceptance evidence without raw JSON editing. A three-overlapping-ring universe view positions AskJamie left, OverKill center, Glee-fully right; Skillz shared and OverKill Found-Ry exclusively central. Seven element details remain accessible on narrow screens and without diagram interpretation.
