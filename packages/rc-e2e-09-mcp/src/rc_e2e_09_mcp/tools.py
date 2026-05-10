"""rc-e2e-09-mcp tool implementations (Sprint 39).

Three RC-E2E-09 service-specific MCP tools backing the FSMA-204 product-
tracking 3-agent Handoff chain. The `get_lot_provenance` tool is also
the cross-service read path for RC-E2E-03 + RC-E2E-07.

SCML.Lot ownership (Sprint 39.4): RC-E2E-09 is the sole writer.
`commit_lot_event` enforces this via the required_scopes check on the
contract — only `service:rc-e2e-09` callers can write.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from apex_core.types import Classification
from fabric_mcp import FABRIC_BACKEND, query_gold_view as _fabric_query_view
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "rc-e2e-09-mcp"
TOOL_VERSION = "1.0.0"
SERVICE_CODE = "RC-E2E-09"

# Read tools accept cross-service scopes; write tool requires RC-E2E-09 scope only.
_REQUIRED_SCOPES_WRITE = ["practice:rc", "service:rc-e2e-09"]
_REQUIRED_SCOPES_READ = ["practice:rc", "service:rc-e2e-09"]
_REQUIRED_SCOPES_CROSS_SERVICE_READ = ["practice:rc"]   # any RC service can read provenance

_VALID_LOT_EVENT_KINDS = (
    "recall_class_I", "recall_class_II", "recall_class_III",
    "trace_audit_pass", "trace_audit_gap_logged",
    "lot_status_held_in_dc", "lot_status_recalled_from_store",
    "lot_status_destruction_only",
)


# ---------------------------------------------------------------------------
# 39.3.1 — get_recall_panel
# ---------------------------------------------------------------------------


def get_recall_panel(
    trigger_event_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Read the recall panel — affected-lot CTE/KDE inventory + regulatory context.

    Returns the canonical envelope consumed by The Analyst (assess) and
    The Compliance Specialist (classify) in the FSMA-204 Handoff chain.

    Raises:
        McpError(NOT_FOUND): no recall panel for that trigger event id.
        McpError(INVALID_INPUT): trigger_event_id empty or > 100 chars.
    """
    if not trigger_event_id or len(trigger_event_id) > 100:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="trigger_event_id must be 1..100 chars",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_recall_panel",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"trigger_event_id": trigger_event_id},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "rc_gold.g_recall_panel",
            {"trigger_event_id": trigger_event_id},
            limit=1000,
            agent_id=agent_id,
            caller_identity=caller_identity,
        )
        if not rows:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No recall panel for trigger_event_id={trigger_event_id!r}",
            )
        # Aggregate into the panel envelope per the prompt contract.
        head = rows[0]
        result = {
            "trigger_event_id": trigger_event_id,
            "trigger_kind": head.get("trigger_kind"),
            "regulatory": {
                "jurisdiction": head.get("jurisdiction"),
                "fda_food_traceability_list_version": head.get("fda_ftl_version"),
                "state_recall_filing_required": head.get("state_recall_filing_required", False),
            },
            "affected_lots": [
                {
                    "lot_key": r.get("lot_key"),
                    "sku_key": r.get("sku_key"),
                    "is_covered_food": r.get("is_covered_food", False),
                    "received_with_temp_log": r.get("received_with_temp_log", False),
                    "cold_chain_compliant_pre_event": r.get("cold_chain_compliant_pre_event", False),
                    "has_critical_tracking_event_log": r.get("has_critical_tracking_event_log", False),
                    "cte_count": r.get("cte_count", 0),
                    "kde_count": r.get("kde_count", 0),
                    "earliest_cte_ts": r.get("earliest_cte_ts"),
                    "latest_cte_ts": r.get("latest_cte_ts"),
                    "supplier_key": r.get("supplier_key"),
                    "downstream_distribution_locations_count":
                        r.get("downstream_distribution_locations_count", 0),
                    "trace_gaps": r.get("trace_gaps", []),
                }
                for r in rows
            ],
        }
        ctx["result"] = result
        return result


# ---------------------------------------------------------------------------
# 39.3.2 — get_lot_provenance (CROSS-SERVICE)
# ---------------------------------------------------------------------------


