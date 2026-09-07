# Filename Migration Ledger

**Status:** Plan only — no files have been moved or renamed.  
**Inventory date:** 2026-09-07  
**Scope:** `canon/`, `docs/`, `governance/`, `inventory/`, `prompts/`, and
`docs/source-material/`

## Purpose and guardrails

This ledger records legacy filename findings, candidate ASCII kebab-case targets,
and the dependencies that must be handled before any rename. It is not approval
to execute a rename.

The current tree contains **45 flagged paths**:

- **39** contain underscores.
- **10** contain uppercase characters; the six `README.md` paths are required
  ecosystem exceptions.
- **3** contain non-ASCII characters.
- **8** exceed the local 100-character planning threshold for a repository
  relative path.
- **10** contain a segment longer than the 64-character portability limit.
- No flagged directory names were found.

The policy's diagnostics are findings, not permission to rename. Existing names
must be classified before a target is approved. In particular:

1. `README.md` is a required ecosystem name and is retained.
2. The nine `canon/` ledger filenames are authority anchors. Their candidate
   targets are recorded, but they stay on hold until the owner approves a
   coordinated authority cutover.
3. `docs/source-material/` retains source filenames by default because the
   filename is part of provenance. Its targets below are optional, abbreviated
   candidates only.
4. Prompt scaffolds and the inventory catalog are intentional templates/catalog
   names, not disposable detritus. They require explicit batch approval.
5. No public web workflow or deployment is configured in this workbench. GitHub
   blob/raw URLs, bookmarks, and downstream clones remain possible external
   dependencies and cannot be inferred from the repository scan.

## Proposed mapping ledger

`candidate target` is the old-to-new mapping to review. A row marked `retain`
has no rename planned; the candidate target is shown only when a future,
owner-approved migration may still be useful.

