"""IEC 61850 SCD (Substation Configuration Description) parser — Sprint 25 §25.2.1.

SCD files are XML documents conforming to IEC 61850-6. They describe a
substation's IEDs (Intelligent Electronic Devices), Logical Devices,
Logical Nodes, Data Objects, and the GOOSE / Sampled-Value publication
patterns linking them.

This parser extracts the address-space hierarchy needed to build an APEX
:class:`AddressSpaceMapping` plus a metadata-only summary of the GOOSE /
SV publications. Per Sprint 25 §25.2.3, raw GOOSE / SV frames are NOT
ingested into APEX — they live entirely in the OT domain.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from apex_protocols.base import AddressSpaceError


NS_61850_SCL = "http://www.iec.ch/61850/2003/SCL"


@dataclass
class GOOSEControlBlock:
    """One GOOSE control block discovered in an SCD."""

    name: str
    app_id: str
    multicast_mac: str = ""
    confRev: int = 1
    dataset: str = ""


@dataclass
class SVControlBlock:
    """One Sampled-Value control block."""

    name: str
    app_id: str
    multicast_mac: str = ""
    smp_rate: int = 0
    """Samples per second."""

    confRev: int = 1
    dataset: str = ""


@dataclass
class LogicalNode:
    """One IEC 61850 Logical Node within a Logical Device."""

    ln_class: str
    """E.g., ``MMXU``, ``XCBR``, ``XSWI``, ``ZCAP``."""

    inst: str
    """Instance number/name."""

    ln_type: str = ""
    prefix: str = ""

    @property
    def reference(self) -> str:
        """Canonical LN reference, e.g., ``CTRL/XCBR1``."""
        return f"{self.prefix}{self.ln_class}{self.inst}"


@dataclass
class LogicalDevice:
    """One Logical Device (LD) inside an IED."""

    inst: str
    logical_nodes: list[LogicalNode] = field(default_factory=list)
    goose_blocks: list[GOOSEControlBlock] = field(default_factory=list)
    sv_blocks: list[SVControlBlock] = field(default_factory=list)


@dataclass
class IED:
    """One IED parsed from an SCD."""

    name: str
    manufacturer: str = ""
    type_name: str = ""
    config_version: str = ""
    logical_devices: list[LogicalDevice] = field(default_factory=list)


@dataclass
class SCDDocument:
    """Parsed SCD top-level document."""

    file_revision: str = ""
    history: list[str] = field(default_factory=list)
    ieds: list[IED] = field(default_factory=list)

    def all_logical_nodes(self) -> list[LogicalNode]:
        out: list[LogicalNode] = []
        for ied in self.ieds:
            for ld in ied.logical_devices:
                out.extend(ld.logical_nodes)
        return out

    def all_goose_blocks(self) -> list[GOOSEControlBlock]:
        out: list[GOOSEControlBlock] = []
        for ied in self.ieds:
            for ld in ied.logical_devices:
                out.extend(ld.goose_blocks)
        return out

    def all_sv_blocks(self) -> list[SVControlBlock]:
        out: list[SVControlBlock] = []
        for ied in self.ieds:
            for ld in ied.logical_devices:
                out.extend(ld.sv_blocks)
        return out


def parse_scd(raw: str) -> SCDDocument:
    """Parse an IEC 61850 SCD XML document."""
    if not raw or not raw.strip():
        raise AddressSpaceError("SCD payload is empty")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise AddressSpaceError(f"SCD XML parse error: {exc}") from exc

    if not root.tag.endswith("SCL"):
        raise AddressSpaceError(
            f"SCD root must be SCL, got {root.tag!r}"
        )

    doc = SCDDocument()

    header = _find_local(root, "Header")
    if header is not None:
        doc.file_revision = header.get("revision", "")
        history = _find_local(header, "History")
        if history is not None:
            doc.history = [
                hi.get("what", "")
                for hi in history
                if hi.tag.split("}")[-1] == "Hitem"
            ]

    for ied_el in [c for c in root if c.tag.split("}")[-1] == "IED"]:
        ied = IED(
            name=ied_el.get("name", ""),
            manufacturer=ied_el.get("manufacturer", ""),
            type_name=ied_el.get("type", ""),
            config_version=ied_el.get("configVersion", ""),
        )
        services = _find_local(ied_el, "Services")  # noqa: F841 — discoverable; not used
        access_point = _find_local(ied_el, "AccessPoint")
        if access_point is not None:
            server = _find_local(access_point, "Server")
            if server is not None:
                for ld_el in [c for c in server if c.tag.split("}")[-1] == "LDevice"]:
                    ld = LogicalDevice(inst=ld_el.get("inst", ""))
                    # Logical nodes
                    for ln_el in [c for c in ld_el if c.tag.split("}")[-1] in ("LN", "LN0")]:
                        ld.logical_nodes.append(
                            LogicalNode(
                                ln_class=ln_el.get("lnClass", "LLN0"),
                                inst=ln_el.get("inst", "1"),
                                ln_type=ln_el.get("lnType", ""),
                                prefix=ln_el.get("prefix", ""),
                            )
                        )
                        # GOOSE / SV control blocks live as children of LN0
                        for gse in [c for c in ln_el if c.tag.split("}")[-1] == "GSEControl"]:
                            ld.goose_blocks.append(
                                GOOSEControlBlock(
                                    name=gse.get("name", ""),
                                    app_id=gse.get("appID", ""),
                                    confRev=int(gse.get("confRev", "1")),
                                    dataset=gse.get("datSet", ""),
                                )
                            )
                        for sv in [c for c in ln_el if c.tag.split("}")[-1] == "SampledValueControl"]:
                            ld.sv_blocks.append(
                                SVControlBlock(
                                    name=sv.get("name", ""),
                                    app_id=sv.get("appID", ""),
                                    confRev=int(sv.get("confRev", "1")),
                                    smp_rate=int(sv.get("smpRate", "0")),
                                    dataset=sv.get("datSet", ""),
                                )
                            )
                    ied.logical_devices.append(ld)
        doc.ieds.append(ied)

    return doc


def _find_local(parent: ET.Element, local_name: str) -> ET.Element | None:
    """Find first DIRECT-CHILD element with matching local name."""
    for child in parent:
        if child.tag.split("}")[-1] == local_name:
            return child
    return None
