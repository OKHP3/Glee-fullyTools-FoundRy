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
| `--dry-run` | — | preview without writing |
| `--audit` | — | show missing files only, do not write |
| `--overwrite` | — | overwrite existing files (default: skip) |

## Tier Differences

- toolette: 9 dirs, 17 files (includes gpt/knowledge/)
- tool: 8 dirs, 16 files (no gpt/knowledge/)
- toolbox: 8 dirs, 16 files (same as tool)

## Design Decisions

**Why:** Brand JSON is always written/updated. It is the single source of truth for
tone/persona across all 50 repos. Every child repo gets an identical copy in assets/.

**Why:** Files that already exist are skipped by default (--overwrite required).
This makes re-running safe after content has been added.

**Why:** Templates embed tone instructions directly into gpt/instructions.md stubs
so the right tone block is already in place when a developer opens the file.

**Why:** `from __future__ import annotations` required for Python 3.11 type hint
compatibility (`str | None` syntax).
