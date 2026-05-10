"""rc-e2e-04-mcp tool implementations (Sprint 34).

Three RC-E2E-04 service-specific MCP tools backing the loyalty-churn agent
fleet. PII fields are tokenised on read; bulk detokenisation goes through
``tokenizer-mcp.bulk_detokenize`` from the Decide agent only.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from apex_core.types import Classification
from fabric_mcp import FABRIC_BACKEND, query_gold_view as _fabric_query_view
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "rc-e2e-04-mcp"
TOOL_VERSION = "1.0.0"
SERVICE_CODE = "RC-E2E-04"
_REQUIRED_SCOPES = ["practice:rc", "service:rc-e2e-04"]

_VALID_TIER_FILTERS = ("top_tier", "platinum", "gold", "silver", "all")


# ---------------------------------------------------------------------------
# 34.2g.1 — get_loyalty_churn_cohort
# ---------------------------------------------------------------------------


def get_loyalty_churn_cohort(
    window_start: str,
    window_end: str,
    tier_filter: str = "top_tier",
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Read the weekly loyalty-churn cohort (PII tokenised).

    Returns a cohort envelope with tokenised customer keys + RFM / engagement
    signals. Operator OBO scope is NOT required at this read — PII stays
    tokenised. Bulk detokenise (Decide agent's HITL path) requires Tier-3 OBO.

    Raises:
        McpError(INVALID_INPUT): tier_filter unknown, or windows malformed.
    """
    if tier_filter not in _VALID_TIER_FILTERS:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"unknown tier_filter {tier_filter!r}; allowed: {_VALID_TIER_FILTERS}",
        )
    try:
        start_dt = datetime.fromisoformat(window_start.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(window_end.replace("Z", "+00:00"))
    except ValueError as exc:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"window timestamps must be ISO-8601: {exc}",
        ) from None
    if start_dt >= end_dt:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="window_start must be before window_end",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_loyalty_churn_cohort",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={
            "window_start": window_start,
            "window_end": window_end,
            "tier_filter": tier_filter,
        },
        classification_applied=[Classification.PII],
    ) as ctx:
        filters: dict[str, Any] = {}
        if tier_filter != "all":
            filters["tier_filter"] = tier_filter
        rows = _fabric_query_view(
            "rc_gold.g_loyalty_churn_cohort",
            filters,
            limit=10000,
            agent_id=agent_id,
            caller_identity=caller_identity,
        )
        result = {
            "cohort_window": {"start": window_start, "end": window_end},
            "tier_filter": tier_filter,
            "cohort_size": len(rows),
            "members": rows,    # each row's PII fields are tokenised
        }
        ctx["result"] = result
        return result


# ---------------------------------------------------------------------------
# 34.2g.2 — get_winback_offer_basis
# ---------------------------------------------------------------------------


