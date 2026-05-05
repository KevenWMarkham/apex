"""EDI X12 emitter — Sprint 23 Task 23.1.

Inverse of :mod:`apex_translators.edi_x12.parser`. Takes a
:class:`ParsedMessage` and renders X12 with the delimiters captured in the
message's ``metadata['delimiters']`` block (or a default set if not present).
"""

from __future__ import annotations

from dataclasses import dataclass

from apex_translators.base import EmitError, ParsedMessage
from apex_translators.edi_x12.parser import EDIX12Delimiters


@dataclass
class EDIX12Emitter:
    """X12 emitter."""

    delimiters: EDIX12Delimiters | None = None
    line_separator: str = ""
    """Per-segment line separator. ISO recommendation: empty (single line)
    is most-compatible. Set to ``"\\n"`` for human-readable output."""

    def emit(self, message: ParsedMessage) -> str:
        """Render a :class:`ParsedMessage` back to X12."""
        delims = self.delimiters or self._delims_from(message)
        if not message.segments:
            raise EmitError("Cannot emit X12 from a message with no segments")

        lines: list[str] = []
        for seg in message.segments:
            elements = [seg.name, *seg.elements]
            lines.append(delims.element.join(elements))

        return delims.segment.join(lines) + delims.segment + (
            self.line_separator if self.line_separator else ""
        )

    @staticmethod
    def _delims_from(message: ParsedMessage) -> EDIX12Delimiters:
        meta = message.metadata.get("delimiters") or {}
        return EDIX12Delimiters(
            element=meta.get("element", "*"),
            component=meta.get("component", ":"),
            segment=meta.get("segment", "~"),
            repetition=meta.get("repetition", "^"),
        )


def emit_x12(message: ParsedMessage, delimiters: EDIX12Delimiters | None = None) -> str:
    """Convenience: emit an X12 message with default options."""
    return EDIX12Emitter(delimiters=delimiters).emit(message)
