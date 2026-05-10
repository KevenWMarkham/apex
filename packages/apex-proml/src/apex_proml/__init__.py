"""APEX PROML — Pricing & Revenue Markup Language canonical entities (RC Practice).

Sprint 30.4. PROML.Pricing carries the active price stack for a SKU × Location
× channel; PROML.DiscountRule carries the policy envelope The Pricer must
honor when proposing markdowns or promotional pricing.
"""

from apex_proml.entities import (
    DiscountRule,
    DiscountRuleKind,
    PriceChannel,
    Pricing,
)

__all__ = [
    "DiscountRule",
    "DiscountRuleKind",
    "PriceChannel",
    "Pricing",
]
