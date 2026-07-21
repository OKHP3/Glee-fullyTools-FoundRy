#!/usr/bin/env python3
"""Audit externally versioned technologies used by the static templates.

This intentionally uses only the Python standard library. It reports drift and
exits non-zero so a scheduled GitHub Actions run makes maintenance visible.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "web-templates" / "index.html"
MERMAID_PACKAGE = "https://registry.npmjs.org/mermaid/latest"


def get_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Glee-fully technology audit"})
    with urlopen(request, timeout=20) as response:  # noqa: S310: fixed HTTPS URLs above
        return response.read().decode("utf-8", errors="replace")


def main() -> int:
    failures: list[str] = []
    lines = ["## Technology version audit", ""]

    template = TEMPLATE.read_text(encoding="utf-8")
    match = re.search(r"mermaid@([^/]+)", template)
    current_mermaid = match.group(1) if match else "not found"

    try:
        latest_mermaid = json.loads(get_text(MERMAID_PACKAGE))["version"]
        lines.append(f"- Mermaid CDN: `{current_mermaid}`; npm latest: `{latest_mermaid}`")
        current_major = int(re.match(r"\d+", current_mermaid).group()) if re.match(r"\d+", current_mermaid) else -1
        latest_major = int(re.match(r"\d+", latest_mermaid).group())
        if current_major < latest_major:
            failures.append(
                f"Mermaid CDN is pinned to major {current_major}, but stable major {latest_major} is available."
            )
    except (KeyError, json.JSONDecodeError, URLError, TimeoutError, ValueError) as error:
        failures.append(f"Could not read Mermaid release metadata: {error}")

    lines.append("- Python scripts: declared as `Python 3`; CI selects the latest stable `3.x`")

    if failures:
        lines.extend(["", "### Review required", ""])
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.extend(["", "No automated version drift was detected."])

    report = "\n".join(lines) + "\n"
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        Path(summary).write_text(report, encoding="utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
