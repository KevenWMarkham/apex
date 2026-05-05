"""MERML Markdown entity."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class MarkdownReason(StrEnum):
    SEASONAL = "SEASONAL"
    OVERSTOCK = "OVERSTOCK"
    DAMAGED = "DAMAGED"
    EXPIRATION = "EXPIRATION"
    COMPETITIVE = "COMPETITIVE"
    CLEARANCE = "CLEARANCE"


class Markdown(CanonicalEntity):
    """Price reduction applied to a SKU — typically for disposition."""

    sku_key: str = Field(..., description="FK → SCML SKU.")
    location_key: str | None = Field(None, description="FK → SCML Location (null = chain-wide).")
    reason: MarkdownReason
    original_price: Decimal = Field(..., ge=Decimal("0"))
    marked_down_price: Decimal = Field(..., ge=Decimal("0"))
    applied_at: datetime
    applied_by: str | None = Field(None, description="Approver identity (user / agent / orchestration).")
    expected_recovery_pct: float | None = Field(None, ge=0.0, le=100.0)
