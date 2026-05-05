"""Tests for apex_identity.scope.ScopeResolver."""

from __future__ import annotations

import pytest

from apex_core.types import Classification, Practice
from apex_identity import (
    AgentRole,
    InMemoryTenantRoleStore,
    MockEntraProvisioningProvider,
    ScopeResolver,
)


def _setup() -> tuple[MockEntraProvisioningProvider, InMemoryTenantRoleStore]:
    prov = MockEntraProvisioningProvider()
    roles = InMemoryTenantRoleStore()
    return prov, roles


def test_resolve_composes_identity_and_role() -> None:
    prov, roles = _setup()
    prov.register("agent-1", "tenant-A")
    roles.set_role("agent-1", AgentRole(
        role_id="rc-reader", tenant_id="tenant-A",
        practice=Practice.RC, persona="store-ops-lead",
        allowed_classifications=(Classification.INTERNAL, Classification.PII),
        row_filters={"region": "US-WEST"},
    ))
    scope = ScopeResolver(prov, roles).resolve("agent-1")
    assert scope.tenant_id == "tenant-A"
    assert scope.practice is Practice.RC
    assert scope.persona == "store-ops-lead"
    assert Classification.PII in scope.classification_visibility
    assert scope.row_filters["region"] == "US-WEST"


def test_resolve_unknown_agent_raises() -> None:
    prov, roles = _setup()
    with pytest.raises(LookupError):
        ScopeResolver(prov, roles).resolve("unknown")


def test_resolve_agent_without_role_raises() -> None:
    prov, roles = _setup()
    prov.register("agent-2", "tenant-A")
    with pytest.raises(LookupError):
        ScopeResolver(prov, roles).resolve("agent-2")


def test_tenant_mismatch_rejected() -> None:
    prov, roles = _setup()
    prov.register("agent-3", "tenant-A")
    roles.set_role("agent-3", AgentRole(
        role_id="weird", tenant_id="tenant-B",
        practice=None, persona=None,
    ))
    with pytest.raises(ValueError):
        ScopeResolver(prov, roles).resolve("agent-3")
