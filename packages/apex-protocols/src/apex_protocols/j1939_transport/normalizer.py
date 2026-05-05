"""J1939 CAN-bus frame normalizer — Sprint 25 Task 25.3.1.

Takes raw CAN frames (29-bit identifier per SAE J1939) and decodes them
into SPN-addressed values usable by upstream agents. Each frame's
arbitration ID encodes:

- Priority (3 bits)
- EDP/DP/Reserved (1 bit)
- DP (1 bit)
- PGN bits (depending on PDU format)
- Source Address (8 bits)

We support the common case (PDU1 + PDU2) sufficient for the AEMP-2.0
cross-OEM signal set. SPN extraction within the 8-byte data payload
uses the per-PGN signal layouts from the
:mod:`apex_protocols.j1939_transport.spn_layouts` table.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable

from apex_protocols.base import ProtocolError


# ---------------------------------------------------------------------------
# Frame
# ---------------------------------------------------------------------------


@dataclass
class CANFrame:
    """One raw 29-bit-id CAN frame as captured from a J1939 bus."""

    arbitration_id: int
    """29-bit J1939 identifier (priority + PGN + source address)."""

    data: bytes
    """Up to 8 data bytes."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class DecodedSignal:
    """One SPN-addressed value extracted from a CAN frame's data payload."""

    pgn: int
    spn: int
    source_address: int
    value: float | int
    units: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Per-PGN SPN layouts (subset matching the AEMP cross-OEM signal set)
# ---------------------------------------------------------------------------


# (start_byte, length_bytes, scale, offset, units)
@dataclass(frozen=True)
class SPNLayout:
    """Layout of one SPN within a PGN's data payload."""

    spn: int
    start_byte: int
    """0-indexed byte offset within the 8-byte data payload."""
    length_bytes: int
    """1, 2, or 4."""
    scale: float
    offset: float
    units: str
    description: str = ""


SPN_LAYOUTS: dict[int, list[SPNLayout]] = {
    # Engine Hours, Revolutions (PGN 65253 / 0xFEE5)
    65253: [
        SPNLayout(spn=247, start_byte=0, length_bytes=4, scale=0.05, offset=0.0, units="h",
                  description="Engine Total Hours of Operation"),
        SPNLayout(spn=249, start_byte=4, length_bytes=4, scale=1000.0, offset=0.0, units="rev",
                  description="Engine Total Revolutions"),
    ],
    # Electronic Engine Controller 1 (PGN 61444 / 0xF004)
    61444: [
        SPNLayout(spn=190, start_byte=3, length_bytes=2, scale=0.125, offset=0.0, units="rpm",
                  description="Engine Speed"),
        SPNLayout(spn=512, start_byte=5, length_bytes=1, scale=1.0, offset=-125.0, units="%",
                  description="Driver's Demand Engine Percent Torque"),
    ],
    # Electronic Engine Controller 2 (PGN 61443 / 0xF003)
    61443: [
        SPNLayout(spn=92, start_byte=2, length_bytes=1, scale=1.0, offset=0.0, units="%",
                  description="Engine Percent Load at Current Speed"),
    ],
    # Dash Display 1 — Fuel Level (PGN 65276 / 0xFEFC)
    65276: [
        SPNLayout(spn=96, start_byte=1, length_bytes=1, scale=0.4, offset=0.0, units="%",
                  description="Fuel Level"),
    ],
    # Vehicle Distance (PGN 65248 / 0xFEE0)
    65248: [
        SPNLayout(spn=245, start_byte=0, length_bytes=4, scale=0.005, offset=0.0, units="km",
                  description="Trip Distance"),
        SPNLayout(spn=244, start_byte=4, length_bytes=4, scale=0.005, offset=0.0, units="km",
                  description="Total Vehicle Distance"),
    ],
    # Fuel Consumption (PGN 65257 / 0xFEE9)
    65257: [
        SPNLayout(spn=250, start_byte=4, length_bytes=4, scale=0.5, offset=0.0, units="L",
                  description="Engine Total Fuel Used"),
        SPNLayout(spn=182, start_byte=0, length_bytes=4, scale=0.5, offset=0.0, units="L",
                  description="Engine Trip Fuel"),
    ],
    # Fuel Economy (PGN 65266 / 0xFEF2)
    65266: [
        SPNLayout(spn=183, start_byte=0, length_bytes=2, scale=0.05, offset=0.0, units="L/h",
                  description="Engine Fuel Rate"),
        SPNLayout(spn=184, start_byte=2, length_bytes=2, scale=1.0/256.0, offset=0.0, units="km/L",
                  description="Engine Instantaneous Fuel Economy"),
    ],
}


# ---------------------------------------------------------------------------
# Arbitration-ID decode
# ---------------------------------------------------------------------------


def _arb_id_to_pgn_sa(arb_id: int) -> tuple[int, int]:
    """Decode J1939 29-bit arbitration ID → (PGN, Source Address).

    PDU Format (PF) is bits 16-23. PDU Specific (PS) is bits 8-15.
    Source Address is bits 0-7. Data Page (DP) is bit 24.
    For PF < 240 (PDU1), the PGN is `DP|PF|0x00`; PS holds the destination
    address. For PF >= 240 (PDU2), the PGN is `DP|PF|PS`.
    """
    sa = arb_id & 0xFF
    ps = (arb_id >> 8) & 0xFF
    pf = (arb_id >> 16) & 0xFF
    dp = (arb_id >> 24) & 0x01
    if pf < 240:
        pgn = (dp << 16) | (pf << 8) | 0x00
    else:
        pgn = (dp << 16) | (pf << 8) | ps
    return pgn, sa


# ---------------------------------------------------------------------------
# Decoder
# ---------------------------------------------------------------------------


def decode_frame(frame: CANFrame) -> list[DecodedSignal]:
    """Decode one CAN frame into all known SPN signals."""
    pgn, sa = _arb_id_to_pgn_sa(frame.arbitration_id)
    layouts = SPN_LAYOUTS.get(pgn, [])
    out: list[DecodedSignal] = []
    for layout in layouts:
        end = layout.start_byte + layout.length_bytes
        if end > len(frame.data):
            continue  # Frame too short for this SPN
        raw = frame.data[layout.start_byte:end]
        # J1939 multi-byte values are little-endian
        raw_int = int.from_bytes(raw, byteorder="little", signed=False)
        # All-bits-set means "not available"; skip
        max_value = (1 << (layout.length_bytes * 8)) - 1
        if raw_int == max_value:
            continue
        scaled = raw_int * layout.scale + layout.offset
        out.append(
            DecodedSignal(
                pgn=pgn,
                spn=layout.spn,
                source_address=sa,
                value=scaled,
                units=layout.units,
                timestamp=frame.timestamp,
            )
        )
    return out


class J1939Normalizer:
    """Multi-frame normalizer.

    Apply :func:`decode_frame` to each frame; expose a generator that
    flattens all decoded signals across an iterable of frames.
    """

    def __init__(self) -> None:
        self._frame_count = 0
        self._signal_count = 0

    def normalize(self, frames: Iterable[CANFrame]) -> Iterable[DecodedSignal]:
        for frame in frames:
            self._frame_count += 1
            for sig in decode_frame(frame):
                self._signal_count += 1
                yield sig

    @property
    def frames_processed(self) -> int:
        return self._frame_count

    @property
    def signals_emitted(self) -> int:
        return self._signal_count

    def known_pgns(self) -> set[int]:
        return set(SPN_LAYOUTS)
