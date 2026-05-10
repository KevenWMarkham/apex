"""rc-e2e-04-mcp — RC-E2E-04 Customer Lifecycle & Loyalty service MCP tools.

Sprint 34. Three tools:

- get_loyalty_churn_cohort     — cohort + tokenised PII for assess + classify
- get_winback_offer_basis       — TRADE_SECRET offer-policy + LTV inputs for Finance Lead
- commit_winback_offer          — campaign write-back from act (decision-emit, idempotent)
"""

from rc_e2e_04_mcp.tools import (
    CONTRACTS,
    commit_winback_offer,
    get_loyalty_churn_cohort,
    get_winback_offer_basis,
)

__all__ = [
    "CONTRACTS",
    "commit_winback_offer",
    "get_loyalty_churn_cohort",
    "get_winback_offer_basis",
]
