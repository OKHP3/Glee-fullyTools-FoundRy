#!/usr/bin/env python3
"""Check the reviewed manifest-validator dependency lock without rewriting it."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REQUIREMENTS = ROOT / "requirements.txt"
DEFAULT_LOCK = ROOT / "requirements-lock.txt"
REQUIREMENT_LINE = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]+\])?"
    r"(?P<specifier>.*)$"
)
EXACT_PIN = re.compile(r"^==\s*(?P<version>[^;\s]+)(?:\s*;\s*.+)?$")
HASH_OPTIONS = re.compile(r"\s+--hash=\S+")
AVAILABLE_VERSIONS = re.compile(r"Available versions:\s*(?P<versions>.+)")


@dataclass(frozen=True)
class Pin:
    name: str
    version: str
    line: int


def canonical_name(name: str) -> str:
    """Normalize a distribution name for comparison."""

    return re.sub(r"[-_.]+", "-", name).lower()


def read_pins(path: Path) -> tuple[dict[str, Pin], list[str]]:
    """Read exact package pins and report malformed entries with line numbers."""

    pins: dict[str, Pin] = {}
    errors: list[str] = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue

        match = REQUIREMENT_LINE.fullmatch(HASH_OPTIONS.sub("", line).strip())
        if match is None:
            errors.append(
                f"{path}:{line_number}: unsupported requirement syntax {line!r}"
            )
            continue

        name = canonical_name(match.group("name"))
        specifier = match.group("specifier").strip()
        pin = EXACT_PIN.fullmatch(specifier)
        if pin is None:
            errors.append(
                f"{path}:{line_number}: {name} must use an exact == version pin"
            )
            continue
        if name in pins:
            errors.append(
                f"{path}:{line_number}: duplicate requirement name {name}"
            )
            continue
        pins[name] = Pin(name, pin.group("version"), line_number)

    return pins, errors


def lock_drift_errors(requirements: Path, lock: Path) -> list[str]:
    """Return deterministic, offline errors for direct requirement/lock drift."""

    declared, errors = read_pins(requirements)
    locked, lock_errors = read_pins(lock)
    errors.extend(lock_errors)

    for name, declared_pin in sorted(declared.items()):
        locked_pin = locked.get(name)
        if locked_pin is None:
            errors.append(
                f"{requirements}:{declared_pin.line}: {name} is declared at "
                f"{declared_pin.version} but missing from {lock}"
            )
        elif locked_pin.version != declared_pin.version:
            errors.append(
                f"{requirements}:{declared_pin.line}: {name} declares "
                f"{declared_pin.version}, but {lock}:{locked_pin.line} locks "
                f"{locked_pin.version}"
            )

    return errors


def latest_version(
    package: str,
    *,
    index_url: str | None = None,
) -> tuple[str | None, str | None]:
    """Ask pip's configured index for the latest version without installing."""

    command = [sys.executable, "-m", "pip", "index", "versions", package]
    if index_url:
        command.extend(["--index-url", index_url])
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    output = f"{result.stdout}\n{result.stderr}"
    match = AVAILABLE_VERSIONS.search(output)
    if result.returncode != 0 or match is None:
        detail = result.stderr.strip() or result.stdout.strip() or "no response"
        return None, detail
    return match.group("versions").split(",", 1)[0].strip(), None


def update_report(
    lock: Path,
    *,
    index_url: str | None = None,
) -> tuple[list[str], list[str]]:
    """Return available updates and network/query warnings for locked packages."""

    locked, errors = read_pins(lock)
    updates: list[str] = []
    warnings = list(errors)
    for name, pin in sorted(locked.items()):
        latest, error = latest_version(name, index_url=index_url)
        if error:
            warnings.append(f"{name}: unable to check available versions ({error})")
        elif latest and latest != pin.version:
            updates.append(
                f"{name}: lock has {pin.version}; latest index version is {latest}"
            )
    return updates, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check manifest-validator lock drift without rewriting dependency files."
    )
    parser.add_argument("--requirements", type=Path, default=DEFAULT_REQUIREMENTS)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument(
        "--check-updates",
        action="store_true",
        help="query pip's package index for newer locked versions",
    )
    parser.add_argument("--index-url", help="optional package index used by --check-updates")
    args = parser.parse_args(argv)

    errors = lock_drift_errors(args.requirements, args.lock)
    if errors:
        print("FAIL validator dependency lock drift:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK validator lock matches direct requirements: {args.lock}")
    if not args.check_updates:
        return 0

    updates, warnings = update_report(args.lock, index_url=args.index_url)
    if updates:
        print("\nAVAILABLE VALIDATOR DEPENDENCY UPDATES:")
        for update in updates:
            print(f"  - {update}")
    if warnings:
        print("\nWARNINGS WHILE CHECKING AVAILABLE UPDATES:")
        for warning in warnings:
            print(f"  - {warning}")

    if updates:
        return 1
    if warnings:
        return 0
    print("OK no newer locked validator dependency versions found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())