---
name: Phase 5 Agent Skill conversion strategy
description: Why 50 GPTs will not become 50 Agent Skills — architectural decision and consolidation model for Phase 5.
---

# Phase 5 Agent Skill Conversion Strategy

## The Core Decision

**50 Custom GPTs → 7–10 domain Agent Skills** (not 1:1 conversion).

**Why:** The 50-entity hierarchy (Toolbox → Tool → Tool-ette → Function) was engineered to work around the Custom GPT 8,000 character instruction limit (~2k tokens). Logic had to be distributed across many small entities because it couldn't fit in one. Agent Skills have no equivalent constraint: SKILL.md is the *discovery/activation layer* (kept lean), while Python scripts, data files, and assets ride alongside in the package. The payload distribution problem disappears.

**How to apply:** Before starting any Phase 5 conversion work, read `docs/agent-skill-conversion-strategy.md`. Do not attempt 1:1 conversion. Identify cross-cutting patterns first (collection, export pipeline, profile intake, opportunity matching, routing) then consolidate per domain.

## Phase Gate

**Phase 5 cannot begin until all 50 GPTs reach pme_ready: true.** The v1.0 completion process is the learning phase — it surfaces what each entity actually does, where patterns repeat, and what the Agent Skill functional map should look like.

## SKILL.md Architecture Rule

- SKILL.md = discovery (name + description, ~100 tokens at startup) + activation (<500 lines, <5k tokens)
- Scripts = functional payload (Python, parameterized, single-responsibility)
- Data assets = domain knowledge (templates, schemas, routing tables, brand JSON)
- SKILL.md must never embed functional logic — that belongs in scripts

## Cross-Cutting Script Patterns Identified

| Script | Covers |
|--------|--------|
| `collection.py` | Books, recipes, destinations, tasks, journal entries — parameterized by type |
| `export_pipeline.py` | DOCX/PDF/plain text output across career, writing, any deliverable domain |
| `profile_intake.py` | Gather profile → assess against rubric → gap analysis (career, wellness, identity) |
| `opportunity_match.py` | User profile + target → keyword extraction + tailored output |
| `suite_router.py` | Intent → skill recommendation (Toolbox equivalent) |

## Preliminary Domain Consolidation

| Agent Skill | Replaces |
|-------------|---------|
| `gleefully-careers` | Tool #01 + Tool-ettes #01a–f |
| `gleefully-collections` | Tool #02 + Tool-ettes |
| `gleefully-food` | Tool #03 + Tool-ettes |
| `gleefully-travel` | Tool #04 + Tool-ettes |
| `gleefully-organize` | Tool #05 + Tool-ettes |
| `gleefully-wellness` | Tool #06 + Tool-ettes |
| `gleefully-identity` | Tool #07 + Tool-ettes |
| `gleefully-hub` | Toolbox #00 |

Full strategy and open questions: `docs/agent-skill-conversion-strategy.md`
