#!/usr/bin/env python3
"""Check relative Markdown links in the repository's maintained indexes."""
from __future__ import annotations

import argparse
import dataclasses
import pathlib
import re
from collections.abc import Iterable
from urllib.parse import unquote, urlsplit


# These are the active, maintained indexes. The nested application and ADR hubs
# have their own local maintenance contexts but are still part of the default
# repository check. The test-suite README documents the adjacent test surface.
# Pilot-package READMEs are handoff notes, not indexes; dated delegation and
# snapshot READMEs are historical lineage. The generated .agents/skills catalog
# has its own checker.
DEFAULT_DOCUMENTS = (
    "README.md",
    "docs/README.md",
    "docs/application/README.md",
    "docs/adr/README.md",
    "prompts/README.md",
    "canon/README.md",
    "evaluation/README.md",
    "governance/README.md",
    "inventory/README.md",
    "templates/README.md",
    "vernacular/README.md",
    "web-templates/README.md",
    "scripts/tests/README.md",
)
PILOT_DOCUMENT_ROOT = pathlib.Path("docs/application/pilots")
PILOT_EXCLUDED_DIRECTORIES = frozenset(
    {"archive", "archives", "generated", "historical", "snapshots"}
)
WORKFLOW_PATH = pathlib.Path(".github/workflows/foundry-app.yml")
WORKFLOW_EVENTS = ("pull_request", "push")

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


def discover_pilot_documents(root: pathlib.Path) -> tuple[str, ...]:
    """Return complete direct pilot-package README paths."""
    pilot_root = root / PILOT_DOCUMENT_ROOT
    if not pilot_root.is_dir():
        return ()

    documents: list[str] = []
    for package_dir in sorted(pilot_root.iterdir()):
        if (
            not package_dir.is_dir()
            or package_dir.name.startswith(".")
            or package_dir.name.lower() in PILOT_EXCLUDED_DIRECTORIES
            or not (package_dir / "project.json").is_file()
            or not (package_dir / "README.md").is_file()
        ):
            continue
        documents.append(
            (PILOT_DOCUMENT_ROOT / package_dir.name / "README.md").as_posix()
        )
    return tuple(documents)


def discover_pilot_package_issues(root: pathlib.Path) -> tuple[LinkIssue, ...]:
    """Report direct pilot packages with exactly one required handoff file."""
    pilot_root = root / PILOT_DOCUMENT_ROOT
    if not pilot_root.is_dir():
        return ()

    issues: list[LinkIssue] = []
    for package_dir in sorted(pilot_root.iterdir()):
        if (
            not package_dir.is_dir()
            or package_dir.name.startswith(".")
            or package_dir.name.lower() in PILOT_EXCLUDED_DIRECTORIES
        ):
            continue

        has_manifest = (package_dir / "project.json").is_file()
        has_readme = (package_dir / "README.md").is_file()
        if has_manifest == has_readme:
            continue

        missing_file = "README.md" if has_manifest else "project.json"
        issues.append(
            LinkIssue(
                source=package_dir.relative_to(root),
                line=0,
                destination=missing_file,
                reason="pilot package missing handoff file",
            )
        )
    return tuple(issues)


def _workflow_value_without_comment(value: str, line_number: int) -> str:
    """Remove an unquoted YAML comment while preserving quoted ``#`` values."""
    stripped = value.lstrip()
    quote: str | None = stripped[0] if stripped[:1] in {"'", '"'} else None
    escaped = False
    index = 0
    while index < len(value):
        char = value[index]
        if quote == '"':
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif quote == "'":
            if char == quote:
                if index + 1 < len(value) and value[index + 1] == quote:
                    index += 1
                else:
                    quote = None
        elif char == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
        index += 1

    if quote is not None:
        raise ValueError(
            f"line {line_number}: unterminated {quote}-quoted path filter"
        )
    return value.strip()


def _workflow_path_value(value: str, line_number: int) -> str:
    """Parse one supported scalar path filter from a workflow list item."""
    value = _workflow_value_without_comment(value, line_number)
    if not value:
        raise ValueError(f"line {line_number}: path filter value is missing")

    if value[0] not in {"'", '"'}:
        return value

    quote = value[0]
    if quote == "'":
        if len(value) < 2 or value[-1] != quote:
            raise ValueError(
                f"line {line_number}: unterminated single-quoted path filter"
            )
        return value[1:-1].replace("''", "'")

    escaped = False
    closing_index: int | None = None
    for index in range(1, len(value)):
        char = value[index]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote:
            closing_index = index
            break
    if closing_index is None or value[closing_index + 1 :].strip():
        raise ValueError(
            f"line {line_number}: malformed double-quoted path filter"
        )
    return value[1:closing_index]


