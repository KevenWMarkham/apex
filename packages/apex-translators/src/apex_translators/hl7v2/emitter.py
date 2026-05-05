"""HL7 v2.x emitter — Sprint 23 Task 23.2."""

from __future__ import annotations

from dataclasses import dataclass

from apex_translators.base import EmitError, ParsedMessage
from apex_translators.hl7v2.parser import (
    MLLP_END,
    MLLP_START,
    HL7v2Delimiters,
)


@dataclass
class HL7v2Emitter:
    """HL7 v2 emitter — segment-level."""

    def emit(self, message: ParsedMessage) -> str:
        if not message.segments:
            raise EmitError("Cannot emit HL7 v2 from a message with no segments")
        delims = self._delims_from(message)

        lines: list[str] = []
        for seg in message.segments:
            if seg.name == "MSH":
                # MSH-1 is the field separator itself; MSH-2 is the encoding
                # token. When we re-render we need to skip the leading
                # field_sep "element" and write
                #     MSH<field_sep><encoding><field_sep>...
                if not seg.elements:
                    raise EmitError("MSH segment has no elements")
                # Drop element[0] which is the field_sep itself
                rest = seg.elements[1:]
                lines.append(seg.name + delims.field + delims.field.join(rest))
            else:
                lines.append(seg.name + delims.field + delims.field.join(seg.elements))

        return delims.segment.join(lines) + delims.segment

    @staticmethod
    def _delims_from(message: ParsedMessage) -> HL7v2Delimiters:
        meta = message.metadata.get("delimiters") or {}
        return HL7v2Delimiters(
            field=meta.get("field", "|"),
            component=meta.get("component", "^"),
            repetition=meta.get("repetition", "~"),
            escape=meta.get("escape", "\\"),
            subcomponent=meta.get("subcomponent", "&"),
            segment=meta.get("segment", "\r"),
        )


def emit_hl7v2(message: ParsedMessage) -> str:
    """Convenience: emit an HL7 v2 message."""
    return HL7v2Emitter().emit(message)


def wrap_mllp(text: str | bytes) -> bytes:
    """Wrap a serialized HL7 v2 ER7 payload in MLLP framing for the wire."""
    payload = text.encode("utf-8") if isinstance(text, str) else text
    return MLLP_START + payload + MLLP_END
