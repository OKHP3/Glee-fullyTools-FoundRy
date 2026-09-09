#!/usr/bin/env python3
"""Check relative Markdown links in the repository's maintained indexes."""
from __future__ import annotations

import argparse
import dataclasses
import pathlib
import re
from collections.abc import Iterable
from urllib.parse import unquote, urlsplit


# These are the active, maintained indexes. snapshots/README.md is intentionally
# excluded because dated snapshots are read-only lineage evidence, not a live
# maintenance surface. The generated .agents/skills catalog has its own checker.
DEFAULT_DOCUMENTS = (
    "README.md",
    "docs/README.md",
    "prompts/README.md",
    "canon/README.md",
    "evaluation/README.md",
    "governance/README.md",
    "inventory/README.md",
    "templates/README.md",
    "vernacular/README.md",
    "web-templates/README.md",
)

# This intentionally handles inline Markdown links, which are the link form used
# by the maintained indexes. Links inside fenced code blocks are not prose links.
LINK_RE = re.compile(
    r"(?<!!)\[[^\]\n]*\]\(\s*(?P<destination><[^>\n]*>|[^)\s]+)"
)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
ATX_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}(?:[ \t]+(.*?)\s*|[ \t]*)$")
SETEXT_HEADING_RE = re.compile(r"^\s{0,3}(?:=+|-+)\s*$")
HTML_TAG_RE = re.compile(r"<[^>\n]*>")
INLINE_LINK_RE = re.compile(r"!?\[([^\]\n]+)\]\([^)\n]*\)")
GITHUB_PUNCTUATION_RE = re.compile(
    r"[\u2000-\u206F\u2E00-\u2E7F\\'!\"#$%&()*+,./:;<=>?@[\]^`{|}~]"
)

# These are the only placeholder forms ignored by this check. A placeholder is
# not a license to hide an arbitrary missing path: use a recognizable token.
PLACEHOLDER_RE = re.compile(
    r"\{\{[^{}\n]+\}\}"  # {{generated-path}}
    r"|\$\{[^{}\n]+\}"  # ${generated_path}
    r"|(?<!\w)(?:placeholder|todo|tbd)(?!\w)"
    r"|(?:^|[/_-])your[-_ ](?:file|path|url|link)(?:$|[/_.-])"
    r"|\.\.\.",
    re.IGNORECASE,
)
ANGLE_PLACEHOLDER_RE = re.compile(
    r"<(?:placeholder|todo|tbd|your[-_ ](?:file|path|url|link))"
    r"(?:\.[^>\s]+)?>",
    re.IGNORECASE,
)


@dataclasses.dataclass(frozen=True)
class LinkIssue:
    source: pathlib.Path
    line: int
    destination: str
    reason: str


@dataclasses.dataclass
class ScanResult:
    files: int = 0
    links: int = 0
    external: int = 0
    anchors: int = 0
    placeholders: int = 0
    issues: list[LinkIssue] = dataclasses.field(default_factory=list)


def _is_fenced(line: str, fence: str | None) -> tuple[bool, str | None]:
    """Return whether a line changes fenced-code state."""
    match = FENCE_RE.match(line)
    if not match:
        return False, fence
    marker = match.group(1)
    if fence is None:
        return True, marker[0]
    if marker[0] == fence:
        return True, None
    return True, fence


def _is_placeholder(raw_destination: str, destination: str) -> bool:
    return bool(
        PLACEHOLDER_RE.search(destination)
        or ANGLE_PLACEHOLDER_RE.search(raw_destination)
    )


def _relative_path(destination: str) -> str:
    """Remove URL query/fragment components and decode the path."""
    return unquote(urlsplit(destination).path)


def _github_heading_slug(heading: str) -> str:
    """Return the GitHub-compatible slug for a rendered Markdown heading."""
    heading = HTML_TAG_RE.sub("", heading)
    heading = INLINE_LINK_RE.sub(r"\1", heading)
    heading = heading.strip().lower()
    heading = GITHUB_PUNCTUATION_RE.sub("", heading)
    return re.sub(r"\s", "-", heading)


