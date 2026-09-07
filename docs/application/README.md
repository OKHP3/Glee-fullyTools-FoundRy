# Glee-fully FoundRy application

This private, owner-run workspace helps you design, evaluate and package systems
and tools. Canon remains in the existing ledgers; application projects are drafts
with their own revision history. No draft is automatically registered or PME-approved.

## Run

Use Python 3.11 or newer. From the repository root:

```bash
python3 -m app.server
```

Open <http://127.0.0.1:8765>. There is no install or build step and no paid model
or external service is required. To use another local port:

```bash
python3 -m app.server --port 8766
```

Stop with Ctrl+C. The application intentionally binds only to loopback. It is
not an authenticated multiuser service or a public deployment target. Do not
reverse-proxy it onto a network or serve the repository root.

## Make a useful package

1. Create a Custom GPT, Agent Skill, workflow or web-tool project.
2. State its purpose, audience, inputs, outputs, constraints and instructions.
3. Define components and their dependencies. Give each acceptance case a clear
   expected result, then record what you actually observed when testing it.
4. Attach relevant pinned Skillz references when useful. These are optional source
   links, not automatically installed or executed agents.
5. Save and review the validation report. Unrun or failed cases are not evidence
   of readiness. Material specification changes invalidate earlier test results.
6. Download JSON for portable backup/import, Markdown for review, or a ZIP package.

The web-tool ZIP contains a runnable record-management starter with add, complete,
reopen and filter behavior. It also contains your complete specification and
handoff material. It is a starting implementation to adapt, not an AI-generated
implementation of arbitrary requirements. Custom GPT/Skill/workflow exports are
reviewable authored packages; platform publication remains a separate action.

Import creates a new project identity, preserves the source identity in its
history and resets evaluation results to unrun. Archive hides completed or
paused drafts from active work while keeping them recoverable.

## Persistence and backup

By default, private SQLite working data is stored in `.foundry-data/`, which is
ignored by Git. It persists across browser reloads and server restarts. Worktree
copies have independent data folders. Export JSON regularly and before moving
or removing a worktree. For a full backup, stop the server, copy the entire
`.foundry-data/` folder to your private backup location, then restart.

`--data-dir` accepts a private directory of your choice. Keep it out of source
control. JSON exports may contain your authored private information; choose
where to share them. The app makes no outbound model requests and has no telemetry.

Revisions prevent a stale tab from silently overwriting a newer save. If a save
conflicts, preserve your unsaved text, reopen the current project and reconcile
it. Validation and exports refer to saved records.

## Reference material and boundaries

The reference shelf exposes a fixed allowlist of PromptChain, scaffold, current
PulseBook, vernacular and canon-overview text. It cannot browse arbitrary files.
It does not execute those prompts or modify their sources. Historical text may
retain the older cross-FoundRy model; the current universe boundary is explained
in the [research report](../research/okhp3-universe-2026-09-07/report.html).

`app/data/skills.json` lists selected public Skillz distribution contracts with
full commit revisions and source paths. Refresh it only after verifying each
new target file; do not treat catalog generation timestamps as behavioral proof.
This is a curated reference shelf, not a replacement catalog or live sync.

The API contract is in [api-contract.md](api-contract.md). There are no endpoints
for executing code, fetching arbitrary URLs, changing canon, sending messages,
publishing repositories or invoking AI providers.

## Verify

```bash
python3 -m unittest discover -s app/tests -v
python3 -m py_compile app/server.py
node --check app/static/app.js
git diff --check
```

The service tests cover persistence, validation, request boundaries and exported
packages. The dated [verification record](verification.md) distinguishes these
checks from browser behavior and external-service evidence. Historical maintenance
audits have documented baseline mismatches and do not establish application health.
