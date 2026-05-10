"""PROML Pricing entity — the active price stack for a SKU × Location × channel.

Sprint 30 item 30.4. Read by The Pricer (RC-E2E-03) to know:

- the **list_price** the merchandiser set
- the **floor_price** below which The Pricer must NOT recommend (TRADE_SECRET)
- the **map_price** (Minimum Advertised Price) imposed by the manufacturer
  contract — bounds advertising price even if the floor is lower
- the **cost_token** snapshot used to validate margin floor adherence

PROML.Pricing carries the *current active* state. The MERML.Price entity
carries the *time-series* of all observed list/promo/markdown events and is
the source of historical truth.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class PriceChannel(StrEnum):
    """Channel the price applies to. Multi-channel pricing per SKU is common."""

    STORE = "STORE"
    ECOM = "ECOM"
    MARKETPLACE = "MARKETPLACE"
    WHOLESALE = "WHOLESALE"


class Pricing(CanonicalEntity, ScdType2Fields):
    """Active price stack for a SKU × Location × Channel at a point in time.

    SCD2 history is required because The Pricer's audit row references the
    ``row_hash`` of the active Pricing record at decision time — proves which
    floor / MAP applied when the markdown was approved.
    """

    sku_key: str = Field(..., description="FK → SCML SKU.")
    location_key: str | None = Field(
        None, description="FK → SCML Location. Null = chain-wide pricing record."
    )
    channel: PriceChannel
    effective_from: datetime = Field(..., description="When this price stack became active.")
    effective_to: datetime | None = Field(
        None, description="When superseded; None while currently active."
    )
    list_price: Decimal = Field(..., ge=Decimal("0"))
    floor_price: Annotated[Decimal, Classification.TRADE_SECRET] | None = Field(
        None,
        ge=Decimal("0"),
        description=(
            "TRADE_SECRET: minimum allowed price after any markdown / promo. "
            "The Pricer must reject candidate decisions below this value."
        ),
    )
    map_price: Annotated[Decimal, Classification.TRADE_SECRET] | None = Field(
        None,
        ge=Decimal("0"),
        description=(
            "TRADE_SECRET: Minimum Advertised Price per manufacturer contract. "
            "Bounds advertising display price even when floor is lower."
        ),
    )
    cost_token: Annotated[str, Classification.TRADE_SECRET] | None = Field(
        None,
        description=(
            "Tokenised supplier-confidential unit cost at effective_from. "
            "Used to validate effective_margin_pct adherence to margin floors."
        ),
    )
    target_margin_pct: Annotated[Decimal, Classification.TRADE_SECRET] | None = Field(
        None,
        description="Target gross margin percent the merchant set. Soft target; floor_price is the hard limit.",
    )
    last_changed_by: str | None = Field(
        None, description="Identity (user / agent / orchestration) that last published this stack."
    )
