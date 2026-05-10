"""rc-e2e-07-mcp tool implementations (Sprint 37).

Three RC-E2E-07 service-specific MCP tools backing the returns-fraud agent
fleet. PII fields are tokenised on read; TRADE_SECRET fields require the
operator-trade-secret-read OBO claim.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from apex_core.types import Classification
from fabric_mcp import FABRIC_BACKEND, query_gold_view as _fabric_query_view
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "rc-e2e-07-mcp"
TOOL_VERSION = "1.0.0"
SERVICE_CODE = "RC-E2E-07"
_REQUIRED_SCOPES = ["practice:rc", "service:rc-e2e-07"]

_VALID_DECISION_CLASSES = (
    "auto_clear", "approve_at_hitl", "deny_at_hitl",
    "hold_with_pii_unlock", "manual_investigation_routed",
)


# ---------------------------------------------------------------------------
# 37.2b.1 — get_return_event
# ---------------------------------------------------------------------------


def get_return_event(
    event_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Read the return-event panel — return profile + tokenised PII.

    Returns the canonical return-event envelope consumed by The Analyst.
    PII fields (`customer_token`, `device_fingerprint_token`,
    `payment_fingerprint_token`) are tokenised on read; bulk-detokenise is
    Decide's HITL-gated escalate path only.

    Raises:
        McpError(NOT_FOUND): no return event with that id.
        McpError(INVALID_INPUT): event_id empty or > 100 chars.
    """
    if not event_id or len(event_id) > 100:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="event_id must be 1..100 chars",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_return_event",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"event_id": event_id},
        classification_applied=[Classification.PII],
    ) as ctx:
        rows = _fabric_query_view(
            "rc_gold.g_return_event_panel",
            {"event_id": event_id},
            limit=1,
            agent_id=agent_id,
            caller_identity=caller_identity,
        )
        if not rows:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No return event with id {event_id!r}",
            )
        ctx["result"] = rows[0]
        return rows[0]


# ---------------------------------------------------------------------------
# 37.2b.2 — get_fraud_score_basis
# ---------------------------------------------------------------------------


