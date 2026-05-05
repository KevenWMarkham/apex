"""Tests for vendor-portal-mcp tools."""

from __future__ import annotations

import pytest

from mcp_common import McpError, McpErrorCode
from vendor_portal_mcp import (
    CONTRACTS,
    InMemoryVendorBackend,
    get_vendor_compliance_score,
    get_vendor_status,
    list_vendor_orders,
    set_vendor_backend,
)


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_vendor_backend(InMemoryVendorBackend(
        statuses={
            "v-001": {"vendor_id": "v-001", "active": True, "tier": "primary"},
        },
        orders_by_vendor={
            "v-001": [
                {"order_id": "O-1", "total": 5000},
                {"order_id": "O-2", "total": 2500},
            ],
        },
        compliance={
            "v-001": {"vendor_id": "v-001", "score": 92, "last_audit": "2026-03-01"},
        },
    ))


def test_get_status() -> None:
    row = get_vendor_status("v-001")
    assert row["tier"] == "primary"


def test_get_status_missing() -> None:
    with pytest.raises(McpError) as exc:
        get_vendor_status("unknown")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_list_orders() -> None:
    rows = list_vendor_orders("v-001")
    assert len(rows) == 2


def test_list_orders_empty() -> None:
    rows = list_vendor_orders("unknown")
    assert rows == []


def test_compliance_score() -> None:
    row = get_vendor_compliance_score("v-001")
    assert row["score"] == 92


def test_compliance_carries_trade_secret_classification() -> None:
    from apex_core.types import Classification
    contract = next(c for c in CONTRACTS if "compliance" in c.name)
    assert Classification.TRADE_SECRET in contract.classification_propagation


def test_contracts() -> None:
    assert len(CONTRACTS) == 3
