# prompts/ — GPT Forge Engine

> The **fabrication engine** of the Glee-fully ecosystem. This folder contains the
> complete Builder-Ready PromptChain — the ritual creation sequence for forging new
> GPTs — plus two structural scaffold templates and a content synthesis megaprompt.
> Nothing new enters the ecosystem without passing through this folder.

---

## Purpose

`prompts/` is where GPTs are born. The Builder-Ready PromptChain is a sequenced,
governance-enforced series of prompts (PROMPT00 through PROMPT05+) that transforms
a raw idea or payload into a fully-compliant, canon-sealed, PME-ready GPT. Each stage
in the chain has a specific function, and the entire process is guarded by governance
clauses established at ignition.

Think of this folder as the forge floor of the cathedral — the working space where
canonical discipline is applied to raw creative material.

---

## Files

| File | Lines | Role |
|------|-------|------|
| [`glee-fully-builder-ready-promptchain-v2-0.md`](glee-fully-builder-ready-promptchain-v2-0.md) | ~5,077 | **The primary creation tool** — full PromptChain PROMPT00–PROMPT05+ with all governance clauses, stage instructions, and expansion logic |
| [`custom-gpt-scaffold.md`](custom-gpt-scaffold.md) | ~281 | Reusable single-GPT field scaffold — name, description, system instructions template with canonical block structure |
| [`custom-gpt-hybrid-scaffold.md`](custom-gpt-hybrid-scaffold.md) | ~320 | Hybrid variant scaffold — supports dual-tone or multi-role GPT construction |
| [`glee-fully-tools-megaprompt.md`](glee-fully-tools-megaprompt.md) | ~318 | Content synthesis megaprompt — multi-pass reconciliation of all canonical sources to generate web content for glee-fully.tools |

---

## The Builder-Ready PromptChain (v2.0)

The PromptChain is a **forward-only, governance-locked sequence**. Each stage must
complete before the next is initiated. The chain cannot be reversed.

### Stage Breakdown

| Stage | Name | What It Does |
|-------|------|-------------|
| **PROMPT00** | Gleefully Chain Ignition Ritual | Declares chain governance (`!EXPANSION_ONLY`, `!APPLY_ALL_CHANGES_NOW`, `!FORGEMODE`). Sets PhaseScope. Requests payload from operator. |
| **PROMPT01** | Payload Ingestion & Tool Canonization | Receives GPT payload (draft, YAML, notes, or brainstorm). Validates against canonical structure. Assigns entity role (Toolbox/Tool/Tool-ette). Binds to ledger schema. |
| **PROMPT02** | Icon Forge & Canon Gate | Creates or validates visual identity — retro 80s icon with Glee butterfly on a symbolic object. Icon is canon-locked as metadata. |
| **PROMPT03** | Registry Upload & Canon Validation | Scans all ledger entries for ID conflicts. Expands missing branches. Creates or updates `dataledger-registry-v3.md` entry with full YAML block. |
| **PROMPT04** | Team Role Enforcement | Assigns discipline metaphors. Confirms routing logic: Toolbox = Coach, Tool = Quarterback, Tool-ette = Specialist, Function = Core Skill, Function-ette = Kicker. |
| **PROMPT05** | Fusion Checkpoint & Personality Infusion | Final tone calibration. Assigns correct overlay (Bleeds GLEE, ForgeDialect.A1, or Watchkeeper.Core). Runs fusion checkpoint. Marks entity PME-ready. |
| **PROMPT06+** | Optional Expansion | Post-PME elaboration, integration, or cross-linking to sibling entities. |

### Key Governance Clauses (Active Throughout Chain)

| Clause | Meaning |
|--------|---------|
| `!EXPANSION_ONLY` | Never simplify or prune. Always expand, specify, deepen, and layer. |
| `!APPLY_ALL_CHANGES_NOW` | All approved changes are applied immediately — no toggles or stalling. |
| `!FORGEMODE` | Drift correction — realigns output to canonical overlay if deviation detected. |
| `!PME_READY` | Output stamp marking an entity as Persona, Metadata, and Export complete. |
| `!CLAUSE` | Output signature required on all canonical clause outputs. |

---

## The Custom GPT Scaffold (`custom-gpt-scaffold.md`)

A reusable fill-in-the-blank template for building GPT instruction blocks. Contains
canonical section ordering:

```
0) Identity & Ecosystem       — suffix law, taxonomy, CanonSeal
1) Persona & Tonality         — overlay, BLEED GLEE toggles, emotional calibration
2) Response Structure         — markdown rules, TL;DR, multi-phase outputs
3) [Tool-specific sections]   — functions, routing logic, export
...
N) Canonical Compliance       — !PME_READY, clause ID, registry reference
```

This scaffold is the structural companion to the FrankenTemplate series in `templates/`.
The FrankenTemplate provides the tone and persona content; the scaffold provides the
section architecture.

---

## The Megaprompt (`glee-fully-tools-megaprompt.md`)

A specialized synthesis prompt that reads the four primary canonical sources and
generates comprehensive content for all pages of the `glee-fully.tools` website:

| Source | Content Pulled |
|--------|---------------|
| `vernacular/glee-fully-vernacular-complete.md` | Tone rules, Glee-isms, overlay modes |
| `docs/gleefully-narrative-overview.docx` | Philosophy, emotional positioning |
| `inventory/inventory-of-toolbox-tools-and-tool-ettes.md` | Entity descriptions, functions |
| `docs/gleefully-technical-overview.docx` | Architecture, PromptChain, canon system |

Output: a multi-pass synthesized Markdown document covering all website sections,
leaving clearly-marked gaps for operator-specific content ("Jamie flair" stubs).

---

## When to Use Each File

| Scenario | Use This |
|----------|----------|
| Forging a new Tool-ette from scratch | `glee-fully-builder-ready-promptchain-v2-0.md` |
| Rapid single-GPT structure scaffold | `custom-gpt-scaffold.md` |
| Dual-tone or complex hybrid entity | `custom-gpt-hybrid-scaffold.md` |
| Generating or refreshing website content | `glee-fully-tools-megaprompt.md` |

---

## Relationship to Other Folders

```
prompts/    <-- governed by        --> governance/ (chain invokes governance clauses at PROMPT00)
prompts/    <-- validates against  --> canon/ (PROMPT03 checks registry, PROMPT05 checks persona)
prompts/    <-- uses scaffolds from --> templates/ (PROMPT01 accepts FrankenTemplate as payload)
prompts/    <-- produces output for --> canon/dataledger-registry-v3.md (PROMPT03 registry entry)
prompts/    <-- triggers           --> evaluation/ (PROMPT05 triggers PulseBook review)
prompts/    <-- synthesizes        --> docs/ (megaprompt reads narrative + technical overviews)
```
