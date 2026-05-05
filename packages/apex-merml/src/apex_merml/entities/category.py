"""MERML Category entity."""

from __future__ import annotations

from pydantic import Field

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class Category(CanonicalEntity, ScdType2Fields):
    """Merchandise category (hierarchical — parent/child)."""

    category_natural: str = Field(..., description="Source-system natural key.")
    category_name: str
    parent_category_key: str | None = Field(
        None, description="FK → parent Category (null for roots)."
    )
    level: int = Field(0, ge=0, le=10, description="Depth in the hierarchy, 0 = root.")
    description: str = ""
