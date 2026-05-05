"""RC Cold Chain Excursion Response — reference orchestration (APEX_Design §16.2).

Shape (sequential with per-step gates):

1. ``detect``  (ZERO_TOUCH)  — classify the excursion
2. ``dispose`` (HITL)        — decide salvage / destroy; pauses for QA concur
3. ``notify``  (ACK_ONLY)    — brief affected staff + store ops

Bump classes drive gate selection. The disposition step fires a MAJOR bump
(it writes to the batch record) so it lands on HITL.
"""

from __future__ import annotations

from typing import Any

from apex_core.types import BumpClass

from apex_orchestrator.gates.approvals import ApprovalsClient
from apex_orchestrator.manifest import StampedManifest, load_manifest_with_stamps
from apex_orchestrator.runtime import Orchestrator


def _detect_step(context: dict[str, Any]) -> dict[str, Any]:
    # Placeholder agent: classify temperature + duration → excursion category.
    temp_high_f = context.get("temp_high_f", 0.0)
    duration_minutes = context.get("duration_minutes", 0)
    threshold_breached = temp_high_f > 41 and duration_minutes > 30
    return {
        "excursion_detected": bool(threshold_breached),
        "excursion_category": "protocol_deviation" if threshold_breached else "within_spec",
    }


def _dispose_step(context: dict[str, Any]) -> dict[str, Any]:
    # Placeholder agent: propose disposition.
    if not context.get("excursion_detected"):
        return {"disposition_proposal": "no_action"}
    return {
        "disposition_proposal": "salvage_if_within_90_minutes_else_destroy",
        "units_at_risk": context.get("units_at_risk", 0),
    }


def _notify_step(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "notified": ["store-ops-lead", "inventory-control"],
        "channel": "teams",
    }


def build_cold_chain_response(
    *,
    approvals: ApprovalsClient,
    manifest_sha: str = "a1b2c3d4",
    policy_sha: str = "e5f6a7b8",
    prompt_sha: str = "9c8b7a6d",
) -> Orchestrator:
    """Assemble the reference Cold Chain Response orchestrator."""
    stamped: StampedManifest = load_manifest_with_stamps({
        "name": "rc-cold-chain-response",
        "stamps": {
            "manifest_version": manifest_sha,
            "policy_version": policy_sha,
            "prompt_version": prompt_sha,
        },
    })

    orch = Orchestrator(stamped, approvals=approvals)
    orch.add_step(
        step_id="detect",
        agent_name="cold-chain-detection-agent",
        agent_version="1.0.0",
        fn=_detect_step,
        bump_class=BumpClass.PATCH,   # detect is observational → ZERO_TOUCH
    )
    orch.add_step(
        step_id="dispose",
        agent_name="cold-chain-disposition-agent",
        agent_version="1.0.0",
        fn=_dispose_step,
        bump_class=BumpClass.MAJOR,   # writes batch disposition → HITL
        approver_group="rc-store-ops-approvers",
    )
    orch.add_step(
        step_id="notify",
        agent_name="store-notification-agent",
        agent_version="1.0.0",
        fn=_notify_step,
        bump_class=BumpClass.MINOR,   # ACK_ONLY — notify + continue
    )
    return orch
