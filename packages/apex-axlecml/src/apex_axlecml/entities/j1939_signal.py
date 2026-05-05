"""AXLECML J1939Signal entity — decoded vehicle-bus signal reference."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class J1939Signal(CanonicalEntity):
    """A decoded SAE J1939 signal reading."""

    spn: int = Field(..., ge=0, description="SAE J1939 Suspect Parameter Number.")
    pgn: int | None = Field(None, ge=0, description="SAE J1939 Parameter Group Number.")
    signal_name: str
    value: Decimal
    unit: str = ""
    equipment_key: str | None = Field(
        None, description="FK → AXLECML Equipment.entity_id."
    )
    captured_at: datetime
    raw_can_frame: str | None = Field(
        None, description="Hex-encoded CAN frame (for audit / replay)."
    )
