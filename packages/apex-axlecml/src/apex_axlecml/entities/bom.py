"""AXLECML BillOfMaterials entity — product structure (STEP AP242-adjacent)."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class BomLine(CanonicalEntity):
    """One line of a BoM — a child component and its quantity under a parent product."""

    bom_id: str = Field(..., description="FK → AXLECML BillOfMaterials.entity_id.")
    parent_product_id: str
    child_product_id: str
    quantity: Decimal = Field(..., gt=Decimal("0"))
    unit_of_measure: str = "each"
    sequence: int | None = None
    is_optional: bool = False


class BillOfMaterials(CanonicalEntity, ScdType2Fields):
    """BoM header — the product whose structure is described by a set of BomLines."""

    product_id: str = Field(..., description="Top-level product identifier.")
    version: str = Field("1.0", description="BoM version / revision.")
    description: str = ""
    is_engineering_bom: bool = Field(
        False, description="Engineering vs manufacturing vs service BoM."
    )
