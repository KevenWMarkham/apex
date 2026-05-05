"""Color-token compliance check — Sprint 29 Task 29.10.4.

Forbids inline hex literals (`#FF5500`, `#abc`, `#80FFFFFF`) in any
CSS / HTML / inline-style declaration EXCEPT the canonical
``docs/apex-design-tokens.css`` file. Every other artifact must
reference colors via `var(--apex-...)`.

This is the second half of the design-token enforcement pair:

- `check_typography_tokens.py` (Task 29.10.3) — font-family declarations
- `check_color_tokens.py` (Task 29.10.4) — color literals
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# Match 3, 4, 6, or 8-digit hex literals after the `#` sigil. Word-boundary
# on the leading char is `(?<![\w&])` to avoid matching CSS escape codes
# or HTML-entity tails (e.g., `&#33;`).
_HEX_RE = re.compile(
    r"(?<![\w&])#([0-9A-Fa-f]{3,4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})\b",
)

# Files to scan
SCAN_EXTENSIONS: frozenset[str] = frozenset({".css", ".html", ".htm"})

SKIP_FRAGMENTS: tuple[str, ...] = (
    "__pycache__", ".git", ".venv", "node_modules", "dist", "build",
    ".pytest_cache", "site-packages",
)

# Tokens file is the canonical home for all hex literals.
ALLOWLIST_BASENAMES: frozenset[str] = frozenset({
    "apex-design-tokens.css",
})

# Documentation files that *describe* the token registry are allowed
# to mention hex literals in their prose. Identified by name suffix.
DOC_NAME_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"appendix-n", re.IGNORECASE),
    re.compile(r"design-system", re.IGNORECASE),
)


@dataclass
class Finding:
    path: Path
    line: int
    hex_value: str
    surrounding: str


def _is_doc_file(path: Path) -> bool:
    name = path.name.lower()
    return any(p.search(name) for p in DOC_NAME_PATTERNS)


def scan_file(path: Path) -> list[Finding]:
    if path.name in ALLOWLIST_BASENAMES:
        return []
    if _is_doc_file(path):
        return []
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    for match in _HEX_RE.finditer(text):
        hex_value = match.group(0)
        line_no = text.count("\n", 0, match.start()) + 1
        # Build a short surrounding context for human readability
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        if line_end == -1:
            line_end = len(text)
        surrounding = text[line_start:line_end].strip()[:140]
        findings.append(Finding(
            path=path, line=line_no, hex_value=hex_value,
            surrounding=surrounding,
        ))
    return findings


def scan_root(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(frag in path.parts for frag in SKIP_FRAGMENTS):
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        findings.extend(scan_file(path))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Color-token compliance — fails the build if any inline hex "
            "literal appears outside docs/apex-design-tokens.css. "
            "Sprint 29 Task 29.10.4."
        )
    )
    parser.add_argument(
        "path", nargs="?", default=".",
        help="Root path to scan (default: current directory).",
    )
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"error: path does not exist: {root}", file=sys.stderr)
        return 2

    findings = scan_root(root)
    if not findings:
        print(f"OK — color-token check clean under {root}")
        return 0

    for f in findings:
        print(
            f"[INLINE_HEX] {f.path}:{f.line}: {f.hex_value} in {f.surrounding!r}",
            file=sys.stderr,
        )
    print(
        f"FAIL — {len(findings)} inline-hex violation(s); "
        "use var(--apex-...) per Appendix N",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