def workflow_path_filters(workflow_text: str, event: str) -> tuple[str, ...]:
    """Extract path filters for one workflow event without a YAML dependency."""
    filters: list[str] = []
    in_event = False
    in_paths = False

    for line_number, line in enumerate(workflow_text.splitlines(), start=1):
        if re.fullmatch(rf"  {re.escape(event)}:\s*(?:#.*)?", line):
            in_event = True
            in_paths = False
            continue
        if in_event and re.match(r"^  \S", line):
            break
        if not in_event:
            continue
        if re.fullmatch(r"    paths:\s*(?:#.*)?", line):
            in_paths = True
            continue
        if not in_paths:
            continue

        if not line.strip() or line.lstrip().startswith("#"):
            continue

        list_item = re.fullmatch(r"^( {6})-\s+(.+)$", line)
        if list_item:
            filters.append(_workflow_path_value(list_item.group(2), line_number))
            continue

        indentation = len(line) - len(line.lstrip(" "))
        if indentation <= 4:
            if indentation == 4 and line.lstrip().startswith("-"):
                raise ValueError(
                    f"line {line_number}: path list item must be indented "
                    "six spaces under paths"
                )
            in_paths = False
            continue

        raise ValueError(
            f"line {line_number}: unsupported structure under paths; "
            "expected a six-space list item"
        )

    return tuple(filters)


def workflow_path_matches(document: str, pattern: str) -> bool:
    """Match a repository path using GitHub Actions filter syntax."""
    tokens: list[str] = []
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if pattern.startswith("**/", index):
            tokens.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            tokens.append(".*")
            index += 2
        elif char == "*":
            tokens.append("[^/]*")
            index += 1
        elif char in "?+" and tokens:
            tokens[-1] = "(?:" + tokens[-1] + ")" + char
            index += 1
        elif char == "[":
            end = pattern.find("]", index + 1)
            content = pattern[index + 1:end]
            if end < 0 or not re.fullmatch(
                r"(?:[a-zA-Z0-9](?:-[a-zA-Z0-9])?)+", content
            ):
                raise ValueError(
                    f"unsupported character class in path filter {pattern!r}"
                )
            tokens.append("[" + content + "]")
            index = end + 1
        elif char == "\\" and index + 1 < len(pattern):
            tokens.append(re.escape(pattern[index + 1]))
            index += 2
        else:
            tokens.append(re.escape(char))
            index += 1
    return re.fullmatch("".join(tokens), document) is not None


def workflow_covers_path(document: str, filters: tuple[str, ...]) -> bool:
    """Apply ordered exclusions and re-inclusions to a repository path."""
    covered = False
    for path_filter in filters:
        excluded = path_filter.startswith("!")
        pattern = path_filter[1:] if excluded else path_filter
        if workflow_path_matches(document, pattern):
            covered = not excluded
    return covered


def check_workflow_document_coverage(
    root: pathlib.Path,
    workflow_text: str | None = None,
) -> list[str]:
    """Return drift issues between maintained documents and workflow filters."""
    workflow_path = root / WORKFLOW_PATH
    if workflow_text is None:
        try:
            workflow_text = workflow_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return [f"{WORKFLOW_PATH} is missing or unreadable"]

    issues: list[str] = []
    for event in WORKFLOW_EVENTS:
        try:
            filters = workflow_path_filters(workflow_text, event)
        except ValueError as error:
            issues.append(f"{WORKFLOW_PATH} {event} paths are malformed: {error}")
            continue
        if not filters:
            issues.append(
                f"{WORKFLOW_PATH} {event} paths are missing; "
                "cannot cover maintained documents"
            )
            continue
        for document in DEFAULT_DOCUMENTS:
            if not workflow_covers_path(document, filters):
                issues.append(
                    f"{WORKFLOW_PATH} {event} paths do not cover maintained "
                    f"document {document}; add a matching filter"
                )
    return issues


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
    parser.add_argument(
        "--pilots",
        action="store_true",
        help="check direct pilot-package READMEs under docs/application/pilots",
    )
    parser.add_argument(
        "--check-workflow-coverage",
        action="store_true",
        help="check workflow path filters cover every maintained document",
    )
    args = parser.parse_args(argv)

    if args.pilots and args.documents:
        parser.error("--pilots cannot be combined with --document")
    if args.check_workflow_coverage and (args.documents or args.pilots):
        parser.error(
            "--check-workflow-coverage cannot be combined with "
            "--document or --pilots"
        )

    root = pathlib.Path(args.root)
    if args.check_workflow_coverage:
        issues = check_workflow_document_coverage(root)
        if issues:
            print("FAIL workflow/document coverage drift:")
            for issue in issues:
                print(f"  - {issue}")
            return 1
        print(
            "OK workflow path filters cover all maintained documents for "
            "pull_request and push"
        )
        return 0

    if args.pilots:
        documents = discover_pilot_documents(root)
        discovery_issues = discover_pilot_package_issues(root)
    else:
        documents = tuple(args.documents) if args.documents else DEFAULT_DOCUMENTS
        discovery_issues = ()
    result = scan(root, documents)
    result.issues = [*discovery_issues, *result.issues]
    if result.issues:
        heading = (
            "FAIL pilot package validation:"
            if args.pilots
            else "FAIL broken Markdown links:"
        )
        print(heading)
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