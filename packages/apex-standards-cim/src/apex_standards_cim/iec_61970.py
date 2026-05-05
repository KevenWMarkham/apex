"""CIM IEC 61970 — power-system core classes (APEX subset)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from apex_standards_cim.shared import MRID, DateTimeInterval

_CIM_CONFIG = ConfigDict(extra="forbid")


class CimLocation(BaseModel):
    """A spatial location of a CIM-modelled asset."""

    model_config = _CIM_CONFIG
    m_rid: MRID
    name: str | None = None
    main_address: str | None = None
    latitude: float | None = Field(None, ge=-90.0, le=90.0)
    longitude: float | None = Field(None, ge=-180.0, le=180.0)


class CimAsset(BaseModel):
    """CIM Asset — a physical or logical asset tracked in the power network."""

    model_config = _CIM_CONFIG
    m_rid: MRID
    name: str | None = None
    description: str = ""
    asset_type: str | None = None
    location_mrid: MRID | None = Field(None, description="FK → CimLocation.m_rid.")
    in_service_date: datetime | None = None
    lifecycle_state: str | None = None


class CimEquipment(BaseModel):
    """CIM Equipment — a piece of network equipment (transformer, line, breaker, ...)."""

    model_config = _CIM_CONFIG
    m_rid: MRID
    name: str | None = None
    description: str = ""
    in_service: bool = True
    normally_in_service: bool = True
    equipment_container_mrid: MRID | None = Field(None, description="Substation / line / bay container.")


class CimEnergyEvent(BaseModel):
    """CIM EnergyEvent — an operational event on the power system (fault, sag, outage)."""

    model_config = _CIM_CONFIG
    m_rid: MRID
    event_type: str = Field(..., description="e.g. 'outage', 'fault', 'voltage_sag'.")
    occurred: DateTimeInterval
    equipment_mrid: MRID | None = Field(None, description="FK → CimEquipment.m_rid.")
    description: str = ""
    severity: int | None = Field(None, ge=1, le=5, description="1 = critical, 5 = informational.")
