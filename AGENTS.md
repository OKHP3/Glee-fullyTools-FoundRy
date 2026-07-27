# AGENTS.md - Glee-fullyTools-FoundRy

Read this file before working in this repository. It is the canonical agent guide
for the repository root. `CLAUDE.md` is a short pointer to this file. No nested
Git repositories or nested agent guides were found during the July 13, 2026 review.

## Project identity

Confirmed by `manifest.yaml`, `README.md`, and the directory layout:

- This is the private `foundry-relay` workbench for the Glee-fully Personalizable
  Tools ecosystem.
- It is a Git repository with lifecycle status `active` and private visibility.
- It is a documentation, governance, prompt, template, evaluation, and ledger
  repository. It is not an application, service, package, or deployable website.
- The repository contains no package manifest, build system, test suite, or runtime
  service configuration.
- The public storefront and child repositories are external consumers of material
  produced here. `web-templates/` contains source assets only and must not be served
  from this workbench.

Inferred from the repository contents:

- Primary users are the owner, GPT builders, and AI agents maintaining a governed
  family of Custom GPT specifications and related public-page source material.
- The workbench's practical mission is to preserve canonical rules and provide the
  source material used to design, evaluate, and relay Glee-fully GPT entities.

Unknown from this checkout:

- The current operational status of the externally hosted GPTs, child repositories,
  public site, and live ChatGPT links. Local documentation reports 40+ entities, but
  that external deployment count is not independently verified here.

## Authority and scope

The authority chain is:

```text
OKHP3/OverKill-Hill-FoundRy
  -> Glee-fullyTools-FoundRy (this repository)
       -> glee-fully-gpt00-* through glee-fully-gpt07-* child repositories
```

Follow parent governance when it is available. Within this repository:

1. `canon/dataledger_*_v3.md` is the data authority.
2. `governance/` defines the rules applied to the canon and build workflow.
3. `prompts/`, `templates/`, `evaluation/`, `vernacular/`, `inventory/`, and
   `docs/` provide governed working material and explanations.
4. GPT-local or ad hoc instructions do not override canon.

This repository is a workbench and relay. Do not add web servers, deployment
workflows, hosted-service configuration, or application infrastructure here.

## Repository map

- `canon/`: nine canonical ledgers. The registry, persona, parameters, system,
  hydration, narrative, ideation, archive, and legacy processing ledgers live here.
  Preserve existing content and `::CanonSeal[...]::` tags. Canonical changes are
  growth-only unless higher authority explicitly directs otherwise.
- `governance/`: the v3.0.1 project directive, project instructions, Strategy Center
  instructions, and the approximately 20,000-line Operator's Cathedral Layout.
- `prompts/`: Builder-Ready PromptChain v2.0, GPT scaffolds, and the multi-tool
  content synthesis prompt.
- `templates/`: lettered FrankenTemplate variants, including the latest `ae` and `y`
  variants, plus hybrid templates.
- `evaluation/`: GPT PulseBook evaluation versions. Use `gpt-pulsebook-evaluation-v1-7.md`
  as the current local rubric; v1.4 and v1.6 are historical references.
- `vernacular/`: complete and lite voice and tone references.
- `inventory/`: human-readable entity catalog that complements the canonical registry.
- `docs/`: narrative, technical, and instruction-structure documentation, including
  source-format `.docx` and `.pdf` files, plus `technology-inventory.md`, the
  source list consumed by `scripts/audit-technology-versions.py`.
- `snapshots/`: dated historical captures. The latest local snapshot is
  `snapshots/2025-09-14/`. Treat snapshots as read-only lineage evidence.
- `web-templates/`: HTML/CSS/JavaScript template assets for child repositories.
  Current files include `index.html`, `theme.css`, `assets/css/theme.css`,
  `assets/js/app.js`, and the page-content update log. Referenced image assets are
  not present in this checkout.
