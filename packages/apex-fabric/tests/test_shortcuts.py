"""Tests for apex_fabric.shortcuts — Sprint 14 Task 14.4."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from apex_fabric.shortcuts import (
    AdlsGen2Target,
    DataverseTarget,
    GoogleCloudStorageTarget,
    OneLakeTarget,
    S3Target,
    ShortcutClient,
    ShortcutPlan,
    ShortcutSpec,
    practice_reference_shortcuts,
)


# ---------------------------------------------------------------------------
# Target dataclasses → Atlas shape
# ---------------------------------------------------------------------------


def test_adls_gen2_target_shape() -> None:
    t = AdlsGen2Target(
        location="https://acct.dfs.core.windows.net",
        subpath="/fs/path",
        connection_id="conn-1",
    )
    assert t.to_atlas() == {
        "adlsGen2": {
            "location": "https://acct.dfs.core.windows.net",
            "subpath": "/fs/path",
            "connectionId": "conn-1",
        }
    }


def test_s3_target_shape() -> None:
    t = S3Target(
        location="https://b.s3.us-east-1.amazonaws.com",
        subpath="/p",
        connection_id="c",
    )
    assert "s3" in t.to_atlas()
    assert t.to_atlas()["s3"]["connectionId"] == "c"


def test_gcs_target_shape() -> None:
    t = GoogleCloudStorageTarget(
        location="https://storage.googleapis.com/b",
        subpath="/p",
        connection_id="c",
    )
    assert "googleCloudStorage" in t.to_atlas()


def test_dataverse_target_shape() -> None:
    t = DataverseTarget(
        environment_url="https://x.crm.dynamics.com",
        delta_lake_folder="folder/path",
        connection_id="c",
    )
    body = t.to_atlas()
    assert body["dataverse"]["environmentUrl"] == "https://x.crm.dynamics.com"
    assert body["dataverse"]["deltaLakeFolder"] == "folder/path"


def test_onelake_target_shape() -> None:
    t = OneLakeTarget(
        workspace_id="ws-1",
        item_id="lh-1",
        path="Tables/scml_sku",
    )
    assert t.to_atlas() == {
        "oneLake": {
            "workspaceId": "ws-1",
            "itemId": "lh-1",
            "path": "Tables/scml_sku",
        }
    }


# ---------------------------------------------------------------------------
# ShortcutSpec
# ---------------------------------------------------------------------------


def test_spec_to_create_body_minimal() -> None:
    spec = ShortcutSpec(
        workspace_id="ws", item_id="lh", name="sku", path="Tables",
        target=OneLakeTarget(workspace_id="src-ws", item_id="src-lh", path="Tables/sku"),
    )
    body = spec.to_create_body()
    assert body["name"] == "sku"
    assert body["path"] == "Tables"
    assert body["target"]["oneLake"]["workspaceId"] == "src-ws"
    assert "description" not in body  # omitted when empty


def test_spec_to_create_body_with_description() -> None:
    spec = ShortcutSpec(
        workspace_id="ws", item_id="lh", name="sku", path="Tables",
        target=OneLakeTarget(workspace_id="x", item_id="y", path="z"),
        description="canonical SKU shortcut",
    )
    body = spec.to_create_body()
    assert body["description"] == "canonical SKU shortcut"


# ---------------------------------------------------------------------------
# Stub HTTP client + ShortcutClient
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
    responses: dict[tuple[str, str], _StubResponse]
    calls: list[tuple[str, str, Any]]

    def __init__(self) -> None:
        self.responses = {}
        self.calls = []

    def get(self, url: str, headers: dict | None = None) -> _StubResponse:
        self.calls.append(("GET", url, None))
        return self.responses.get(("GET", url), _StubResponse(200, {"value": []}))

    def post(self, url: str, json: dict | None = None, headers: dict | None = None) -> _StubResponse:
        self.calls.append(("POST", url, json))
        return self.responses.get(
            ("POST", url),
            _StubResponse(201, {"id": "new", "name": (json or {}).get("name", "")}),
        )

    def delete(self, url: str, headers: dict | None = None) -> _StubResponse:
        self.calls.append(("DELETE", url, None))
        return self.responses.get(("DELETE", url), _StubResponse(204, None))


def _token() -> str:
    return "TEST-TOKEN"


def _spec(name: str = "sku") -> ShortcutSpec:
    return ShortcutSpec(
        workspace_id="ws-1",
        item_id="lh-1",
        name=name,
        path="Tables",
        target=OneLakeTarget(workspace_id="src-ws", item_id="src-lh", path=f"Tables/{name}"),
    )


def test_create_shortcut_posts_correct_url_and_body() -> None:
    stub = _StubClient()
    client = ShortcutClient(token_provider=_token, http_client=stub)
    client.create_shortcut(_spec("scml_sku"))
    method, url, body = stub.calls[0]
    assert method == "POST"
    assert url.endswith("/v1/workspaces/ws-1/items/lh-1/shortcuts")
    assert body["name"] == "scml_sku"
    assert body["target"]["oneLake"]["path"] == "Tables/scml_sku"


def test_list_shortcuts_returns_value_array() -> None:
    stub = _StubClient()
    stub.responses[
        ("GET", "https://api.fabric.microsoft.com/v1/workspaces/ws-1/items/lh-1/shortcuts")
    ] = _StubResponse(200, {"value": [{"name": "scml_sku", "path": "Tables"}]})
    client = ShortcutClient(token_provider=_token, http_client=stub)
    results = client.list_shortcuts("ws-1", "lh-1")
    assert len(results) == 1


def test_delete_shortcut_uses_path_and_name() -> None:
    stub = _StubClient()
    client = ShortcutClient(token_provider=_token, http_client=stub)
    client.delete_shortcut("ws-1", "lh-1", "scml_sku", "Tables")
    method, url, _ = stub.calls[0]
    assert method == "DELETE"
    assert url.endswith("/items/lh-1/shortcuts/Tables/scml_sku")


def test_ensure_shortcut_skips_when_existing() -> None:
    stub = _StubClient()
    stub.responses[
        ("GET", "https://api.fabric.microsoft.com/v1/workspaces/ws-1/items/lh-1/shortcuts")
    ] = _StubResponse(
        200,
        {"value": [{"name": "scml_sku", "path": "Tables", "id": "existing"}]},
    )
    client = ShortcutClient(token_provider=_token, http_client=stub)
    result = client.ensure_shortcut(_spec("scml_sku"))
    assert result["id"] == "existing"
    # No POST invoked
    assert all(c[0] != "POST" for c in stub.calls)


def test_ensure_shortcut_creates_when_missing() -> None:
    stub = _StubClient()
    client = ShortcutClient(token_provider=_token, http_client=stub)
    result = client.ensure_shortcut(_spec("new_table"))
    assert result["name"] == "new_table"
    assert any(c[0] == "POST" for c in stub.calls)


# ---------------------------------------------------------------------------
# ShortcutPlan + practice_reference_shortcuts
# ---------------------------------------------------------------------------


def test_shortcut_plan_to_payload() -> None:
    plan = ShortcutPlan()
    plan.add(_spec("a"))
    plan.add(_spec("b"))
    payload = plan.to_payload()
    assert len(payload) == 2
    assert payload[0]["name"] == "a"


def test_practice_reference_shortcuts_creates_one_per_table() -> None:
    plan = practice_reference_shortcuts(
        tenant_workspace_id="tenant-ws",
        tenant_lakehouse_id="tenant-lh",
        practice_reference_workspace_id="rc-ref-ws",
        practice_reference_lakehouse_id="rc-ref-lh",
        silver_table_names=["scml_sku", "scml_lot", "merml_price"],
    )
    assert len(plan.specs) == 3
    # Every spec points at the right tenant lakehouse and the right
    # source table in the Practice-reference workspace.
    for spec, table in zip(plan.specs, ["scml_sku", "scml_lot", "merml_price"], strict=True):
        assert spec.workspace_id == "tenant-ws"
        assert spec.item_id == "tenant-lh"
        assert spec.name == table
        assert spec.path == "Tables"
        assert isinstance(spec.target, OneLakeTarget)
        assert spec.target.workspace_id == "rc-ref-ws"
        assert spec.target.path == f"Tables/{table}"


def test_practice_reference_shortcuts_apply_via_client() -> None:
    """End-to-end smoke: plan.apply() invokes ShortcutClient idempotently."""
    plan = practice_reference_shortcuts(
        tenant_workspace_id="ws", tenant_lakehouse_id="lh",
        practice_reference_workspace_id="src-ws",
        practice_reference_lakehouse_id="src-lh",
        silver_table_names=["scml_sku"],
    )
    stub = _StubClient()
    client = ShortcutClient(token_provider=_token, http_client=stub)
    results = plan.apply(client)
    assert len(results) == 1
    assert results[0]["name"] == "scml_sku"


# ---------------------------------------------------------------------------
# Conformance — every Atlas-bound payload is JSON-serialisable
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_every_target_round_trips_through_json() -> None:
    import json
    targets = [
        AdlsGen2Target("https://x", "/y", "c"),
        S3Target("https://x", "/y", "c"),
        GoogleCloudStorageTarget("https://x", "/y", "c"),
        DataverseTarget("https://x", "f", "c"),
        OneLakeTarget("ws", "lh", "p"),
    ]
    for t in targets:
        body = t.to_atlas()
        assert json.loads(json.dumps(body)) == body
