# AGENTS.md — Glee-fullyTools-FoundRy

> **For AI agents, assistants, and LLM tools navigating this repository.**
> Read this file first. It tells you what this repo is, what it contains,
> what you are and are not allowed to do here, and where to find everything.

---

## What This Repository Is

This is the **private workbench and relay FoundRy** for the Glee-fully Personalizable
Tools™ ecosystem — a governed network of 40+ Custom GPTs organized as a living tree
(Toolbox → Tools → Tool-ettes → Functions → Function-ettes).

This is NOT a web application. Do not configure web server workflows, deployment
targets, or live-site infrastructure for this repository.

---

## Authority Chain

```
OKHP3/OverKill-Hill  (root governance — overrides all)
  └─ OKHP3/Glee-fullyTools-FoundRy  ◀ THIS REPO
       └─ glee-fully-gpt00-*  through  glee-fully-gpt07-*
```

Parent FoundRy governance applies here. When in conflict, defer to the root.

---

## Governed Child Repository Families

| Family Pattern | Scope |
|----------------|-------|
| `glee-fully-gpt00-*` | Toolbox (Trunk) entities |
| `glee-fully-gpt01-*` | Discovered Careers branch |
| `glee-fully-gpt02-*` | Treasured Finds branch |
| `glee-fully-gpt03-*` | Tasty Tracker branch |
| `glee-fully-gpt04-*` | Traveler's Guide branch |
| `glee-fully-gpt05-*` | Organized Life branch |
| `glee-fully-gpt06-*` | Healthy Bee-ing branch |
| `glee-fully-gpt07-*` | Identity Known branch |

---

## Directory Map

### `canon/` — The Authoritative Source of Truth

The 9 canonical dataLedger files. These override all other sources.
**Do not remove content. Do not alter CanonSeal tags.**

| File | Role | When to Read |
|------|------|-------------|
| `dataLedger_registry_v3.md` | All registered GPT entities and IDs | Checking entity existence, adding new GPTs |
| `dataLedger_persona_v3.md` | Tone overlays and persona schemas | Tone questions, overlay assignments |
| `dataLedger_parameters_v3.md` | Runtime flags and suffix rules | Execution modes, toggle decisions |
| `dataLedger_system_v3.md` | PME/CME engine schemas | Lifecycle questions, engine logic |
| `dataLedger_hydration_v3.md` | Runtime snapshots and handoff schema | Cross-GPT continuity, thread restoration |
| `dataLedger_narrative_v3.md` | Finalized narrative clauses | Brand copy, canonical descriptions |
| `dataLedger_ideation_v3.md` | Active idea seeds | Finding candidate new Tools/Tool-ettes |
| `dataLedger_archive_v3.md` | Retired logic | Checking deprecation status |
| `dataLedger_processing_v3.md` | ⚠️ Legacy only — deprioritized | Only for pre-v3.0.1 trail lookup |

### `governance/` — Directives and Cathedral Layout

| File | Role |
|------|------|
| `glee-fully_project_governance_v3.0.1.md` | Canonical Governance Directive — primary rule document |
| `glee-fully_project_instructions.md` | Project-level execution compliance instructions |
| `00-glee-fully-strategy-center_instructions.md` | StrategyCenter project instructions |
| `operator's-cathedral-layout-📐.md` | Master architecture reference (865KB — comprehensive layout) |

### `docs/` — Overviews and Synthesis

| File | Role |
|------|------|
| `gleefully_technical_overview.md` | Engineering architecture, PromptChain lifecycle, role discipline |
| `gleefully_narrative_overview.md` | Brand story, ecosystem metaphors, tone philosophy |
| `structure-and-ordering-for-custom-gpt-instruction-blocks.md` | GPT instruction block ordering rules |

### `prompts/` — Build Engine and Scaffolds

| File | Role |
|------|------|
| `glee-fully-builder-ready-promptchain-v2.0.md` | Primary GPT forge engine (PROMPT00–PROMPT05+) |
| `custom_gpt_scaffold.md` | Base GPT instruction scaffold |
| `custom_gpt_hybrid_scaffold.md` | Hybrid scaffold for branch/twig combinations |
| `glee-fully_tools_megaprompt.md` | Megaprompt for multi-tool operations |

### `vernacular/` — Voice and Tone Reference

