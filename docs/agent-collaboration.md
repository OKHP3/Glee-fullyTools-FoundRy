# Collaboration across agent hosts

Owner direction recorded September 7, 2026. Optimize useful results per token;
longer elapsed time is acceptable. The owner reports more capacity in ChatGPT,
some in Claude and a small allocation in GitHub Copilot. These are preferences,
not measured balances, model settings or permission to incur new charges.

## Scope and authority

This protocol applies to `OKHP3/Glee-fullyTools-FoundRy`. Read `AGENTS.md` first.
Its canon, public-source identity, loopback runtime and private working-data
boundaries apply to every participant. Coordination notes are operational
records, not canonical ledger entries or PME approval.

The owner reports that six regional website/FoundRy Repls are executing their
sync directives. Do not interrupt or duplicate an existing assignment. This
repository does not coordinate or authorize edits to all six. Skillz was supplied
as context only; it is not a seventh assigned workstream. Shared patterns may be
proposed for other repositories, but adoption belongs to their own assignments.

## Default division of work

| Host | Preferred contribution | Capacity discipline |
|---|---|---|
| ChatGPT / Codex | Coordination, repository analysis, implementation, conflict reasoning and integration | Use the larger existing allocation for substantial work; use tools for deterministic operations |
| Replit | Its local Git reconciliation, environment checks, running documented commands and reporting workspace-specific results | Finish the current directive first; avoid repeating research or implementation already delivered in Git |
| Claude | A bounded independent review, design critique or difficult reasoning task with a clear deliverable | Supply only the relevant contract, diff and evidence; reserve capacity for a question that benefits from another perspective |
| GitHub Copilot | A focused diff review or small, well-specified code edit | Avoid broad repository exploration, repeated full reviews and automatic expansion into unrelated improvements |

These are defaults, not capability restrictions. Prefer an available host that
can complete the work reliably within the owner's existing allocation. Token
balances are not interchangeable between services. This protocol does not share
credentials, transfer credits, launch agents or connect their conversations.
Use an existing authorized connector, or let the owner relay the task packet.
If a host lacks access, report that gap without claiming delivery or execution.

Use the least expensive capable model and lightest sufficient reasoning available
to that host. Do not select a smaller model when predictable rework would cost
more. Do not change billing, subscribe, buy credits or enable paid APIs. Report
usage only when the host exposes it; otherwise mark it unknown. Stop an unchanged
retry after the same failure recurs, package the evidence and escalate once with
a specific question. A changed diagnosis can justify another bounded attempt.

## One coordinator and one writer per scope

1. Use one existing GitHub issue or PR as the work item's coordination record.
   If none exists, the coordinator prepares the packet below and creates the
   record only within the owner's authorized scope. Until then, the owner-relayed
   packet is the handoff; do not invent a live assignment or issue URL.
2. Honor an existing coordinator. Otherwise default to the current ChatGPT/Codex
   session. Record the actual coordinator and execution host, not just a vendor.
   Only that coordinator changes assignments and chooses the integration order.
3. Before editing, the coordinator records one writer, owned paths, branch and
   acceptance criteria. A volunteer waits for assignment acknowledgment before
   overlapping edits. A comment is not an atomic lock; unresolved ownership means
   read-only work until the coordinator reconciles it. Silence is not a handoff.
4. Default to one implementation worker. Add a parallel worker only for a bounded,
   independent task with non-overlapping paths and useful work for each participant.
   Agents may propose subagents; the coordinator approves the task and capacity
   before they start. Reviewers remain read-only unless explicitly assigned a fix.
5. Use an isolated branch and checkout/worktree for each writer. Never let two
   agents switch branches or write an index in the same checkout concurrently.
   Separate worktrees still share Git refs; coordinate operations on shared refs.
6. Record status as `planned`, `assigned`, `running`, `blocked`, `review`, `merged`
   or `verified`. Record the base/head SHA when status changes. A pushed branch is
   not merged; a merged PR is not proof that Replit pulled it or that an app ran.

## Start by reconciling Git

Verify the root, origin, branch, status and unfinished Git operations. Fetch origin
without pruning, and compare against current `origin/main`, not an old handoff SHA.
Preserve local changes, unique commits and untracked authored files before any
branch switch. Keep ignored databases, secrets and backups outside public commits.
A clean, behind-only main can use `git pull --ff-only origin main`. Preserve
divergent work on a recovery ref and prepare an integration branch; never force
push, hard-reset or delete local work to manufacture parity.

