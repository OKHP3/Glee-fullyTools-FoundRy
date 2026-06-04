# snapshots/ — Historical State Captures

This folder contains point-in-time captures of ledger files and template assets.
Snapshots are read-only reference material — they document the state of the FoundRy
at a specific point in time and serve as rollback references.

## Available Snapshots

| Folder | Date | Contents |
|--------|------|----------|
| `2025-09-08/` | Sep 8, 2025 | Ledger files (registry, persona, parameters, system, hydration) + vernacular + cathedral layout |
| `2025-09-14/` | Sep 14, 2025 | Same as 2025-09-08 + supertemplate v1.0, v1.2, v1.5 |

## Important

- **Do not edit snapshot files.** They are historical records.
- The **canonical (current) versions** of all ledger files live in `canon/`.
- When comparing versions, diff the `canon/` file against the relevant snapshot.
- New snapshots should be dated `YYYY-MM-DD/` format when added.

## Snapshot Contents (2025-09-14 — most recent)

```
dataledger_hydration_v3.md
dataledger_parameters_v3.md
dataledger_persona_v3.md
dataledger_registry_v3.md
dataledger_system_v3.md
glee-fully-vernacular-complete.md
glee-fully-vernacular-lite.md
operators-cathedral-layout.md
glee-fully-supertemplate-v1-0.md
glee-fully-super-template-v1-2.md
glee-fully-super-template-v1-5.md
```

## Snapshot Contents (2025-09-08)

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
