"""J1939 smoke-test dataset — Sprint 25 §25.3.

Synthetic CAN frame capture covering the AEMP-2.0-aligned signal set.
Each entry is a (arbitration_id, data_bytes) pair the J1939 normalizer
can decode.

Arbitration ID layout (29-bit): priority(3) | EDP+DP(2) | PF(8) | PS(8) | SA(8)
For PF >= 240, PGN = (DP << 16) | (PF << 8) | PS.

Source address 0x00 = Engine #1; data bytes are little-endian per J1939.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


def _arb(priority: int, pgn: int, sa: int) -> int:
    """Build a 29-bit arbitration ID."""
    pf = (pgn >> 8) & 0xFF
    if pf >= 240:
        ps = pgn & 0xFF
    else:
        ps = 0  # destination 0 (broadcast); real busses set this
    dp = (pgn >> 16) & 0x01
    return ((priority & 0x07) << 26) | (dp << 24) | (pf << 16) | (ps << 8) | (sa & 0xFF)


_BASE_TS = datetime(2025, 6, 30, 14, 30, tzinfo=timezone.utc)


# (arbitration_id, data_bytes, offset_seconds_from_base)
J1939_FRAME_CAPTURE: list[tuple[int, bytes, float]] = [
    # PGN 65253 (0xFEE5) — engine hours = 1234.5h (raw 24690, scale 0.05)
    # 24690 = 0x6072 LE -> 72 60 00 00, then 4 zeros for revolutions
    (_arb(6, 65253, 0x00), bytes([0x72, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]), 0.0),
    # PGN 61444 (0xF004) — engine speed 1800 rpm (raw = 14400, scale 0.125)
    # 14400 = 0x3840 LE -> 40 38; lives at start_byte=3
    (_arb(3, 61444, 0x00), bytes([0xFF, 0xFF, 0xFF, 0x40, 0x38, 0x80, 0xFF, 0xFF]), 0.05),
    # PGN 61443 (0xF003) — engine load 75% (raw 75)
    (_arb(3, 61443, 0x00), bytes([0xFF, 0xFF, 0x4B, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]), 0.10),
    # PGN 65276 (0xFEFC) — fuel level 78% (raw = 195, scale 0.4)
    (_arb(6, 65276, 0x00), bytes([0xFF, 0xC3, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]), 0.20),
    # PGN 65248 (0xFEE0) — total distance 5000 km (raw 1_000_000, scale 0.005)
    # 1_000_000 = 0x000F4240 LE -> 40 42 0F 00; lives at byte 4..8
    (_arb(6, 65248, 0x00), bytes([0x00, 0x00, 0x00, 0x00, 0x40, 0x42, 0x0F, 0x00]), 0.30),
    # PGN 65257 (0xFEE9) — engine total fuel 2000 L (raw 4000, scale 0.5)
    # 4000 = 0x0FA0 LE -> A0 0F 00 00; lives at byte 4..8
    (_arb(6, 65257, 0x00), bytes([0x00, 0x00, 0x00, 0x00, 0xA0, 0x0F, 0x00, 0x00]), 0.40),
    # PGN 65266 (0xFEF2) — engine fuel rate 12 L/h (raw 240, scale 0.05)
    # 240 = 0x00F0 LE -> F0 00; lives at byte 0..2
    (_arb(2, 65266, 0x00), bytes([0xF0, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]), 0.50),
    # Burst of engine-speed frames within the throttle window —
    # used to verify the throttler drops in-window samples
    (_arb(3, 61444, 0x00), bytes([0xFF, 0xFF, 0xFF, 0x40, 0x38, 0x80, 0xFF, 0xFF]), 0.55),
    (_arb(3, 61444, 0x00), bytes([0xFF, 0xFF, 0xFF, 0x40, 0x38, 0x80, 0xFF, 0xFF]), 0.60),
]


def frames_with_timestamps():
    """Yield (arbitration_id, data, timestamp) tuples for the dataset."""
    for arb_id, data, offset in J1939_FRAME_CAPTURE:
        yield arb_id, data, _BASE_TS + timedelta(seconds=offset)
