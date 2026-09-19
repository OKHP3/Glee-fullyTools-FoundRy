# Manifest validator tests

The suite also includes offline technology-audit regression tests for numeric
version drift, prerelease/yanked-release filtering, unavailable metadata, and
controlled Mermaid updates. Run just those without third-party packages:

```bash
python3 -m unittest discover -s scripts/tests -p 'test_technology_versions.py' -v
```

These regression tests cover the current nested manifest schema and the legacy
manifest audit's `brand.domain` check. Each malformed manifest is created in a
temporary directory, so the tracked root `manifest.yaml` is never edited.

Run from the repository root:

```bash
python3 -m unittest discover -s scripts/tests -v
```

Install the declared validator dependencies first when setting up a new
environment:

```bash
python3 -m pip install -r requirements.txt
```
