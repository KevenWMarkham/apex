"""ledger-mcp tool implementations (Sprint 12).

Thin MCP wrapper around :mod:`apex_audit`. The append-tool now enforces the
full 14-field ``AuditRow`` contract (Section 11.2). Any emission missing a
required field or a ``trace_id`` is rejected at the MCP boundary.
"""

from __future__ import annotations

from typing import Any

from apex_audit import (
    AppendOnlyViolationError,
    AuditRow,
    AuditStore,
    TraceMissingError,
)
from apex_audit import verify_row as audit_verify_row
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call
from pydantic import ValidationError

SERVER_NAME = "ledger-mcp"
TOOL_VERSION = "1.1.0"  # Sprint 12: full 14-field contract

# Sprint 12: dev secret. Production pulls from Key Vault, keyed by tenant_id.
_DEV_LEDGER_SECRET = b"apex-ledger-dev-secret"

_STORE = AuditStore(signing_key=_DEV_LEDGER_SECRET)


def reset_ledger() -> None:
    """Test helper - replace the in-memory store with a fresh one."""
    global _STORE
    _STORE = AuditStore(signing_key=_DEV_LEDGER_SECRET)


def append_audit_row(
    row: dict[str, Any],
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, str]:
    """Append a 14-field decision audit row to the immutable ledger.

    Validates ``row`` through :class:`apex_audit.AuditRow` (Section 11.2) so
    every required field is present with a non-empty value. Missing fields
    raise ``McpError(INVALID_INPUT)``; overwrite attempts on a sealed
    ``decision_id`` raise ``McpError(CONFLICT)``; emissions missing
    ``trace_id`` raise ``McpError(INVALID_INPUT)`` via Section 11.6.
    """
    try:
        audit_row = AuditRow(**row)
    except ValidationError as exc:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"AuditRow validation failed: {exc.errors()}",
        ) from exc
    with traced_call(
        tool_name=f"{SERVER_NAME}.append_audit_row",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={
            "trace_id": audit_row.trace_id,
            "decision_id": audit_row.decision_id,
        },
    ) as ctx:
        try:
            sealed = _STORE.append(audit_row)
        except TraceMissingError as exc:
            raise McpError(
                code=McpErrorCode.INVALID_INPUT, message=str(exc),
            ) from exc
        except AppendOnlyViolationError as exc:
            raise McpError(code=McpErrorCode.CONFLICT, message=str(exc)) from exc
        out = {"row_id": audit_row.decision_id}
        ctx["result"] = out
        # Expose the sealed row for tests / immediate consumers.
        ctx["sealed_row"] = sealed
        return out


def fetch_row_by_trace(
    trace_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict[str, Any]]:
    """Return every audit row emitted for a given trace_id, in append order."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.fetch_row_by_trace",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"trace_id": trace_id},
    ) as ctx:
        rows = _STORE.by_trace(trace_id)
        ctx["result"] = rows
        return rows


def verify_row_signature(
    row_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Recompute the signature for a stored row and compare."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.verify_row_signature",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"row_id": row_id},
    ) as ctx:
        try:
            ok = _STORE.verify(row_id)
        except KeyError as exc:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No row with id {row_id!r}",
            ) from exc
        result = {"row_id": row_id, "signature_valid": ok}
        ctx["result"] = result
        return result


# Re-exported for consumers that want direct access (e.g. apex-orchestrator
# when emitting composite rows).
def _get_store() -> AuditStore:
    return _STORE


__all__ = [
    "CONTRACTS",
    "_get_store",
    "append_audit_row",
    "fetch_row_by_trace",
    "reset_ledger",
    "verify_row_signature",
    # Exposed so callers can construct canonical rows without importing
    # apex_audit directly (reduces coupling in the MCP layer).
    "audit_verify_row",
]


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.append_audit_row", version=TOOL_VERSION,
        description="Append a 14-field decision audit row to the immutable ledger.",
    ),
    ToolContract(
        name=f"{SERVER_NAME}.fetch_row_by_trace", version=TOOL_VERSION,
        description="Fetch every audit row for a trace_id in append order.",
    ),
    ToolContract(
        name=f"{SERVER_NAME}.verify_row_signature", version=TOOL_VERSION,
        description="Recompute + compare the HMAC signature for a stored row.",
    ),
]
