"""J1939 SPN (Signal Parameter Number) metadata + seed registry + loader hook.

The seed covers ~20 SPNs commonly referenced by APEX reference deployments.
Tenants supply the full catalog via :func:`load_spn_catalog`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class J1939SPN:
    """Metadata for one J1939 Signal Parameter Number."""

    spn: int
    name: str
    units: str
    resolution: float
    offset: float
    range_min: float
    range_max: float
    length_bits: int
    category: str = ""


# Seed registry — ~20 widely-referenced SPNs (public-knowledge subset).
SEED_SPNS: dict[int, J1939SPN] = {
    190: J1939SPN(190, "Engine Speed", "rpm", 0.125, 0.0, 0.0, 8031.875, 16, "engine"),
    84: J1939SPN(84, "Wheel-Based Vehicle Speed", "km/h", 0.00390625, 0.0, 0.0, 250.996, 16, "vehicle"),
    110: J1939SPN(110, "Engine Coolant Temperature", "degC", 1.0, -40.0, -40.0, 210.0, 8, "engine"),
    100: J1939SPN(100, "Engine Oil Pressure", "kPa", 4.0, 0.0, 0.0, 1000.0, 8, "engine"),
    98: J1939SPN(98, "Engine Oil Level", "percent", 0.4, 0.0, 0.0, 100.0, 8, "engine"),
    96: J1939SPN(96, "Fuel Level 1", "percent", 0.4, 0.0, 0.0, 100.0, 8, "fuel"),
    183: J1939SPN(183, "Engine Fuel Rate", "L/h", 0.05, 0.0, 0.0, 3212.75, 16, "fuel"),
    247: J1939SPN(247, "Engine Total Hours of Operation", "hr", 0.05, 0.0, 0.0, 210554060.75, 32, "engine"),
    245: J1939SPN(245, "Engine Total Distance", "km", 0.125, 0.0, 0.0, 526385151.9, 32, "vehicle"),
    102: J1939SPN(102, "Engine Intake Manifold #1 Pressure", "kPa", 2.0, 0.0, 0.0, 500.0, 8, "engine"),
    105: J1939SPN(105, "Engine Intake Manifold 1 Temperature", "degC", 1.0, -40.0, -40.0, 210.0, 8, "engine"),
    173: J1939SPN(173, "Engine Exhaust Gas Temperature", "degC", 0.03125, -273.0, -273.0, 1735.0, 16, "emissions"),
    91: J1939SPN(91, "Accelerator Pedal Position 1", "percent", 0.4, 0.0, 0.0, 100.0, 8, "driver"),
    92: J1939SPN(92, "Engine Percent Load At Current Speed", "percent", 1.0, 0.0, 0.0, 125.0, 8, "engine"),
    513: J1939SPN(513, "Actual Engine - Percent Torque", "percent", 1.0, -125.0, -125.0, 125.0, 8, "engine"),
    544: J1939SPN(544, "Engine Reference Torque", "Nm", 1.0, 0.0, 0.0, 64255.0, 16, "engine"),
    158: J1939SPN(158, "Battery Potential / Power Input 1", "V", 0.05, 0.0, 0.0, 3212.75, 16, "electrical"),
    168: J1939SPN(168, "Battery Potential (Voltage)", "V", 0.05, 0.0, 0.0, 3212.75, 16, "electrical"),
    1636: J1939SPN(1636, "Engine Intake Manifold 1 Air Temperature", "degC", 0.03125, -273.0, -273.0, 1735.0, 16, "engine"),
    975: J1939SPN(975, "Estimated Percent Fan Speed", "percent", 0.4, 0.0, 0.0, 100.0, 8, "cooling"),
}


def lookup_spn(spn: int, catalog: dict[int, J1939SPN] | None = None) -> J1939SPN | None:
    """Look up an SPN in the supplied catalog, falling back to the seed.

    Args:
        spn: The SPN number.
        catalog: An optional tenant-supplied catalog. When omitted, only the
            APEX seed is searched.
    """
    if catalog and spn in catalog:
        return catalog[spn]
    return SEED_SPNS.get(spn)


def load_spn_catalog(source: dict[int, J1939SPN]) -> dict[int, J1939SPN]:
    """Accept a tenant-supplied SPN catalog and return a merged dict.

    Tenant entries override seed entries on collision. Returns a new dict —
    the seed is not mutated.
    """
    merged = dict(SEED_SPNS)
    merged.update(source)
    return merged