def get_lot_provenance(
    lot_key: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Cross-service read — return the canonical lot-provenance envelope.

    This is the SOLE read path for non-RC-E2E-09 services that need lot
    history (RC-E2E-03's classify reads this for the FSMA-204 conformance
    check; RC-E2E-07's assess reads it when investigating refund-fraud-
    by-recall patterns).

    Per the SCML.Lot ownership boundary (Sprint 39.4): non-RC-E2E-09 services
    MUST NOT write to SCML.Lot. They consume only this read.

    Returns the lot's current SCD2 state plus its event history (recall
    classifications, trace-audit results, lot-status changes).

    Raises:
        McpError(NOT_FOUND): no lot with that key.
        McpError(INVALID_INPUT): lot_key empty.
    """
    if not lot_key:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="lot_key is required",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_lot_provenance",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"lot_key": lot_key},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "rc_gold.g_lot_provenance",
            {"lot_key": lot_key},
            limit=200,
            agent_id=agent_id,
            caller_identity=caller_identity,
        )
        if not rows:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No lot provenance for lot_key={lot_key!r}",
            )
        # Sort events by event_ts descending for typical "what's the
        # current status" reads. Consumers can paginate from the head.
        events_sorted = sorted(
            rows, key=lambda r: r.get("event_ts") or "", reverse=True,
        )
        head = events_sorted[0]
        result = {
            "lot_key": lot_key,
            "sku_key": head.get("sku_key"),
            "supplier_key": head.get("supplier_key"),
            "is_covered_food": head.get("is_covered_food", False),
            "current_status": head.get("event_kind"),
            "current_event_ts": head.get("event_ts"),
            # FSMA-204 fields RC-E2E-03's classify reads:
            "received_with_temp_log": head.get("received_with_temp_log", False),
            "cold_chain_compliant_pre_event": head.get("cold_chain_compliant_pre_event", False),
            "has_critical_tracking_event_log": head.get("has_critical_tracking_event_log", False),
            "events": [
                {
                    "event_kind": r.get("event_kind"),
                    "event_ts": r.get("event_ts"),
                    "decision_id": r.get("decision_id"),
                    "trace_id": r.get("trace_id"),
                }
                for r in events_sorted
            ],
        }
        ctx["result"] = result
        return result


# ---------------------------------------------------------------------------
# 39.3.3 — commit_lot_event (idempotent on (decision_id, lot_key, event_kind))
# ---------------------------------------------------------------------------


_COMMITTED_LOT_EVENTS: dict[tuple[str, str, str], dict[str, Any]] = {}


def commit_lot_event(
    decision_id: str,
    lot_key: str,
    event_kind: str,
    operator_principal: str,
    *,
    sku_key: str | None = None,
    trace_id: str | None = None,
    compliance_attestation_id: str | None = None,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Write a lot-event SCD2 row to SCML.Lot — RC-E2E-09 sole writer.

    Idempotent on ``(decision_id, lot_key, event_kind)``. Re-calling with
    the same triple returns the prior commit without a second write.

    Returns the lot_event_id + downstream_invalidation_keys (the cache keys
    the Foundry runtime will publish to Eventstream for cross-service
    consumers RC-E2E-03 + RC-E2E-07).

    Raises:
        McpError(INVALID_INPUT): unknown event_kind, missing required fields.
        McpError(CONFLICT): same triple already committed with different params.
    """
    if not decision_id or not lot_key:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="decision_id and lot_key are required",
        )
    if event_kind not in _VALID_LOT_EVENT_KINDS:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"event_kind must be one of {_VALID_LOT_EVENT_KINDS}",
        )
    if not operator_principal:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="operator_principal is required (decision audit-row field)",
        )
    # Class I recalls require attestation id (regulatory chain-of-custody)
    if event_kind == "recall_class_I" and not compliance_attestation_id:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=(
                "event_kind=recall_class_I requires compliance_attestation_id "
                "(FSMA-204 / 21 CFR 7.3 chain-of-custody field)"
            ),
        )

    with traced_call(
        tool_name=f"{SERVER_NAME}.commit_lot_event",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={
            "decision_id": decision_id,
            "lot_key": lot_key,
            "event_kind": event_kind,
            "operator_principal": operator_principal,
            "sku_key": sku_key,
            "compliance_attestation_id": compliance_attestation_id,
            "trace_id": trace_id,
        },
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        key = (decision_id, lot_key, event_kind)
        prior = _COMMITTED_LOT_EVENTS.get(key)
        if prior is not None:
            same = (
                prior["operator_principal"] == operator_principal
                and prior.get("sku_key") == sku_key
            )
            if not same:
                raise McpError(
                    code=McpErrorCode.CONFLICT,
                    message=(
                        f"({decision_id}, {lot_key}, {event_kind}) already "
                        "committed with different parameters; refusing to overwrite"
                    ),
                )
            ctx["result"] = prior
            return prior

        lot_event_id = f"scml-lot-{decision_id}-{lot_key}-{event_kind}"
        # Downstream invalidation keys flow to the Eventstream Activator.
        # RC-E2E-03 + RC-E2E-07 listen on these to invalidate their Gold-mart
        # join caches when a lot's status changes.
        downstream_invalidation_keys = [
            f"rc-e2e-03/g_excursion_decision_panel/lot_key/{lot_key}",
            f"rc-e2e-07/g_return_event_panel/lot_key/{lot_key}",
        ]
        commit = {
            "lot_event_id": lot_event_id,
            "decision_id": decision_id,
            "lot_key": lot_key,
            "sku_key": sku_key,
            "event_kind": event_kind,
            "operator_principal": operator_principal,
            "compliance_attestation_id": compliance_attestation_id,
            "trace_id": trace_id,
            "scd2_valid_from": datetime.now(UTC).isoformat(),
            "downstream_invalidation_keys": downstream_invalidation_keys,
            "outcome": "ok",
            "service_code": SERVICE_CODE,
        }
        _COMMITTED_LOT_EVENTS[key] = commit
        ctx["result"] = commit
        return commit


def _reset_committed_lot_events_for_test() -> None:
    """Test-only helper — clear idempotency cache between tests."""
    _COMMITTED_LOT_EVENTS.clear()


# ---------------------------------------------------------------------------
# Tool contracts
# ---------------------------------------------------------------------------


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_recall_panel",
        version=TOOL_VERSION,
        description="Read the recall panel — affected-lot CTE/KDE inventory.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES_READ,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_lot_provenance",
        version=TOOL_VERSION,
        description=(
            "CROSS-SERVICE read — return the canonical lot-provenance envelope. "
            "Sole read path for RC-E2E-03 + RC-E2E-07 lot history."
        ),
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES_CROSS_SERVICE_READ,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.commit_lot_event",
        version=TOOL_VERSION,
        description=(
            "Write a lot-event SCD2 row to SCML.Lot — RC-E2E-09 sole writer. "
            "Idempotent on (decision_id, lot_key, event_kind)."
        ),
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES_WRITE,
    ),
]


# Keep FABRIC_BACKEND import live so static analysis sees it.
_ = FABRIC_BACKEND
