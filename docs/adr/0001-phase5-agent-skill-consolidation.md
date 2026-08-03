# ADR-0001: Phase 5 — Consolidate 50 GPTs into Domain Agent Skills

## Status

Accepted

## Date

2026-08-03

## Context

The Glee-fully ecosystem was built as 50 individual Custom GPTs, each scoped to a narrow
domain (journaling, recipe collection, habit tracking, etc.). This 1:1 structure was an
engineering workaround for the OpenAI GPT Builder's ~8k instruction payload limit — not
an inherent domain requirement. When payload space is exhausted, a GPT must be split into
a narrower child entity.

Agent Skills have a fundamentally different architecture:

- `SKILL.md` is the discovery and activation layer (kept lean)
- Python scripts, data files, and reference assets carry the functional payload
- No equivalent payload wall exists

The 50 GPT hierarchy was the workaround, not the product.

Additionally, cross-cutting capabilities exist across multiple GPTs:
- **Collection management** (recipes, books, items, tasks) — shared schema
- **Journaling and reflection** — shared prompting and formatting patterns
- **Habit and goal tracking** — shared lifecycle model
- **Personalization overlays** — tone, style, and preference profiles
- **Notification and reminder logic** — shared scheduling model

## Decision

Phase 5 will consolidate 50 GPTs into 7–10 domain Agent Skills, organized around genuine
domain boundaries rather than payload-driven splits.

The consolidation sequence is domain-by-domain, not a bulk migration:

1. Each domain Agent Skill is built and validated.
2. The child repos it replaces are archived at that time.
3. No bulk migration or pre-consolidation repo restructuring is done before Phase 5 begins.

`SKILL.md` for each Agent Skill remains the discovery layer only (lean). Python scripts
carry the functional workflow.

## Decision Drivers

- Payload wall constraint does not exist for Agent Skills — hierarchy workaround is no longer needed
- Cross-cutting capabilities are more maintainable as shared procedures in a composable skill
- 50 individual Agent Skills would recreate the same fragmentation problem
- Phase 1–4 work (getting all 50 GPTs to v1.0) proceeds in parallel; Phase 5 does not block on it

## Considered Options

### Option 1: 1:1 conversion (50 GPTs → 50 Agent Skills)
- **Pros:** Direct mapping; no semantic redesign required
- **Cons:** Recreates the fragmentation; misses consolidation opportunity; more maintenance overhead

### Option 2: 7–10 domain Agent Skills (chosen)
- **Pros:** Matches actual domain boundaries; reduces maintenance; enables shared procedure libraries
- **Cons:** Requires domain boundary design work; semantic loss analysis needed per domain

### Option 3: Single monolithic Agent Skill
- **Pros:** Simplest distribution
- **Cons:** Destroys discoverability; trigger precision collapses; not composable

## Consequences

### Positive
- Maintenance surface shrinks from 50 entities to 7–10
- Cross-cutting capabilities (collections, journaling, habits) get a proper shared implementation
- Agent Skill packages are self-contained with scripts + assets + SKILL.md
- Child repos are archived as each domain skill goes live — clean, staged deprecation

### Negative
- Domain boundary design work required before Phase 5 begins
- Semantic loss analysis needed per domain (handled by `okhp3-gpt-skill-conversion-plan` skill)
- Some GPT-specific behaviors may not transfer cleanly (retrieval ranking, UI-only features)

### Risks
- Scope creep on domain boundary design delaying Phase 5 start
- Mitigation: boundaries can be drafted as proposals during Phase 4 without blocking Phase 4 work

## Implementation Notes

- Full strategy and open questions: `docs/agent-skill-conversion-strategy.md`
- Conversion planning skill: `.agents/skills/okhp3-gpt-skill-conversion-plan/`
- Skill authoring workflow: `.agents/skills/okhp3-skill-foundry/`

## Related Decisions

- Future ADR (pending): Domain boundary map for the 7–10 Agent Skills
- Future ADR (pending): Phase 6 decision — custom SPA vs. Agent Skills only

## References

- `docs/agent-skill-conversion-strategy.md` — Full Phase 5 planning document
- Session notes: voice memo transcripts in `attached_assets/` (2026-08-03 session)
