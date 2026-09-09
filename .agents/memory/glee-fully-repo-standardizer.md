---
name: glee-fully-repo-standardizer skill
description: Covers location, usage, and design decisions for the scaffold skill deployed to all 50 Glee-fully child repos.
---

# glee-fully-repo-standardizer skill

## Location

`.agents/skills/glee-fully-repo-standardizer/`
- `SKILL.md` — agent instructions and trigger conditions
- `assets/glee-fully-brand.json` — canonical brand/tone/persona payload
- `scripts/scaffold.py` — the scaffold generator

## How to Run

From the root of any glee-fully child repo:

```bash
python3 /path/to/.agents/skills/glee-fully-repo-standardizer/scripts/scaffold.py \
  --tier toolette \
  --name "Entity Name" \
  --id 01a \
  --parent "Parent Tool Name" \
  --parent-url "https://chatgpt.com/g/g-..." \
  --chatgpt-url "https://chatgpt.com/g/g-..."
```

## Key Args

| Arg | Required | Default |
|-----|----------|---------|
| `--tier` | No | auto-detected from manifest or repo name |
| `--name` | No | derived from directory name |
| `--id` | No | empty (placeholdered) |
| `--parent` | No | empty (placeholdered) |
| `--parent-url` | No | empty |
| `--chatgpt-url` | No | empty |
| `--tone` | No | tier default (toolbox=BledsGLEE, tool=GleeRich, toolette=GleeLite) |
| `--inventory` | No | canonical catalog is used automatically; an explicit path overrides it |
| `--dry-run` | — | preview without writing |
| `--audit` | — | show missing files only, do not write |
| `--overwrite` | — | overwrite existing files (default: skip) |

## Tier Differences (v1.1.0)

- toolette: 9 dirs, 17 files (includes gpt/knowledge/ with KF-README.md)
- tool: 8 dirs, 16 files (no gpt/knowledge/)
- toolbox: 8 dirs, 16 files (same as tool)

## Inventory Pre-Population (v1.1.0)

The scaffold automatically resolves
`inventory/inventory-of-toolbox-tools-and-tool-ettes.md` relative to the
standardizer repository. Pass `--inventory /path/to/inventory-of-toolbox-tools-and-tool-ettes.md`
to intentionally override the catalog. The importer auto-fills:
- `gpt/description.md` ← Full Description
- `docs/overview.md` ← Elevator Pitch (in "What It Is" section)
- `docs/functions.md` ← Primary Functions (each with stub Trigger/Output/Notes)
- `gpt/instructions.md §1` ← Full Description + parent link + ChatGPT URL

Match is by `--id` first, then `--name`. Uses FoundRy inventory at
`inventory/inventory-of-toolbox-tools-and-tool-ettes.md`.

## Design Decisions

**Why:** Brand JSON is always written/updated. It is the single source of truth for
tone/persona across all 50 repos. Every child repo gets an identical copy in assets/.

**Why:** Files that already exist are skipped by default (--overwrite required).
This makes re-running safe after content has been added.

**Why:** Templates embed tone instructions directly into gpt/instructions.md stubs
so the right tone block is already in place when a developer opens the file.

**Why:** `from __future__ import annotations` required for Python 3.11 type hint
compatibility (`str | None` syntax).

**Why:** `gpt/instructions.md` follows the Operator's Cathedral Layout 8-section
standard (§1 Identity, §2 Persona/Tone, §3 Dialogue Policy, §4 Core Functions,
§5 Knowledge Policy, §6 Output Policy, §7 Safety, §8 Examples). Reference:
`governance/operators-cathedral-layout.md`.

**Why:** `gpt/knowledge/KF-README.md` (not .gitkeep) added to toolette tier.
Guides the portfolio approach (8 KF types: Charter, Glossary, Policies,
Procedures, Templates, Good/Bad Examples, FAQ) per OKH KF Playbook v1.0.

## Inventory Parser Notes

- Inventory format: `**🪚 Parent Tool (Branch🌵):**` uses `:**` (colon before close-bold)
  → regex must be `:\*\*` not `\*\*:` for parent matching
- Elevator pitch format: `📒 **EntityName** text...`
  → strip with `re.sub(r"^📒\s*(?:\*+[^*]+\*+\s*)?", "", pitch)` to get clean text
- Tool display name in inventory includes "Glee-fully " prefix (e.g., "Glee-fully Discovered Careers")
  → match by `--id` is more reliable than `--name` for Tool tier entities

The canonical inventory currently begins with a UTF-8 BOM, so the first Toolbox
heading is not matched by the parser's anchored header regex while later Tool and
Tool-ette entries are. Until the parser normalizes the BOM, regression checks
should exercise a later known entry rather than treating the first Toolbox entry
as proof of importer health.

**Why:** This is an input-format edge case that is not obvious from the rendered
Markdown and can make a seemingly valid catalog appear empty to the importer.

**How to apply:** Normalize leading BOM characters when improving the parser; keep
the catalog contract check focused on a known entry that the current parser can
actually import.
