"""HL7 v2.x parser — Sprint 23 Task 23.2.

MLLP framing per the HL7 wire protocol:

- Start block: ``\\x0b`` (vertical tab, "VT")
- End block: ``\\x1c\\r`` (FS + CR)

Inside the framed payload, segments are CR-delimited (``\\r``), fields are
``|``-delimited, repetitions are ``~``, components are ``^``, sub-components
are ``&``, and escape is ``\\``. The MSH segment carries the field
separator at MSH-1 and the four other delimiters at MSH-2.

This parser handles the named segment library:

- MSH (message header)
- PID (patient identification)
- PV1 (patient visit)
- OBX (observation/result)
- OBR (observation request)
- ORC (common order)
- RXE (pharmacy/treatment encoded order)
- AL1 (patient allergy information)

plus passes through any other segments encountered, raw, into
:attr:`ParsedMessage.segments`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from apex_translators.base import (
    FORMAT_HL7V2,
    ParseError,
    ParsedMessage,
    Segment,
)


# ---------------------------------------------------------------------------
# MLLP framing
# ---------------------------------------------------------------------------

MLLP_START = b"\x0b"
MLLP_END = b"\x1c\r"


def strip_mllp(framed: bytes | str) -> str:
    """Strip MLLP framing bytes from a wire payload, returning the inner ER7."""
    payload = framed.encode("utf-8") if isinstance(framed, str) else framed
    if payload.startswith(MLLP_START):
        payload = payload[len(MLLP_START) :]
    if payload.endswith(MLLP_END):
        payload = payload[: -len(MLLP_END)]
    return payload.decode("utf-8")


# ---------------------------------------------------------------------------
# Delimiters
# ---------------------------------------------------------------------------


@dataclass
class HL7v2Delimiters:
    """Per HL7 v2 spec: MSH-1 carries field separator; MSH-2 carries the rest."""

    field: str = "|"
    component: str = "^"
    repetition: str = "~"
    escape: str = "\\"
    subcomponent: str = "&"
    segment: str = "\r"
    """Segments are CR-delimited per the HL7 wire spec; tooling often
    converts to LF or CRLF. Parser tolerates both."""


SUPPORTED_SEGMENTS: frozenset[str] = frozenset({
    "MSH", "PID", "PV1", "OBX", "OBR", "ORC", "RXE", "AL1",
})


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


@dataclass
class HL7v2Parser:
    """HL7 v2.x parser — segment-level."""

    def parse(self, raw: str) -> ParsedMessage:
        text = raw.strip("\r\n ")
        if not text.startswith("MSH"):
            raise ParseError("HL7 v2 message must begin with MSH segment")
        if len(text) < 8:
            raise ParseError("MSH segment is too short")

        # Field separator from MSH-1 (the char right after 'MSH')
        field_sep = text[3]
        # Encoding chars are the MSH-2 token (4 chars: comp ^, rep ~, esc \, subcomp &)
        # MSH layout: MSH | <encoding> | sender | ...  ⇒ chars [4..8]
        encoding = text[4:8]
        if len(encoding) < 4:
            raise ParseError("MSH-2 (encoding characters) is too short")
        delims = HL7v2Delimiters(
            field=field_sep,
            component=encoding[0],
            repetition=encoding[1],
            escape=encoding[2],
            subcomponent=encoding[3],
        )

        # Segment-split: tolerate CR / LF / CRLF
        normalized = text.replace("\r\n", "\r").replace("\n", "\r")
        segment_lines = [s for s in normalized.split("\r") if s]

        segments: list[Segment] = []
        for line in segment_lines:
            if line.startswith("MSH"):
                # MSH is special: field 1 IS the separator, so the second
                # element starts at position 3 (with the separator), and the
                # encoding chars at MSH-2 are positions 4-7. Skip past the MSH
                # name + the encoding token, then split on the field separator.
                head = line[:3]
                rest = line[3:]
                # MSH split: tail.split(field_sep) gives [encoding, sender, ...]
                # but HL7 convention shows MSH-1 as the separator itself, so
                # we re-insert it as the first element.
                tail_elements = rest.split(delims.field)
                # tail_elements[0] is empty because rest starts with the separator
                # tail_elements[1] is the encoding chars (MSH-2)
                # tail_elements[2..] are MSH-3 onward
                # We expose elements as [field_sep, encoding, MSH-3, MSH-4, ...]
                if tail_elements and tail_elements[0] == "":
                    tail_elements = tail_elements[1:]
                elements = [delims.field, *tail_elements]
                segments.append(Segment(name=head, elements=elements, raw=line))
            else:
                fields = line.split(delims.field)
                segments.append(
                    Segment(name=fields[0], elements=fields[1:], raw=line)
                )

        msg = ParsedMessage(
            format=FORMAT_HL7V2,
            segments=segments,
            raw=text,
            metadata={
                "delimiters": {
                    "field": delims.field,
                    "component": delims.component,
                    "repetition": delims.repetition,
                    "escape": delims.escape,
                    "subcomponent": delims.subcomponent,
                    "segment": delims.segment,
                },
            },
        )

        msh = msg.first("MSH")
        if msh is None:
            raise ParseError("HL7 v2 message missing MSH after split")
        # MSH layout (1-indexed in HL7 spec; 0-indexed in our list):
        #   elements[0] = field separator (MSH-1)
        #   elements[1] = encoding chars (MSH-2)
        #   elements[2] = sending application (MSH-3)
        #   elements[3] = sending facility (MSH-4)
        #   elements[4] = receiving application (MSH-5)
        #   elements[5] = receiving facility (MSH-6)
        #   elements[6] = date/time of message (MSH-7)
        #   elements[8] = message type ^ trigger (MSH-9)
        #   elements[9] = message control id (MSH-10)
        #   elements[11] = version (MSH-12)
        if len(msh.elements) >= 3:
            msg.sender = msh.elements[2]
        if len(msh.elements) >= 5:
            msg.receiver = msh.elements[4]
        if len(msh.elements) >= 7:
            msg.sent_at = _parse_hl7_dtm(msh.elements[6])
        if len(msh.elements) >= 9:
            # Message type may be "ADT^A04" — keep the raw composite
            msg.message_type = msh.elements[8].split(delims.component)[0:2]
            msg.message_type = "^".join(msg.message_type) if isinstance(msg.message_type, list) else msh.elements[8]
        if len(msh.elements) >= 10:
            msg.control_number = msh.elements[9]
        if len(msh.elements) >= 12:
            msg.version = msh.elements[11]

        return msg


def parse_hl7v2(raw: str) -> ParsedMessage:
    """Convenience: parse an HL7 v2 message with default options."""
    return HL7v2Parser().parse(raw)


def _parse_hl7_dtm(dtm: str) -> datetime | None:
    """Parse HL7 DTM (YYYYMMDDHHMMSS[.S]) → tz-aware UTC datetime."""
    s = dtm.strip()
    if not s:
        return None
    try:
        if len(s) >= 14:
            return datetime(
                year=int(s[0:4]),
                month=int(s[4:6]),
                day=int(s[6:8]),
                hour=int(s[8:10]),
                minute=int(s[10:12]),
                second=int(s[12:14]),
                tzinfo=timezone.utc,
            )
        if len(s) >= 12:
            return datetime(
                year=int(s[0:4]),
                month=int(s[4:6]),
                day=int(s[6:8]),
                hour=int(s[8:10]),
                minute=int(s[10:12]),
                tzinfo=timezone.utc,
            )
        if len(s) >= 8:
            return datetime(
                year=int(s[0:4]),
                month=int(s[4:6]),
                day=int(s[6:8]),
                tzinfo=timezone.utc,
            )
    except ValueError:
        return None
    return None
