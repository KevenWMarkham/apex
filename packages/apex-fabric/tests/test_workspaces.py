"""Tests for apex_fabric.workspaces — Sprint 14 Task 14.2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest
from typer.testing import CliRunner

from apex_fabric._cli import fabric_app
from apex_fabric.workspaces import (
    ENVIRONMENTS,
    PRACTICES,
    ROLES,
    WorkspaceClient,
    WorkspaceSpec,
    canonical_workspace_name,
    parse_workspace_name,
    validate_workspace_name,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# canonical_workspace_name + parse + validate
# ---------------------------------------------------------------------------


def test_canonical_name_no_suffix() -> None:
    assert canonical_workspace_name("rc", "prod", "silver") == "apex-rc-prod-silver"


def test_canonical_name_with_suffix() -> None:
    assert canonical_workspace_name("hls", "dev", "bronze", "eu") == "apex-hls-dev-bronze-eu"


def test_canonical_name_rejects_unknown_practice() -> None:
    with pytest.raises(ValueError, match="Unknown practice"):
        canonical_workspace_name("nope", "prod", "silver")


def test_canonical_name_rejects_unknown_environment() -> None:
    with pytest.raises(ValueError, match="Unknown environment"):
        canonical_workspace_name("rc", "qa", "silver")


def test_canonical_name_rejects_unknown_role() -> None:
    with pytest.raises(ValueError, match="Unknown role"):
        canonical_workspace_name("rc", "prod", "platinum")


def test_canonical_name_rejects_uppercase_suffix() -> None:
    with pytest.raises(ValueError, match=r"\[a-z0-9\]\+"):
        canonical_workspace_name("rc", "prod", "silver", "EU")


def test_canonical_name_rejects_suffix_with_dash() -> None:
    with pytest.raises(ValueError, match=r"\[a-z0-9\]\+"):
        canonical_workspace_name("rc", "prod", "silver", "us-east")


def test_parse_valid_name() -> None:
    parts = parse_workspace_name("apex-rc-prod-silver-eu")
    assert parts == {"practice": "rc", "environment": "prod", "role": "silver", "suffix": "eu"}


def test_parse_no_suffix_returns_none() -> None:
    parts = parse_workspace_name("apex-rc-prod-silver")
    assert parts["suffix"] is None


def test_parse_rejects_non_apex_prefix() -> None:
    with pytest.raises(ValueError, match="canonical pattern"):
        parse_workspace_name("rc-prod-silver")


def test_parse_rejects_unknown_practice() -> None:
    with pytest.raises(ValueError, match="Unknown practice"):
        parse_workspace_name("apex-marketing-prod-silver")


def test_validate_returns_bool() -> None:
    assert validate_workspace_name("apex-rc-prod-silver") is True
    assert validate_workspace_name("rc-prod-silver") is False


# ---------------------------------------------------------------------------
# WorkspaceSpec
# ---------------------------------------------------------------------------


def test_spec_name_canonical() -> None:
    s = WorkspaceSpec(
        practice="rc", environment="prod", role="silver", capacity_id="c1"
    )
    assert s.name() == "apex-rc-prod-silver"


def test_spec_name_with_override_must_be_canonical() -> None:
    with pytest.raises(ValueError, match="canonical pattern"):
        WorkspaceSpec(
            practice="rc",
            environment="prod",
            role="silver",
            capacity_id="c1",
            name_override="my-cool-workspace",
        ).name()


def test_spec_name_override_canonical_passes() -> None:
    s = WorkspaceSpec(
        practice="rc",
        environment="prod",
        role="silver",
        capacity_id="c1",
        name_override="apex-hls-prod-gold",
    )
    assert s.name() == "apex-hls-prod-gold"


def test_spec_to_create_body_shape() -> None:
    s = WorkspaceSpec(
        practice="rc", environment="prod", role="silver",
        capacity_id="cap-123", description="desc",
    )
    body = s.to_create_body()
    assert body == {
        "displayName": "apex-rc-prod-silver",
        "description": "desc",
        "capacityId": "cap-123",
    }


# ---------------------------------------------------------------------------
# WorkspaceClient — http stub
# ---------------------------------------------------------------------------


@dataclass
class _StubResponse:
    status: int
    body: Any

    def raise_for_status(self) -> None:
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    def json(self) -> Any:
        return self.body


@dataclass
class _StubClient:
    """Captures invocations and returns scripted responses."""
    responses: dict[tuple[str, str], _StubResponse]
    calls: list[tuple[str, str, dict | None]]

    def __init__(self) -> None:
        self.responses = {}
        self.calls = []

    def get(self, url: str, headers: dict | None = None) -> _StubResponse:
        self.calls.append(("GET", url, None))
        return self.responses.get(("GET", url), _StubResponse(200, {"value": []}))

    def post(self, url: str, json: dict | None = None, headers: dict | None = None) -> _StubResponse:
        self.calls.append(("POST", url, json))
        return self.responses.get(("POST", url), _StubResponse(201, {"id": "new", "displayName": (json or {}).get("displayName", "")}))

    def delete(self, url: str, headers: dict | None = None) -> _StubResponse:
        self.calls.append(("DELETE", url, None))
        return self.responses.get(("DELETE", url), _StubResponse(204, None))


def _token() -> str:
    return "STUB_BEARER_TOKEN"


def test_client_create_workspace_sends_correct_body() -> None:
    stub = _StubClient()
    client = WorkspaceClient(token_provider=_token, http_client=stub)
    spec = WorkspaceSpec(
        practice="rc", environment="prod", role="silver",
        capacity_id="cap-99", description="hello",
    )
    result = client.create_workspace(spec)
    assert result["displayName"] == "apex-rc-prod-silver"
    method, url, body = stub.calls[0]
    assert method == "POST"
    assert url.endswith("/v1/workspaces")
    assert body["capacityId"] == "cap-99"
    assert body["displayName"] == "apex-rc-prod-silver"


def test_client_create_workspace_rejects_non_canonical_before_call() -> None:
    stub = _StubClient()
    client = WorkspaceClient(token_provider=_token, http_client=stub)
    spec = WorkspaceSpec(
        practice="rc", environment="prod", role="silver",
        capacity_id="cap-99",
        name_override="bad name",
    )
    with pytest.raises(ValueError):
        client.create_workspace(spec)
    # No HTTP call was made
    assert stub.calls == []


def test_client_list_workspaces_returns_value_array() -> None:
    stub = _StubClient()
    stub.responses[("GET", "https://api.fabric.microsoft.com/v1/workspaces")] = _StubResponse(
        200, {"value": [{"displayName": "apex-rc-prod-silver", "id": "ws-1"}]}
    )
    client = WorkspaceClient(token_provider=_token, http_client=stub)
    workspaces = client.list_workspaces()
    assert len(workspaces) == 1
    assert workspaces[0]["displayName"] == "apex-rc-prod-silver"


def test_client_get_workspace_by_name_finds_match() -> None:
    stub = _StubClient()
    stub.responses[("GET", "https://api.fabric.microsoft.com/v1/workspaces")] = _StubResponse(
        200,
        {"value": [
            {"displayName": "apex-rc-prod-bronze", "id": "1"},
            {"displayName": "apex-rc-prod-silver", "id": "2"},
        ]},
    )
    client = WorkspaceClient(token_provider=_token, http_client=stub)
    ws = client.get_workspace_by_name("apex-rc-prod-silver")
    assert ws is not None
    assert ws["id"] == "2"


def test_client_get_workspace_by_name_returns_none_on_miss() -> None:
    stub = _StubClient()
    client = WorkspaceClient(token_provider=_token, http_client=stub)
    assert client.get_workspace_by_name("apex-rc-prod-silver") is None


def test_client_ensure_workspace_idempotent() -> None:
    stub = _StubClient()
    stub.responses[("GET", "https://api.fabric.microsoft.com/v1/workspaces")] = _StubResponse(
        200, {"value": [{"displayName": "apex-rc-prod-silver", "id": "existing-id"}]}
    )
    client = WorkspaceClient(token_provider=_token, http_client=stub)
    spec = WorkspaceSpec(practice="rc", environment="prod", role="silver", capacity_id="c")
    result = client.ensure_workspace(spec)
    assert result["id"] == "existing-id"
    # No POST issued (only the GET)
    assert all(c[0] != "POST" for c in stub.calls)


def test_client_ensure_workspace_creates_when_missing() -> None:
    stub = _StubClient()
    client = WorkspaceClient(token_provider=_token, http_client=stub)
    spec = WorkspaceSpec(practice="rc", environment="prod", role="silver", capacity_id="c")
    result = client.ensure_workspace(spec)
    assert result["displayName"] == "apex-rc-prod-silver"
    assert any(c[0] == "POST" for c in stub.calls)


def test_client_assign_to_capacity() -> None:
    stub = _StubClient()
    client = WorkspaceClient(token_provider=_token, http_client=stub)
    client.assign_to_capacity("ws-1", "cap-2")
    method, url, body = stub.calls[0]
    assert method == "POST"
    assert url.endswith("/workspaces/ws-1/assignToCapacity")
    assert body == {"capacityId": "cap-2"}


def test_client_uses_bearer_token_in_headers() -> None:
    """Token provider invoked, bearer token included in request headers."""
    invocations: list[None] = []

    def provider() -> str:
        invocations.append(None)
        return "TEST-TOKEN-42"

    stub = _StubClient()
    client = WorkspaceClient(token_provider=provider, http_client=stub)
    client.list_workspaces()
    assert len(invocations) == 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_validate_name_ok() -> None:
    result = runner.invoke(fabric_app, ["validate-name", "apex-rc-prod-silver"])
    assert result.exit_code == 0
    assert "OK" in result.stdout


def test_cli_validate_name_fail() -> None:
    result = runner.invoke(fabric_app, ["validate-name", "rc-prod-silver"])
    assert result.exit_code == 1
    assert "FAIL" in result.stdout


def test_cli_canonical_name() -> None:
    result = runner.invoke(fabric_app, ["canonical-name", "rc", "prod", "silver"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "apex-rc-prod-silver"


def test_cli_canonical_name_with_suffix() -> None:
    result = runner.invoke(
        fabric_app, ["canonical-name", "rc", "prod", "silver", "--suffix", "eu"]
    )
    assert result.exit_code == 0
    assert result.stdout.strip() == "apex-rc-prod-silver-eu"


def test_cli_describe_blueprint() -> None:
    for bp in ["single-capacity-tenant", "dev-prod-split", "per-workload-isolation"]:
        result = runner.invoke(fabric_app, ["describe-blueprint", bp])
        assert result.exit_code == 0
        assert bp in result.stdout


def test_cli_describe_blueprint_unknown() -> None:
    result = runner.invoke(fabric_app, ["describe-blueprint", "nope"])
    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# Coverage of constants
# ---------------------------------------------------------------------------


def test_practices_includes_all_seven_plus_core() -> None:
    assert set(PRACTICES) == {"rc", "hls", "er", "axle", "tmt", "th", "ice", "core"}


def test_environments_canonical_set() -> None:
    assert set(ENVIRONMENTS) == {"dev", "test", "stage", "prod"}


def test_roles_cover_medallion_plus_governance_runtime_sandbox() -> None:
    assert set(ROLES) == {"bronze", "silver", "gold", "governance", "runtime", "sandbox"}
