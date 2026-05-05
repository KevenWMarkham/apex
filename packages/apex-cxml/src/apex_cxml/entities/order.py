"""CXML Order entity."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity


class OrderStatus(StrEnum):
    DRAFT = "DRAFT"
    PLACED = "PLACED"
    PICKED = "PICKED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"


class Order(CanonicalEntity):
    """Customer order header (lines captured via related entities, later sprints)."""

    order_natural: str = Field(..., description="Source-system natural key.")
    customer_key: str | None = Field(None, description="FK → CXML Customer (null = guest).")
    placed_at: datetime
    status: OrderStatus = OrderStatus.DRAFT
    total_amount: Decimal = Field(..., ge=Decimal("0"))
    currency: str = Field("USD", min_length=3, max_length=3)
    payment_method_token: Annotated[str, Classification.PCI] | None = Field(
        None, description="Tokenised payment-method reference (PCI-scoped)."
    )
    fulfillment_location_key: str | None = Field(
        None, description="FK → SCML Location (store / DC fulfilling the order)."
    )
