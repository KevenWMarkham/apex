"""SCML Lot entity — traceability unit for recall / cold-chain."""

from __future__ import annotations

from datetime import date

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class Lot(CanonicalEntity):
    """Traceability lot — a specific production / receipt batch of a SKU."""

    lot_number: str = Field(..., description="Lot / batch identifier.")
    sku_key: str = Field(..., description="FK → SCML SKU.")
    manufacture_date: date | None = None
    expiration_date: date | None = None
    origin_country: str | None = Field(None, min_length=2, max_length=3)
    quantity_received: int | None = Field(None, ge=0)
