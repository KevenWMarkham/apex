"""MERML Competitor entity — observed competitor prices for matched SKUs.

Sprint 30 item 30.3. Read by The Pricer for floor / ceiling / MAP rules and
by the Markdown Agent to gauge competitive pressure when proposing markdowns.

Bronze source is the ``competitor-pricing`` Dataflow Gen2 pipeline (per
``services/rc/_bronze/landing-config.yaml``).
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class CompetitorChannel(StrEnum):
    """Channel the competitor price was observed on."""

    ECOM = "ECOM"
    BRICK = "BRICK"
    MARKETPLACE = "MARKETPLACE"


class CompetitorMatchKind(StrEnum):
    """How the competitor SKU was matched to ours."""

    GTIN = "GTIN"                # Exact GS1 GTIN match
    MPN = "MPN"                  # Manufacturer part number
    HEURISTIC = "HEURISTIC"      # Title + attribute fuzzy match
    MANUAL = "MANUAL"            # Buyer-curated mapping


class Competitor(CanonicalEntity, ScdType2Fields):
    """Observed competitor price for a SKU at a point in time.

    SCD2 history is required because The Pricer needs the price observed at
    the moment a markdown candidate was scored, not the latest snapshot. The
    Pricing Agent's audit row references ``row_hash`` to prove which observation
    drove the decision.
    """

    sku_key: str = Field(..., description="FK → our SCML SKU.")
    competitor_name: str = Field(..., description="Free-form competitor identifier (e.g., 'Target').")
    competitor_sku_natural: str | None = Field(
        None, description="The competitor's own SKU id, when known."
    )
    match_kind: CompetitorMatchKind
    match_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="0..1 confidence; <0.7 should not gate decisions."
    )
    channel: CompetitorChannel
    observed_at: datetime
    list_price: Decimal = Field(..., ge=Decimal("0"))
    promo_price: Decimal | None = Field(
        None, ge=Decimal("0"), description="Promotional price when one is active."
    )
    in_stock: bool | None = Field(None, description="Stock signal at observation time.")
    source_url: str | None = Field(
        None, description="Where the price was scraped from (audit / debugging only)."
    )
