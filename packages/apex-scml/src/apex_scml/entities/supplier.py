"""SCML Supplier entity."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class SupplierTier(StrEnum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    TERTIARY = "TERTIARY"


class Supplier(CanonicalEntity, ScdType2Fields):
    """Supplier / vendor record."""

    supplier_natural: str = Field(..., description="Source-system natural key.")
    supplier_name: str
    tier: SupplierTier = SupplierTier.PRIMARY
    contact_email_token: Annotated[str, Classification.PII] | None = Field(
        None, description="Tokenised contact email."
    )
    contact_phone_token: Annotated[str, Classification.PII] | None = Field(
        None, description="Tokenised contact phone."
    )
    is_active: bool = True
