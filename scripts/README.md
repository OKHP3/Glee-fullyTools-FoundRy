# scripts/ — Governance Utility Scripts

> Python utility scripts for maintaining the health, hygiene, and governance compliance
> of this FoundRy repository. Dependency-light by design — all scripts run with
> stock Python 3, no virtual environment or third-party packages required.

---

## Purpose

`scripts/` provides the automated tooling layer for this workbench. These scripts
handle the tasks that would be tedious or error-prone to do manually: normalizing
filenames to canonical ASCII standard, auditing the manifest for required fields,
checking registry integrity, and generating sync posture reports for the
foundry-to-governance relay relationship.

They are maintenance tools, not build tools. They do not generate GPT content —
they verify and enforce the structural conventions that keep this repo trustworthy
as a canonical source.

---

## Files

| Script | Purpose | When to Run |
|--------|---------|-------------|
| [`normalize_filenames.py`](normalize_filenames.py) | Renames files to lowercase-kebab-case ASCII — strips emoji, non-breaking hyphens, version dots, camelCase, and other non-standard characters | After adding or renaming any files |
| [`manifest-audit.py`](manifest-audit.py) | Validates `manifest.yaml` for required governance fields (`schema_version`, `repo`, `lifecycle_status`, etc.) | After editing `manifest.yaml` |
| [`registry-audit.py`](registry-audit.py) | Checks `canon/dataledger-registry-v3.md` for required structural markers | After editing the registry ledger |
| [`foundry-sync.py`](foundry-sync.py) | Audits this repo against the OKHP3 Tier 0→1→2 governance model — checks for required baseline paths | Periodically, or after restructuring |
| [`check-registry.py`](check-registry.py) | Lightweight registry file presence check | Quick integrity check |
| [`sync-report.py`](sync-report.py) | Generates a sync posture report for the parent foundry relay relationship | Before governance sync or reporting |
| [`validate-manifest.py`](validate-manifest.py) | Extended manifest validation — checks field values, not just presence | Full manifest compliance check |
| [`audit-technology-versions.py`](audit-technology-versions.py) | Checks live Python and Mermaid release metadata against the static template | Monthly via GitHub Actions, or on demand |
| [`check-markdown-links.py`](check-markdown-links.py) | Validates relative links in the maintained repository and governed folder indexes | Before merging documentation, prompt, or governed-content changes |

---

## Script Details

### `normalize_filenames.py`

The most-used script in this repo. Enforces the canonical filename convention:
**lowercase-kebab-case ASCII only**.

```bash
# Dry run (shows what would change, does not rename)
python3 scripts/normalize_filenames.py .

# Apply renaming recursively, including directories
python3 scripts/normalize_filenames.py . --recursive --ascii-only --include-dirs --apply
```

**What it corrects:**

| Issue | Example | Result |
|-------|---------|--------|
| Emoji in filename | `🦋-vernacular.md` | `vernacular.md` |
| Non-breaking hyphen | `glee‑fully.md` | `glee-fully.md` |
| camelCase dataLedger prefix | `dataLedger_registry_v3.md` | `dataledger-registry-v3.md` |
| Version dots | `template-v1.5.md` | `template-v1-5.md` |
| Apostrophes | `operator's-layout.md` | `operators-layout.md` |
| Uppercase non-standard names | Any file not in PRESERVE_NAMES list | lowercased |

**Preserved names** (never renamed): `README.md`, `AGENTS.md`, `CHANGELOG.md`,
`LICENSE.md`, `CODEOWNERS`, `FUNDING.yml`, `.gitignore`, `manifest.yaml`.

---

### `manifest-audit.py`

Validates `manifest.yaml` for the current repository manifest schema and a
recognized `lifecycle_status` value. Install the declared validator dependencies
once from the repository root before running the full check:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate-manifest.py
python3 scripts/manifest-audit.py .
# Output: OK or FAIL with missing fields listed
```

**Required fields:** `schema_version`, `repo`, `name`, `display_name`, `type`,
`lifecycle_status`, `visibility`, `brand.domain`, `author`

**Valid lifecycle statuses:** `spark`, `research`, `concept`, `prototype`,
`capability`, `productizing`, `product`, `active`, `archived`, `deprecated`

---

### `foundry-sync.py`

Checks this relay repository against the OKHP3 Tier 0→1→2 governance baseline.
Verifies that required structural paths exist and flags any missing elements.

```bash
python3 scripts/foundry-sync.py
python3 scripts/foundry-sync.py --strict  # also checks recommended paths
```

---

### `registry-audit.py`

Validates that `canon/dataledger-registry-v3.md` contains the required structural
markers for a well-formed registry file.

```bash
python3 scripts/registry-audit.py .
```

---

### `check-markdown-links.py`

Checks the maintained Markdown indexes for broken relative links without making
network requests. By default it checks `README.md`, `docs/README.md`,
the maintained nested hubs `docs/application/README.md`,
`docs/adr/README.md`, and `scripts/tests/README.md`, `prompts/README.md`, and
the active governed indexes:
`canon/README.md`, `evaluation/README.md`, `governance/README.md`,
`inventory/README.md`, `templates/README.md`, `vernacular/README.md`, and
`web-templates/README.md`.

Nested scope is deliberate: the application and ADR READMEs are maintained
indexes, while `docs/application/pilots/*/README.md` are package handoff notes,
`docs/delegation/2026-09-07-coop-pertition/README.md` is dated delegation
lineage, and `snapshots/README.md` contains read-only historical records. Those
documents are intentionally excluded from this affordable default scan. The
generated `.agents/skills/README.md` catalog is maintained by its own catalog
tooling. The `docs/**` and `scripts/tests/**` workflow filters include every
maintained nested index listed above.

External URLs, anchor-only links, and explicit placeholder tokens
(`{{...}}`, `${...}`, `placeholder`, `TODO`, `TBD`, `your-file`, `your-path`,
`your-url`, `your-link`, or `...`) are reported as skipped categories rather
than treated as repository paths.

```bash
python3 scripts/check-markdown-links.py .
```

Pass one or more `--document PATH` options to check a different set of
Markdown files relative to the repository root.

---

## Running a Full Compliance Check

To verify the repo is in clean compliance across all dimensions:

```bash
# 1. Filename normalization (dry run)
python3 scripts/normalize_filenames.py . --recursive --ascii-only --include-dirs

# 2. Manifest validation
python3 -m pip install -r requirements.txt
python3 scripts/validate-manifest.py
python3 scripts/manifest-audit.py .

# 3. Registry integrity
python3 scripts/registry-audit.py .

# 4. Foundry sync posture
python3 scripts/foundry-sync.py

# 5. Sync report
python3 scripts/sync-report.py

# 6. Maintained Markdown links
python3 scripts/check-markdown-links.py .
```

---

## Governance Rules (This Folder)

| Rule | Detail |
|------|--------|
| **Python 3 only** | No third-party packages — stock stdlib only |
| **No site-rendering scripts** | Do not place web build or deployment scripts here |
| **Dry-run by default** | Normalize script requires `--apply` flag to make changes |
| **Non-destructive** | Scripts report and audit; they do not delete or overwrite canonical content |

---

## Relationship to Other Folders

```
scripts/    <-- enforces conventions on  --> all folders (filename normalization)
scripts/    <-- validates structure of   --> manifest.yaml (manifest-audit)
scripts/    <-- audits integrity of      --> canon/dataledger-registry-v3.md (registry-audit)
scripts/    <-- checks compliance with   --> governance/ (foundry-sync checks baseline paths)
```
