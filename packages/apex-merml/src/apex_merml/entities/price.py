"""MERML Price entity."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class PriceKind(StrEnum):
    LIST = "LIST"
    REGULAR = "REGULAR"
    PROMOTIONAL = "PROMOTIONAL"
    CLEARANCE = "CLEARANCE"
    MEMBER = "MEMBER"


class Price(CanonicalEntity):
    """Effective price for a SKU at a location over a time window."""

    sku_key: str = Field(..., description="FK → SCML SKU.")
    location_key: str | None = Field(None, description="FK → SCML Location (null = chain-wide).")
    kind: PriceKind
    amount: Decimal = Field(..., ge=Decimal("0"))
    currency: str = Field("USD", min_length=3, max_length=3)
    effective_from: datetime
    effective_to: datetime | None = Field(None, description="Exclusive end; None = open-ended.")