| ID | Legacy path | Signals | Classification | Candidate target | Disposition |
|---|---|---|---|---|---|
| C-01 | `canon/README.md` | uppercase | required name | `canon/README.md` | **Retain** — ecosystem exception |
| C-02 | `canon/dataledger_archive_v3.md` | underscore | authority anchor | `canon/dataledger-archive-v3.md` | **Hold** — coordinated canon cutover |
| C-03 | `canon/dataledger_hydration_v3.md` | underscore | authority anchor | `canon/dataledger-hydration-v3.md` | **Hold** — coordinated canon cutover |
| C-04 | `canon/dataledger_ideation_v3.md` | underscore | authority anchor | `canon/dataledger-ideation-v3.md` | **Hold** — coordinated canon cutover |
| C-05 | `canon/dataledger_narrative_v3.md` | underscore | authority anchor | `canon/dataledger-narrative-v3.md` | **Hold** — coordinated canon cutover |
| C-06 | `canon/dataledger_parameters_v3.md` | underscore | authority anchor | `canon/dataledger-parameters-v3.md` | **Hold** — coordinated canon cutover |
| C-07 | `canon/dataledger_persona_v3.md` | underscore | authority anchor | `canon/dataledger-persona-v3.md` | **Hold** — coordinated canon cutover |
| C-08 | `canon/dataledger_processing_v3.md` | underscore | authority anchor / legacy ledger | `canon/dataledger-processing-v3.md` | **Hold** — coordinated canon cutover |
| C-09 | `canon/dataledger_registry_v3.md` | underscore | authority anchor / registry | `canon/dataledger-registry-v3.md` | **Hold** — highest-impact canon cutover |
| C-10 | `canon/dataledger_system_v3.md` | underscore | authority anchor | `canon/dataledger-system-v3.md` | **Hold** — coordinated canon cutover |
| D-01 | `docs/README.md` | uppercase | required name | `docs/README.md` | **Retain** — ecosystem exception |
| D-02 | `docs/adr/README.md` | uppercase | required name | `docs/adr/README.md` | **Retain** — ecosystem exception |
| D-03 | `docs/gleefully_narrative_overview.md` | underscore | ordinary canonical documentation | `docs/gleefully-narrative-overview.md` | **Candidate** — docs batch |
| D-04 | `docs/gleefully_technical_overview.md` | underscore | ordinary canonical documentation | `docs/gleefully-technical-overview.md` | **Candidate** — docs batch |
| S-01 | `docs/source-material/Pasted-I-agree-with-your-assessment-Yes-the-Gleefully-Tools-fo_1782330748956.txt` | uppercase, underscore, long path, long segment | historical/source material | `docs/source-material/pasted-agreement-gleefully-tools-1782330748956.txt` | **Retain by default** — provenance rename requires approval |
| S-02 | `docs/source-material/Pasted-I-currently-have-ChatGPT-projects-for-every-one-of-the-_1782331669792.txt` | uppercase, underscore, long path, long segment | historical/source material | `docs/source-material/pasted-chatgpt-projects-1782331669792.txt` | **Retain by default** — provenance rename requires approval |
| S-03 | `docs/source-material/Pasted-So-before-we-convert-from-think-and-plan-and-consider-a_1782340307856.txt` | uppercase, underscore, long path, long segment | historical/source material | `docs/source-material/pasted-conversion-timeline-1782340307856.txt` | **Retain by default** — provenance rename requires approval |
| S-04 | `docs/source-material/Pasted-a-consideration-that-should-go-into-the-timeline-and-th_1782339541411.txt` | uppercase, underscore, long path, long segment | historical/source material | `docs/source-material/pasted-timeline-consideration-1782339541411.txt` | **Retain by default** — provenance rename requires approval |
| S-05 | `docs/source-material/custom-gpt-construction-standard-and-comparison-with-agent-skil_1782332849643.md` | underscore, long path, long segment | historical/source material | `docs/source-material/custom-gpt-construction-standard-agent-skills-1782332849643.md` | **Retain by default** — provenance rename requires approval |
| S-06 | `docs/source-material/custom-gpt-definitive-reference-guide_1782332849643.md` | underscore | historical/source material | `docs/source-material/custom-gpt-definitive-reference-guide-1782332849643.md` | **Retain by default** — provenance rename requires approval |
| S-07 | `docs/source-material/custom-gpt-explanation_1782332953494.docx` | underscore | historical/source material | `docs/source-material/custom-gpt-explanation-1782332953494.docx` | **Retain by default** — provenance rename requires approval |
| S-08 | `docs/source-material/custom-gpt-operationalization-capabilities,-privacy,-and-publ_1782332953495.docx` | underscore, long path, long segment | historical/source material | `docs/source-material/custom-gpt-operationalization-1782332953495.docx` | **Retain by default** — provenance rename requires approval |
| S-09 | `docs/source-material/custom-gpts-vs-agent-skills-a-mid‑2026-comparison_1782332849642.md` | underscore, non-ASCII, long segment | historical/source material | `docs/source-material/custom-gpts-vs-agent-skills-mid-2026-comparison-1782332849642.md` | **Retain by default** — Unicode normalization requires approval |
| S-10 | `docs/source-material/custom_gpts_whitepaper_overkillhill_v1.0_1782332953493.docx` | underscore | historical/source material | `docs/source-material/custom-gpts-whitepaper-overkill-hill-v1-0-1782332953493.docx` | **Retain by default** — paired source/export names |
| S-11 | `docs/source-material/custom_gpts_whitepaper_overkillhill_v1.0_1782332953493.md` | underscore | historical/source material | `docs/source-material/custom-gpts-whitepaper-overkill-hill-v1-0-1782332953493.md` | **Retain by default** — paired source/export names |
| S-12 | `docs/source-material/designing-grade-a-custom-gpts-the-overkill-hill-p3tm-method_1782332953494.docx` | underscore, long segment | historical/source material | `docs/source-material/designing-grade-a-custom-gpts-p3tm-1782332953494.docx` | **Retain by default** — provenance rename requires approval |
| S-13 | `docs/source-material/from-novelty-to-necessity-mastering-custom-gpts-in-2025-evolu_1782332953495.docx` | underscore, long path, long segment | historical/source material | `docs/source-material/from-novelty-to-necessity-custom-gpts-2025-1782332953495.docx` | **Retain by default** — provenance rename requires approval |
| S-14 | `docs/source-material/glee-fullytools-repositories_1782330271546.txt` | underscore | historical/source material | `docs/source-material/glee-fullytools-repositories-1782330271546.txt` | **Retain by default** — provenance rename requires approval |
| S-15 | `docs/source-material/glee‑fully-vernacular-complete_1782332849642.md` | underscore, non-ASCII | historical/source material | `docs/source-material/glee-fully-vernacular-complete-1782332849642.md` | **Retain by default** — Unicode normalization requires approval |
| S-16 | `docs/source-material/inventory_of_toolbox_tools_and_tool-ettes_1782330271545.md` | underscore | historical/source material | `docs/source-material/inventory-of-toolbox-tools-and-tool-ettes-1782330271545.md` | **Retain by default** — provenance rename requires approval |
| S-17 | `docs/source-material/llm-structured-outputs-and-validation-best-practices-q1-2026-_1782332953495.docx` | underscore, long path, long segment | historical/source material | `docs/source-material/llm-structured-outputs-validation-q1-2026-1782332953495.docx` | **Retain by default** — provenance rename requires approval |
| S-18 | `docs/source-material/master-craft-guidebook-custom-gpts-late-2025_1782332953494.md` | underscore | historical/source material | `docs/source-material/master-craft-guidebook-custom-gpts-late-2025-1782332953494.md` | **Retain by default** — provenance rename requires approval |
| S-19 | `docs/source-material/okh_knowledgefile_playbook_v1.0.0_2026-01-11_1782332953493.md` | underscore | historical/source material | `docs/source-material/okh-knowledgefile-playbook-v1-0-0-2026-01-11-1782332953493.md` | **Retain by default** — preserve version/date tokens |
| S-20 | `docs/source-material/operator’s-cathedral-layout_1782332849643.md` | underscore, non-ASCII | historical/source material | `docs/source-material/operators-cathedral-layout-1782332849643.md` | **Retain by default** — Unicode normalization requires approval |
| S-21 | `docs/source-material/what-is-a-custom-gpt_1782332953494.docx` | underscore | historical/source material | `docs/source-material/what-is-a-custom-gpt-1782332953494.docx` | **Retain by default** — provenance rename requires approval |
| G-01 | `governance/00-glee-fully-strategy-center_instructions.md` | underscore | authority anchor / system instructions | `governance/00-glee-fully-strategy-center-instructions.md` | **Hold** — update governance references as one batch |
| G-02 | `governance/README.md` | uppercase | required name | `governance/README.md` | **Retain** — ecosystem exception |
| G-03 | `governance/glee-fully_project_governance_v3-0-1.md` | underscore | authority anchor / CanonSeal directive | `governance/glee-fully-project-governance-v3-0-1.md` | **Hold** — authority and CanonSeal dependency |
| G-04 | `governance/glee-fully_project_instructions.md` | underscore | authority anchor / project instructions | `governance/glee-fully-project-instructions.md` | **Hold** — update governance references as one batch |
| I-01 | `inventory/README.md` | uppercase | required name | `inventory/README.md` | **Retain** — ecosystem exception |
| I-02 | `inventory/inventory_of_toolbox_tools_and_tool-ettes.md` | underscore | ordinary content / catalog source | `inventory/inventory-of-toolbox-tools-and-tool-ettes.md` | **Candidate** — catalog/tooling batch |
| P-01 | `prompts/README.md` | uppercase | required name | `prompts/README.md` | **Retain** — ecosystem exception |
| P-02 | `prompts/custom_gpt_hybrid_scaffold.md` | underscore | intentional template | `prompts/custom-gpt-hybrid-scaffold.md` | **Candidate** — template batch |
| P-03 | `prompts/custom_gpt_scaffold.md` | underscore | intentional template | `prompts/custom-gpt-scaffold.md` | **Candidate** — template batch |
| P-04 | `prompts/glee-fully_tools_megaprompt.md` | underscore | intentional template / synthesis prompt | `prompts/glee-fully-tools-megaprompt.md` | **Candidate** — template batch |

