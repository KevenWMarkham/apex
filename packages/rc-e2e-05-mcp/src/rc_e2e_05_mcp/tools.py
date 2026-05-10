"""rc-e2e-05-mcp tool implementations (Sprint 35).

Three RC-E2E-05 service-specific MCP tools backing the on-shelf-availability
agent fleet. INTERNAL classification only — no TRADE_SECRET / PII fields.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from apex_core.types import Classification
from fabric_mcp import FABRIC_BACKEND, query_gold_view as _fabric_query_view
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "rc-e2e-05-mcp"
TOOL_VERSION = "1.0.0"
SERVICE_CODE = "RC-E2E-05"
_REQUIRED_SCOPES = ["practice:rc", "service:rc-e2e-05"]

_VALID_COMPLETION_KINDS = ("complete", "skip_bay_empty", "skip_supervisor")


# ---------------------------------------------------------------------------
# 35.2b.1 — get_oos_event
# ---------------------------------------------------------------------------


def get_oos_event(
    event_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Read the OSA event panel — affected SKUs + inventory + velocity baseline.

    Returns the event envelope + per-SKU inventory + 24h velocity buckets +
    7-day baseline velocity + per-SKU `key_value_flag` + replenishment ETA.

    Raises:
        McpError(NOT_FOUND): no OSA event with that id.
        McpError(INVALID_INPUT): event_id empty or > 100 chars.
    """
    if not event_id or len(event_id) > 100:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="event_id must be 1..100 chars",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_oos_event",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"event_id": event_id},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "rc_gold.g_oos_event_panel",
            {"event_id": event_id},
            limit=1000,
            agent_id=agent_id,
            caller_identity=caller_identity,
        )
        if not rows:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No OSA event with id {event_id!r}",
            )
        result = {
            "event_id": event_id,
            "store_id": rows[0].get("store_id"),
            "bay_id": rows[0].get("bay_id"),
            "event_ts": rows[0].get("event_ts"),
            "signal_kind": rows[0].get("signal_kind"),
            "affected_skus": [
                {
                    "sku_key": r.get("sku_key"),
                    "bay_id": r.get("bay_id"),
                    "on_hand_qty": r.get("on_hand_qty"),
                    "last_sold_at": r.get("last_sold_at"),
                    "last_received_at": r.get("last_received_at"),
                    "key_value_flag": r.get("key_value_flag", False),
                    "unit_retail": r.get("unit_retail"),
                    "baseline_velocity_hourly": r.get("baseline_velocity_hourly"),
                    "pos_velocity_24h": r.get("pos_velocity_24h"),
                    "replenishment_eta_minutes": r.get("replenishment_eta_minutes"),
                    "matched_sku_confidence": r.get("matched_sku_confidence"),
                    "observed_qty": r.get("observed_qty"),
                }
                for r in rows
            ],
        }
        ctx["result"] = result
        return result


# ---------------------------------------------------------------------------
# 35.2b.2 — get_shelf_gap_assignment_basis
# ---------------------------------------------------------------------------


