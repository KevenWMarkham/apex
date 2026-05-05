"""Entra managed-identity middleware stub.

Sprint 7 ships the shape; Sprint 10's ``apex-identity`` wires real Entra
token validation + service-principal scope resolution.
"""

from __future__ import annotations

from dataclasses import dataclass

from mcp_common.errors import McpError, McpErrorCode


@dataclass(frozen=True, slots=True)
class AgentIdentity:
    """The caller identity an MCP tool sees after auth.

    Sprint 7 stub — populated from an env-var / test fixture. Sprint 10
    replaces with Entra-issued claims (``sub``, ``tid``, ``app_id``, roles).
    """

    agent_id: str
    tenant_id: str
    entra_object_id: str | None = None
    scopes: tuple[str, ...] = ()


def require_agent_identity(identity: AgentIdentity | None) -> AgentIdentity:
    """Fail the call with ``McpError.UNAUTHENTICATED`` if ``identity`` is None."""
    if identity is None:
        raise McpError(
            code=McpErrorCode.UNAUTHENTICATED,
            message="AgentIdentity is required (Sprint 10: Entra token validation).",
        )
    return identity