def get_winback_offer_basis(
    customer_token: str,
    cohort_window_start: str,
    cohort_window_end: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Read TRADE_SECRET winback offer basis for one tokenised customer.

    Projects predicted_ltv_decline_24m_usd, response_elasticity_curve,
    matched_offer_rules with caps, consent_personalization, and the
    elasticity_model_version. Caller identity must hold the
    ``operator-trade-secret-read`` claim from the OBO token.

    Returns the customer's tokenised id back unchanged — the FinanceLead
    agent does NOT detokenise here; that path is Decide's HITL gate.

    Raises:
        McpError(INVALID_INPUT): customer_token empty.
        McpError(NOT_FOUND): no winback basis for that token.
    """
    if not customer_token:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="customer_token is required",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_winback_offer_basis",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={
            "customer_token": customer_token,
            "cohort_window_start": cohort_window_start,
            "cohort_window_end": cohort_window_end,
        },
        classification_applied=[Classification.TRADE_SECRET],
    ) as ctx:
        rows = _fabric_query_view(
            "rc_gold.g_winback_offer_basis",
            {"customer_token": customer_token},
            limit=1,
            agent_id=agent_id,
            caller_identity=caller_identity,
        )
        if not rows:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No winback basis for customer_token={customer_token!r}",
            )
        ctx["result"] = rows[0]
        return rows[0]


# ---------------------------------------------------------------------------
# 34.2g.3 — commit_winback_offer (decision-emit, idempotent)
# ---------------------------------------------------------------------------


_COMMITTED_CAMPAIGNS: dict[str, dict[str, Any]] = {}


def commit_winback_offer(
    campaign_natural: str,
    cohort_window_start: str,
    cohort_window_end: str,
    approved_member_offers: list[dict[str, Any]],
    operator_principal: str,
    tier3_pii_unlock_request_id: str,
    *,
    trace_id: str | None = None,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Write a winback campaign back to CXML.Campaign.

    Per the act prompt, this is the only path that creates a campaign row.
    Idempotent on ``campaign_natural`` — re-calling with the same key
    returns the prior result without a second write.

    The ``tier3_pii_unlock_request_id`` is the audit handle from the
    Decide agent's HITL approval. Production wiring cross-checks the
    unlock record's TTL is still valid; the in-memory backend accepts
    the caller's word but stores the id for audit reconstruction.

    Raises:
        McpError(INVALID_INPUT): empty offers, missing operator/unlock id, etc.
        McpError(CONFLICT): same campaign_natural already committed with
            different parameters.
    """
    if not campaign_natural:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="campaign_natural is required",
        )
    if not approved_member_offers:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="approved_member_offers must contain at least one offer",
        )
    if not operator_principal:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="operator_principal is required (decision audit-row field)",
        )
    if not tier3_pii_unlock_request_id:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=(
                "tier3_pii_unlock_request_id is required — proves Tier-3 PII "
                "unlock was authorised by HITL before this campaign distributes"
            ),
        )
    # Validate offer shape
    for i, offer in enumerate(approved_member_offers):
        if "customer_token" not in offer:
            raise McpError(
                code=McpErrorCode.INVALID_INPUT,
                message=f"approved_member_offers[{i}] missing customer_token",
            )
        depth = offer.get("offer_depth_pct")
        if depth is not None and not (0 <= depth <= 100):
            raise McpError(
                code=McpErrorCode.INVALID_INPUT,
                message=f"approved_member_offers[{i}].offer_depth_pct must be in [0, 100]",
            )

    with traced_call(
        tool_name=f"{SERVER_NAME}.commit_winback_offer",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={
            "campaign_natural": campaign_natural,
            "cohort_window_start": cohort_window_start,
            "cohort_window_end": cohort_window_end,
            "approved_count": len(approved_member_offers),
            "operator_principal": operator_principal,
            "tier3_pii_unlock_request_id": tier3_pii_unlock_request_id,
            "trace_id": trace_id,
        },
        classification_applied=[Classification.TRADE_SECRET],
    ) as ctx:
        prior = _COMMITTED_CAMPAIGNS.get(campaign_natural)
        if prior is not None:
            same = (
                prior["approved_count"] == len(approved_member_offers)
                and prior["cohort_window_start"] == cohort_window_start
                and prior["cohort_window_end"] == cohort_window_end
                and prior["operator_principal"] == operator_principal
            )
            if not same:
                raise McpError(
                    code=McpErrorCode.CONFLICT,
                    message=(
                        f"campaign_natural {campaign_natural!r} already committed "
                        "with different parameters; refusing to overwrite"
                    ),
                )
            ctx["result"] = prior
            return prior

        cxml_campaign_id = f"cxml-campaign-{campaign_natural}"
        commit = {
            "campaign_natural": campaign_natural,
            "cxml_campaign_id": cxml_campaign_id,
            "cohort_window_start": cohort_window_start,
            "cohort_window_end": cohort_window_end,
            "approved_count": len(approved_member_offers),
            "operator_principal": operator_principal,
            "tier3_pii_unlock_request_id": tier3_pii_unlock_request_id,
            "trace_id": trace_id,
            "applied_at": datetime.now(UTC).isoformat(),
            "outcome": "ok",
            "service_code": SERVICE_CODE,
        }
        _COMMITTED_CAMPAIGNS[campaign_natural] = commit
        ctx["result"] = commit
        return commit


def _reset_committed_campaigns_for_test() -> None:
    """Test-only helper. Clears the idempotency cache between tests."""
    _COMMITTED_CAMPAIGNS.clear()


# ---------------------------------------------------------------------------
# Tool contracts
# ---------------------------------------------------------------------------


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_loyalty_churn_cohort",
        version=TOOL_VERSION,
        description=(
            "Read the weekly loyalty-churn cohort with tokenised PII fields. "
            "Bulk detokenise (HITL path) is provided by tokenizer-mcp."
        ),
        classification_propagation=[Classification.PII],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_winback_offer_basis",
        version=TOOL_VERSION,
        description=(
            "Read TRADE_SECRET winback offer basis for a tokenised customer. "
            "operator-trade-secret-read OBO claim required."
        ),
        classification_propagation=[Classification.TRADE_SECRET, Classification.PII],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.commit_winback_offer",
        version=TOOL_VERSION,
        description=(
            "Write a winback campaign back to CXML.Campaign. Idempotent on "
            "campaign_natural. Requires tier3_pii_unlock_request_id from HITL."
        ),
        classification_propagation=[Classification.TRADE_SECRET, Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
]


# Keep FABRIC_BACKEND import live so static analysis sees it.
_ = FABRIC_BACKEND