def get_shelf_gap_assignment_basis(
    store_id: str,
    as_of: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Read the workforce roster + bay layout + task duration norms.

    Returns the clocked-in associate roster (tokenised IDs), per-associate
    zone authorisations + skill tier, the bay-to-bay travel-time matrix, and
    per-task-kind expected-duration norms. The Workforce Capacity Sizer uses
    this to build a walkable assignment plan.

    Associate IDs are tokenised — never raw employee numbers.

    Raises:
        McpError(NOT_FOUND): no roster snapshot for that store / time.
    """
    if not store_id:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="store_id is required",
        )
    try:
        datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    except ValueError:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"as_of must be ISO-8601: {as_of!r}",
        ) from None
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_shelf_gap_assignment_basis",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"store_id": store_id, "as_of": as_of},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "rc_gold.g_shelf_gap_assignment_basis",
            {"store_id": store_id},
            limit=200,
            agent_id=agent_id,
            caller_identity=caller_identity,
        )
        if not rows:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No assignment basis for store {store_id!r} as_of {as_of!r}",
            )
        # The Gold mart aggregates roster + bay_layout + task_duration_norms
        # into one row; canonical envelope wraps these together.
        head = rows[0]
        result = {
            "store_id": store_id,
            "as_of": as_of,
            "shift_capacity_minutes_remaining": head.get("shift_capacity_minutes_remaining"),
            "associates": head.get("associates", []),
            "bay_layout": head.get("bay_layout", {}),
            "task_duration_norms": head.get("task_duration_norms", {}),
        }
        ctx["result"] = result
        return result


# ---------------------------------------------------------------------------
# 35.2b.3 — commit_task_dispatch (idempotent on (dispatch_id, associate_id, task_order))
# ---------------------------------------------------------------------------


# Idempotency cache. Production swaps for Cosmos / Redis.
_COMMITTED_DISPATCH: dict[tuple[str, str, int], dict[str, Any]] = {}


def commit_task_dispatch(
    dispatch_id: str,
    associate_id: str,
    task_order: int,
    operator_principal: str,
    *,
    sku_key: str | None = None,
    bay_id: str | None = None,
    task_kind: str | None = None,
    completion_kind: str | None = None,    # None = fan-out; set on completion
    trace_id: str | None = None,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Write a task-dispatch event back to CXML.AssociateTask + audit row.

    Two phases:

    - **Fan-out** (`completion_kind=None`): records that an associate's card
      was dispatched. Requires sku_key + bay_id + task_kind.
    - **Completion ingest** (`completion_kind` in `complete` /
      `skip_bay_empty` / `skip_supervisor`): records an associate's action.

    Idempotent on ``(dispatch_id, associate_id, task_order)`` — re-calling
    with the same triple returns the prior commit without a second write.

    Raises:
        McpError(INVALID_INPUT): missing required field for the phase or
            unknown completion_kind.
        McpError(CONFLICT): same key already committed with different params.
    """
    if not dispatch_id or not associate_id:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="dispatch_id and associate_id are required",
        )
    if task_order < 1:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="task_order must be >= 1",
        )
    if not operator_principal:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="operator_principal is required (decision audit-row field)",
        )

    is_fanout = completion_kind is None
    if is_fanout:
        if not sku_key or not bay_id or not task_kind:
            raise McpError(
                code=McpErrorCode.INVALID_INPUT,
                message="fan-out phase requires sku_key + bay_id + task_kind",
            )
    else:
        if completion_kind not in _VALID_COMPLETION_KINDS:
            raise McpError(
                code=McpErrorCode.INVALID_INPUT,
                message=f"completion_kind must be one of {_VALID_COMPLETION_KINDS}",
            )

    with traced_call(
        tool_name=f"{SERVER_NAME}.commit_task_dispatch",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={
            "dispatch_id": dispatch_id,
            "associate_id": associate_id,
            "task_order": task_order,
            "phase": "fanout" if is_fanout else "completion",
            "completion_kind": completion_kind,
            "operator_principal": operator_principal,
            "sku_key": sku_key,
            "bay_id": bay_id,
            "task_kind": task_kind,
        },
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        key = (dispatch_id, associate_id, task_order)
        prior = _COMMITTED_DISPATCH.get(key)
        if prior is not None:
            same = (
                prior["phase"] == ("fanout" if is_fanout else "completion")
                and prior.get("completion_kind") == completion_kind
                and prior.get("sku_key") == sku_key
                and prior.get("bay_id") == bay_id
            )
            if not same:
                raise McpError(
                    code=McpErrorCode.CONFLICT,
                    message=(
                        f"({dispatch_id}, {associate_id}, {task_order}) already "
                        "committed with different parameters; refusing to overwrite"
                    ),
                )
            ctx["result"] = prior
            return prior

        cxml_associate_task_id = f"cxml-associatetask-{dispatch_id}-{associate_id}-{task_order}"
        commit = {
            "dispatch_id": dispatch_id,
            "associate_id": associate_id,
            "task_order": task_order,
            "cxml_associate_task_id": cxml_associate_task_id,
            "phase": "fanout" if is_fanout else "completion",
            "completion_kind": completion_kind,
            "sku_key": sku_key,
            "bay_id": bay_id,
            "task_kind": task_kind,
            "operator_principal": operator_principal,
            "trace_id": trace_id,
            "applied_at": datetime.now(UTC).isoformat(),
            "outcome": "ok",
            "service_code": SERVICE_CODE,
        }
        _COMMITTED_DISPATCH[key] = commit
        ctx["result"] = commit
        return commit


def _reset_committed_dispatch_for_test() -> None:
    """Test-only helper — clear idempotency cache between tests."""
    _COMMITTED_DISPATCH.clear()


# ---------------------------------------------------------------------------
# Tool contracts
# ---------------------------------------------------------------------------


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_oos_event",
        version=TOOL_VERSION,
        description="Read the OSA event panel for one shelf-gap event.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_shelf_gap_assignment_basis",
        version=TOOL_VERSION,
        description=(
            "Read the workforce roster + bay layout + task duration norms "
            "for the workforce-capacity quantification step."
        ),
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.commit_task_dispatch",
        version=TOOL_VERSION,
        description=(
            "Write a task-dispatch event (fan-out or completion). "
            "Idempotent on (dispatch_id, associate_id, task_order)."
        ),
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
]


# Keep FABRIC_BACKEND import live so static analysis sees it.
_ = FABRIC_BACKEND
