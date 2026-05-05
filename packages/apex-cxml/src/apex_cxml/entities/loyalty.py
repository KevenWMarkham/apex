"""CXML Loyalty entity."""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class LoyaltyTier(StrEnum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    DIAMOND = "DIAMOND"


class Loyalty(CanonicalEntity, ScdType2Fields):
    """Loyalty-program membership for a Customer."""

    customer_key: str = Field(..., description="FK → CXML Customer.")
    program_code: str = Field(..., description="Loyalty program identifier.")
    member_number_token: Annotated[str, Classification.MEMBER_ONLY] = Field(
        ..., description="Tokenised member number."
    )
    tier: LoyaltyTier = LoyaltyTier.BRONZE
    points_balance: int = Field(0, ge=0)
    enrolled_date: date
    is_active: bool = True
