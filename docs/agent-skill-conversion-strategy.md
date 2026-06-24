# Agent Skill Conversion Strategy
## Glee-fully Personalizable Tools™ — Phase 5 Architecture

**Status:** Planning Document — Pre-Phase 5
**Author:** OverKill Hill P³ (Jamie Hill)
**Created:** 2026-06-24
**Expansion-Only:** This document grows forward. Sections are never removed, only elaborated.

---

## Core Architectural Insight

### Why 50 GPTs Does Not Mean 50 Agent Skills

The Glee-fully ecosystem was built as 50 Custom GPTs (1 Toolbox, 7 Tools, 42 Tool-ettes)
specifically because of a **platform constraint**: Custom GPTs have an ~8,000 character
instruction block limit (~2,000 tokens). To distribute meaningful functional logic across
the suite, the hierarchy became the payload management strategy:

```
Toolbox (Trunk)       ← routing only, minimal payload
  └─ Tool (Branch)    ← category routing, light logic
       └─ Tool-ette   ← single-task executor, full payload
            └─ Function ← atomic logic unit
```

Each layer was scoped tightly so its instruction payload fit within the 8k limit.
**The hierarchy was an engineering workaround, not an inherent domain requirement.**

Agent Skills have a fundamentally different architecture:

| Dimension | Custom GPT | Agent Skill |
|-----------|-----------|-------------|
| Instruction limit | ~8,000 chars hard limit | SKILL.md is the *discovery* layer — lean by design |
| Functional payload | Embedded in instruction block | Packaged as Python scripts, data files, and assets alongside SKILL.md |
| Distribution unit | Config-centric (instruction text) | Package-centric (SKILL.md + scripts/ + assets/ + data/) |
| Cross-GPT reuse | Not possible — each GPT is isolated | Scripts can be shared across skills or called by multiple skills |
| Hierarchy requirement | Required for payload management | Optional — collapse if domain logic fits in shared scripts |

### The Consolidation Principle

> A domain that required 6-7 Custom GPTs to stay within instruction limits
> may be expressible as **1-2 Agent Skills** where the scripts carry the logic.

Instead of converting 50 GPTs → 50 Agent Skills, Phase 5 should ask:
**"What is the smallest set of Agent Skills that delivers the same functional surface?"**

Preliminary answer: **7–10 domain Agent Skills**, each packaging:
- A lean SKILL.md (~200–400 lines) covering discovery, activation, and top-level orchestration
- Multiple Python scripts covering the functional tasks previously split across Tool-ettes
- Shared data files (tone overlays, entity registries, output templates)
- Assets (brand JSON, schema files)

---

## Identified Cross-Cutting Patterns

These functional patterns repeat across multiple Tool-ettes and are strong candidates
for shared scripts within consolidated Agent Skills:

