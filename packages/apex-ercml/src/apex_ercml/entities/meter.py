"""ERCML Meter entity — Pattern C over CIM Meter (IEC 61968)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class MeterKind(StrEnum):
    ELECTRICITY = "electricity"
    GAS = "gas"
    WATER = "water"
    HEAT = "heat"


class Meter(CanonicalEntity, ScdType2Fields):
    """Utility meter — AMI or legacy."""

    cim_mrid: str = Field(..., description="CIM Master Resource Identifier.")
    serial_number: str
    kind: MeterKind = MeterKind.ELECTRICITY
    customer_key: str | None = Field(None, description="FK → customer (external).")
    location_key: str | None = None
    install_date: datetime | None = None
    remove_date: datetime | None = None
    manufacturer: str | None = None
    model: str | None = None
