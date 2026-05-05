"""EDI X12 parser — Sprint 23 Task 23.1.

Auto-detects delimiters from the ISA segment (positions 3, 105, and the
ISA segment terminator). Walks the ST/SE pair to extract individual
transactions; each transaction's segments are flattened into the
:class:`ParsedMessage.segments` list with the envelope segments preserved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterator

from apex_translators.base import (
    FORMAT_EDI_X12,
    ParseError,
    ParsedMessage,
    Segment,
)

# X12 envelope segment names
ENVELOPE_SEGMENTS: frozenset[str] = frozenset({
    "ISA", "GS", "ST", "SE", "GE", "IEA",
})

# Supported transaction-set ids (§23.1.1, §23.1.2)
RETAIL_TRANSACTIONS: frozenset[str] = frozenset({"850", "856", "810", "820"})
HLS_TRANSACTIONS: frozenset[str] = frozenset({"837", "835", "270", "271"})
SUPPORTED_TRANSACTIONS: frozenset[str] = RETAIL_TRANSACTIONS | HLS_TRANSACTIONS


@dataclass
class EDIX12Delimiters:
    """X12 delimiters auto-detected from ISA. Defaults align with common practice."""

    element: str = "*"
    """Element separator (ISA position 4 -- the char immediately after 'ISA')."""

    component: str = ":"
    """Component / sub-element separator (ISA position 105)."""

    segment: str = "~"
    """Segment terminator (one position after ISA's final element)."""

    repetition: str = "^"
    """Repetition separator (ISA-11 in 5010+; pre-5010 uses 'U' as a placeholder)."""


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------


def _detect_delimiters(raw: str) -> EDIX12Delimiters:
    """Auto-detect EDI X12 delimiters from a raw payload."""
    if not raw.startswith("ISA"):
        raise ParseError(
            "EDI X12 payload must start with 'ISA' segment header"
        )
    if len(raw) < 106:
        raise ParseError("ISA header too short — need ≥ 106 characters")

    # Element separator: ISA[3]  (the char right after 'ISA')
    element = raw[3]
    # Component separator: ISA[104]  (after the 16th element)
    component = raw[104]
    # Repetition separator: ISA[82] (5010); older releases place 'U' here
    repetition = raw[82]
    # Segment terminator: ISA[105]
    segment = raw[105]

    return EDIX12Delimiters(
        element=element,
        component=component,
        segment=segment,
        repetition=repetition,
    )


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


@dataclass
class EDIX12Parser:
    """X12 segment-level parser.

    Builds a :class:`ParsedMessage` whose ``segments`` list is the flat
    sequence of every segment in document order, including envelope
    segments (ISA / GS / ST / SE / GE / IEA). Downstream consumers can
    walk by segment name or by ST/SE boundaries to extract individual
    transactions.
    """

    delimiters: EDIX12Delimiters | None = None

    def parse(self, raw: str) -> ParsedMessage:
        """Parse a raw EDI X12 payload."""
        text = raw.strip()
        if not text:
            raise ParseError("EDI X12 payload is empty")
        delims = self.delimiters or _detect_delimiters(text)

        segments: list[Segment] = []
        for raw_seg in text.split(delims.segment):
            raw_seg = raw_seg.strip("\r\n ")
            if not raw_seg:
                continue
            elements = raw_seg.split(delims.element)
            name = elements[0]
            if not name:
                continue
            segments.append(
                Segment(name=name, elements=elements[1:], raw=raw_seg)
            )

        # Pull envelope-level metadata from ISA / GS / ST
        msg = ParsedMessage(
            format=FORMAT_EDI_X12,
            segments=segments,
            raw=text,
            metadata={
                "delimiters": {
                    "element": delims.element,
                    "component": delims.component,
                    "segment": delims.segment,
                    "repetition": delims.repetition,
                },
            },
        )

        isa = msg.first("ISA")
        if isa is None:
            raise ParseError("EDI X12 payload missing ISA envelope segment")
        if len(isa.elements) < 16:
            raise ParseError(
                f"ISA segment too short: expected 16 elements, got {len(isa.elements)}"
            )

        msg.sender = isa.elements[5].strip()  # ISA-06 Interchange Sender ID
        msg.receiver = isa.elements[7].strip()  # ISA-08 Interchange Receiver ID
        msg.control_number = isa.elements[12].strip()  # ISA-13 ICN
        msg.version = isa.elements[11].strip()  # ISA-12 Version

        # ISA-09 + ISA-10 = YYMMDD + HHMM
        try:
            date_str = isa.elements[8].strip()
            time_str = isa.elements[9].strip()
            if len(date_str) == 6 and len(time_str) == 4:
                year = 2000 + int(date_str[0:2])
                msg.sent_at = datetime(
                    year=year,
                    month=int(date_str[2:4]),
                    day=int(date_str[4:6]),
                    hour=int(time_str[0:2]),
                    minute=int(time_str[2:4]),
                    tzinfo=timezone.utc,
                )
        except (ValueError, IndexError):
            # ISA timestamp malformed; non-fatal — leave sent_at None
            pass

        st = msg.first("ST")
        if st is not None and len(st.elements) >= 1:
            msg.message_type = st.elements[0].strip()

        return msg


def parse_x12(raw: str, delimiters: EDIX12Delimiters | None = None) -> ParsedMessage:
    """Convenience: parse an X12 payload with default options."""
    return EDIX12Parser(delimiters=delimiters).parse(raw)


# ---------------------------------------------------------------------------
# Transaction-set iteration
# ---------------------------------------------------------------------------


def iter_transaction_sets(msg: ParsedMessage) -> Iterator[list[Segment]]:
    """Yield each ST..SE transaction set as a list of segments (inclusive)."""
    current: list[Segment] | None = None
    for seg in msg.segments:
        if seg.name == "ST":
            current = [seg]
        elif seg.name == "SE":
            if current is None:
                raise ParseError("SE segment without matching ST")
            current.append(seg)
            yield current
            current = None
        elif current is not None:
            current.append(seg)
    if current is not None:
        raise ParseError("ST segment without matching SE (unterminated transaction)")
