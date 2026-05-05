"""CIM IEC 61968 — utility-operations classes (APEX subset)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from apex_standards_cim.shared import MRID, UnitSymbol

_CIM_CONFIG = ConfigDict(extra="forbid")


class CimMeterKind(StrEnum):
    ELECTRICITY = "electricity"
    GAS = "gas"
    WATER = "water"
    HEAT = "heat"


class CimMeter(BaseModel):
    """IEC 61968 Meter — an AMI meter or legacy meter."""

    model_config = _CIM_CONFIG
    m_rid: MRID
    serial_number: str
    kind: CimMeterKind = CimMeterKind.ELECTRICITY
    customer_mrid: MRID | None = None
    location_mrid: MRID | None = None
    install_date: datetime | None = None
    remove_date: datetime | None = None


class CimReading(BaseModel):
    """IEC 61968 Reading — a single value from a meter at a point in time."""

    model_config = _CIM_CONFIG
    meter_mrid: MRID
    timestamp: datetime
    value: Decimal
    unit: UnitSymbol = UnitSymbol.KWH
    quality_flag: str | None = Field(None, description="e.g. 'estimated', 'substituted', 'measured'.")


class CimCustomer(BaseModel):
    """IEC 61968 Customer — an account / service relationship."""

    model_config = _CIM_CONFIG
    m_rid: MRID
    name: str | None = None
    kind: str | None = Field(None, description="e.g. 'residential', 'commercial', 'industrial'.")
    status: str | None = None


class CimWorkOrder(BaseModel):
    """IEC 61968 WorkOrder — a maintenance / inspection job."""

    model_config = _CIM_CONFIG
    m_rid: MRID
    work_order_number: str
    status: str = Field(..., description="e.g. 'open', 'assigned', 'complete'.")
    priority: int | None = Field(None, ge=1, le=5)
    created: datetime
    scheduled: datetime | None = None
    asset_mrid: MRID | None = None
    description: str = ""
