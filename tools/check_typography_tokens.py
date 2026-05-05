"""Typography-token compliance check — Sprint 29 Task 29.10.3.

Scans CSS / HTML / inline-style declarations for ``font-family`` values
and asserts each declaration uses ONLY families registered in the
APEX design-token catalog (Sprint 29 Task 29.2 Appendix N).

The registry is the source of truth — ``Fraunces``, ``IBM Plex Sans``,
``JetBrains Mono`` plus the system-fallback chain. Any other family
name appearing in `font-family:` is a violation.

CSS-variable-based declarations (``font-family: var(--apex-font-body);``)
are always allowed since the variable resolves through
``apex-design-tokens.css``, the single source of truth.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# Approved family names from Appendix N §1
APPROVED_FAMILIES: frozenset[str] = frozenset({
    # Display / body / mono
    "fraunces",
    "ibm plex sans",
    "jetbrains mono",
    # System-fallback chain (always allowed)
    "system-ui",
    "-apple-system",
    "blinkmacsystemfont",
    "segoe ui fallback",
    "sans-serif",
    "serif",
    "monospace",
    "system",
    "ui-sans-serif",
    "ui-serif",
    "ui-monospace",
    # Stack fallbacks listed in apex-design-tokens.css for Mono / Display
    "consolas",
    "courier new",
    "courier",
    "times new roman",
    "times",
    "inherit",
    "initial",
    "unset",
    "revert",
})


# Match `font-family:` declarations across CSS + inline style attrs
_FONT_FAMILY_RE = re.compile(
    r"font-family\s*:\s*([^;}\"']+)",
    re.IGNORECASE,
)


# Files to scan
SCAN_EXTENSIONS: frozenset[str] = frozenset({".css", ".html", ".htm"})

# Skip noise dirs
SKIP_FRAGMENTS: tuple[str, ...] = (
    "__pycache__", ".git", ".venv", "node_modules", "dist", "build",
    ".pytest_cache", "site-packages",
)

# Allowlist: tokens file is the only place inline strings are expected
# (it ships the CSS custom properties referenced by every other artifact).
ALLOWLIST_BASENAMES: frozenset[str] = frozenset({
    "apex-design-tokens.css",
})


@dataclass
class Finding:
    path: Path
    line: int
    declaration: str
    unapproved: tuple[str, ...]


def _split_family_list(declaration: str) -> list[str]:
    """Split a `font-family` declaration into individual family tokens.

    Handles quoted family names with spaces (`"IBM Plex Sans"`) and
    bare names (`Fraunces`).
    """
    out: list[str] = []
    i = 0
    n = len(declaration)
    while i < n:
        # Skip whitespace + commas
        while i < n and declaration[i] in " \t\n\r,":
            i += 1
        if i >= n:
            break
        # Quoted name?
        if declaration[i] in ('"', "'"):
            quote = declaration[i]
            j = i + 1
            while j < n and declaration[j] != quote:
                j += 1
            out.append(declaration[i + 1:j].strip())
            i = j + 1
        else:
            j = i
            while j < n and declaration[j] != ",":
                j += 1
            out.append(declaration[i:j].strip())
            i = j
    return [f for f in out if f]


def is_var_reference(declaration: str) -> bool:
    """True if the entire declaration is `var(--apex-font-...)`."""
    return bool(re.match(r"^\s*var\(\s*--[\w-]+\s*\)", declaration, re.IGNORECASE))


def scan_file(path: Path) -> list[Finding]:
    if path.name in ALLOWLIST_BASENAMES:
        return []
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    for match in _FONT_FAMILY_RE.finditer(text):
        declaration = match.group(1).strip()
        if is_var_reference(declaration):
            continue
        families = _split_family_list(declaration)
        unapproved = tuple(
            f for f in families
            if f.lower() not in APPROVED_FAMILIES
        )
        if unapproved:
            line_no = text.count("\n", 0, match.start()) + 1
            findings.append(Finding(
                path=path, line=line_no,
                declaration=declaration, unapproved=unapproved,
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
            "Typography-token compliance check — fails the build if any "
            "CSS / HTML font-family declaration uses an unapproved family. "
            "Sprint 29 Task 29.10.3."
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
        print(f"OK — typography-token check clean under {root}")
        return 0

    for f in findings:
        print(
            f"[UNAPPROVED_FONT] {f.path}:{f.line}: declaration "
            f"{f.declaration!r} contains unapproved families "
            f"{list(f.unapproved)}",
            file=sys.stderr,
        )
    print(
        f"FAIL — {len(findings)} typography-token violation(s); "
        "use Fraunces / IBM Plex Sans / JetBrains Mono per Appendix N",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