### 1. Collection Management
**Appears in:** Treasured Finds (#02), Tasty Tracker (#03), Traveler's Guide (#04),
Organized Life (#05), Identity Known (#07)

**Pattern:** Add item → tag/categorize → search/filter → export list → manage versions

**Consolidation opportunity:** One `collection.py` script parameterized by collection type
(books, recipes, destinations, tasks, journal entries). The Agent Skill SKILL.md describes
the collection domain; the script handles the logic regardless of what's being collected.

---

### 2. Export / Format Pipeline
**Appears in:** Resume Builder (#01a), Resume Customizer (#01b), Letter Composer (#01d),
and any Tool-ette that produces a deliverable document

**Pattern:** Generate content → apply format template → offer export (DOCX, PDF, plain text)

**Consolidation opportunity:** One `export_pipeline.py` script that accepts content +
format target + template ID. Shared across career, writing, and any other domain that
produces exportable documents.

---

### 3. Profile / Intake Flow
**Appears in:** Career Fitness (#01c), bLinkIn Tuner (#01e), Healthy Bee-ing (#06),
Identity Known (#07)

**Pattern:** Gather user profile data → assess against a standard → generate
gap analysis or recommendations → track over time

**Consolidation opportunity:** One `profile_intake.py` script with domain-specific
schemas passed as data files. The scoring logic is identical; what changes is the rubric.

---

### 4. Job/Opportunity Matching
**Appears in:** Resume Customizer (#01b), Career Seeker (#01f)

**Pattern:** Input: user profile + target opportunity → keyword extraction →
gap analysis → tailored output

**Consolidation opportunity:** One `opportunity_match.py` that handles resume-to-job,
profile-to-role, and potentially recipe-to-pantry or similar matching patterns.

---

### 5. Routing / Navigation Logic
**Appears in:** Toolbox (#00), all 7 Tools (#01–#07)

**Pattern:** Understand user intent → identify best sub-entity → provide link + framing

**Consolidation opportunity:** One routing Agent Skill (the "Toolbox equivalent") with
a routing table data file that maps intent signals to skill recommendations. The routing
table updates as skills are added; the routing logic stays constant.

---

## Proposed Phase 5 Architecture: 7–10 Domain Agent Skills

Preliminary consolidation model (to be refined before Phase 5 begins):

| Agent Skill | Covers | Packages |
|-------------|--------|---------|
| `gleefully-careers` | Tool #01 + all 6 Tool-ettes | resume_builder.py, resume_customizer.py, career_fitness.py, letter_composer.py, blinkIn_tuner.py, career_seeker.py, export_pipeline.py, opportunity_match.py |
| `gleefully-collections` | Tool #02 (Treasured Finds) + Tool-ettes | collection.py (parameterized for items/media/collectibles), export_pipeline.py |
| `gleefully-food` | Tool #03 (Tasty Tracker) + Tool-ettes | collection.py (recipes), meal_planner.py, grocery_list.py |
| `gleefully-travel` | Tool #04 (Traveler's Guide) + Tool-ettes | collection.py (destinations), itinerary_builder.py, trip_planner.py |
| `gleefully-organize` | Tool #05 (Organized Life) + Tool-ettes | task_manager.py, dashboard_builder.py, collection.py (tasks) |
| `gleefully-wellness` | Tool #06 (Healthy Bee-ing) + Tool-ettes | profile_intake.py (wellness), habit_tracker.py, goal_tracker.py |
| `gleefully-identity` | Tool #07 (Identity Known) + Tool-ettes | journal.py, profile_intake.py (reflection), collection.py (entries) |
| `gleefully-hub` | Toolbox #00 | routing_table.yaml, suite_router.py |

**Shared package across all skills:**
- `gleefully-brand.json` — tone overlays, persona, Glee-isms
- `export_pipeline.py` — format/export logic
- `canon_schema.py` — registry validation helpers

---

## Phase Ordering and Dependencies

### Phase 1–4: All 50 GPTs to v1.0 (UNCHANGED)

The v1.0 completion work on all 50 Custom GPTs remains the correct path.
**Why this doesn't change:**

1. The GPTs are live and in active use — they must be maintained and completed regardless
   of what comes after.
2. The v1.0 process is the learning phase: building each Tool-ette's instruction block
   surfaces exactly what functionality it provides, what edge cases it handles, and where
   cross-cutting patterns live. This knowledge is what informs the consolidation model.
3. The PulseBook evaluation at v1.0 produces a precise functional map of every entity —
   that map is the Phase 5 input.
4. The canon registry entry for each entity becomes the data file that informs the
   Agent Skill routing table.

**In short: you cannot consolidate what you have not yet fully articulated.**

### Phase 5: Strategic Consolidation (Post v1.0 on all 50)

The conversion process for each domain:

```
Phase 5 Steps (per domain):
  1. Audit all Tool-ette PulseBooks for the domain
  2. Identify shared functional patterns (see Cross-Cutting Patterns above)
  3. Extract shared logic → parameterized Python scripts
  4. Write SKILL.md (lean — discovery + orchestration only)
  5. Package: SKILL.md + scripts/ + data/ + assets/
  6. Test each former Tool-ette's function against the consolidated skill
  7. Deprecate the Custom GPTs (archive in canon, update registry)
  8. Update routing table to point to Agent Skills
```

**Gates for Phase 5 start:** All 50 GPTs at pme_ready: true in their manifests.

---

## Key Design Rules for Phase 5 Agent Skills

### SKILL.md is the Discovery Layer — Keep it Lean

SKILL.md serves three functions in the Agent Skills progressive disclosure model:
1. **Discovery** (~100 tokens): `name` + `description` — what the agent sees at startup
2. **Activation** (<500 lines, <5k tokens): full SKILL.md loaded when skill is invoked
3. **Execution**: scripts and assets loaded as needed

**Rule:** SKILL.md should describe *what* the skill does and *when* to use it.
The *how* lives in the scripts. Never embed functional logic in SKILL.md.

### Scripts Carry the Functional Payload

Each domain Agent Skill will have a `scripts/` directory. Scripts should be:
- Single-responsibility (one function per script)
- Parameterized (accept domain context as arguments, not hardcoded)
- Reusable across skills where the pattern is shared
- Documented with docstrings (the script header is part of the package's self-description)

### Data Files Carry the Domain Knowledge

Knowledge that would have been in Custom GPT knowledge files becomes data assets:
- `routing_table.yaml` — intent → skill/function mapping
- `templates/` — output format templates (resume, letter, list, itinerary, etc.)
- `schemas/` — input validation schemas per domain
- `gleefully-brand.json` — always included (canonical tone + persona)

### Canonical Registry Continuity

Every entity that existed as a Custom GPT should have a canon registry entry.
Agent Skills inherit those entries; the registry tracks the conversion:
- `custom_gpt_url` → preserved (the GPT remains live during transition)
- `agent_skill_id` → added when conversion is complete
- `lifecycle_status` → `active` (GPT) → `transitioning` → `agent_skill`

---

## Open Questions (To Resolve Before Phase 5)

These require answers before consolidation architecture is finalized:

1. **Routing:** Will the `gleefully-hub` Agent Skill handle routing to other Agent Skills,
   or does each domain skill include its own routing logic?

2. **Cross-domain patterns:** The `collection.py` pattern appears across 5 domains.
   Should it be a shared library imported by multiple skills, or duplicated per skill?

3. **User session continuity:** Custom GPTs maintain context within a session.
   Agent Skills invoked by a parent orchestrator — how is context passed between skills?

4. **Knowledge file migration:** Custom GPT knowledge files (KF-CHARTER, KF-PROCEDURES, etc.)
   become data assets in the Agent Skill package. What is the migration format?

5. **Versioning:** Agent Skills follow semver (1.0.0). How does this align with the
   Custom GPT lifecycle stages (draft → active → archived)?

---

## Relationship to Existing Work

| Existing Asset | Role in Phase 5 |
|---------------|-----------------|
| `gpt/instructions.md` in each child repo | Source material for SKILL.md authoring + script logic extraction |
| `gpt/knowledge/` in each child repo | Source for data asset files (templates, schemas, examples) |
| `assets/gleefully-brand.json` | Included verbatim in every Agent Skill package |
| `pulsebook/pulsebook-v1-7.md` | Functional map used to identify cross-cutting patterns |
| `canon/registry-entry.md` | Becomes the Agent Skill registry entry |
| `inventory/inventory_of_toolbox_tools_and_tool-ettes.md` | Routing table source data |

---

*This document is Expansion-Only. New insights, patterns, and decisions are added forward.*
*CanonSeal will be applied when Phase 5 architecture is finalized and approved.*
