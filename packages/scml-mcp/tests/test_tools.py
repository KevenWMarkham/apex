"""Tests for scml-mcp tools."""

from __future__ import annotations

import pytest

from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from mcp_common import McpError, McpErrorCode
from scml_mcp import (
    CONTRACTS,
    get_sku_by_key,
    list_shipments_by_destination,
    list_skus_by_supplier,
)


@pytest.fixture(autouse=True)
def _seed_fabric() -> InMemoryFabricBackend:
    b = InMemoryFabricBackend(
        entities={
            ("sku", "SKU-001"): {"sku_natural": "SKU-001", "supplier_key": "sup-1"},
        },
        views={
            "gold_scml.sku": [
                {"sku_natural": "SKU-001", "supplier_key": "sup-1"},
                {"sku_natural": "SKU-002", "supplier_key": "sup-1"},
                {"sku_natural": "SKU-003", "supplier_key": "sup-2"},
            ],
            "gold_scml.shipment": [
                {"shipment_natural": "SHIP-01", "destination_key": "loc-A"},
                {"shipment_natural": "SHIP-02", "destination_key": "loc-B"},
            ],
        },
    )
    set_fabric_backend(b)
    return b


def test_get_sku_by_key() -> None:
    row = get_sku_by_key("SKU-001")
    assert row["sku_natural"] == "SKU-001"


def test_get_sku_missing_raises() -> None:
    with pytest.raises(McpError) as exc:
        get_sku_by_key("NO-SUCH-SKU")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_list_skus_by_supplier_filters() -> None:
    rows = list_skus_by_supplier("sup-1")
    assert len(rows) == 2
    assert all(r["supplier_key"] == "sup-1" for r in rows)


def test_list_shipments_by_destination() -> None:
    rows = list_shipments_by_destination("loc-A")
    assert len(rows) == 1
    assert rows[0]["shipment_natural"] == "SHIP-01"


def test_contracts_declare_rc_scope() -> None:
    for c in CONTRACTS:
        assert "practice:rc" in c.required_scopes