| File | Role |
|------|------|
| `🦋-glee-fully-vernacular-complete.md` | Full voice library — all tone patterns, phrases, expressions |
| `🦋-glee-fully-vernacular-lite.md` | Condensed quick-reference for tone compliance |

### `templates/` — GPT Instruction Template Variants

FrankenTemplate iterations (alphabetically lettered: a, ab, ae, c, e, g, h, i, j, k, m, n, o, q, r, s, t, u, v, y).
Each letter represents a distinct structural or tonal iteration. Use the latest (`ae` or `y`) as base.

### `evaluation/` — GPT Quality Rubrics

| File | Role |
|------|------|
| `gpt-pulsebook-evaluation-v1.4.md` | PulseBook evaluation v1.4 |
| `gpt-pulsebook-evaluation-v1.6.md` | PulseBook evaluation v1.6 |
| `gpt-pulsebook-evaluation-v1.7.md` | PulseBook evaluation v1.7 (latest) |

### `inventory/` — Entity Catalog

| File | Role |
|------|------|
| `inventory_of_toolbox_tools_and_tool-ettes.md` | Full catalog of all registered Tools and Tool-ettes |

### `web-templates/` — Webpage Template Assets

Static HTML/CSS templates for Glee-fully child repo public-facing pages.
**These are template assets only. Do not serve from this workbench.**

### `snapshots/` — Historical State Captures

Point-in-time ledger and template snapshots. Latest is `2025-09-14/`.
Use for lineage verification and rollback reference only.

---

## Governance Rules You Must Follow

### 1. Expansion-Only Discipline
Never delete, simplify, or reduce existing content in any canonical file.
All edits add detail, specificity, or capability. Existing clauses are never removed.

### 2. Growth-Only Mutation
If a file has a `::CanonSeal[...]::` tag, it is locked for growth only.
Any edit must preserve all prior content and extend it.

### 3. Canon Authority Hierarchy
```
canon/ dataLedger_* files  >  governance/ directives  >  GPT-local logic
```
When sources conflict, the canon files win.

### 4. Output Signature Requirement
All outputs from canonical logic must carry a `!CLAUSE` ID declared in
`canon/dataLedger_registry_v3.md`. Format:
```yaml
!CLAUSE: !PME_READY
ID: [EntityType].[Name].[MajorVersion].[MinorVersion].[Patch]
Summary: [One line]
TargetPhase: [Gleam / Ideation / Archive]
DeclaredBy: Glee-fully FoundRy
```

### 5. Tone Default
Threads without an explicit overlay default to `GleeTone.A1`
(uplifting, whimsical, clear, and articulate). Log deviations in
`canon/dataLedger_persona_v3.md` using `!DRIFT_EVENT`.

### 6. No Prompt-Local Memory
Runtime state must not be stored in GPT-local logic or prompt context.
All continuity uses `canon/dataLedger_hydration_v3.md`.

### 7. Suffix Law
`-R` and `-Rᵧ` suffixes are exclusive to OverKill Hill P³ and The GPT Found-Rᵧ.
Glee-fully GPTs are **exempt** — do not apply these suffixes here.
Violations must be retired to `canon/dataLedger_archive_v3.md` with `!LEGACY_RETIRED`.

### 8. This Is a Workbench — No Web Server
Do not configure HTTP server workflows, deployment targets, or static site builds.
The `web-templates/` folder is template source material, not a deployable site.

---

## Required Files for Every Child Repository

```
AGENTS.md       ← AI agent navigation (this format)
README.md       ← Human-readable overview
CHANGELOG.md    ← Version history
LICENSE.md      ← License declaration
manifest.yaml   ← Repo metadata (schema_version, type, brand_domain, parent_foundry)
```

---

## Clause Lifecycle (Quick Reference)

```
ideation_v3.md  →  registry_v3.md / persona_v3.md / parameters_v3.md
                →  narrative_v3.md  (finalized)
                →  archive_v3.md    (retired)
```

Clauses may re-enter ideation from `hydration_v3.md` with updated `!CLAUSE` tags.

---

## Key Contacts and Links

| Resource | URL |
|----------|-----|
| Public Tools Site | https://glee-fully.tools |
| OKHP3 Universe | https://overkillhill.com/universe |
| Contact | contact@glee-fully.tools |

---

## Principle

> *The capability is durable. The platform wrapper is temporary.*
