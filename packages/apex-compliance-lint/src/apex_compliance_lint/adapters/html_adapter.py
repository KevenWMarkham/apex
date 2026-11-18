"""HTML file adapter — Sprint 29 Task 29.9.2.

Strips HTML tags + script/style blocks, extracts visible text. Uses
stdlib ``html.parser`` so no external dependencies. Preserves line
numbers so the linter can report accurate line/column positions.
"""

from __future__ import annotations

import contextlib
from html.parser import HTMLParser
from pathlib import Path

from apex_compliance_lint.types import FileAdapter

_SKIP_TAGS = {"script", "style", "noscript", "template"}


class _TextExtractor(HTMLParser):
    """Extracts visible text per source line, ignoring script/style/noscript."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self._lines: dict[int, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in _SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in _SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        # ``getpos()`` returns 1-indexed (line, col) of THIS data event
        line, _col = self.getpos()
        # Data may itself span multiple lines — split and bucket per line
        for offset, segment in enumerate(data.splitlines() or [data]):
            stripped = segment.strip()
            if not stripped:
                continue
            self._lines.setdefault(line + offset, []).append(stripped)

    def into_lines(self) -> list[tuple[int, str]]:
        """Return collected text as ``(line, text)`` pairs, joining fragments on each line."""
        return [(ln, " ".join(parts)) for ln, parts in sorted(self._lines.items())]


class HTMLAdapter(FileAdapter):
    """Extract visible text from an HTML file."""

    file_extensions = (".html", ".htm")

    def extract(self, path: Path) -> list[tuple[int, str]]:
        """Return visible text per source line, skipping script/style/noscript/template.

        Falls back to the raw non-blank lines when parsing yields no text.
        """
        raw = path.read_text(encoding="utf-8", errors="replace")
        parser = _TextExtractor()
        # Malformed HTML — keep whatever was parsed; plain-text fallback below
        with contextlib.suppress(Exception):
            parser.feed(raw)
        lines = parser.into_lines()
        if lines:
            return lines
        # Fallback: treat as plain text
        return [(i + 1, line) for i, line in enumerate(raw.splitlines()) if line.strip()]
