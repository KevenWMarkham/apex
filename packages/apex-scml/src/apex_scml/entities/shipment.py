"""SCML Shipment entity."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from apex_schemas_common import CanonicalEntity
from apex_schemas_common.standards import SSCC


class Shipment(CanonicalEntity):
    """Shipment / pallet — GS1 SSCC-aligned."""

    shipment_natural: str = Field(..., description="Source-system natural key.")
    sscc: SSCC | None = Field(None, description="GS1 Serial Shipping Container Code (18 digits).")
    origin_key: str = Field(..., description="FK → SCML Location (origin).")
    destination_key: str = Field(..., description="FK → SCML Location (destination).")
    ship_datetime: datetime
    arrival_datetime: datetime | None = None
    carrier_name: str | None = None
    status: str = Field("IN_TRANSIT", description="Shipment status code.")
