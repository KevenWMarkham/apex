"""SAE J1939 ↔ AEMP 2.0 — Sprint 24 Task 24.5.

J1939 is the CAN-bus telematics protocol used inside heavy equipment;
AEMP 2.0 is the cross-OEM fleet telematics standard built on top of
J1939 (Caterpillar, Deere, Komatsu, etc. all emit AEMP-shaped JSON via
their telematics gateways).

This translator provides the **named-PGN mapping** for the most common
equipment-health and operational signals so cross-OEM fleet aggregation
works without bespoke per-vendor adapters.

Bidirectional. Round-trip ``aemp_to_j1939(j1939_to_aemp(x))`` preserves
the named PGN's `value`, `units`, and `timestamp` exactly; OEM-specific
extensions outside the named set are documented in ``LOSSY_CASES.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# AEMP 2.0 named event types
# ---------------------------------------------------------------------------


AEMP_EVENT_TYPES: tuple[str, ...] = (
    "EngineHours",
    "EngineSpeed",
    "EngineLoad",
    "FuelLevel",
    "FuelConsumption",
    "FuelRate",
    "DefLevel",
    "DistanceTraveled",
    "Location",
    "PayloadTotal",
    "EquipmentMode",
    "MalfunctionIndicator",
)


# ---------------------------------------------------------------------------
# J1939 PGN ↔ AEMP event-type mapping (Task 24.5.1)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PGNMapping:
    """Mapping between a J1939 PGN/SPN signal and an AEMP 2.0 event type."""

    pgn: int
    """Parameter Group Number."""

    spn: int
    """Suspect Parameter Number."""

    aemp_event: str
    """AEMP 2.0 event type name."""

    units: str
    """Standard units (units of measure for the value)."""

    description: str = ""


# Subset covering the AEMP 2.0 minimum-cross-OEM signal set. Real fleets
# carry hundreds of PGNs; AEMP standardizes the small set every OEM emits.
J1939_PGN_MAP: dict[int, PGNMapping] = {
    65253: PGNMapping(65253, 247,  "EngineHours",         "h",       "Engine total hours of operation"),
    61444: PGNMapping(61444, 190,  "EngineSpeed",         "rpm",     "Engine speed"),
    61443: PGNMapping(61443, 92,   "EngineLoad",          "%",       "Percent engine load at current speed"),
    65276: PGNMapping(65276, 96,   "FuelLevel",           "%",       "Fuel level (tank %)"),
    65257: PGNMapping(65257, 250,  "FuelConsumption",     "L",       "Total fuel used"),
    65266: PGNMapping(65266, 183,  "FuelRate",            "L/h",     "Engine fuel rate"),
    65110: PGNMapping(65110, 1761, "DefLevel",            "%",       "Diesel exhaust fluid level"),
    65248: PGNMapping(65248, 245,  "DistanceTraveled",    "km",      "Total vehicle distance"),
    65267: PGNMapping(65267, 584,  "Location",            "deg",     "Vehicle position (lat/lon, decimal degrees)"),
    65093: PGNMapping(65093, 1804, "PayloadTotal",        "t",       "Total payload"),
    61441: PGNMapping(61441, 970,  "EquipmentMode",       "code",    "Equipment operating mode"),
    65226: PGNMapping(65226, 1213, "MalfunctionIndicator","code",    "Active diagnostic trouble code"),
}


# Inverse — by AEMP event type → PGN
AEMP_PGN_MAP: dict[str, PGNMapping] = {m.aemp_event: m for m in J1939_PGN_MAP.values()}


# ---------------------------------------------------------------------------
# Containers
# ---------------------------------------------------------------------------


@dataclass
class J1939Frame:
    """One J1939 CAN frame: PGN/SPN + value + timestamp + source address."""

    pgn: int
    spn: int
    value: float | int | str
    units: str = ""
    source_address: int = 0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AEMPEvent:
    """One AEMP 2.0 telematics event."""

    event_type: str
    value: float | int | str
    units: str
    equipment_id: str
    """OEM-assigned equipment serial / asset id."""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    oem: str = ""
    extras: dict[str, Any] = field(default_factory=dict)
    """OEM-specific extension fields surfaced as metadata; documented as
    lossy in ``LOSSY_CASES.md``."""


# ---------------------------------------------------------------------------
# Translators
# ---------------------------------------------------------------------------


def j1939_to_aemp(
    frame: J1939Frame,
    *,
    equipment_id: str,
    oem: str = "",
) -> AEMPEvent:
    """Translate a J1939 CAN frame to an AEMP 2.0 event.

    Raises:
        KeyError: if the frame's PGN is not in ``J1939_PGN_MAP``.
    """
    mapping = J1939_PGN_MAP.get(frame.pgn)
    if mapping is None:
        raise KeyError(
            f"J1939 PGN {frame.pgn} has no AEMP 2.0 mapping. "
            f"Extend J1939_PGN_MAP if this is a named cross-OEM signal. "
            f"Known PGNs: {sorted(J1939_PGN_MAP)}"
        )
    return AEMPEvent(
        event_type=mapping.aemp_event,
        value=frame.value,
        units=mapping.units,
        equipment_id=equipment_id,
        timestamp=frame.timestamp,
        oem=oem,
        extras={
            "_source_pgn": frame.pgn,
            "_source_spn": frame.spn,
            "_source_address": frame.source_address,
        },
    )


def aemp_to_j1939(event: AEMPEvent) -> J1939Frame:
    """Translate an AEMP 2.0 event back to a J1939 CAN frame.

    Raises:
        KeyError: if the event type is not in ``AEMP_PGN_MAP``.
    """
    mapping = AEMP_PGN_MAP.get(event.event_type)
    if mapping is None:
        raise KeyError(
            f"AEMP event type {event.event_type!r} has no J1939 mapping. "
            f"Known: {sorted(AEMP_PGN_MAP)}"
        )
    extras = event.extras or {}
    return J1939Frame(
        pgn=mapping.pgn,
        spn=mapping.spn,
        value=event.value,
        units=event.units,
        source_address=int(extras.get("_source_address", 0)),
        timestamp=event.timestamp,
    )
