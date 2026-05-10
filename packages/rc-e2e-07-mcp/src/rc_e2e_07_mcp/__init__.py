"""rc-e2e-07-mcp — RC-E2E-07 Returns & Refund Integrity MCP tools.

Sprint 37. Three tools:

- get_return_event           — return profile + tokenised customer/device/payment for assess
- get_fraud_score_basis      — 5-graph neighbourhood + loss economics for classify + quantify
- commit_hold_decision       — final write-back from act (idempotent on decision_id)
"""

from rc_e2e_07_mcp.tools import (
    CONTRACTS,
    commit_hold_decision,
    get_fraud_score_basis,
    get_return_event,
)

__all__ = [
    "CONTRACTS",
    "commit_hold_decision",
    "get_fraud_score_basis",
    "get_return_event",
]
