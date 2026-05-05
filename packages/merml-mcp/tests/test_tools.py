"""Tests for merml-mcp tools."""

from __future__ import annotations

import pytest

from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from mcp_common import McpError, McpErrorCode
from merml_mcp import (
    CONTRACTS,
    get_current_price,
    list_active_promotions,
    list_recent_markdowns,
)


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_fabric_backend(InMemoryFabricBackend(
        views={
            "gold_merml.price": [
                {"sku_key": "sku-1", "kind": "REGULAR", "amount": 9.99, "location_key": None},
            ],
            "gold_merml.promotion": [
                {"promotion_natural": "P-1", "is_active": True},
                {"promotion_natural": "P-2", "is_active": False},
            ],
            "gold_merml.markdown": [
                {"sku_key": "sku-1", "reason": "SEASONAL"},
                {"sku_key": "sku-1", "reason": "OVERSTOCK"},
                {"sku_key": "sku-2", "reason": "DAMAGED"},
            ],
        },
    ))


def test_get_current_price() -> None:
    row = get_current_price("sku-1")
    assert row["amount"] == 9.99


def test_get_price_missing() -> None:
    with pytest.raises(McpError) as exc:
        get_current_price("nope")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_list_active_promotions() -> None:
    rows = list_active_promotions()
    assert len(rows) == 1
    assert rows[0]["promotion_natural"] == "P-1"


def test_list_recent_markdowns_sku() -> None:
    rows = list_recent_markdowns("sku-1")
    assert len(rows) == 2


def test_contracts() -> None:
    assert len(CONTRACTS) == 3
