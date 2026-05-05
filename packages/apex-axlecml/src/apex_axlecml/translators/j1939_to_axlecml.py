"""J1939 → AXLECML translators."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from apex_standards_j1939 import (
    CanFrame,
    J1939SPN,
    lookup_spn,
)

from apex_axlecml.entities import J1939Signal


def _envelope(*, entity_id: str, event_ts: datetime, source_system: str = "j1939") -> dict[str, Any]:
    return {
        "event_id": uuid4(),
        "event_ts": event_ts,
        "entity_id": entity_id,
        "source_system": source_system,
        "source_system_ts": datetime.now(UTC),
    }


def j1939_signal_from_frame(
    frame: CanFrame,
    *,
    spn: int,
    value: Decimal,
    equipment_key: str | None = None,
    source_system: str = "j1939",
    catalog: dict[int, J1939SPN] | None = None,
) -> J1939Signal:
    """Assemble an AXLECML J1939Signal from a decoded CAN frame + SPN.

    The real decoder (Sprint 15 telematics adapter) does the raw-bytes →
    ``value`` conversion using SPN metadata (resolution, offset, length_bits);
    this translator assumes the caller has already produced ``value`` and
    supplies structure + metadata lookup.
    """
    spn_meta = lookup_spn(spn, catalog=catalog)
    name = spn_meta.name if spn_meta else f"SPN-{spn}"
    unit = spn_meta.units if spn_meta else ""
    captured_at = frame.timestamp or datetime.now(UTC)

    return J1939Signal(
        **_envelope(
            entity_id=f"j1939_signal:{spn}:{captured_at.isoformat()}",
            event_ts=captured_at,
            source_system=source_system,
        ),
        spn=spn,
        pgn=frame.pgn,
        signal_name=name,
        value=value,
        unit=unit,
        equipment_key=equipment_key,
        captured_at=captured_at,
        raw_can_frame=frame.data.hex() if frame.data else None,
    )  # type: ignore[arg-type]
