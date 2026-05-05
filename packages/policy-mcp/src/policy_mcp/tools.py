"""policy-mcp tool implementations."""

from __future__ import annotations

from apex_core.semver import SemVer
from apex_core.semver import classify_bump as _semver_classify
from apex_core.types import BumpClass, GateKind
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "policy-mcp"
TOOL_VERSION = "1.0.0"


# Sprint 7 stub: default gate-kind mapping. Sprint 10 will load per-tenant overrides.
_DEFAULT_GATE_MAPPING: dict[BumpClass, GateKind] = {
    BumpClass.PATCH: GateKind.ZERO_TOUCH,
    BumpClass.MINOR: GateKind.ACK_ONLY,
    BumpClass.MAJOR: GateKind.HITL,
}


def evaluate_policy(
    policy_ref: str,
    context: dict,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Evaluate a named policy against a context. Sprint 7 stub: always allowed."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.evaluate_policy",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"policy_ref": policy_ref, "context": context},
    ) as ctx:
        result = {
            "allowed": True,
            "reason": "default-allow (Sprint 7 stub; Sprint 10 wires real policy engine)",
            "policy_ref": policy_ref,
        }
        ctx["result"] = result
        return result


def check_compliance(
    bump_class: str,
    tenant_id: str = "default",
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Resolve the gate kind for a bump class per tenant policy."""
    try:
        bc = BumpClass(bump_class)
    except ValueError as exc:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"Unknown bump_class {bump_class!r}",
        ) from exc
    with traced_call(
        tool_name=f"{SERVER_NAME}.check_compliance",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"bump_class": bump_class, "tenant_id": tenant_id},
    ) as ctx:
        gate = _DEFAULT_GATE_MAPPING[bc]
        result = {"bump_class": bc.value, "gate_kind": gate.value, "tenant_id": tenant_id}
        ctx["result"] = result
        return result


def classify_bump(
    previous: str,
    current: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Classify the SemVer bump between two versions (delegates to apex-core)."""
    try:
        prev_v = SemVer.parse(previous)
        curr_v = SemVer.parse(current)
        bump = _semver_classify(prev_v, curr_v)
    except ValueError as exc:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=str(exc),
        ) from exc
    with traced_call(
        tool_name=f"{SERVER_NAME}.classify_bump",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"previous": previous, "current": current},
    ) as ctx:
        result = {"previous": previous, "current": current, "bump_class": bump.value}
        ctx["result"] = result
        return result


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.evaluate_policy", version=TOOL_VERSION,
        description="Evaluate a named policy against a context (allow / deny / reason).",
    ),
    ToolContract(
        name=f"{SERVER_NAME}.check_compliance", version=TOOL_VERSION,
        description="Resolve gate kind for a bump class per tenant policy.",
    ),
    ToolContract(
        name=f"{SERVER_NAME}.classify_bump", version=TOOL_VERSION,
        description="Classify SemVer bump PATCH / MINOR / MAJOR.",
    ),
]