def _heading_texts(text: str) -> Iterable[str]:
    """Yield Markdown heading text while ignoring fenced-code examples."""
    lines = text.splitlines()
    fence: str | None = None
    for index, line in enumerate(lines):
        changed, fence = _is_fenced(line, fence)
        if changed or fence is not None:
            continue

        match = ATX_HEADING_RE.match(line)
        if match:
            heading = match.group(1) or ""
            heading = re.sub(r"[ \t]+#+[ \t]*$", "", heading)
            yield heading
            continue

        if (
            line.strip()
            and index + 1 < len(lines)
            and SETEXT_HEADING_RE.match(lines[index + 1])
        ):
            yield line.strip()


def _heading_ids(text: str) -> set[str]:
    """Return the heading IDs GitHub would expose for a Markdown document."""
    ids: set[str] = set()
    next_suffix: dict[str, int] = {}
    for heading in _heading_texts(text):
        base = _github_heading_slug(heading)
        if not base:
            continue

        heading_id = base
        if heading_id in ids:
            suffix = next_suffix.get(base, 1)
            heading_id = f"{base}-{suffix}"
            while heading_id in ids:
                suffix += 1
                heading_id = f"{base}-{suffix}"
            next_suffix[base] = suffix + 1
        else:
            next_suffix.setdefault(base, 1)
        ids.add(heading_id)
    return ids


def scan_file(path: pathlib.Path, root: pathlib.Path, result: ScanResult) -> None:
    """Scan one Markdown file and append any broken relative links."""
    text = path.read_text(encoding="utf-8", errors="replace")
    source = path.relative_to(root)
    result.files += 1
    fence: str | None = None
    heading_ids = _heading_ids(text)
    target_heading_ids: dict[pathlib.Path, set[str]] = {path: heading_ids}

    for line_number, line in enumerate(text.splitlines(), start=1):
        changed, fence = _is_fenced(line, fence)
        if changed or fence is not None:
            continue

        for match in LINK_RE.finditer(line):
            result.links += 1
            raw_destination = match.group("destination").strip()
            destination = raw_destination
            if destination.startswith("<") and destination.endswith(">"):
                destination = destination[1:-1].strip()

            if _is_placeholder(raw_destination, destination):
                result.placeholders += 1
                continue

            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc or destination.startswith("//"):
                result.external += 1
                continue

            relative_path = _relative_path(destination)
            target = (path.parent / relative_path).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                result.issues.append(
                    LinkIssue(source, line_number, destination, "outside repository")
                )
                continue

            if not target.exists():
                result.issues.append(
                    LinkIssue(source, line_number, destination, "target does not exist")
                )
                continue

            if not parsed.path and parsed.fragment:
                result.anchors += 1

            if parsed.fragment and target.is_file() and target.suffix.lower() == ".md":
                if target not in target_heading_ids:
                    target_heading_ids[target] = _heading_ids(
                        target.read_text(encoding="utf-8", errors="replace")
                    )
                fragment = unquote(parsed.fragment)
                if fragment not in target_heading_ids[target]:
                    result.issues.append(
                        LinkIssue(source, line_number, destination, "heading does not exist")
                    )


def scan(root: pathlib.Path, documents: tuple[str, ...]) -> ScanResult:
    """Scan the selected maintained Markdown documents under *root*."""
    root = root.resolve()
    result = ScanResult()
    for document in documents:
        path = (root / document).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            result.issues.append(
                LinkIssue(path, 0, document, "document is outside repository")
            )
            continue
        if not path.is_file():
            result.issues.append(LinkIssue(path, 0, document, "document missing"))
            continue
        scan_file(path, root, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate relative Markdown links in maintained repository indexes."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="repository root (default: current directory)",
    )
    parser.add_argument(
        "--document",
        action="append",
        dest="documents",
        metavar="PATH",
        help="document relative to root; repeat to override the defaults",
    )
    args = parser.parse_args(argv)

    documents = tuple(args.documents) if args.documents else DEFAULT_DOCUMENTS
    result = scan(pathlib.Path(args.root), documents)
    if result.issues:
        print("FAIL broken Markdown links:")
        for issue in result.issues:
            location = f"{issue.source}:{issue.line}" if issue.line else str(issue.source)
            print(f"  - {location}: {issue.destination!r} ({issue.reason})")
        return 1

    print(
        f"OK checked {result.links} links in {result.files} files; "
        f"skipped {result.external} external, {result.anchors} anchor, "
        f"and {result.placeholders} placeholder links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())