"""Entra managed-identity provisioning + tenant role store.

Sprint 10 ships the interface + a mock backed by in-memory dicts. Sprint 14
wires the Microsoft Graph SDK for real app-registration automation.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol, runtime_checkable

from apex_core.types import Classification, Practice
from mcp_common import AgentIdentity


@dataclass(frozen=True, slots=True)
class AgentRole:
    """A defined role within a tenant — binds an agent's capabilities.

    Sprint 10: roles are configured in-process. Sprint 13 wires Purview /
    Unified Catalog role definitions so tenants edit them declaratively.
    """

    role_id: str
    tenant_id: str
    practice: Practice | None
    persona: str | None = None
    allowed_classifications: tuple[Classification, ...] = ()
    scopes: tuple[str, ...] = ()
    row_filters: dict[str, str] = field(default_factory=dict)


# --- Provisioning provider --------------------------------------------------


@runtime_checkable
class EntraProvisioningProvider(Protocol):
    """Protocol for Entra app-registration automation."""

    def register(
        self,
        agent_id: str,
        tenant_id: str,
        scopes: tuple[str, ...] = (),
    ) -> AgentIdentity:
        """Register ``agent_id`` in ``tenant_id`` with ``scopes`` and return its identity."""
        ...

    def lookup(self, agent_id: str) -> AgentIdentity | None:
        """Return the active identity for ``agent_id``, or None if unknown or revoked."""
        ...

    def revoke(self, agent_id: str) -> None:
        """Revoke the identity registered for ``agent_id``."""
        ...


@dataclass
class MockEntraProvisioningProvider:
    """In-memory Entra provider for dev + tests.

    The deterministic ``entra_object_id`` derivation is handy for tests —
    real Entra allocates opaque object IDs; production callers should never
    depend on the derivation algorithm.
    """

    _identities: dict[str, AgentIdentity] = field(default_factory=dict)
    _revoked_at: dict[str, datetime] = field(default_factory=dict)

    @staticmethod
    def _derive_oid(agent_id: str, tenant_id: str) -> str:
        digest = hashlib.sha256(f"{tenant_id}|{agent_id}".encode()).hexdigest()
        return f"{digest[:8]}-{digest[8:12]}-{digest[12:16]}-{digest[16:20]}-{digest[20:32]}"

    def register(
        self,
        agent_id: str,
        tenant_id: str,
        scopes: tuple[str, ...] = (),
    ) -> AgentIdentity:
        """Register ``agent_id`` with a deterministic object id and return its identity.

        Re-registering a revoked agent clears its revocation.
        """
        identity = AgentIdentity(
            agent_id=agent_id,
            tenant_id=tenant_id,
            entra_object_id=self._derive_oid(agent_id, tenant_id),
            scopes=scopes,
        )
        self._identities[agent_id] = identity
        self._revoked_at.pop(agent_id, None)
        return identity

    def lookup(self, agent_id: str) -> AgentIdentity | None:
        """Return the registered identity for ``agent_id``, or None."""
        return self._identities.get(agent_id)

    def revoke(self, agent_id: str) -> None:
        """Drop the identity for ``agent_id`` and record the revocation time; no-op if unknown."""
        if agent_id in self._identities:
            self._revoked_at[agent_id] = datetime.now(UTC)
            self._identities.pop(agent_id)

    # Test helpers (not part of the Protocol)

    def registered_count(self) -> int:
        """Return the number of currently registered (non-revoked) identities."""
        return len(self._identities)


# --- Role store -------------------------------------------------------------


@runtime_checkable
class TenantRoleStore(Protocol):
    """Maps an agent_id → its assigned :class:`AgentRole`."""

    def get_role(self, agent_id: str) -> AgentRole | None:
        """Return the role assigned to ``agent_id``, or None if unassigned."""
        ...

    def set_role(self, agent_id: str, role: AgentRole) -> None:
        """Assign ``role`` to ``agent_id``, replacing any previous assignment."""
        ...


@dataclass
class InMemoryTenantRoleStore:
    """Dict-backed :class:`TenantRoleStore` for dev and tests."""

    _roles: dict[str, AgentRole] = field(default_factory=dict)

    def get_role(self, agent_id: str) -> AgentRole | None:
        """Return the role assigned to ``agent_id``, or None if unassigned."""
        return self._roles.get(agent_id)

    def set_role(self, agent_id: str, role: AgentRole) -> None:
        """Assign ``role`` to ``agent_id``, replacing any previous assignment."""
        self._roles[agent_id] = role