- `scripts/`: small Python 3 maintenance and audit utilities. They are not build or
  deployment tools.
- `attached_assets/`: imported research, drafts, and reference files. Treat these as
  non-canonical source material unless a canonical file explicitly adopts their content.
- `.agents/`: repository-local skill catalog and agent memory/reference material.
  It is not the source of truth for canon. `.agents/memory/` holds agent-maintained
  reference notes (foundry structure, repo-standardizer state, phase notes).
  `.agents/skills/` holds 20+ installed and in-development agent skill packages,
  including several `okhp3-thread-context-extraction-*` platform variants and a
  `thread-extract-ws` evaluation workspace with iteration benchmarks. Treat skill
  benchmark and eval output under `.agents/skills/*/iteration-*` and
  `.agents/skills/*/benchmarks/` as working data, not canon.
- `manifest.yaml`, `README.md`, `CHANGELOG.md`, `LICENSE.md`, and `replit.md`: root
  metadata, human orientation, history, license, and workbench context.

## Core architecture and workflows

The documented entity model is Toolbox, Tool, Tool-ette, Function, and
Function-ette. Child repository families are named as follows:

| Pattern | Domain |
|---|---|
| `glee-fully-gpt00-*` | Toolbox trunk |
| `glee-fully-gpt01-*` | Discovered Careers |
| `glee-fully-gpt02-*` | Treasured Finds |
| `glee-fully-gpt03-*` | Tasty Tracker |
| `glee-fully-gpt04-*` | Traveler's Guide |
| `glee-fully-gpt05-*` | Organized Life |
| `glee-fully-gpt06-*` | Healthy Bee-ing |
| `glee-fully-gpt07-*` | Identity Known |

The documented clause lifecycle is:

```text
ideation -> registry / persona / parameters -> narrative -> archive
                         ^
                         |
                 hydration re-entry
```

`processing` is legacy and deprioritized. Runtime continuity belongs in
`dataledger_hydration_v3.md`, not in prompt-local memory. Canonical outputs must
carry a `!CLAUSE` identifier declared in `canon/dataledger_registry_v3.md`.

The Builder-Ready PromptChain in `prompts/` describes the PROMPT00 through PROMPT05
creation flow. The PulseBook rubric in `evaluation/` is the local evaluation
reference before an entity is treated as PME-ready in the documented workflow.

## Non-negotiable conventions

- Expansion-only discipline: do not delete, simplify, or collapse existing canonical
  content. Add detail or retire logic through the documented archive path.
- Canon authority: when canon, governance, README material, and GPT-local content
  conflict, canon wins.
- CanonSeal integrity: never alter or remove a `::CanonSeal[...]::` tag.
- Tone default: use `GleeTone.A1` for an untagged thread. Log a genuine tone drift
  through the persona ledger using the repository's `!DRIFT_EVENT` convention.
- Suffix law: `-R` and `-Ry` are reserved to OverKill Hill P3 and The GPT Found-Ry.
  Glee-fully GPTs are exempt. Do not introduce those suffixes into Glee-fully names.
- No prompt-local memory: use the hydration ledger for continuity and handoff state.
- Brand rules: do not use em dashes in generated content, preserve standalone punchy
  lines, and keep verbosity proportional to understanding produced.
- Do not put secrets, credentials, personal data, or machine-specific paths into
  guidance, canon, prompts, or generated artifacts.

## Safe change procedure

Before changing anything:

1. Read this file, `README.md`, `manifest.yaml`, and the relevant folder README.
2. Check `git status --short` and preserve existing user changes.
3. For canon or governance work, read the applicable directive and ledger before
   editing. Search for existing IDs and seals before adding content.
4. Keep changes limited to the requested scope. Do not edit dependencies, generated
   artifacts, CI behavior, or unrelated documentation as a side effect.
5. Use non-destructive version-control operations. Never use `git reset --hard`,
   `git checkout --`, or broad deletion commands unless the owner explicitly asks.
