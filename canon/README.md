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
| [`dataLedger_registry_v3.md`](dataLedger_registry_v3.md) | All registered Tools, Tool-ettes, Functions, Function-ettes and their IDs | ✅ Active |
| [`dataLedger_persona_v3.md`](dataLedger_persona_v3.md) | Voice archetypes, tone overlays, persona drift logs | ✅ Active |
| [`dataLedger_parameters_v3.md`](dataLedger_parameters_v3.md) | Runtime flags, execution toggles, suffix mode rules | ✅ Active |
| [`dataLedger_system_v3.md`](dataLedger_system_v3.md) | PME/CME engine schemas, suffix compliance, lifecycle control | ✅ Active |
| [`dataLedger_hydration_v3.md`](dataLedger_hydration_v3.md) | Runtime snapshots, rehydration schemas, cross-GPT handoff | ✅ Active |
| [`dataLedger_narrative_v3.md`](dataLedger_narrative_v3.md) | Final essays, storyworlds, documentation-grade narrative clauses | 🌱 Seeded |
| [`dataLedger_ideation_v3.md`](dataLedger_ideation_v3.md) | Idea seeds, raw stubs, tonal fragments | 🌱 Seeded |
| [`dataLedger_archive_v3.md`](dataLedger_archive_v3.md) | Retired logic, sunset entities, drifted overlays | 🌱 Seeded |
| [`dataLedger_processing_v3.md`](dataLedger_processing_v3.md) | ⚠️ Deprioritized — legacy mid-run scaffolds only | 🔻 Legacy |

---

## Clause Lifecycle Flow

```
🌱 ideation_v3.md        # Spark — raw ideas and seeds
     ↓
📁 registry_v3.md        # Register the entity
   persona_v3.md         # Lock tone/overlay
   parameters_v3.md      # Declare runtime flags
     ↓
✨ narrative_v3.md        # Finalized canonical clauses
     ↓
☠️ archive_v3.md          # Retired / deprecated logic
```

Clauses may re-enter ideation if rehydrated from `hydration_v3.md` with updated `!CLAUSE` tags.

---

## Governance Rules

- **Growth-Only:** Never delete content from these files. Retire to `archive_v3.md` using `!LEGACY_RETIRED`.
- **CanonSeal:** Do not remove or alter `::CanonSeal[...]::` tags.
- **Output Signatures:** All outputs must carry a `!CLAUSE` ID declared in `registry_v3.md`.
- **No Prompt-Local Memory:** All continuity flows through `hydration_v3.md`.
- **Tone Fallback:** Untagged threads default to `GleeTone.A1` and log to `persona_v3.md` via `!DRIFT_EVENT`.
