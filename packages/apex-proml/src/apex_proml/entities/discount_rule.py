"""PROML DiscountRule entity — the policy envelope The Pricer must honor.

Sprint 30 item 30.4. Read by The Pricer to know what kinds of discounts /
markdowns it's allowed to recommend, and what the maximum cap is per rule.

A rule can be scoped to:
- a specific SKU (by ``sku_key``)
- a specific Category (by ``category_key``)
- chain-wide (both null)

When multiple rules match, The Pricer applies the *most restrictive* —
i.e. the smallest ``cap_pct`` wins. The audit row lists the matched
``rule_natural`` keys so an auditor can replay the decision.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import Field, model_validator

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class DiscountRuleKind(StrEnum):
    """Policy class — drives The Pricer's matching logic."""

    BUYER_LADDER = "BUYER_LADDER"        # Tiered markdown ladder set by the buyer
    SEASONAL = "SEASONAL"                # Seasonal markdown rule (e.g. Q4 clearance)
    CLEARANCE = "CLEARANCE"              # End-of-life markdown rule
    MARGIN_FLOOR = "MARGIN_FLOOR"        # Hard margin-floor rule (cannot violate)
    COMPETITOR_MATCH = "COMPETITOR_MATCH"  # Match-or-beat-competitor rule


class DiscountRule(CanonicalEntity, ScdType2Fields):
    """A pricing policy / cap that The Pricer must honor.

    SCD2 history is required because The Pricer's audit row pins the rule
    version (``row_hash``) that gated each markdown decision.
    """

    rule_natural: str = Field(..., description="Source-system natural key for the rule.")
    rule_kind: DiscountRuleKind
    rule_name: str = Field(..., description="Human-readable rule name for HITL surfaces.")
    description: str = Field("", description="Operator-facing rationale.")

    # --- Scoping (most-restrictive wins when multiple rules match) ----------
    sku_key: str | None = Field(None, description="FK → SCML SKU. Null = not SKU-specific.")
    category_key: str | None = Field(
        None, description="FK → MERML Category. Null = not category-specific."
    )

    # --- Window -------------------------------------------------------------
    effective_from: datetime
    effective_to: datetime | None = None

    # --- Cap (TRADE_SECRET — competitive sensitivity) -----------------------
    cap_pct: Annotated[Decimal, Classification.TRADE_SECRET] | None = Field(
        None,
        ge=Decimal("0"),
        le=Decimal("100"),
        description=(
            "TRADE_SECRET: maximum markdown / discount this rule allows, as a "
            "percent off list_price. The Pricer rejects candidates exceeding this."
        ),
    )
    margin_floor_pct: Annotated[Decimal, Classification.TRADE_SECRET] | None = Field(
        None,
        ge=Decimal("0"),
        le=Decimal("100"),
        description=(
            "TRADE_SECRET: minimum gross-margin percent the rule enforces. "
            "When set, The Pricer computes effective_margin_pct against cost "
            "and rejects candidates that would breach this floor."
        ),
    )

    # --- HITL routing -------------------------------------------------------
    requires_hitl_above_pct: Decimal | None = Field(
        None,
        ge=Decimal("0"),
        le=Decimal("100"),
        description=(
            "When the proposed markdown exceeds this percent, route to "
            "Operations Lead HITL even if the cap allows it."
        ),
    )

    @model_validator(mode="after")
    def _at_least_one_constraint(self) -> "DiscountRule":
        """A rule must have at least one of cap_pct / margin_floor_pct."""
        if self.cap_pct is None and self.margin_floor_pct is None:
            raise ValueError(
                "DiscountRule must set at least one of cap_pct or margin_floor_pct."
            )
        return self
