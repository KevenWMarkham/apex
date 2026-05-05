"""EPCIS 2.0 parser — Sprint 23 Task 23.4.

Detects JSON-LD vs. XML by sniffing the first non-whitespace character.
Both forms produce the same :class:`ParsedMessage` shape: one
:class:`Segment` per EPCIS event with the event JSON populated into
``data``.

Foundation for FSMA 204 traceability orchestrations — every parsed event
is bindable to SCML Lot / Shipment entities (Sprint 23 §23.4.2).
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any

from apex_translators.base import (
    FORMAT_EPCIS,
    ParseError,
    ParsedMessage,
    Segment,
)


EPCIS_EVENT_TYPES: tuple[str, ...] = (
    "ObjectEvent",
    "AggregationEvent",
    "TransactionEvent",
    "TransformationEvent",
    "AssociationEvent",  # 2.0 addition
)

NS_EPCIS = "urn:epcglobal:epcis:xsd:2"
NS_EPCISQ = "urn:epcglobal:epcis-query:xsd:2"
NS_CBV = "urn:epcglobal:cbv:mda"


@dataclass
class EPCISParser:
    """EPCIS 2.0 multi-format parser."""

    def parse(self, raw: str) -> ParsedMessage:
        if not raw or not raw.strip():
            raise ParseError("EPCIS payload is empty")
        stripped = raw.lstrip()
        if stripped.startswith("{") or stripped.startswith("["):
            return self._parse_json(raw)
        if stripped.startswith("<"):
            return self._parse_xml(raw)
        raise ParseError(
            "EPCIS payload first non-whitespace character must be '{', '[', or '<'"
        )

    # -------------------------- JSON -----------------------------------

    def _parse_json(self, raw: str) -> ParsedMessage:
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ParseError(f"EPCIS JSON parse error: {exc}") from exc
        if not isinstance(doc, dict):
            raise ParseError("EPCIS JSON root must be an object")

        msg = ParsedMessage(format=FORMAT_EPCIS, raw=raw)
        msg.message_type = doc.get("type", doc.get("@type", "EPCISDocument"))
        msg.version = doc.get("schemaVersion", "2.0")

        # Document creation date
        msg.metadata["creation_date"] = doc.get(
            "creationDate", doc.get("epcis:creationDate", "")
        )
        msg.metadata["context"] = doc.get("@context", "")

        # Events live in epcisBody.eventList
        body = doc.get("epcisBody") or doc.get("epcis:epcisBody") or {}
        events = body.get("eventList") or body.get("epcis:eventList") or []
        if not isinstance(events, list):
            raise ParseError("EPCIS eventList must be an array")

        for event in events:
            if not isinstance(event, dict):
                continue
            event_type = event.get("type") or event.get("@type") or "ObjectEvent"
            msg.segments.append(
                Segment(name=event_type, data=dict(event))
            )

        return msg

    # -------------------------- XML ------------------------------------

    def _parse_xml(self, raw: str) -> ParsedMessage:
        try:
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            raise ParseError(f"EPCIS XML parse error: {exc}") from exc

        msg = ParsedMessage(format=FORMAT_EPCIS, raw=raw)
        msg.message_type = "EPCISDocument"
        msg.version = root.get("schemaVersion", "2.0")
        msg.metadata["creation_date"] = root.get("creationDate", "")

        # Find every event regardless of namespace prefix
        for event_el in _iter_events(root):
            local_name = event_el.tag.split("}")[-1]
            data = _xml_to_dict(event_el)
            data["@type"] = local_name
            msg.segments.append(Segment(name=local_name, data=data))

        return msg


def parse_epcis(raw: str) -> ParsedMessage:
    """Convenience: parse an EPCIS 2.0 payload (JSON-LD or XML)."""
    return EPCISParser().parse(raw)


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------


def _iter_events(root: ET.Element):
    """Yield every event-typed element in the document tree."""
    type_set = set(EPCIS_EVENT_TYPES)
    for el in root.iter():
        local = el.tag.split("}")[-1]
        if local in type_set:
            yield el


def _xml_to_dict(el: ET.Element) -> dict[str, Any]:
    """Recursive XML element → dict, dropping namespace prefixes."""
    out: dict[str, Any] = {}
    for child in el:
        local = child.tag.split("}")[-1]
        if list(child):
            sub = _xml_to_dict(child)
        elif child.text and child.text.strip():
            sub = child.text.strip()
        else:
            sub = ""
        # If we already saw this key, promote to list
        if local in out:
            existing = out[local]
            if isinstance(existing, list):
                existing.append(sub)
            else:
                out[local] = [existing, sub]
        else:
            out[local] = sub
    # Capture attributes too
    for k, v in el.attrib.items():
        out["@" + k] = v
    return out