6. Re-read every changed guidance file and verify every newly referenced path or
   command before handing the work back.

## Verified maintenance commands

Run commands from the repository root. These are the useful checks currently
available, with their present limitations:

```bash
git status --short --branch
git diff --check
python3 scripts/normalize_filenames.py . --recursive --ascii-only --include-dirs
python3 scripts/manifest-audit.py .
python3 scripts/registry-audit.py .
python3 scripts/foundry-sync.py
python3 scripts/sync-report.py
python3 scripts/audit-technology-versions.py
```

`audit-technology-versions.py` checks `docs/technology-inventory.md` entries
against current upstream versions. It also runs on a monthly schedule via
`.github/workflows/technology-version-audit.yml` (with `.github/dependabot.yml`
alongside it for dependency PRs). Neither workflow has produced a verified run
in this checkout; treat their output as unconfirmed until a run is observed.

The filename normalizer is dry-run by default. Do not pass `--apply` without an
explicit request because the current dry run proposes 12 renames, including a
case-normalization proposal for `CLAUDE.md` and changes under `attached_assets/`.

The other audits are useful evidence, but they are not currently clean for this
repository:

- `manifest-audit.py` expects a top-level `brand_domain:` field, while the current
  manifest stores it as `brand.domain`.
- `registry-audit.py` checks for `registry/index.yaml`, which is absent. The actual
  canonical registry is `canon/dataledger_registry_v3.md`.
- `foundry-sync.py` checks for `_template/`, `registry/`, `schemas/`, and `.github/`
  paths that are absent from this workbench. Its strict baseline appears to target a
  different FoundRy layout.
- `sync-report.py` runs and reports the same absent inherited-baseline paths; it is
  a report, not proof of repository compliance.

No build, test, package-install, local-server, or deployment command is defined or
verified for this workbench. Do not invent one. The repository's meaningful checks
are documentation review, canon-preservation review, and the read-only maintenance
audits above.

## Known gaps and stale claims

- Several README files describe the repository as containing live or deployed GPTs.
  Treat that as project documentation, not local proof of current external status.
- `README.md` and `web-templates/README.md` describe image assets and some template
  layout details that are not present in the current checkout. Do not create missing
  assets merely to satisfy documentation claims.
- The audit scripts contain assumptions from another FoundRy baseline and should not
  be silently treated as repository health gates. Updating those scripts is separate
  work and requires an explicit request.
- `CHANGELOG.md` lists planned population of several seeded ledgers and a child-repo
  registry. Confirm owner intent before treating those as current requirements.
- The canonical registry and other ledgers use Markdown/YAML hybrid content. Preserve
  their existing syntax and lineage while following the growth-only rule.

- This section and the repository map were last synced to commit `7114b31`
  (2026-07-22). Commits since the July 13 review added the CI technology-audit
  workflow, `docs/technology-inventory.md`, `scripts/audit-technology-versions.py`,
  and a reorganized `.agents/skills/` catalog (renamed `okhp3-thread-context-
  extraction-workspace` to `thread-extract-ws`, among other renames). Re-check
  this list against `git log` before relying on it if substantial time has
  passed since that commit.

## Keeping this guide current

Update this file when the repository's actual structure, authority chain, validation
commands, or non-goals change. Base updates on files or executable checks. Label
inferences and unknowns instead of presenting them as facts. Keep `CLAUDE.md` as a
short pointer unless Claude-specific instructions genuinely need to be added.

## Output signature reference

When producing output from canonical logic, use the repository's declared clause
format and an ID that already exists in the registry:

```yaml
!CLAUSE: !PME_READY
ID: [EntityType].[Name].[MajorVersion].[MinorVersion].[Patch]
Summary: [One line]
TargetPhase: [Gleam / Ideation / Archive]
DeclaredBy: Glee-fully FoundRy
```

> The capability is durable. The platform wrapper is temporary.
