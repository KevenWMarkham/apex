"""SCML Item entity — brand / product-family level above SKU."""

from __future__ import annotations

from pydantic import Field

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class Item(CanonicalEntity, ScdType2Fields):
    """Abstract product concept above SKU (brand / product-family level)."""

    item_natural: str = Field(..., description="Source-system natural key.")
    brand: str | None = None
    product_family: str | None = None
    description: str = Field("", description="Short marketing description.")
