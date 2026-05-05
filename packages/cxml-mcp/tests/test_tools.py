"""Tests for cxml-mcp tools."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from cxml_mcp import (
    CONTRACTS,
    get_customer_by_key,
    list_interactions_by_customer,
    list_orders_by_customer,
)
from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from mcp_common import McpError, McpErrorCode


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_fabric_backend(InMemoryFabricBackend(
        entities={
            ("customer", "cust-1"): {"customer_natural": "cust-1", "email_token": "tok_xyz"},
        },
        views={
            "gold_cxml.order": [
                {"order_natural": "O-1", "customer_key": "cust-1"},
                {"order_natural": "O-2", "customer_key": "cust-1"},
            ],
            "gold_cxml.interaction": [
                {"event_id": "i-1", "customer_key": "cust-1", "channel": "WEB"},
            ],
        },
    ))


def test_get_customer() -> None:
    row = get_customer_by_key("cust-1")
    assert row["email_token"].startswith("tok_")


def test_get_customer_missing() -> None:
    with pytest.raises(McpError) as exc:
        get_customer_by_key("nope")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_list_orders() -> None:
    rows = list_orders_by_customer("cust-1")
    assert len(rows) == 2


def test_list_interactions() -> None:
    rows = list_interactions_by_customer("cust-1")
    assert rows[0]["channel"] == "WEB"


def test_pci_classification_on_orders() -> None:
    orders_contract = next(c for c in CONTRACTS if "orders" in c.name)
    assert Classification.PCI in orders_contract.classification_propagation
