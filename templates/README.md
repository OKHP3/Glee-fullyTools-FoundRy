# templates/ — FrankenTemplate GPT Instruction Variants

This folder contains iterative GPT instruction template variants used to develop
and refine the scaffold for Glee-fully Tool-ette instruction blocks.

## Naming Convention

Files are named `glee-fully_frankentemplate_[letter].md` where the letter indicates
the iteration. Letter-based suffixes are sequential development stages, not random.

| File | Notes |
|------|-------|
| `glee-fully_frankentemplate_a.md` | Original base template |
| `glee-fully_frankentemplate_ab.md` | A/B hybrid variant |
| `glee-fully_frankentemplate_ae.md` | Advanced/extended variant (most complete branch-twig hybrid) |
| `glee-fully_frankentemplate_c.md` | Alternate structure exploration |
| `glee_fully_franken_template_c_enhanced_hybrid.md` | Enhanced hybrid build |
| `glee_fully_franken_template_c_enhanced_hybrid_branch_twig.md` | Branch-twig specific enhanced hybrid |
| `glee-fully_frankentemplate_e.md` through `_j.md` | Sequential iteration refinements |
| `glee-fully_frankentemplate_k.md` through `_o.md` | Continued refinement series |
| `glee-fully_frankentemplate_q.md` through `_t.md` | Structural experiments |
| `glee-fully_frankentemplate_u.md` through `_y.md` | Late-stage refinements |

## Usage

When forging a new Tool-ette, start with the latest iteration (`_ae` or `_y`) as
the structural base. Feed it into the PromptChain (`prompts/glee-fully-builder-ready-promptchain-v2-0.md`)
at PROMPT01 as the payload scaffold.

## Governance

All templates are subject to Expansion-Only Discipline — never simplify or remove
structure from existing templates. New variants should be new lettered files.
