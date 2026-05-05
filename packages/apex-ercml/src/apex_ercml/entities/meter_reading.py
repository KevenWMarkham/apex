"""ERCML MeterReading entity — Pattern C over CIM Reading (IEC 61968)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class ReadingQuality(StrEnum):
    MEASURED = "measured"
    ESTIMATED = "estimated"
    SUBSTITUTED = "substituted"
    SUSPECT = "suspect"
    REJECTED = "rejected"


class MeterReading(CanonicalEntity):
    """A single meter value at a point in time."""

    meter_key: str = Field(..., description="FK → ERCML Meter.entity_id.")
    cim_mrid: str | None = Field(None, description="CIM Reading MRID when available.")
    timestamp: datetime
    value: Decimal
    unit: str = Field("kWh", description="UCUM / IEC 61970 unit symbol.")
    quality: ReadingQuality = ReadingQuality.MEASURED
    channel: str | None = Field(
        None, description="Meter channel (e.g. 'real_energy', 'demand')."
    )
