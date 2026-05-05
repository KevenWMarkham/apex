"""J1939 PGN (Parameter Group Number) metadata + seed registry + loader hook."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class J1939PGN:
    """Metadata for one J1939 Parameter Group Number."""

    pgn: int
    acronym: str
    name: str
    default_priority: int
    length_bytes: int
    transmission_rate_ms: int | None = None
    spns: tuple[int, ...] = field(default_factory=tuple)


# Seed registry — ~10 widely-referenced PGNs.
SEED_PGNS: dict[int, J1939PGN] = {
    61444: J1939PGN(61444, "EEC1", "Electronic Engine Controller 1", 3, 8, 20,
                    (190, 513, 92)),
    65262: J1939PGN(65262, "ET1", "Engine Temperature 1", 6, 8, 1000,
                    (110, 174, 175, 52, 53)),
    65263: J1939PGN(65263, "EFL/P1", "Engine Fluid Level / Pressure 1", 6, 8, 500,
                    (94, 98, 100, 101, 22, 109)),
    65265: J1939PGN(65265, "CCVS1", "Cruise Control / Vehicle Speed 1", 6, 8, 100,
                    (84, 595, 596, 597)),
    65266: J1939PGN(65266, "LFE1", "Fuel Economy (Liquid) 1", 6, 8, 100,
                    (182, 183, 184)),
    65248: J1939PGN(65248, "VDHR", "High Resolution Vehicle Distance", 6, 8, 1000,
                    (917, 918)),
    65253: J1939PGN(65253, "HOURS", "Engine Hours / Revolutions", 6, 8, None,
                    (247, 249)),
    65279: J1939PGN(65279, "WFI", "Water in Fuel Indicator 1", 6, 8, 1000,
                    (97,)),
    61443: J1939PGN(61443, "EEC2", "Electronic Engine Controller 2", 3, 8, 50,
                    (91, 92, 558, 559)),
    65271: J1939PGN(65271, "VEP1", "Vehicle Electrical Power 1", 6, 8, 1000,
                    (158, 167, 168)),
}


def lookup_pgn(pgn: int, catalog: dict[int, J1939PGN] | None = None) -> J1939PGN | None:
    """Look up a PGN in the supplied catalog, falling back to the seed."""
    if catalog and pgn in catalog:
        return catalog[pgn]
    return SEED_PGNS.get(pgn)


def load_pgn_catalog(source: dict[int, J1939PGN]) -> dict[int, J1939PGN]:
    """Accept a tenant-supplied PGN catalog and return a merged dict."""
    merged = dict(SEED_PGNS)
    merged.update(source)
    return merged
