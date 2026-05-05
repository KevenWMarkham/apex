"""Tests for apex_identity.provisioning."""

from __future__ import annotations

from apex_core.types import Classification, Practice
from apex_identity import (
    AgentRole,
    InMemoryTenantRoleStore,
    MockEntraProvisioningProvider,
)


def test_register_produces_stable_oid() -> None:
    prov = MockEntraProvisioningProvider()
    a = prov.register("agent-1", "tenant-A")
    b = prov.register("agent-1", "tenant-A")
    assert a.entra_object_id == b.entra_object_id


def test_register_different_tenants_different_oid() -> None:
    prov = MockEntraProvisioningProvider()
    a = prov.register("agent-1", "tenant-A")
    b = prov.register("agent-1", "tenant-B")
    assert a.entra_object_id != b.entra_object_id


def test_lookup_and_revoke() -> None:
    prov = MockEntraProvisioningProvider()
    prov.register("agent-1", "tenant-A", scopes=("practice:rc",))
    assert prov.lookup("agent-1") is not None
    prov.revoke("agent-1")
    assert prov.lookup("agent-1") is None


def test_role_store_round_trip() -> None:
    roles = InMemoryTenantRoleStore()
    role = AgentRole(
        role_id="rc-store-ops-reader",
        tenant_id="tenant-A",
        practice=Practice.RC,
        persona="store-ops-lead",
        allowed_classifications=(Classification.INTERNAL,),
        scopes=("practice:rc",),
        row_filters={"region": "US-WEST"},
    )
    roles.set_role("agent-1", role)
    assert roles.get_role("agent-1") is role
    assert roles.get_role("unknown") is None


def test_registered_count_test_helper() -> None:
    prov = MockEntraProvisioningProvider()
    assert prov.registered_count() == 0
    prov.register("a1", "t")
    prov.register("a2", "t")
    assert prov.registered_count() == 2
    prov.revoke("a1")
    assert prov.registered_count() == 1
