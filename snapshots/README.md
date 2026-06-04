# snapshots/ — Historical State Captures

> Point-in-time captures of critical ecosystem files — ledgers, templates, vernacular,
> and architectural blueprints — preserved as **read-only historical records**.
> Snapshots serve as rollback references, version comparison baselines, and audit
> trail evidence for canon evolution over time.

---

## Purpose

The `snapshots/` folder is the ecosystem's time-machine layer. As the canonical files
in `canon/`, `templates/`, `vernacular/`, and `governance/` evolve, dated snapshots
capture the complete state of the system at meaningful moments — major schema versions,
significant template iterations, or pre-deployment checkpoints.

These are **not backups** in the operational sense. They are intentional, human-authored
state captures taken when the ecosystem reaches a milestone. They document *what existed*
at a specific date and are preserved permanently per Expansion-Only Discipline.

---

## Available Snapshots

| Folder | Date | Contents | Purpose |
|--------|------|----------|---------|
| [`2025-09-08/`](2025-09-08/) | Sep 8, 2025 | 5 ledgers + vernacular (complete + lite) + cathedral layout | Pre-template-release ledger baseline |
| [`2025-09-14/`](2025-09-14/) | Sep 14, 2025 | Everything in Sep 8 + supertemplate v1.0, v1.2, v1.5 | Post-supertemplate-series milestone |

---

## Snapshot Contents

### `2025-09-14/` (Most Recent)

```
dataledger_hydration_v3.md        Runtime continuity snapshot
dataledger_parameters_v3.md       Runtime flags and toggles
dataledger_persona_v3.md          Persona and tone overlay state
dataledger_registry_v3.md         Entity registry state at this date
dataledger_system_v3.md           PME/CME and lifecycle rule state
glee-fully-vernacular-complete.md Full voice and tone reference
glee-fully-vernacular-lite.md     Condensed voice reference
operators-cathedral-layout.md     Architectural blueprint snapshot
glee-fully-supertemplate-v1-0.md  Template: Supertemplate v1.0
glee-fully-super-template-v1-2.md Template: Supertemplate v1.2
glee-fully-super-template-v1-5.md Template: Supertemplate v1.5
```

### `2025-09-08/`

```
dataledger_hydration_v3.md
dataledger_parameters_v3.md
dataledger_persona_v3.md
dataledger_registry_v3.md
dataledger_system_v3.md
glee-fully-vernacular-complete.md
glee-fully-vernacular-lite.md
operators-cathedral-layout.md
```

---

## How to Use Snapshots

### Comparing Against Current Canon

To diff a historical ledger against the current version:

```bash
diff snapshots/2025-09-14/dataledger_registry_v3.md canon/dataledger_registry_v3.md
```

### Understanding What Changed Between Snapshots

```bash
diff snapshots/2025-09-08/dataledger_registry_v3.md snapshots/2025-09-14/dataledger_registry_v3.md
```

### Rollback Reference

If the current `canon/` file has drifted or been corrupted, use the most recent
snapshot as the reference baseline. Snapshots are never themselves "restored" over
canon — they are read and used to manually reconstruct the correct state.

---

## Governance Rules (This Folder)

| Rule | Detail |
|------|--------|
| **Read-only** | Do not edit any file inside a dated snapshot subfolder |
| **No in-place restoration** | Use snapshots as reference, not as files to copy-paste over canon |
| **Dated subfolders required** | All snapshots live inside `YYYY-MM-DD/` named folders — never loose at root |
| **Forward-only** | New snapshots are added, old ones are never deleted |
| **Coverage expectation** | A snapshot should capture all files that have changed since the previous snapshot |

---

## When to Create a New Snapshot

Create a dated snapshot when:

- A new ledger schema version is locked (e.g., v3 → v4)
- A new supertemplate or FrankenTemplate series is finalized
- A major deployment milestone is reached (new Tool or batch of Tool-ettes go live)
- Before a significant structural refactor of any canonical file
- When a governance directive version is incremented

### Creating a Snapshot

```bash
mkdir snapshots/YYYY-MM-DD
cp canon/*.md snapshots/YYYY-MM-DD/
cp vernacular/*.md snapshots/YYYY-MM-DD/
cp governance/operators-cathedral-layout.md snapshots/YYYY-MM-DD/
# Add any templates or other files that changed significantly
```

Then commit with a message like:
`snapshot: YYYY-MM-DD — [reason for snapshot]`

---

## Relationship to Other Folders

```
snapshots/    <-- captures state of  --> canon/ (ledger files)
snapshots/    <-- captures state of  --> vernacular/ (voice guides)
snapshots/    <-- captures state of  --> governance/ (cathedral layout)
snapshots/    <-- captures state of  --> templates/ (supertemplate versions)
snapshots/    <-- audit trail for    --> CHANGELOG.md (ecosystem version history)
```
