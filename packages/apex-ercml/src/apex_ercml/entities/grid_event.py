"""ERCML GridEvent entity — Pattern C over CIM EnergyEvent (IEC 61970)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class GridEventType(StrEnum):
    OUTAGE = "outage"
    FAULT = "fault"
    VOLTAGE_SAG = "voltage_sag"
    VOLTAGE_SWELL = "voltage_swell"
    FREQUENCY_DEVIATION = "frequency_deviation"
    EQUIPMENT_ALARM = "equipment_alarm"
    SCHEDULED_MAINTENANCE = "scheduled_maintenance"
    STORM = "storm"
    OTHER = "other"


class GridEvent(CanonicalEntity):
    """An operational event on the power network."""

    cim_mrid: str | None = Field(None, description="CIM EnergyEvent MRID when available.")
    event_type: GridEventType
    occurred_start: datetime
    occurred_end: datetime | None = None
    equipment_key: str | None = Field(
        None, description="FK → ERCML Asset.entity_id."
    )
    severity: int | None = Field(
        None, ge=1, le=5, description="1 = critical, 5 = informational."
    )
    description: str = ""
    customers_affected: int | None = Field(None, ge=0)
