# templates/ — FrankenTemplate GPT Instruction Variants

This folder contains iterative GPT instruction template variants used to develop
and refine the scaffold for Glee-fully Tool-ette instruction blocks.

## Naming Convention

Files are named `glee-fully_frankentemplate_[letter].md` where the letter indicates
the iteration. Letter-based suffixes are sequential development stages, not random.

| File | Notes |
|------|-------|
| `_a.md` | Original base template |
| `_ab.md` | A/B hybrid variant |
| `_ae.md` | Advanced/extended variant (most complete branch-twig hybrid) |
| `_c.md` | Alternate structure exploration |
| `_c_enhanced_hybrid.md` | Enhanced hybrid build |
| `_c_enhanced_hybrid_branch_twig.md` | Branch-twig specific enhanced hybrid |
| `_e`, `_g`, `_h`, `_i`, `_j` | Sequential iteration refinements |
| `_k`, `_m`, `_n`, `_o` | Continued refinement series |
| `_q`, `_r`, `_s`, `_t` | Structural experiments |
| `_u`, `_v`, `_y` | Late-stage refinements |

## Usage

When forging a new Tool-ette, start with the latest iteration (`_ae` or `_y`) as
the structural base. Feed it into the PromptChain (`prompts/glee-fully-builder-ready-promptchain-v2.0.md`)
at PROMPT01 as the payload scaffold.

## Governance

All templates are subject to Expansion-Only Discipline — never simplify or remove
structure from existing templates. New variants should be new lettered files.
