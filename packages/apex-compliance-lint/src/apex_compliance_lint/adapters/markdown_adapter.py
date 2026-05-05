"""Markdown adapter — Sprint 29 Task 29.9.2.

Extracts visible prose from a markdown file. Strips fenced code blocks,
inline code, link/image URLs (keeping link text), and YAML frontmatter.
Preserves line numbers for accurate reporting.
"""

from __future__ import annotations

import re
from pathlib import Path

from apex_compliance_lint.types import FileAdapter


_FENCE_RE = re.compile(r"^\s*```")
_INLINE_CODE_RE = re.compile(r"`[^`]+`")
_LINK_TEXT_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
_HEADING_HASH_RE = re.compile(r"^#+\s*")


class MarkdownAdapter(FileAdapter):
    """Extract prose from a markdown file."""

    file_extensions = (".md", ".markdown")

    def extract(self, path: Path) -> list[tuple[int, str]]:
        raw = path.read_text(encoding="utf-8", errors="replace")
        lines: list[tuple[int, str]] = []
        in_fence = False
        in_frontmatter = False
        frontmatter_consumed = False

        for i, line in enumerate(raw.splitlines(), 1):
            # YAML frontmatter — skip the entire `---` block at the top
            if i == 1 and line.strip() == "---":
                in_frontmatter = True
                continue
            if in_frontmatter:
                if line.strip() == "---":
                    in_frontmatter = False
                    frontmatter_consumed = True
                continue

            # Fenced code blocks
            if _FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            # Strip inline code
            stripped = _INLINE_CODE_RE.sub(" ", line)
            # Replace links with their visible text + drop image alts
            stripped = _IMAGE_RE.sub(r"\1", stripped)
            stripped = _LINK_TEXT_RE.sub(r"\1", stripped)
            # Strip leading heading hashes
            stripped = _HEADING_HASH_RE.sub("", stripped).strip()

            if stripped:
                lines.append((i, stripped))

        return lines
