"""CAN 2.0B extended frame shape used to carry J1939 PDUs.

This is the canonical payload shape the Sprint 15 telematics adapters emit;
APEX canonical entities in AXLE / ICE consume ``CanFrame`` via the
``translators/j1939_to_*.py`` modules (built in those Practice packages).
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CanFrame(BaseModel):
    """A single J1939 CAN 2.0B extended frame."""

    model_config = ConfigDict(extra="forbid")

    pgn: int = Field(..., ge=0, le=0x3FFFF, description="Parameter Group Number.")
    source_address: int = Field(..., ge=0, le=255, description="Source ECU address.")
    priority: int = Field(6, ge=0, le=7, description="CAN priority (0 = highest).")
    data: bytes = Field(..., min_length=0, max_length=8, description="0-8 bytes of payload.")
    timestamp: datetime | None = Field(None, description="Capture timestamp.")

    @property
    def can_id(self) -> int:
        """The 29-bit extended CAN identifier assembled from the header fields."""
        return (self.priority << 26) | ((self.pgn & 0x3FFFF) << 8) | (self.source_address & 0xFF)
