"""OPC UA NodeSet XML parser — Sprint 25 Task 25.1.1 / 25.1.2.

OPC UA address spaces ship as NodeSet2.xml files (companion specs
publish them; tenants export them from their servers via
`UaExpert` / `UA Configuration Tool`). This parser walks the NodeSet
XML and extracts the `UAVariable` and `UAObject` nodes that an APEX
adapter mapping references.

We do NOT try to model the full UA information model — the parser is
narrow on purpose. Adapters care about NodeId + BrowseName + DataType
+ DisplayName so the address-space mapping config can validate that
every mapped node actually exists in the server's address space.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from apex_protocols.base import AddressSpaceError


NS_NODESET = "http://opcfoundation.org/UA/2011/03/UANodeSet.xsd"


class NodeSetParseError(AddressSpaceError):
    """Raised when an OPC UA NodeSet XML cannot be parsed."""


@dataclass
class NodeSetEntry:
    """One UAVariable or UAObject extracted from a NodeSet XML."""

    node_id: str
    browse_name: str
    display_name: str
    node_class: str
    """``UAVariable``, ``UAObject``, ``UAMethod``, etc."""

    data_type: str = ""
    """OPC UA DataType node id reference (e.g., ``i=10`` for Float)."""

    parent_node_id: str = ""
    """Resolved from `<References>` with HasComponent / HasProperty types."""

    references: list[str] = field(default_factory=list)


def parse_nodeset(raw: str) -> list[NodeSetEntry]:
    """Parse an OPC UA NodeSet2 XML and return UA nodes."""
    if not raw or not raw.strip():
        raise NodeSetParseError("NodeSet XML payload is empty")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise NodeSetParseError(f"NodeSet XML parse error: {exc}") from exc

    if not root.tag.endswith("UANodeSet"):
        raise NodeSetParseError(
            f"NodeSet root must be UANodeSet, got {root.tag!r}"
        )

    entries: list[NodeSetEntry] = []
    for el in root:
        local = el.tag.split("}")[-1]
        if local not in ("UAVariable", "UAObject", "UAMethod"):
            continue
        node_id = el.get("NodeId", "")
        if not node_id:
            continue
        entry = NodeSetEntry(
            node_id=node_id,
            browse_name=el.get("BrowseName", ""),
            display_name=_find_display_name(el),
            node_class=local,
            data_type=el.get("DataType", ""),
        )
        # Pull HasComponent / HasProperty references (parent linkage)
        for ref_root in el:
            if ref_root.tag.split("}")[-1] != "References":
                continue
            for ref in ref_root:
                ref_type = ref.get("ReferenceType", "")
                is_forward = ref.get("IsForward", "true").lower() != "false"
                target = (ref.text or "").strip()
                if not target:
                    continue
                # An *inverse* HasComponent / HasProperty edge points back
                # to the parent that contains this node.
                if ref_type in ("HasComponent", "HasProperty") and not is_forward:
                    entry.parent_node_id = target
                entry.references.append(f"{ref_type}{'->' if is_forward else '<-'}{target}")
        entries.append(entry)

    return entries


def _find_display_name(el: ET.Element) -> str:
    for child in el:
        if child.tag.split("}")[-1] == "DisplayName":
            return (child.text or "").strip()
    return ""
