"""MERML Promotion entity."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class PromotionType(StrEnum):
    PERCENT_OFF = "PERCENT_OFF"
    AMOUNT_OFF = "AMOUNT_OFF"
    BOGO = "BOGO"           # Buy One Get One
    BUNDLE = "BUNDLE"
    MEMBER_ONLY = "MEMBER_ONLY"


class Promotion(CanonicalEntity):
    """Promotional offer bound to one or more SKUs."""

    promotion_natural: str = Field(..., description="Source-system natural key.")
    promotion_type: PromotionType
    sku_keys: list[str] = Field(default_factory=list, description="FKs → SCML SKU (empty = all).")
    discount_value: Decimal = Field(..., ge=Decimal("0"))
    starts_at: datetime
    ends_at: datetime
    description: str = ""
    is_active: bool = True
