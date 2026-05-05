"""Tests for fabric-mcp tools."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from fabric_mcp import (
    CONTRACTS,
    InMemoryFabricBackend,
    get_entity_by_key,
    list_classifications,
    query_gold_view,
    set_fabric_backend,
)
from mcp_common import McpError, McpErrorCode


@pytest.fixture
def backend() -> InMemoryFabricBackend:
    b = InMemoryFabricBackend(
        entities={
            ("sku", "sku:001"): {"sku_natural": "SKU-001", "status": "ACTIVE"},
        },
        views={
            "gold.v_sku": [
                {"sku_natural": "SKU-001", "status": "ACTIVE"},
                {"sku_natural": "SKU-002", "status": "INACTIVE"},
                {"sku_natural": "SKU-003", "status": "ACTIVE"},
            ],
        },
        field_classifications={
            "customer": {
                "email_token": Classification.PII,
                "birth_year": Classification.INTERNAL,
            },
        },
    )
    set_fabric_backend(b)
    return b


def test_get_entity_by_key(backend: InMemoryFabricBackend) -> None:
    row = get_entity_by_key("sku", "sku:001")
    assert row["sku_natural"] == "SKU-001"


def test_get_entity_missing_raises(backend: InMemoryFabricBackend) -> None:
    with pytest.raises(McpError) as exc:
        get_entity_by_key("sku", "nope")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_query_gold_view_filter(backend: InMemoryFabricBackend) -> None:
    rows = query_gold_view("gold.v_sku", {"status": "ACTIVE"})
    assert len(rows) == 2


def test_query_gold_view_respects_limit(backend: InMemoryFabricBackend) -> None:
    rows = query_gold_view("gold.v_sku", {}, limit=1)
    assert len(rows) == 1


def test_query_gold_view_bad_limit(backend: InMemoryFabricBackend) -> None:
    with pytest.raises(McpError) as exc:
        query_gold_view("gold.v_sku", {}, limit=0)
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_list_classifications(backend: InMemoryFabricBackend) -> None:
    m = list_classifications("customer")
    assert m["email_token"] == "pii"
    assert m["birth_year"] == "internal"


def test_contracts_exported() -> None:
    names = {c.name for c in CONTRACTS}
    assert "fabric-mcp.get_entity_by_key" in names
    assert "fabric-mcp.query_gold_view" in names
    assert "fabric-mcp.list_classifications" in names
