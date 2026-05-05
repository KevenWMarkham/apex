"""CIM (IEC 61968/61970) ↔ ISO 15926 — Sprint 24 Task 24.4.

CIM models the electric-utility domain (substations, feeders, conducting
equipment); ISO 15926 models the process-industry domain (pipes, vessels,
instruments). Both share an underlying asset/topology pattern, so this
translator provides a **named-equipment-class mapping** that bridges the
common subset.

The mapping is intentionally narrow — it covers the equipment classes
that appear in cross-industry asset programmes (utility-scale plants
with mixed electrical + mechanical assets). Equipment classes outside
the named set raise :class:`KeyError` from the explicit map; callers
extend ``CIM_ISO_EQUIPMENT_MAP`` as new mappings are needed.

Bidirectional. Round-trip ``iso15926_to_cim(cim_to_iso15926(x)) == x`` for
all entries in ``CIM_ISO_EQUIPMENT_MAP``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Named equipment-class mapping (Task 24.4.2)
# ---------------------------------------------------------------------------


# CIM equipment class → ISO 15926 reference-data-library class
CIM_ISO_EQUIPMENT_MAP: dict[str, str] = {
    # CIM electrical-grid asset → ISO 15926 RDL equivalent
    "Asset":                "PHYSICAL_OBJECT",
    "ConductingEquipment":  "ELECTRIC_CONDUCTOR",
    "Substation":           "ELECTRICAL_SUBSTATION",
    "Bay":                  "FUNCTIONAL_LOCATION",
    "PowerTransformer":     "POWER_TRANSFORMER",
    "Breaker":              "CIRCUIT_BREAKER",
    "Disconnector":         "DISCONNECTOR_SWITCH",
    "Feeder":               "DISTRIBUTION_FEEDER",
    "GeneratingUnit":       "GENERATING_UNIT",
    "Switch":               "ELECTRICAL_SWITCH",
    "Terminal":             "ELECTRICAL_TERMINAL",
    "EnergyConsumer":       "ELECTRIC_LOAD",
    "ACLineSegment":        "OVERHEAD_LINE_SEGMENT",
}


# Inverse — built once, frozen at import
ISO_CIM_EQUIPMENT_MAP: dict[str, str] = {v: k for k, v in CIM_ISO_EQUIPMENT_MAP.items()}


# ---------------------------------------------------------------------------
# Container classes
# ---------------------------------------------------------------------------


@dataclass
class CIMAsset:
    """A CIM asset (61968/61970-flavored)."""

    cim_class: str
    """CIM class name, e.g., ``Substation``, ``PowerTransformer``."""

    mrid: str
    """Master resource id (CIM RDF identifier)."""

    name: str = ""
    description: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)
    """Other CIM-typed attributes — passed through to ISO 15926 ``properties``."""


@dataclass
class ISO15926Asset:
    """An ISO 15926 asset (Reference Data Library-classified)."""

    rdl_class: str
    """ISO 15926 RDL class name, e.g., ``ELECTRICAL_SUBSTATION``."""

    object_id: str
    """ISO 15926 object identifier (typically a URI fragment)."""

    name: str = ""
    description: str = ""
    properties: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Translators
# ---------------------------------------------------------------------------


def cim_to_iso15926(asset: CIMAsset) -> ISO15926Asset:
    """Translate a CIM asset to an ISO 15926 asset."""
    if asset.cim_class not in CIM_ISO_EQUIPMENT_MAP:
        raise KeyError(
            f"CIM class {asset.cim_class!r} has no ISO 15926 mapping. "
            f"Extend CIM_ISO_EQUIPMENT_MAP if this is a real equipment class. "
            f"Known: {sorted(CIM_ISO_EQUIPMENT_MAP)}"
        )
    return ISO15926Asset(
        rdl_class=CIM_ISO_EQUIPMENT_MAP[asset.cim_class],
        object_id=asset.mrid,
        name=asset.name,
        description=asset.description,
        properties={"_cim_class": asset.cim_class, **asset.attributes},
    )


def iso15926_to_cim(asset: ISO15926Asset) -> CIMAsset:
    """Translate an ISO 15926 asset to a CIM asset."""
    if asset.rdl_class not in ISO_CIM_EQUIPMENT_MAP:
        raise KeyError(
            f"ISO 15926 class {asset.rdl_class!r} has no CIM mapping. "
            f"Extend CIM_ISO_EQUIPMENT_MAP if this is a real equipment class. "
            f"Known: {sorted(ISO_CIM_EQUIPMENT_MAP)}"
        )
    cim_class = ISO_CIM_EQUIPMENT_MAP[asset.rdl_class]
    # Drop the round-trip marker from attributes
    attrs = {k: v for k, v in asset.properties.items() if k != "_cim_class"}
    return CIMAsset(
        cim_class=cim_class,
        mrid=asset.object_id,
        name=asset.name,
        description=asset.description,
        attributes=attrs,
    )
