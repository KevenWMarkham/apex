"""OAGIS BOD parser — Sprint 23 Task 23.5.

Parses an OAGIS Business Object Document. The BOD root tag combines a Verb
with a Noun (e.g., ``ProcessItem``, ``SyncCarrier``). The parser populates
the message envelope from ``ApplicationArea`` and emits one segment per
top-level Noun child.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any

from apex_translators.base import (
    FORMAT_OAGIS,
    ParseError,
    ParsedMessage,
    Segment,
)


OAGIS_VERBS: tuple[str, ...] = (
    "Get", "Show", "Process", "Acknowledge",
    "Sync", "Confirm", "Notify", "Cancel", "Update", "Change",
)


@dataclass
class OAGISParser:
    """OAGIS BOD parser."""

    def parse(self, raw: str) -> ParsedMessage:
        if not raw or not raw.strip():
            raise ParseError("OAGIS payload is empty")
        try:
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            raise ParseError(f"OAGIS XML parse error: {exc}") from exc

        # Strip namespace from local tag
        local_root = root.tag.split("}")[-1]
        if not local_root:
            raise ParseError("OAGIS BOD has no root tag")

        # Decompose root: <Verb><Noun> e.g., 'ProcessItem' → verb=Process, noun=Item
        verb, noun = _split_verb_noun(local_root)
        if verb is None:
            raise ParseError(
                f"OAGIS BOD root {local_root!r} does not start with a recognized OAGIS verb"
            )

        msg = ParsedMessage(format=FORMAT_OAGIS, raw=raw)
        msg.message_type = local_root
        msg.metadata["verb"] = verb
        msg.metadata["noun"] = noun

        # ApplicationArea — sender/creation/BODID
        app = _find_local(root, "ApplicationArea")
        if app is not None:
            sender = _find_local(app, "Sender")
            if sender is not None:
                logical_id = _find_local(sender, "LogicalID")
                if logical_id is not None and logical_id.text:
                    msg.sender = logical_id.text.strip()
            creation = _find_local(app, "CreationDateTime")
            if creation is not None and creation.text:
                msg.metadata["creation_datetime"] = creation.text.strip()
            bod_id = _find_local(app, "BODID")
            if bod_id is not None and bod_id.text:
                msg.control_number = bod_id.text.strip()

        # DataArea — Verb element + 1..N Noun elements
        data_area = _find_local(root, "DataArea")
        if data_area is None:
            raise ParseError(
                f"OAGIS BOD {local_root!r} missing DataArea"
            )

        for child in list(data_area):
            local = child.tag.split("}")[-1]
            if local in OAGIS_VERBS:
                # Skip the inner <Verb/> — it carries action semantics, not noun data
                continue
            data = _xml_to_dict(child)
            data["@type"] = local
            msg.segments.append(Segment(name=local, data=data))

        return msg


def parse_oagis(raw: str) -> ParsedMessage:
    """Convenience: parse an OAGIS BOD."""
    return OAGISParser().parse(raw)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _split_verb_noun(tag: str) -> tuple[str | None, str]:
    """Split ``ProcessItem`` → (``Process``, ``Item``)."""
    for verb in sorted(OAGIS_VERBS, key=len, reverse=True):
        if tag.startswith(verb):
            noun = tag[len(verb) :]
            return verb, noun
    return None, tag


def _find_local(parent: ET.Element, local_name: str) -> ET.Element | None:
    """Find first child whose tag local-name matches ``local_name``."""
    for child in parent.iter():
        if child.tag.split("}")[-1] == local_name and child is not parent:
            return child
    return None


def _xml_to_dict(el: ET.Element) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for child in el:
        local = child.tag.split("}")[-1]
        if list(child):
            sub = _xml_to_dict(child)
        elif child.text and child.text.strip():
            sub = child.text.strip()
        else:
            sub = ""
        if local in out:
            existing = out[local]
            if isinstance(existing, list):
                existing.append(sub)
            else:
                out[local] = [existing, sub]
        else:
            out[local] = sub
    for k, v in el.attrib.items():
        out["@" + k] = v
    return out