## Reference and impact audit

This audit was performed against tracked text files and exact legacy
basenames. It found no tracked relative links to the 21 source-material
filenames. That does **not** prove there are no external bookmarks or
downstream references.

### Canon batch C-02 through C-10 — highest risk

The nine candidate canon paths are referenced across the following tracked
surfaces; the exact subset varies by ledger:

- `README.md`, `CHANGELOG.md`, and `AGENTS.md`
- `canon/README.md`
- `docs/gleefully_technical_overview.md`
- `evaluation/README.md`
- `governance/README.md`
- `governance/00-glee-fully-strategy-center_instructions.md`
- `governance/glee-fully_project_governance_v3-0-1.md`
- `governance/glee-fully_project_instructions.md`
- `governance/operators-cathedral-layout.md`
- `prompts/custom_gpt_hybrid_scaffold.md`
- `prompts/custom_gpt_scaffold.md`
- `prompts/glee-fully-builder-ready-promptchain-v2-0.md`
- `snapshots/README.md`, `vernacular/README.md`, and `web-templates/README.md`
- `inventory/README.md`, `prompts/README.md`, and `scripts/README.md` for
  registry-specific references
- `.agents/skills/glee-fully-repo-standardizer/assets/glee-fully-brand.json`
  and `.agents/skills/glee-fully-repo-standardizer/scripts/scaffold.py` for
  registry/hydration-related source references

The nine canonical files contain `::CanonSeal[...]::` tags. A filename move
must not alter file contents or those tags. Historical copies under
`snapshots/` are not proposed for renaming as part of this plan.

### Documentation batch D-03 through D-04

The two candidate docs filenames appear in:

- `README.md`
- `docs/README.md`

They are also source-format siblings of
`gleefully-narrative-overview.docx/.pdf` and
`gleefully-technical-overview.docx/.pdf`; those sibling names are already safe
and are not part of this ledger. `prompts/README.md` and
`web-templates/README.md` reference the safe source-format siblings, not the
flagged Markdown paths.

### Governance batch G-01, G-03, G-04

Tracked references are:

