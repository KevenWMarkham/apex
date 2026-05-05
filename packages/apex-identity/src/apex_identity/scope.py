"""Scope resolver — composes identity + role into a fully-populated ScopeContext."""

from __future__ import annotations

from mcp_common import ScopeContext

from apex_identity.provisioning import EntraProvisioningProvider, TenantRoleStore


class ScopeResolver:
    """Resolves an ``agent_id`` to a :class:`ScopeContext` ready for lattice evaluation.

    The resolver composes:

    - **Identity**: looked up from the :class:`EntraProvisioningProvider`.
    - **Role**: looked up from the :class:`TenantRoleStore` — provides the
      practice, persona, allowed classifications, and row filters.

    Resolution fails closed: unknown agents or unassigned roles raise
    ``LookupError`` — the caller decides whether to map that to an MCP
    ``UNAUTHENTICATED`` / ``SCOPE_DENIED`` response.
    """

    def __init__(
        self,
        provider: EntraProvisioningProvider,
        roles: TenantRoleStore,
    ) -> None:
        self.provider = provider
        self.roles = roles

    def resolve(self, agent_id: str) -> ScopeContext:
        """Return the current ``ScopeContext`` for ``agent_id``."""
        identity = self.provider.lookup(agent_id)
        if identity is None:
            raise LookupError(f"Agent {agent_id!r} is not provisioned.")
        role = self.roles.get_role(agent_id)
        if role is None:
            raise LookupError(f"Agent {agent_id!r} has no assigned role.")
        if role.tenant_id != identity.tenant_id:
            raise ValueError(
                f"Role tenant {role.tenant_id!r} does not match identity "
                f"tenant {identity.tenant_id!r}."
            )
        return ScopeContext(
            tenant_id=identity.tenant_id,
            practice=role.practice,
            persona=role.persona,
            classification_visibility=frozenset(role.allowed_classifications),
            row_filters=dict(role.row_filters),
        )
