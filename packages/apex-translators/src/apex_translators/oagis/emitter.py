"""OAGIS BOD emitter — Sprint 23 Task 23.5.

Renders an :class:`apex_translators.base.ParsedMessage` back to an OAGIS
BOD. Outputs a fixed minimal envelope; a full XSD-aware emit is out of
scope for v1.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any

from apex_translators.base import EmitError, ParsedMessage


@dataclass
class OAGISEmitter:
    """OAGIS BOD emitter."""

    encoding: str = "utf-8"

    def emit(self, message: ParsedMessage) -> str:
        if message.format != "oagis":
            raise EmitError(
                f"OAGIS emitter requires format='oagis', got {message.format!r}"
            )
        verb = message.metadata.get("verb", "Sync")
        if not message.message_type:
            raise EmitError("OAGIS message_type is required (e.g., 'SyncItem')")

        root = ET.Element(message.message_type)

        # ApplicationArea
        app = ET.SubElement(root, "ApplicationArea")
        sender = ET.SubElement(app, "Sender")
        ET.SubElement(sender, "LogicalID").text = message.sender or ""
        ET.SubElement(app, "CreationDateTime").text = message.metadata.get(
            "creation_datetime", ""
        )
        ET.SubElement(app, "BODID").text = message.control_number or ""

        # DataArea
        data_area = ET.SubElement(root, "DataArea")
        ET.SubElement(data_area, verb)
        for seg in message.segments:
            child = ET.SubElement(data_area, seg.name)
            _dict_to_xml(child, seg.data)

        return ET.tostring(root, encoding="unicode")


def emit_oagis(message: ParsedMessage) -> str:
    """Convenience: emit an OAGIS BOD."""
    return OAGISEmitter().emit(message)


def _dict_to_xml(parent: ET.Element, data: Any) -> None:
    if not isinstance(data, dict):
        if isinstance(data, str):
            parent.text = data
        return
    for k, v in data.items():
        if k.startswith("@"):
            if k != "@type":
                parent.set(k[1:], str(v))
            continue
        if isinstance(v, list):
            for item in v:
                child = ET.SubElement(parent, k)
                _dict_to_xml(child, item)
        elif isinstance(v, dict):
            child = ET.SubElement(parent, k)
            _dict_to_xml(child, v)
        else:
            child = ET.SubElement(parent, k)
            if v not in (None, ""):
                child.text = str(v)
