"""IATA PADIS parser — Sprint 23 Task 23.6.

PADIS messages are line-oriented, slash-delimited within lines, with a
TTY-style header. The parser supports PNL/ADL/PRL with sufficient detail
for binding to TH ``TravelerML`` and ``OpsML-TH`` canonical schemas.

Example PNL header::

    PNL
    DL0123/30JUN/JFKLHR/Y
    .R/A/0
    1HOLLAND/JOHN MR
    .R/SSR DOCS DL HK1 P/USA/123456789/USA/15JAN80/M/15JAN30/HOLLAND/JOHN
    .L/L1   2/3
    .E/R-PAX/CTC

Each non-blank line is a record; ``.X/`` continuations get attached to the
preceding traveler record.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from apex_translators.base import (
    FORMAT_PADIS,
    ParseError,
    ParsedMessage,
    Segment,
)


PADIS_MESSAGE_TYPES: tuple[str, ...] = (
    "PNL",  # Passenger Name List
    "ADL",  # Add/Delete List
    "PRL",  # Passenger Reconfirmation List
    "PFS",  # Passenger Final Sales
    "PSM",  # Passenger Service Message
)


# Flight key regex: DL0123/30JUN/JFKLHR/Y or AA1234/15DEC/SFOORD
_FLIGHT_KEY_RE = re.compile(
    r"^([A-Z]{2,3})(\d{1,4})/(\d{1,2}[A-Z]{3})/([A-Z]{6,9})(?:/([A-Z]))?$"
)


# Traveler record: leading numeric count followed by SURNAME/FIRSTNAME [TITLE]
_TRAVELER_RE = re.compile(r"^(\d+)([A-Z][A-Z'\- ]*)/([A-Z][A-Z' \-]*?)(?:\s+([A-Z]+))?\s*$")


@dataclass
class PADISParser:
    """IATA PADIS one-way parser."""

    def parse(self, raw: str) -> ParsedMessage:
        if not raw or not raw.strip():
            raise ParseError("PADIS payload is empty")
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
        if not lines:
            raise ParseError("PADIS payload has no non-blank lines")

        header = lines[0].upper()
        if header not in PADIS_MESSAGE_TYPES:
            raise ParseError(
                f"PADIS message header {header!r} not in supported set "
                f"{PADIS_MESSAGE_TYPES}"
            )

        msg = ParsedMessage(format=FORMAT_PADIS, raw=raw)
        msg.message_type = header

        # Optional flight-key second line
        flight_idx = 1
        if len(lines) > 1:
            fk_match = _FLIGHT_KEY_RE.match(lines[1])
            if fk_match is not None:
                airline, flight_num, date, route, cls = fk_match.groups()
                origin, destination = route[:3], route[3:6]
                msg.metadata["flight"] = {
                    "carrier": airline,
                    "flight_number": flight_num,
                    "departure_date": date,
                    "origin": origin,
                    "destination": destination,
                    "class": cls or "",
                }
                msg.sender = airline
                flight_idx = 2

        current_pax: Segment | None = None
        for line in lines[flight_idx:]:
            # Continuation lines start with '.'
            if line.startswith("."):
                if current_pax is None:
                    # Continuation without a preceding pax — capture as a
                    # message-level supplementary record (e.g., header SSR)
                    msg.segments.append(
                        Segment(
                            name="SUPPLEMENTARY",
                            elements=[line],
                            raw=line,
                        )
                    )
                    continue
                current_pax.data.setdefault("continuations", []).append(line)
                continue

            # Try to match a traveler record
            tr_match = _TRAVELER_RE.match(line)
            if tr_match is not None:
                count, surname, given, title = tr_match.groups()
                pax = Segment(
                    name="PAX",
                    raw=line,
                    data={
                        "count": int(count),
                        "surname": surname.strip(),
                        "given_name": given.strip(),
                        "title": (title or "").strip(),
                    },
                )
                msg.segments.append(pax)
                current_pax = pax
                continue

            # Other unstructured line — capture
            msg.segments.append(
                Segment(name="UNSTRUCTURED", elements=[line], raw=line)
            )
            current_pax = None

        return msg


def parse_padis(raw: str) -> ParsedMessage:
    """Convenience: parse a PADIS message."""
    return PADISParser().parse(raw)