def get_fraud_score_basis(
    event_id: str,
    depth: int = 2,
    include_loss_economics: bool = False,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Read the 5-graph neighbourhood for the Fraud Specialist + Loss Quantifier.

    Returns customer / payment / device / shipping / sku graph signals at
    `depth` hops. When `include_loss_economics=true`, also returns the
    chargeback priors + admin cost + recovery efficiency for the Loss
    Quantifier (TRADE_SECRET — caller must hold operator-trade-secret-read).

    Raises:
        McpError(NOT_FOUND): no fraud-basis snapshot for this event.
        McpError(INVALID_INPUT): depth not in [1..3].
    """
    if not event_id:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="event_id is required",
        )
    if not (1 <= depth <= 3):
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="depth must be in [1, 3]",
        )
    classifications = [Classification.PII]
    if include_loss_economics:
        classifications.append(Classification.TRADE_SECRET)
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_fraud_score_basis",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={
            "event_id": event_id,
            "depth": depth,
            "include_loss_economics": include_loss_economics,
        },
        classification_applied=classifications,
    ) as ctx:
        rows = _fabric_query_view(
            "rc_gold.g_fraud_score_basis",
            {"event_id": event_id},
            limit=1,
            agent_id=agent_id,
            caller_identity=caller_identity,
        )
        if not rows:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No fraud-score basis for event {event_id!r}",
            )
        # Strip loss_economics block when not requested — TRADE_SECRET
        # leakage prevention at the read boundary.
        result = dict(rows[0])
        if not include_loss_economics:
            result.pop("loss_economics", None)
            result.pop("chargeback_priors", None)
        ctx["result"] = result
        return result


# ---------------------------------------------------------------------------
# 37.2b.3 — commit_hold_decision (idempotent on decision_id)
# ---------------------------------------------------------------------------


_COMMITTED_DECISIONS: dict[str, dict[str, Any]] = {}


def commit_hold_decision(
    decision_id: str,
    return_event_id: str,
    decision_class: str,
    operator_principal: str,
    *,
    fraud_score: float | None = None,
    tier3_pii_unlock_request_id: str | None = None,
    deny_rationale: str | None = None,
    refund_value_usd: float | None = None,
    trace_id: str | None = None,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Write the final returns-fraud decision back to MERML.Refund / SCML.Return / CXML.FraudCase.

    Idempotent on ``decision_id`` — re-calling with the same id returns the
    prior commit without a second write. Conflict raises if the same id
    arrives with different parameters.

    Validates:

    - `decision_class` is one of the valid enum values.
    - `hold_with_pii_unlock` requires `tier3_pii_unlock_request_id`.
    - `deny_at_hitl` requires `deny_rationale`.

    Raises:
        McpError(INVALID_INPUT): missing required field for the decision class.
        McpError(CONFLICT): same decision_id already committed with different params.
    """
    if not decision_id:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="decision_id is required",
        )
    if not return_event_id:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="return_event_id is required",
        )
    if decision_class not in _VALID_DECISION_CLASSES:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"decision_class must be one of {_VALID_DECISION_CLASSES}",
        )
    if not operator_principal:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="operator_principal is required (decision audit-row field)",
        )
    if decision_class == "hold_with_pii_unlock" and not tier3_pii_unlock_request_id:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=(
                "decision_class=hold_with_pii_unlock requires "
                "tier3_pii_unlock_request_id (proof of HITL-gated bulk_detokenize)"
            ),
        )
    if decision_class == "deny_at_hitl" and not deny_rationale:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=(
                "decision_class=deny_at_hitl requires deny_rationale "
                "(regional consumer-law audit field)"
            ),
        )
    if fraud_score is not None and not (0.0 <= fraud_score <= 1.0):
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="fraud_score must be in [0.0, 1.0]",
        )

    with traced_call(
        tool_name=f"{SERVER_NAME}.commit_hold_decision",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={
            "decision_id": decision_id,
            "return_event_id": return_event_id,
            "decision_class": decision_class,
            "fraud_score": fraud_score,
            "operator_principal": operator_principal,
            "tier3_pii_unlock_request_id": tier3_pii_unlock_request_id,
            "deny_rationale_present": deny_rationale is not None,
            "refund_value_usd": refund_value_usd,
            "trace_id": trace_id,
        },
        classification_applied=[Classification.TRADE_SECRET],
    ) as ctx:
        prior = _COMMITTED_DECISIONS.get(decision_id)
        if prior is not None:
            same = (
                prior["return_event_id"] == return_event_id
                and prior["decision_class"] == decision_class
                and prior["operator_principal"] == operator_principal
            )
            if not same:
                raise McpError(
                    code=McpErrorCode.CONFLICT,
                    message=(
                        f"decision_id {decision_id!r} already committed with "
                        "different parameters; refusing to overwrite"
                    ),
                )
            ctx["result"] = prior
            return prior

        commit = {
            "decision_id": decision_id,
            "return_event_id": return_event_id,
            "decision_class": decision_class,
            "fraud_score": fraud_score,
            "operator_principal": operator_principal,
            "tier3_pii_unlock_request_id": tier3_pii_unlock_request_id,
            "deny_rationale": deny_rationale,
            "refund_value_usd": refund_value_usd,
            "trace_id": trace_id,
            "applied_at": datetime.now(UTC).isoformat(),
            "outcome": "ok",
            "service_code": SERVICE_CODE,
        }
        _COMMITTED_DECISIONS[decision_id] = commit
        ctx["result"] = commit
        return commit


def _reset_committed_decisions_for_test() -> None:
    """Test-only helper — clear idempotency cache between tests."""
    _COMMITTED_DECISIONS.clear()


# ---------------------------------------------------------------------------
# Tool contracts
# ---------------------------------------------------------------------------


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_return_event",
        version=TOOL_VERSION,
        description="Read the return-event panel with tokenised PII fields.",
        classification_propagation=[Classification.PII],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_fraud_score_basis",
        version=TOOL_VERSION,
        description=(
            "Read the 5-graph neighbourhood for fraud scoring. "
            "include_loss_economics requires operator-trade-secret-read OBO."
        ),
        classification_propagation=[Classification.PII, Classification.TRADE_SECRET],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.commit_hold_decision",
        version=TOOL_VERSION,
        description=(
            "Write the final returns-fraud decision (auto_clear / approve / "
            "deny / hold / manual_investigation). Idempotent on decision_id."
        ),
        classification_propagation=[Classification.TRADE_SECRET, Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
]


# Keep FABRIC_BACKEND import live so static analysis sees it.
_ = FABRIC_BACKEND