- G-01: `README.md` and `governance/README.md`.
- G-03: `.agents/skills/glee-fully-repo-standardizer/SKILL.md`,
  `README.md`, `canon/README.md`, and `governance/README.md`.
- G-04: `README.md` and `governance/README.md`.

These are operating and authority documents. If approved, update every
reference in the same commit and preserve any CanonSeal content byte-for-byte
apart from intentional link/path text changes.

### Catalog batch I-02

The catalog filename appears in:

- `.agents/memory/glee-fully-repo-standardizer.md`
- `.agents/skills/glee-fully-repo-standardizer/scripts/scaffold.py`
- `README.md`
- `docs/agent-skill-conversion-strategy.md`
- `inventory/README.md`
- `prompts/README.md`
- `web-templates/README.md`

The scaffold script is a real importer/reference and must be updated and
tested with the catalog rename. Its help text, embedded source note, and
default path all need review.

### Prompt/template batch P-02 through P-04

- P-02 and P-03 appear in `README.md` and `prompts/README.md`.
- P-04 appears in `README.md`, `docs/README.md`, and `prompts/README.md`.

`manifest.yaml` points to the non-flagged
`prompts/glee-fully-builder-ready-promptchain-v2-0.md`, not to P-02 through
P-04. Re-run manifest validation after any prompt batch regardless.

### Source-material batch S-01 through S-21

No tracked Markdown, script, manifest, or relative-link importer was found for
these exact basenames. Their risk is provenance and external reference
stability rather than an in-repository import graph. The existing
`docs/README.md` explicitly says source-material files retain their source
filenames. Default action is therefore retention; any rename requires a
separate approval that accepts the provenance trade-off and records the
timestamp-preserving mapping above.

### Manifest, script, and public URL checks

- `manifest.yaml` has no direct reference to a flagged filename. Its
  `canon_ledger_path: canon/` directory reference remains valid, and its
  prompt-chain path is not flagged.
- The repository's `scripts/` directory has no executable reference to a
  flagged basename in the current scan. `scripts/README.md` does document
  the registry path and must be updated if the canon registry moves.
- `.agents/skills/glee-fully-repo-standardizer/scripts/scaffold.py` is an
  impacted script for the registry/hydration and inventory mappings.
- There is no configured web workflow or deployment target. No application
  route is known to serve these paths. GitHub blob/raw URLs, external
  bookmarks, downstream clones, and future public-site tooling are external
  impacts and require owner confirmation before a rename.

## Approval-gated batches

No batch is approved by this ledger. Approval must identify the batch and
accept each row's candidate target.

| Batch | Rows | Recommended order | Required approval and checks |
|---|---|---|---|
| B0: required names and source retention | C-01, D-01, D-02, G-02, I-01, P-01, S-01–S-21 | First, as a no-op decision | Confirm these paths remain stable; do not rename source material by default |
| B1: ordinary docs | D-03–D-04 | Low-risk first candidate | Update root/docs README references; check sibling source/export links and external GitHub URLs |
| B2: intentional prompt templates | P-02–P-04 | After B1 | Update root/docs/prompts README references; run prompt/manifest validation |
| B3: catalog and tooling | I-02 | After B2 | Update all seven catalog references and `scaffold.py`; exercise the scaffold help/default path |
| B4: governance anchors | G-01, G-03–G-04 | Only after explicit authority approval | Update all listed governance references; preserve CanonSeal content; run governance/manifest checks |
| B5: canonical ledgers | C-02–C-10 | Last and only as a coordinated cutover | Update the complete canon reference set, keep snapshots unchanged, run registry and link checks, and confirm no external URL dependency |

## Execution protocol after approval

For each approved batch:

1. Re-run the inventory and case-folded/NFC collision check against the current
   tree. Abort if a target now exists or collides after normalization.
2. Capture the pre-migration reference list and hashes for authority/source
   files. Do not edit source-material contents.
3. Use `git mv`. For any future case-only rename, use a two-step temporary
   path on case-insensitive filesystems.
4. Update all tracked relative Markdown links, prose path references, scripts,
   and manifests in the same commit. Do not update historical snapshot text
   merely because it describes an earlier tree.
5. Run the relevant link/reference checks, `scripts/registry-audit.py` for a
   registry change, and manifest validation for any batch that touches a
   referenced path.
6. Re-run portability diagnostics on the final tree and verify that every old
   path is either intentionally retained, deliberately replaced, or documented
   as an external compatibility risk.
7. Record the approval, execution date, validation result, and any compatibility
   anchor in this ledger before beginning the next batch.

## Current decision

**Explicit approval is still required.** This task creates the inventory,
mapping, dependency audit, and batch plan only. No rename, compatibility stub,
redirect, or content rewrite should be performed from this ledger alone.