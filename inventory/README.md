# inventory/ — Toolbox Entity Catalog

This folder contains the master catalog of all Tools, Tool-ettes, Functions,
and Function-ettes in the Glee-fully Personalizable Tools™ ecosystem.

## Files

| File | Purpose |
|------|---------|
| `inventory_of_toolbox_tools_and_tool-ettes.md` | Full inventory — all registered entities with descriptions, IDs, and status |

## Relationship to Canon

The inventory file is a human-readable companion to `canon/dataLedger_registry_v3.md`.
The registry is the canonical source of truth (machine-readable, YAML schema).
The inventory is the browsable catalog (narrative descriptions, organized by branch).

When adding new entities:
1. Add the entity to `canon/dataLedger_registry_v3.md` first (canonical registration)
2. Update `inventory_of_toolbox_tools_and_tool-ettes.md` with a human-readable entry
3. Both files must stay in sync — the registry wins on conflicts
