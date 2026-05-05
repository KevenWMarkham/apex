"""SCML Location entity."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields
from apex_schemas_common.standards import GLN


class LocationType(StrEnum):
    STORE = "STORE"
    DC = "DC"
    WAREHOUSE = "WAREHOUSE"
    SUPPLIER_SITE = "SUPPLIER_SITE"
    CROSS_DOCK = "CROSS_DOCK"


class Location(CanonicalEntity, ScdType2Fields):
    """Physical or logical location — GS1 GLN-aligned."""

    location_natural: str = Field(..., description="Source-system natural key.")
    gln: GLN | None = Field(None, description="GS1 Global Location Number (13 digits).")
    location_type: LocationType
    name: str = Field(..., description="Human name of the location.")
    address_token: Annotated[str, Classification.INTERNAL] | None = Field(
        None, description="Tokenised structured address."
    )
    region: str | None = Field(None, description="Logical region code (e.g. US-WEST).")
    latitude: float | None = Field(None, ge=-90.0, le=90.0)
    longitude: float | None = Field(None, ge=-180.0, le=180.0)
