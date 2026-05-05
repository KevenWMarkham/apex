"""Restricted-terminology guardrail — Sprint 20 Task 20.5.4 (BL.P.138).

CI scanner: walks the APEX monorepo source tree and fails the build if any
file contains content that looks like a redistributed restricted-terminology
dump (LOINC / SNOMED / ICD / CPT / IEC / ISO standard text).

What this scanner CANNOT do is detect arbitrary IP-laundering — the goal is
to catch the obvious case (someone committed a `loinc.csv` or pasted a
SNOMED concept table into a markdown file) rather than to be a forensic
audit tool.

Detection strategy:

1. **Filename guards.** Block any file whose basename matches a known
   restricted-content pattern (e.g., ``loinc.csv``, ``snomed_*.txt``,
   ``icd10cm_*.zip``).

2. **Content fingerprints.** Scan text files for fingerprints that strongly
   indicate redistributed restricted content (e.g., ``LOINC_NUM,COMPONENT,PROPERTY``
   header from the LOINC table dump; SNOMED RF2 file delimiters in a
   non-licence-attribution file).

3. **Allowlist.** ``LICENSE-ATTRIBUTION.md`` files are exempt — they're
   *expected* to mention the restricted standards by name.

Exit 0 = clean. Exit 1 = restricted content detected.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

RESTRICTED_FILENAMES: list[re.Pattern[str]] = [
    re.compile(r"^loinc.*\.(csv|tsv|txt|zip|xlsx?)$", re.IGNORECASE),
    re.compile(r"^snomed.*\.(csv|tsv|txt|zip|rf2|xlsx?)$", re.IGNORECASE),
    re.compile(r"^icd[-_]?10.*\.(csv|tsv|txt|zip|xlsx?)$", re.IGNORECASE),
    re.compile(r"^icd[-_]?11.*\.(csv|tsv|txt|zip|xlsx?)$", re.IGNORECASE),
    re.compile(r"^cpt.*\.(csv|tsv|txt|zip|xlsx?)$", re.IGNORECASE),
    re.compile(r"^iso[-_]?14224.*\.(pdf|docx?)$", re.IGNORECASE),
    re.compile(r"^iec[-_]?6197[08].*\.(pdf|docx?)$", re.IGNORECASE),
    re.compile(r"^j1939.*\.(pdf|docx?)$", re.IGNORECASE),
]

# Content fingerprints — strong signals of restricted-content dumps
CONTENT_FINGERPRINTS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\bLOINC_NUM\b\s*,\s*COMPONENT\b\s*,\s*PROPERTY\b", re.MULTILINE),
        "LOINC table-dump CSV header",
    ),
    (
        re.compile(r"\bsct2_Concept_Full_\w+_\d+\.txt", re.MULTILINE),
        "SNOMED RF2 release filename",
    ),
    (
        re.compile(
            r"\bICD-10-CM\s+TABULAR\s+LIST\s+OF\s+DISEASES\s+AND\s+INJURIES",
            re.MULTILINE | re.IGNORECASE,
        ),
        "ICD-10-CM tabular text",
    ),
    (
        re.compile(
            r"^\s*Current\s+Procedural\s+Terminology\s+\(?CPT\)?\s+is\s+a\s+registered",
            re.MULTILINE | re.IGNORECASE,
        ),
        "CPT licence preamble (suggests AMA full text)",
    ),
]

# File extensions worth scanning for content fingerprints
SCAN_EXTENSIONS: set[str] = {
    ".py", ".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml",
}

# Path fragments to skip entirely
SKIP_PATH_FRAGMENTS: list[str] = [
    "__pycache__", ".git", ".venv", "node_modules", "dist", "build",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "site-packages",
]

# Filenames where mentioning restricted-terminology names is expected
ALLOWLIST_FILENAMES: set[str] = {
    "license-attribution.md",
    "license_attribution.md",
    "license.md",
    "attribution.md",
    "readme.md",
    "changelog.md",
}


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    path: Path
    code: str
    message: str


def scan_path(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        # Skip noise directories
        if any(frag in path.parts for frag in SKIP_PATH_FRAGMENTS):
            continue

        # Filename-pattern check (this fires on ANY file regardless of contents)
        for pattern in RESTRICTED_FILENAMES:
            if pattern.match(path.name):
                # Allowlist sanity-check files (a `loinc-attribution.md` is fine)
                if path.name.lower() in ALLOWLIST_FILENAMES:
                    continue
                findings.append(
                    Finding(
                        path=path,
                        code="RESTRICTED_FILENAME",
                        message=(
                            f"Filename matches restricted-content pattern "
                            f"({pattern.pattern}); restricted vocabulary dumps "
                            f"must not be checked into the APEX monorepo"
                        ),
                    )
                )
                break

        # Content fingerprint check — only on text files
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        if path.name.lower() in ALLOWLIST_FILENAMES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern, label in CONTENT_FINGERPRINTS:
            if pattern.search(text):
                findings.append(
                    Finding(
                        path=path,
                        code="RESTRICTED_CONTENT_FINGERPRINT",
                        message=f"file contains {label}",
                    )
                )

    return findings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Scan the APEX monorepo for redistributed restricted-terminology "
            "content (LOINC / SNOMED / ICD / CPT / IEC / ISO / SAE J1939). "
            "Exits 1 if any restricted content is detected."
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

    findings = scan_path(root)
    if not findings:
        print(f"OK — no restricted-terminology content detected under {root}")
        return 0

    for f in findings:
        print(f"[{f.code}] {f.path}: {f.message}", file=sys.stderr)
    print(
        f"FAIL — {len(findings)} restricted-content issue(s) detected",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
