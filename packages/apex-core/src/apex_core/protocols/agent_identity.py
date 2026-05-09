"""AgentIdentityProvider protocol — agent identity, blueprints, OBO, CA.

APEX-M satisfies via Microsoft Entra Agent ID (GA April 2026).
APEX-G satisfies via Google Cloud IAM + service account impersonation.
APEX-A satisfies via AWS IAM roles + STS AssumeRole.

Adapters that federate identity (Okta, Auth0, Ping) implement this for
the federation slot in `client_approved_architecture.identity.federation`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class AgentBlueprint:
    """Template for creating individual agent identities with shared
    governance, conditional access, and lifecycle policy."""
    blueprint_id: str
    parent_id: str | None
    label: str
    conditional_access_policy_ids: list[str] = field(default_factory=list)
    role_assignments: list[str] = field(default_factory=list)
    lifecycle_policy: dict[str, Any] = field(default_factory=dict)
    notes: str = ""


@dataclass(frozen=True)
class AgentIdentity:
    """A specific agent's identity, derived from a blueprint."""
    identity_id: str           # provider-specific OID
    blueprint_id: str
    agent_id: str              # APEX-scoped (variant:service:scenario:role)
    principal_id: str
    tenant_id: str
    federated: bool = False


@runtime_checkable
class AgentIdentityProvider(Protocol):
    """Provision, look up, and govern agent identities."""

    variant: str

    def create_blueprint(self, blueprint: AgentBlueprint) -> AgentBlueprint:
        """Create or update an agent identity blueprint."""
        ...

    def provision_identity(
        self, *, blueprint_id: str, agent_id: str
    ) -> AgentIdentity:
        """Provision a child identity from the named blueprint."""
        ...

    def get_identity(self, agent_id: str) -> AgentIdentity | None:
        """Look up an existing agent identity by APEX-scoped id."""
        ...

    def revoke_identity(self, agent_id: str, *, reason: str) -> None:
        """Revoke (not delete) an identity. Audit trail preserved."""
        ...

    def acquire_obo_token(
        self,
        *,
        agent_id: str,
        operator_principal: str,
        target_resource: str,
    ) -> str:
        """Exchange operator principal token for agent + on-behalf-of."""
        ...

    def list_blueprints(self) -> list[AgentBlueprint]:
        """All blueprints for this provider."""
        ...
