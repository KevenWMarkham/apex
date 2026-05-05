"""SCML SKU entity."""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields
from apex_schemas_common.standards import GTIN14


class SkuStatus(StrEnum):
    """Lifecycle status of a SKU."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DISCONTINUED = "DISCONTINUED"


class SKU(CanonicalEntity, ScdType2Fields):
    """Sellable product variant (size / colour / pack) — GS1 GTIN-aligned."""

    sku_natural: str = Field(..., description="Source-system natural key.")
    gtin: GTIN14 | None = Field(None, description="GS1 Global Trade Item Number (14 digits).")
    sku_status: SkuStatus = Field(..., description="Lifecycle status.")
    category_key: str = Field(..., description="FK → MERML Category.")
    supplier_key: str | None = Field(None, description="FK → SCML Supplier.")
    description: str = Field("", description="Short merchandising description.")
    unit_cost_token: Annotated[str, Classification.TRADE_SECRET] | None = Field(
        None, description="Tokenised supplier-confidential unit cost."
    )
    unit_retail: Decimal | None = Field(None, description="List retail price.")
    case_pack: int | None = Field(None, ge=1, description="Units per case.")
    weight_kg: Decimal | None = Field(None, ge=Decimal("0"))
