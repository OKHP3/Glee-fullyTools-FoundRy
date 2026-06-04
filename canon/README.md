# canon/ — Canonical Data Ledger Schema

This folder contains the **9 authoritative dataLedger files** for the Glee-fully
Personalizable Tools™ ecosystem. These are the single source of truth for all
governance, registry, persona, and runtime logic across all GPTs and child repositories.

> **Canon Law:** These files override GPT-local logic, tool drift, and legacy (v1/v2)
> ledger schema. Governed by `::CanonSeal[GleeCoreDirective.v3.0.1.locked]::`

---

## The 9 Ledger Files

| File | Purpose | Status |
|------|---------|--------|
| [`dataledger_registry_v3.md`](dataledger_registry_v3.md) | All registered Tools, Tool-ettes, Functions, Function-ettes and their IDs | Active |
| [`dataledger_persona_v3.md`](dataledger_persona_v3.md) | Voice archetypes, tone overlays, persona drift logs | Active |
| [`dataledger_parameters_v3.md`](dataledger_parameters_v3.md) | Runtime flags, execution toggles, suffix mode rules | Active |
| [`dataledger_system_v3.md`](dataledger_system_v3.md) | PME/CME engine schemas, suffix compliance, lifecycle control | Active |
| [`dataledger_hydration_v3.md`](dataledger_hydration_v3.md) | Runtime snapshots, rehydration schemas, cross-GPT handoff | Active |
| [`dataledger_narrative_v3.md`](dataledger_narrative_v3.md) | Final essays, storyworlds, documentation-grade narrative clauses | Seeded |
| [`dataledger_ideation_v3.md`](dataledger_ideation_v3.md) | Idea seeds, raw stubs, tonal fragments | Seeded |
| [`dataledger_archive_v3.md`](dataledger_archive_v3.md) | Retired logic, sunset entities, drifted overlays | Seeded |
| [`dataledger_processing_v3.md`](dataledger_processing_v3.md) | Deprioritized — legacy mid-run scaffolds only | Legacy |

---

## Clause Lifecycle Flow

```
dataledger_ideation_v3.md        # Spark -- raw ideas and seeds
     |
     v
dataledger_registry_v3.md        # Register the entity
dataledger_persona_v3.md         # Lock tone/overlay
dataledger_parameters_v3.md      # Declare runtime flags
     |
     v
dataledger_narrative_v3.md       # Finalized canonical clauses
     |
     v
dataledger_archive_v3.md         # Retired / deprecated logic
```

Clauses may re-enter ideation if rehydrated from `dataledger_hydration_v3.md` with updated `!CLAUSE` tags.

---

## Governance Rules

- **Growth-Only:** Never delete content from these files. Retire to `dataledger_archive_v3.md` using `!LEGACY_RETIRED`.
- **CanonSeal:** Do not remove or alter `::CanonSeal[...]::` tags.
- **Output Signatures:** All outputs must carry a `!CLAUSE` ID declared in `dataledger_registry_v3.md`.
- **No Prompt-Local Memory:** All continuity flows through `dataledger_hydration_v3.md`.
- **Tone Fallback:** Untagged threads default to `GleeTone.A1` and log to `dataledger_persona_v3.md` via `!DRIFT_EVENT`.
