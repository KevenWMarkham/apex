"""Integration tests for AgentIdentityProviderEntra against a real Lab Entra tenant.

Sprint 41 — Phase I.1 Production Entra Agent ID wiring per ADR-006 +
agent-identity-blueprints.md.

Run with:
    pip install -e 'apex-m[integration]'
    pytest -m integration apex-m/tests/integration/test_identity_entra.py

Skipped when:
    - APEX_TEST_TENANT_ID env var unset (default)
    - Or `pytest -m 'not integration'` is passed (default)

Environment variables required:
    APEX_TEST_TENANT_ID         Lab Entra tenant id (GUID)
    APEX_TEST_CLIENT_ID         Lab agent app registration client id
    AZURE_FEDERATED_TOKEN_FILE  WIF token file (set by GitHub Actions / Azure DevOps)

Or for local dev:
    az login --tenant <APEX_TEST_TENANT_ID>
"""
from __future__ import annotations

import os
import uuid
from typing import Iterator

import pytest


pytestmark = pytest.mark.integration


def _config_or_skip():
    tenant_id = os.environ.get("APEX_TEST_TENANT_ID")
    client_id = os.environ.get("APEX_TEST_CLIENT_ID")
    if not tenant_id or not client_id:
        pytest.skip(
            "APEX_TEST_TENANT_ID and APEX_TEST_CLIENT_ID required for integration tests. "
            "See apex-m/tests/integration/__init__.py for setup."
        )
    from apex_m.identity_entra import EntraAgentIdConfig
    return EntraAgentIdConfig(tenant_id=tenant_id, client_id=client_id)


@pytest.fixture
def provider():
    """Real `AgentIdentityProviderEntra` against Lab tenant."""
    config = _config_or_skip()
    from apex_m.identity_entra import AgentIdentityProviderEntra
    return AgentIdentityProviderEntra(config)


@pytest.fixture
def cleanup_blueprint_id() -> Iterator[str]:
    """Generate a unique-per-test blueprint id; revoke on teardown."""
    bp_id = f"apex-m-it-test-{uuid.uuid4().hex[:8]}"
    yield bp_id
    # Best-effort cleanup; per ADR-006 disable cascades.
    config = _config_or_skip()
    try:
        from apex_m.identity_entra import AgentIdentityProviderEntra
        provider = AgentIdentityProviderEntra(config)
        # Real impl would issue DELETE; this is the test-cleanup path.
        provider.revoke_identity(f"apex-m:it-test:{bp_id}", reason="integration-test-cleanup")
    except Exception:
        pass


def test_create_blueprint_idempotent(provider, cleanup_blueprint_id):
    """41.3.2: idempotent blueprint upsert."""
    from apex_core.protocols import AgentBlueprint
    bp = AgentBlueprint(
        blueprint_id=cleanup_blueprint_id,
        parent_id=None,
        label=f"APEX-M Integration Test {cleanup_blueprint_id}",
        notes="Created by Sprint 41 integration test; auto-revoked on teardown.",
    )
    # First call creates.
    result1 = provider.create_blueprint(bp)
    assert result1.blueprint_id == cleanup_blueprint_id
    # Second call updates (idempotent).
    result2 = provider.create_blueprint(bp)
    assert result2.blueprint_id == cleanup_blueprint_id


def test_provision_identity(provider, cleanup_blueprint_id):
    """41.3.2: identity provision."""
    from apex_core.protocols import AgentBlueprint
    provider.create_blueprint(AgentBlueprint(
        blueprint_id=cleanup_blueprint_id,
        parent_id=None,
        label="apex-m IT test",
    ))
    agent_id = f"apex-m:it-test:{cleanup_blueprint_id}:assess"
    identity = provider.provision_identity(blueprint_id=cleanup_blueprint_id, agent_id=agent_id)
    assert identity.agent_id == agent_id
    assert identity.blueprint_id == cleanup_blueprint_id
    assert identity.principal_id  # populated by Microsoft Graph


def test_get_identity_returns_provisioned(provider, cleanup_blueprint_id):
    """41.3.2: get_identity round-trip."""
    from apex_core.protocols import AgentBlueprint
    provider.create_blueprint(AgentBlueprint(blueprint_id=cleanup_blueprint_id, parent_id=None, label="x"))
    agent_id = f"apex-m:it-test:{cleanup_blueprint_id}:classify"
    provider.provision_identity(blueprint_id=cleanup_blueprint_id, agent_id=agent_id)
    looked_up = provider.get_identity(agent_id)
    assert looked_up is not None
    assert looked_up.agent_id == agent_id


def test_revoke_then_get_returns_none(provider, cleanup_blueprint_id):
    """41.3.2: revoke is observable."""
    from apex_core.protocols import AgentBlueprint
    provider.create_blueprint(AgentBlueprint(blueprint_id=cleanup_blueprint_id, parent_id=None, label="x"))
    agent_id = f"apex-m:it-test:{cleanup_blueprint_id}:decide"
    provider.provision_identity(blueprint_id=cleanup_blueprint_id, agent_id=agent_id)
    provider.revoke_identity(agent_id, reason="integration-test")
    # Real impl: get_identity returns None or marks revoked
    looked_up = provider.get_identity(agent_id)
    # Some Microsoft Graph endpoints return the soft-deleted record; verify
    # via a follow-up flag check rather than strict None.
    assert looked_up is None or getattr(looked_up, "deleted", False)


def test_list_blueprints_includes_apex_m_prefix_only(provider, cleanup_blueprint_id):
    """41.3.2: list_blueprints filter — only apex-m-* prefixed."""
    from apex_core.protocols import AgentBlueprint
    provider.create_blueprint(AgentBlueprint(blueprint_id=cleanup_blueprint_id, parent_id=None, label="x"))
    blueprints = provider.list_blueprints()
    assert any(bp.blueprint_id == cleanup_blueprint_id for bp in blueprints)
    assert all(bp.blueprint_id.startswith("apex-m") for bp in blueprints)


def test_obo_requires_operator_assertion(provider, cleanup_blueprint_id):
    """41.2.3: OBO flow raises ValueError without operator_assertion."""
    from apex_core.protocols import AgentBlueprint
    provider.create_blueprint(AgentBlueprint(blueprint_id=cleanup_blueprint_id, parent_id=None, label="x"))
    agent_id = f"apex-m:it-test:{cleanup_blueprint_id}:act"
    provider.provision_identity(blueprint_id=cleanup_blueprint_id, agent_id=agent_id)
    with pytest.raises(ValueError, match="operator_assertion"):
        provider.acquire_obo_token(
            agent_id=agent_id,
            operator_principal="testuser@contoso.com",
            target_resource="https://graph.microsoft.com/.default",
        )