Read the incoming `AGENTS.md`, `README.md`, `manifest.yaml` and relevant folder
guides after synchronization. Replit's existing sync job owns its checkout until
it reports completion or explicitly hands it over. Other hosts may work from
isolated GitHub-based checkouts on separately assigned tasks. If Replit has unique
unpublished work, inspect that work before assigning an overlapping scope.

## Small task and handoff packet

Keep this in the assigned issue/PR or send it through the owner. Do not copy entire
conversations or large ledgers when precise paths and commit references suffice.
Keep public records free of account balances, credentials, local database contents,
private transcripts and machine-specific paths.

```text
Task / issue:
Objective and acceptance criteria:
Coordinator / assigned worker / reviewer:
Repository / base SHA / branch / current head SHA:
Owned paths / exclusions / dependencies:
Status and last evidence timestamp:
Relevant instructions and source paths:
Completed changes and decision rationale:
Checks: command, result, tested SHA; NOT RUN and why:
Remaining defect or exact blocker:
Next action and receiving host:
Resource limit / escalation condition:
Recovery ref or sanitized backup confirmation:
```

The receiver acknowledges the task and source revision before writing. A handoff
should contain one precise next action. Link full logs only for failures; otherwise
summarize results. Update on milestones or new evidence. Prefer completion events
and existing CI status notifications; avoid frequent unchanged polling, duplicate
research and multiple agents re-running the same unchanged checks.

## Review, integrate and verify

The implementer performs the narrow checks appropriate to the change. For app
behavior, the documented baseline is:

```bash
python3 -m unittest discover -s app/tests -v
python3 -m py_compile app/server.py
node --check app/static/app.js
git diff --check
```

Documentation-only changes need content, link/path and whitespace review, not
invented runtime tests. Required repository CI gates still apply. Reuse checks
only for the same relevant source revision and environment; integration changes
or new evidence can require reruns. Never report a missing tool or skipped check
as a pass. An independent review is useful for consequential behavior, security
boundaries or disputed reasoning; it is not mandatory duplicate work for every typo.

The coordinator reviews the actual diff, resolves findings and integrates one PR
at a time within the owner's merge authorization. Fetch and inspect current main
before each merge, preserve substantive local work and run the necessary checks.
Do not assume review approval transfers to a changed head. Do not merge another
repository's PR, alter canon or enable public hosting merely because agents are
collaborating.

After integration, the receiving Repl fetches and fast-forwards when safe, then
reports its own HEAD, origin/main, ahead/behind counts, working-tree state and
applicable validation. Delete a completed branch only after proving integration
and checking for unique work; preserve application data before worktree cleanup.
Before archiving a Codex thread, treat that operation as potential worktree
removal: inventory dirty, untracked and ignored files; preserve required working
data and unique commits; verify archive contents and integration; then archive
the thread and prune its completed refs. Thread history and Git bundles do not
preserve uncommitted databases. Check for remaining worktrees after archiving
and report any preservation failure explicitly.

Close the work item with evidence and remaining limitations. Only report another
host as synchronized or verified after receiving its attributable completion
record or inspecting that host directly.

## Entry points and supporting references

- `AGENTS.md`: canonical repository instructions and a short collaboration summary.
- `CLAUDE.md`: existing pointer to `AGENTS.md`; no duplicate authority document.
- `replit.md`: local execution and collaboration entry point.
- `.github/copilot-instructions.md`: short Copilot entry point, following the
  [GitHub repository-instructions convention](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions).
- `.agents/skills/okhp3-replit-github-sync/SKILL.md`: Git reconciliation guidance.
- `.agents/skills/okhp3-session-handoff/SKILL.md`: evidence-bearing handoff structure.

Current assignment state is not inferred from these instructions. The owner has
reported Replit sync activity; this document does not independently verify its
completion or assign new work to any external host.

The owner subsequently authorized the [September 7 coop-pertition program](delegation/2026-09-07-coop-pertition/README.md).
Its register records 20 FoundRy and six website assignments to isolated ChatGPT/Codex
threads. Consult that dated record for actual ownership and dispatch evidence.
