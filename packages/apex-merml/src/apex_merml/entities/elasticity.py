"""MERML Elasticity entity — price-elasticity coefficients per SKU × Location.

Sprint 30 item 30.3. Read by RC-E2E-03's Pricing Agent (The Pricer) to drive
markdown / promotional pricing recommendations. The model is fit upstream by
the RC pricing science team and lands in Silver as a periodically-refreshed
parameter table.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class ElasticityModelKind(StrEnum):
    """Model class that produced the coefficient."""

    LOG_LOG = "LOG_LOG"              # Constant-elasticity log-log regression
    SEMI_LOG = "SEMI_LOG"            # log(Q) = α + β·P
    PIECEWISE = "PIECEWISE"          # Piecewise linear over price segments
    BAYESIAN = "BAYESIAN"            # Bayesian hierarchical model


class Elasticity(CanonicalEntity, ScdType2Fields):
    """Price-elasticity coefficient for a SKU × Location at a fitted point.

    The coefficient is the percent change in unit demand for a 1% change in
    price. Negative values indicate the typical demand-curve direction. The
    Pricer agent reads ``coefficient`` and ``confidence_lower``/``upper`` to
    decide how aggressively to mark down.

    Per ADR-005 sensitivity model, ``coefficient`` is TRADE_SECRET because the
    elasticity surface is one of the most differentiating analytical assets
    the RC practice maintains for a tenant.
    """

    sku_key: str = Field(..., description="FK → SCML SKU.")
    location_key: str | None = Field(
        None, description="FK → SCML Location. Null = chain-wide coefficient."
    )
    category_key: str | None = Field(
        None, description="FK → MERML Category. Used as a fallback when SKU-level fit is sparse."
    )
    model_kind: ElasticityModelKind
    fit_at: datetime = Field(..., description="When the underlying model was fit.")
    coefficient: Annotated[Decimal, Classification.TRADE_SECRET] = Field(
        ..., description="Elasticity coefficient. Typically negative for normal goods."
    )
    confidence_lower: Annotated[Decimal, Classification.TRADE_SECRET] | None = Field(
        None, description="Lower bound of the 95%% confidence interval."
    )
    confidence_upper: Annotated[Decimal, Classification.TRADE_SECRET] | None = Field(
        None, description="Upper bound of the 95%% confidence interval."
    )
    sample_size: int | None = Field(None, ge=0, description="Observations used in the fit.")
    holdout_r_squared: float | None = Field(
        None, ge=0.0, le=1.0, description="Holdout R² of the fit."
    )
    valid_for_price_min: Decimal | None = Field(
        None, description="Lower bound of price range over which the coefficient is valid."
    )
    valid_for_price_max: Decimal | None = Field(
        None, description="Upper bound of price range over which the coefficient is valid."
    )
