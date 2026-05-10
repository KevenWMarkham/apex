"""Tests for the end-to-end POST /api/deployments orchestration (Sprint 46.3)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from apex_wizard.deployments import _reset_deployment_store_for_test
from apex_wizard.main import app


@pytest.fixture
def client(monkeypatch) -> TestClient:
    # Force mock mode so we don't need az on PATH
    monkeypatch.setenv("APEX_FORCE_MOCK", "true")
    _reset_deployment_store_for_test()
    return TestClient(app)


# ---------------------------------------------------------------------------
# Happy path — PSG green → what-if → deploy → record persisted
# ---------------------------------------------------------------------------


def test_create_deployment_happy_path_succeeds(client: TestClient) -> None:
    body = {
        "tenant": "bigbox-prod",
        "wave": "w2",
        "selections": [
            {
                "service_code": "RC-E2E-03",
                "featured_scenarios": ["rc-cold-chain-excursion-mid-shift"],
            },
        ],
        "operator": "marisol.reyes@labtenant.onmicrosoft.com",
        "note": "first deploy",
    }
    response = client.post("/api/deployments", json=body)
    assert response.status_code == 200
    record = response.json()
    assert record["status"] == "succeeded"
    assert record["tenant"] == "bigbox-prod"
    assert record["wave"] == "w2"
    assert record["operator"] == "marisol.reyes@labtenant.onmicrosoft.com"
    # bicep what-if summary attached
    assert record["bicep_what_if_summary"]["mode"] == "mock"
    # audit row id is the deploy's correlation id
    assert record["audit_row_id"].startswith("mock-")


# ---------------------------------------------------------------------------
# Destructive-changes second-confirm gate
# ---------------------------------------------------------------------------


def test_destructive_changes_require_second_confirm(client: TestClient, monkeypatch) -> None:
    """When what-if reports Delete, the operator must re-submit with confirm flag."""
    # Patch the default runner to return destructive changes
    from apex_wizard import bicep_runner

    def destructive_factory(*, log=None):
        return bicep_runner.MockBicepRunner(preset_changes=(
            bicep_runner.WhatIfChange(
                change_kind="Delete",
                resource_id="/r-doomed",
                resource_type="Microsoft.Storage/storageAccounts",
            ),
        ))
    monkeypatch.setattr(bicep_runner, "get_default_runner", destructive_factory)
    # The deployments module imports get_default_runner at call time so
    # monkey-patching the module re-exports works.
    from apex_wizard import deployments as deployments_mod
    monkeypatch.setattr(deployments_mod, "get_default_runner", destructive_factory, raising=False)
    # Also patch where create_deployment imports from inside the function
    # body — the test client uses the apex_wizard.main app which re-imports.
    import apex_wizard.bicep_runner as br_mod
    monkeypatch.setattr(br_mod, "get_default_runner", destructive_factory)

    body = {
        "tenant": "bigbox-prod",
        "wave": "w2",
        "selections": [{"service_code": "RC-E2E-03", "featured_scenarios": ["x"]}],
        "operator": "op@x.com",
        "note": "no confirmation",
    }
    response = client.post("/api/deployments", json=body)
    assert response.status_code == 412
    detail = response.json()["detail"]
    assert detail["error"] == "destructive_changes_pending_confirm"


def test_destructive_changes_proceed_with_confirm_flag(client: TestClient, monkeypatch) -> None:
    from apex_wizard import bicep_runner
    import apex_wizard.bicep_runner as br_mod

    def destructive_factory(*, log=None):
        return bicep_runner.MockBicepRunner(preset_changes=(
            bicep_runner.WhatIfChange(
                change_kind="Delete",
                resource_id="/r-doomed",
                resource_type="Microsoft.Storage/storageAccounts",
            ),
        ))
    monkeypatch.setattr(br_mod, "get_default_runner", destructive_factory)

    body = {
        "tenant": "bigbox-prod",
        "wave": "w2",
        "selections": [{"service_code": "RC-E2E-03", "featured_scenarios": ["x"]}],
        "operator": "op@x.com",
        "note": "reviewed diff confirm_destructive=true",
    }
    response = client.post("/api/deployments", json=body)
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Record listing + retrieval
# ---------------------------------------------------------------------------


def test_list_deployments_filters_by_tenant(client: TestClient) -> None:
    for tenant in ("bigbox-prod", "smallchain-prod"):
        client.post("/api/deployments", json={
            "tenant": tenant,
            "wave": "w2",
            "selections": [{"service_code": "RC-E2E-03", "featured_scenarios": ["x"]}],
            "operator": "op@x.com",
        })
    all_resp = client.get("/api/deployments")
    assert all_resp.status_code == 200
    assert len(all_resp.json()) == 2

    filtered_resp = client.get("/api/deployments?tenant=bigbox-prod")
    assert filtered_resp.status_code == 200
    rows = filtered_resp.json()
    assert len(rows) == 1
    assert rows[0]["tenant"] == "bigbox-prod"


def test_get_deployment_returns_record(client: TestClient) -> None:
    create_resp = client.post("/api/deployments", json={
        "tenant": "bigbox-prod",
        "wave": "w2",
        "selections": [{"service_code": "RC-E2E-03", "featured_scenarios": ["x"]}],
        "operator": "op@x.com",
    })
    deployment_id = create_resp.json()["id"]
    get_resp = client.get(f"/api/deployments/{deployment_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == deployment_id


def test_get_deployment_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get("/api/deployments/nope")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Health endpoint + security-gate endpoint sanity
# ---------------------------------------------------------------------------


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_security_gate_endpoint_returns_15_gates(client: TestClient) -> None:
    response = client.get("/api/security-gate?tenant=bigbox-prod")
    assert response.status_code == 200
    body = response.json()
    assert body["tenant"] == "bigbox-prod"
    assert len(body["gates"]) == 15


def test_security_gate_with_context_evaluates_psg_15(client: TestClient) -> None:
    payload = {
        "tenant": "bigbox-prod",
        "use_case_data": {
            "use_case_id": "rc-e2e-05--bigbox-prod",
            "substrate": "prod",
            "personas_active": [{"id": "jamie-oconnor-store-manager"}],
            "persona_principal_bindings": {
                "jamie-oconnor-store-manager": {
                    "binding_mode": "entra_group",
                    "entra_group_object_id": "group-001",
                },
            },
        },
    }
    response = client.post("/api/security-gate/with-context", json=payload)
    assert response.status_code == 200
    body = response.json()
    psg_15 = next(g for g in body["gates"] if g["gate_id"] == "PSG-15")
    assert psg_15["status"] == "green"
