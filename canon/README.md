# canon/ — Canonical Data Ledger System

> **This folder is the single source of truth for the entire Glee-fully ecosystem.**
> All GPT governance, identity, tone, runtime behavior, and lifecycle rules are declared
> here. These files override all other sources — GPT-local logic, legacy schema, prompt
> context, and any prior version of the same ledger.

---

## Purpose

The `canon/` folder houses the **9 canonical dataLedger files** — a schema system that
governs 40+ Custom GPTs across the Glee-fully Personalizable Tools™ ecosystem. Think of
this as the constitution + database of record for the entire suite. Every GPT built in
this ecosystem is validated against, and routes its output through, these files.

The ledger system was designed to solve the core problem of drift: when a network of
dozens of specialized GPTs evolves over time, without a shared authority, each GPT
gradually diverges in tone, behavior, and identity. The canonical ledger system prevents
that. Ledgers are locked with `::CanonSeal[...]::` tags and grow only forward — no
content is ever removed, only expanded or retired.

---

## The 9 Ledger Files

| File | Role | Status | Priority |
|------|------|--------|----------|
| [`dataledger-registry-v3.md`](dataledger-registry-v3.md) | Master entity registry — all registered Tools, Tool-ettes, Functions, Function-ettes with IDs, ChatGPT links, descriptions, and lifecycle tags | Active | Critical |
| [`dataledger-persona-v3.md`](dataledger-persona-v3.md) | Voice archetypes, tone overlay definitions, persona drift event logs | Active | Critical |
| [`dataledger-parameters-v3.md`](dataledger-parameters-v3.md) | Runtime flags, execution toggles, BLEED GLEE / Calm mode switches, suffix law rules | Active | Critical |
| [`dataledger-system-v3.md`](dataledger-system-v3.md) | PME/CME engine schemas, suffix compliance rules, lifecycle control logic | Active | Critical |
| [`dataledger-hydration-v3.md`](dataledger-hydration-v3.md) | Runtime snapshots, rehydration schemas, cross-GPT session handoff | Active | Critical |
| [`dataledger-narrative-v3.md`](dataledger-narrative-v3.md) | Finalized brand essays, storyworlds, documentation-grade narrative clauses | Active — seeded | High |
| [`dataledger-ideation-v3.md`](dataledger-ideation-v3.md) | Raw idea seeds, candidate Tool-ette stubs, tonal fragments awaiting promotion | Active — seeded | Medium |
| [`dataledger-archive-v3.md`](dataledger-archive-v3.md) | Retired logic, sunset entities, deprecated overlays — preserved, never deleted | Active — seeded | Reference |
| [`dataledger-processing-v3.md`](dataledger-processing-v3.md) | Legacy mid-run scaffolds — deprioritized as of v3.0.1 | Legacy | Low |

---

## Clause Lifecycle

Canonical clauses follow a strict one-way lifecycle. Rehydration from
`dataledger-hydration-v3.md` is the only allowed re-entry point.

```
dataledger-ideation-v3.md        (spark — raw ideas and seeds)
        |
        v
dataledger-registry-v3.md        (register the entity with ID + metadata)
dataledger-persona-v3.md         (lock tone overlay and persona assignment)
dataledger-parameters-v3.md      (declare runtime flags and toggles)
        |
        v
dataledger-narrative-v3.md       (finalized canonical clauses and brand copy)
        |
        v
dataledger-archive-v3.md         (retired / deprecated — !LEGACY_RETIRED)
```

Rehydration path:
```
dataledger-hydration-v3.md  -->  dataledger-ideation-v3.md  (with !CLAUSE update)
```

---

## How Entries Are Structured

Each registered entity in `dataledger-registry-v3.md` contains:

- **Manifest title** and suite context
- **Builder description** (≤300 chars — ready to paste into ChatGPT Builder)
- **System Instructions snapshot** (the actual GPT instructions)
- **Sample Conversation Starters** (YAML-boxed)
- **Embedded YAML schema block** (machine-readable metadata)
- **PME status, tone overlay, and lifecycle tags**

Each entry is stamped with a `!CLAUSE` ID:

```yaml
!CLAUSE: !PME_READY
ID: Toolette.ResumeBuilder.1.0.0
Summary: Guides resume creation and export
TargetPhase: Gleam
DeclaredBy: Glee-fully FoundRy
```

---

## Governance Rules (Applies to This Folder)

| Rule | Detail |
|------|--------|
| **Growth-Only** | Never delete content. Retire to `dataledger-archive-v3.md` with `!LEGACY_RETIRED` |
| **CanonSeal Integrity** | `::CanonSeal[...]::` tags must not be removed or altered under any circumstance |
| **Override Authority** | These files override GPT-local logic, prompt context, and all legacy (v1/v2) schema |
| **No Prompt-Local Memory** | All runtime continuity must flow through `dataledger-hydration-v3.md` |
| **Output Signatures** | All canonical outputs must carry a `!CLAUSE` ID declared in `dataledger-registry-v3.md` |
| **Tone Fallback** | Untagged threads default to `GleeTone.A1` and log via `!DRIFT_EVENT` in persona ledger |
| **Conflict Resolution** | When ledgers conflict, priority: registry > persona > parameters > system |

---

## Who Uses This Folder

| Actor | How They Use It |
|-------|----------------|
| **GPT Builder (human operator)** | References during PROMPT03 (Registry Upload) to validate new entity IDs and check for conflicts |
| **AI agents** | Read these files to understand current entity state, tone rules, and what exists in the ecosystem |
| **The PromptChain** | Routes all clause outputs to the appropriate ledger at each lifecycle stage |
| **Evaluation framework** | PulseBook evaluation rubrics cross-reference registry entries for compliance checks |
| **Snapshot system** | `snapshots/` contains dated point-in-time copies of these files for rollback reference |

---

## Relationship to Other Folders

```
canon/         <-- governed by --> governance/glee-fully-project-governance-v3-0-1.md
canon/         <-- validated by --> evaluation/ (PulseBook rubrics)
canon/         <-- populated by --> prompts/ (PromptChain creates registry entries)
canon/         <-- described in --> docs/ (technical + narrative overviews)
canon/         <-- archived in  --> snapshots/ (dated historical captures)
```

---

## Current State (as of v3.1.0)

- **registry**: Active — contains live ChatGPT links for 40+ deployed GPTs
- **persona, parameters, system, hydration**: Active and schema-complete
- **narrative, ideation, archive**: Seeded — structurally initialized, content being populated
- **processing**: Deprioritized — preserved for legacy reference only
