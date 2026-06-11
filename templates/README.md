# templates/ — FrankenTemplate GPT Instruction Variants

> The **iterative scaffold library** for Glee-fully GPT instruction blocks. This folder
> contains 22+ lettered variants of the FrankenTemplate — each representing a
> development-stage refinement of the canonical GPT instruction scaffold. These are
> the raw materials fed into the PromptChain to forge new Tool-ettes.

---

## Purpose

`templates/` is the forge's material supply room. Before a new GPT can be built via
the PromptChain, a structural scaffold is needed — a template that defines the shape,
sections, and required blocks of the GPT's system instructions. The FrankenTemplate
series is that scaffold, evolving through lettered iterations as the canonical standard
for instruction structure has grown more sophisticated.

The name "FrankenTemplate" reflects its origin: an assembled-from-parts structure that
combines the best sections of each prior iteration into progressively more complete and
capable scaffolds. Like Frankenstein's creation, it is built from the strongest available
pieces rather than conceived whole.

---

## Files

### Primary Variants (Start Here)

| File | Notes | When to Use |
|------|-------|-------------|
| [`glee-fully_frankentemplate_ae.md`](glee-fully_frankentemplate_ae.md) | **Most complete** — full Toolbox + Tool + Tool-ette three-level scaffold with BLEED GLEE mode, visit-aware dialog, and all canonical blocks | Building any new entity from scratch |
| [`glee-fully_frankentemplate_ab.md`](glee-fully_frankentemplate_ab.md) | A/B hybrid — advanced two-branch structure | Branch-level Tool variants |
| [`glee_fully_franken_template_c_enhanced_hybrid.md`](glee_fully_franken_template_c_enhanced_hybrid.md) | Enhanced hybrid build on the C-line | Hybrid tone experiments |
| [`glee_fully_franken_template_c_enhanced_hybrid_branch_twig.md`](glee_fully_franken_template_c_enhanced_hybrid_branch_twig.md) | Branch-twig specific version of the enhanced C-hybrid | Branch + Tool-ette pairing |

### Iteration Series (Development History)

| File | Series | Notes |
|------|--------|-------|
| `glee-fully_frankentemplate_a.md` | A | Original base — placeholder-driven, minimal structure |
| `glee-fully_frankentemplate_c.md` | C | Alternate structural exploration |
| `glee-fully_frankentemplate_e.md` | E–J | Sequential refinement series |
| `glee-fully_frankentemplate_g.md` | | |
| `glee-fully_frankentemplate_h.md` | | |
| `glee-fully_frankentemplate_i.md` | | |
| `glee-fully_frankentemplate_j.md` | | |
| `glee-fully_frankentemplate_k.md` | K–O | Continued refinement series |
| `glee-fully_frankentemplate_m.md` | | |
| `glee-fully_frankentemplate_n.md` | | |
| `glee-fully_frankentemplate_o.md` | | |
| `glee-fully_frankentemplate_q.md` | Q–T | Structural experiments |
| `glee-fully_frankentemplate_r.md` | | |
| `glee-fully_frankentemplate_s.md` | | |
| `glee-fully_frankentemplate_t.md` | | |
| `glee-fully_frankentemplate_u.md` | U–Y | Late-stage refinements |
| `glee-fully_frankentemplate_v.md` | | |
| `glee-fully_frankentemplate_y.md` | | |

> Note: Letters B, D, F, L, P, W, X are skipped — some iterations were absorbed into
> adjacent variants or were discarded during development. The letter sequence documents
> the development history, not alphabetical completeness.

---

## What a FrankenTemplate Contains

A mature FrankenTemplate (e.g., `_ae`) defines the structure for all three entity tiers:

### Toolbox (Trunk) Block
- Identity declaration and ecosystem attribution
- BLEED GLEE mode toggle and tone assignment
- Visit-aware dialog flow (`gleeVisitFlow_v1`) — first timer, welcome back, feedback nudge
- Suite navigation links (all 7 Tools)
- Routing logic — how to direct users to the right branch

### Tool (Branch) Block
- Role declaration as router (GLEE-RICH tone)
- Tool-ette listing and description
- Intent-matching logic — how to read user need and route appropriately
- Cross-Tool awareness

### Tool-ette (Twig) Block
- Role declaration as specialist (GLEE-LITE tone)
- Primary function blocks (each Function/Leaf)
- Export logic
- Conversation starters (format: 12 starters across 3 categories)
- Canvas mode behavior
- BLEED GLEE / Calm toggle handling

---

## How to Use Templates

### For a New Tool-ette Build

1. Start with `glee-fully_frankentemplate_ae.md` (most complete)
2. Copy the Twig-level block
3. Fill in the bracketed placeholders (`[Tool-ette Name]`, `[Parent Tool]`, etc.)
4. Feed the completed scaffold as a payload into `prompts/glee-fully-builder-ready-promptchain-v2-0.md` at **PROMPT01**
5. The PromptChain will validate, expand, and canonize the scaffold into a full GPT

### For a New Tool or Toolbox

Use the corresponding branch-level or trunk-level block from `_ae` as the base.

### For Comparing Instruction Structure Evolution

Browse the lettered series chronologically (`_a` → `_ae`) to understand how the
canonical instruction standard has evolved. Each iteration preserves the prior
structure and adds or refines specific sections.

---

## Governance Rules (This Folder)

| Rule | Detail |
|------|--------|
| **Expansion-Only** | Never remove or simplify structure from an existing template |
| **New iterations = new files** | Create a new lettered file; do not overwrite prior variants |
| **Letter naming** | Continue the alphabetical lettered system; multi-letter names (ab, ae) indicate hybrid variants |
| **Placeholders** | Bracketed `[text]` marks operator fill-in zones; do not pre-fill with generic content |
| **Snapshots** | Finalized supertemplate versions (v1.0, v1.2, v1.5) live in `snapshots/` as locked reference |

---

## Relationship to Other Folders

```
templates/    <-- implements rules from  --> governance/ (canonical structure rules)
templates/    <-- feeds into             --> prompts/ (PromptChain PROMPT01 payload)
templates/    <-- must align with        --> canon/ (ledger schema for YAML blocks)
templates/    <-- tone defined by        --> vernacular/ (BLEED GLEE / GLEE-LITE rules)
templates/    <-- milestone versions in  --> snapshots/ (supertemplate v1.0, v1.2, v1.5)
```

---

## Version Lineage

```
glee-fully_frankentemplate_a.md        (original base)
        |
        v
glee-fully_frankentemplate_c.md        (structural exploration)
        |
        v
... e, g, h, i, j, k, m, n, o ...     (sequential refinements)
        |
        v
glee-fully_frankentemplate_ae.md       (current most complete — three-tier)
        |
        v
[snapshots] glee-fully-supertemplate-v1-0/v1-2/v1-5.md  (frozen milestone releases)
```
