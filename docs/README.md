# docs/ — Ecosystem Documentation

> Human-readable documentation for the Glee-fully Personalizable Tools™ ecosystem.
> These files explain the *why*, *what*, and *how* of the system — its philosophy,
> architecture, and design principles — in plain prose intended for both human readers
> and AI agents needing orientation context.

---

## Purpose

The `docs/` folder is the ecosystem's knowledge base. While `canon/` defines the rules
and `governance/` enforces them, `docs/` explains them. These documents serve three
audiences: builders forging new GPTs, AI agents navigating the system cold, and anyone
seeking to understand the ecosystem's architecture before working inside it.

This is also where source-format documents (Word, PDF) live alongside their Markdown
equivalents — making the docs portable across tools while keeping canonical versions
in Markdown for version control.

Imported research, drafts, pasted source material, and other non-canonical references
are kept under [`source-material/`](source-material/). Files there retain their source
filenames and provenance; canonical content belongs in the governed folders described
above.

---

## Files

| File | Format | Purpose |
|------|--------|---------|
| [`gleefully_technical_overview.md`](gleefully_technical_overview.md) | Markdown | Primary technical reference — architecture, PromptChain lifecycle, tone overlays, role discipline, and cross-ecosystem compatibility |
| [`gleefully_narrative_overview.md`](gleefully_narrative_overview.md) | Markdown | Brand philosophy and storytelling — the "why" behind Glee-fully, ecosystem metaphors, emotional design rationale |
| [`structure-and-ordering-for-custom-gpt-instruction-blocks.md`](structure-and-ordering-for-custom-gpt-instruction-blocks.md) | Markdown | Reference for how to structure and order GPT instruction blocks when building new entities |
| `gleefully-technical-overview.docx` | Word | Source document for the technical overview |
| `gleefully-technical-overview.pdf` | PDF | Portable export of the technical overview |
| `gleefully-narrative-overview.docx` | Word | Source document for the narrative overview |
| `gleefully-narrative-overview.pdf` | PDF | Portable export of the narrative overview |
| `content-synthesis-for-glee-fully.docx` | Word | Content synthesis document — multi-pass reconciliation of canonical sources |
| `content-synthesis-for-glee-fully.pdf` | PDF | Portable export of the content synthesis |
| `brand-origin-story.docx` | Word | Brand origin story and founding narrative |
| [`glee-fully-repository-crosswalk.md`](glee-fully-repository-crosswalk.md) | Markdown | Operational snapshot crosswalking the 51 in-scope child GitHub repositories to their adjacent local clones |

---

## Document Summaries

### Technical Overview (`gleefully_technical_overview.md`)

The technical reference document. Covers:

- **The Trunk-Branch-Twig-Leaf model** — how the Toolbox, Tools, Tool-ettes, Functions,
  and Function-ettes relate to each other architecturally
- **The Canon System** — how the 9 dataLedger files govern the ecosystem
- **The PromptChain lifecycle** — PROMPT00 through PROMPT05, what each step does, and
  what "PME-ready" means
- **Tone overlays** — Bleeds GLEE, ForgeDialect.A1, and Watchkeeper.Core
- **Role discipline** — Coach, Quarterback, Specialist, Core Skill, Kicker archetypes
- **A worked example** — forging a new Tool-ette step by step
- **A Mermaid architecture diagram** of the full ecosystem
- **Cross-ecosystem compatibility** with OverKill Hill P³ and The GPT Found-Ry

### Narrative Overview (`gleefully_narrative_overview.md`)

The brand story and philosophical foundation. Covers:

- Why Glee-fully exists — the problem of joyless productivity tools
- The muse (Glee, Pacific Northwest, chai, color-coding, cozy chaos)
- How the ecosystem is structured as a living tree metaphor
- What it feels like to use Glee-fully — tone attunement, emotional design
- The hidden canon — governance as architecture
- The "cathedral of code and personality" metaphor
- Growth-without-reduction philosophy
- The broader vision: joy as infrastructure

### Instruction Block Structure (`structure-and-ordering-for-custom-gpt-instruction-blocks.md`)

A technical reference for GPT builders. Defines the canonical ordering of sections
within a GPT's system instructions — ensuring consistency across all entities.

---

## Relationship to Other Folders

```
docs/       <-- synthesizes --> canon/ (explains what the ledgers contain)
docs/       <-- describes  --> governance/ (explains the rules in plain language)
docs/       <-- informs    --> prompts/ (megaprompt uses docs/ as synthesis source)
docs/       <-- supports   --> web-templates/ (content source for public-facing pages)
docs/       <-- referenced in --> inventory/ (elevator pitches draw on narrative docs)
docs/source-material/ <-- supplies evidence to --> docs/ and Phase 5 decision records
```

---

## Usage Notes

- When onboarding a new AI agent to this repo, point them to `gleefully_technical_overview.md` first.
- When a human needs to understand the ecosystem's purpose, start with `gleefully_narrative_overview.md`.
- The `.docx` and `.pdf` files are source/export formats — the `.md` files are the canonical versions for this repo.
- `source-material/` contains imported, non-canonical inputs and should not be treated as a source of authority without explicit adoption.
- The `content-synthesis-for-glee-fully.docx` and `brand-origin-story.docx` are working documents that may be used to generate or refresh website content via the megaprompt (`prompts/glee-fully_tools_megaprompt.md`).
