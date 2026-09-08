#!/usr/bin/env python3
"""Validate the repository's current manifest schema.

Usage:
    python3 scripts/validate-manifest.py path/to/manifest.yaml
    python3 scripts/validate-manifest.py  # validates ./manifest.yaml

Validates a manifest.yaml against schemas/manifest.schema.yaml.
PyYAML and jsonschema are declared in requirements.txt. If jsonschema is
unavailable, the current-manifest structural checks still provide a useful
fallback after PyYAML loads the document.
"""

import sys
import re
from pathlib import Path


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        print("ERROR: pyyaml is not installed. Run: pip install pyyaml")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_with_jsonschema(manifest: dict, schema: dict, manifest_path: str) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return []  # Fall through to structural checks

    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda e: list(e.path)):
        path = " → ".join(str(p) for p in error.path) if error.path else "(root)"
        errors.append(f"  [{path}] {error.message}")
    return errors


def structural_checks(manifest: dict, manifest_path: str) -> list[str]:
    """Lightweight checks for environments without jsonschema."""
    errors = []

    required_top = [
        "schema_version",
        "repo",
        "brand",
        "ecosystem",
        "authority_chain",
        "governance",
        "toolbox_structure",
        "tone_overlays",
        "required_child_files",
        "author",
        "organization",
        "contact",
        "application",
    ]
    for field in required_top:
        if field not in manifest:
            errors.append(f"  Missing required field: {field}")

    repo = manifest.get("repo", {})
    for field in ["name", "display_name", "type", "lifecycle_status", "visibility", "description"]:
        if field not in repo:
            errors.append(f"  repo.{field} is missing")

    brand = manifest.get("brand", {})
    for field in ["domain", "display_name", "public_site", "tagline", "tone_default", "muse"]:
        if field not in brand:
            errors.append(f"  brand.{field} is missing")

    authority_chain = manifest.get("authority_chain", {})
    child_families = authority_chain.get("child_families", [])
    if not child_families:
        errors.append("  authority_chain.child_families must have at least one entry")

    tones = manifest.get("tone_overlays", [])
    if not tones:
        errors.append("  tone_overlays must have at least one entry")

    required_child_files = manifest.get("required_child_files", [])
    if not required_child_files:
        errors.append("  required_child_files must have at least one entry")

    return errors


def main():
    # Determine manifest path
    if len(sys.argv) > 1:
        manifest_path = Path(sys.argv[1])
    else:
        manifest_path = Path("manifest.yaml")

    if not manifest_path.exists():
        print(f"ERROR: File not found: {manifest_path}")
        sys.exit(1)

    # Find schema relative to this script
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    schema_path = repo_root / "schemas" / "manifest.schema.yaml"

    print(f"Manifest : {manifest_path}")
    print(f"Schema   : {schema_path}")

    manifest = load_yaml(manifest_path)
    errors = []

    # Use the checked-in schema when the optional validator is installed.
    if schema_path.exists():
        schema = load_yaml(schema_path)
        errors = validate_with_jsonschema(manifest, schema, str(manifest_path))
        if errors:
            print("\nSchema validation errors:")
            for e in errors:
                print(e)
        else:
            # Always run structural checks too
            errors = structural_checks(manifest, str(manifest_path))
            if errors:
                print("\nStructural check errors:")
                for e in errors:
                    print(e)
    else:
        print(f"NOTE: Schema not found at {schema_path}, running structural checks only.")
        errors = structural_checks(manifest, str(manifest_path))
        if errors:
            print("\nStructural check errors:")
            for e in errors:
                print(e)

    if errors:
        print(f"\n❌ FAIL — {len(errors)} error(s) found in {manifest_path}")
        sys.exit(1)
    else:
        print(f"\n✅ PASS — {manifest_path} is valid")
        sys.exit(0)


if __name__ == "__main__":
    main()
