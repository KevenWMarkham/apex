"""Tests for apex_identity.lattice.evaluate_visibility."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel

from apex_core.types import Classification, Practice
from apex_identity import evaluate_visibility
from mcp_common import ScopeContext


class _Widget(BaseModel):
    name: str
    unit_retail: float
    unit_cost: Annotated[float, Classification.TRADE_SECRET]
    customer_email: Annotated[str, Classification.PII]
    internal_note: Annotated[str, Classification.INTERNAL] | None = None
    region: str


def _row() -> dict:
    return {
        "name": "Widget",
        "unit_retail": 9.99,
        "unit_cost": 2.50,
        "customer_email": "a@b.com",
        "internal_note": "restock soon",
        "region": "US-WEST",
    }


def _scope(
    *, classifications: set[Classification] | None = None,
    row_filters: dict[str, str] | None = None,
) -> ScopeContext:
    return ScopeContext(
        tenant_id="t",
        practice=Practice.RC,
        classification_visibility=frozenset(classifications or set()),
        row_filters=row_filters or {},
    )


def test_no_classification_always_visible() -> None:
    d = evaluate_visibility(_Widget, _row(), _scope())
    assert "name" in d.visible_fields
    assert "unit_retail" in d.visible_fields


def test_classification_without_scope_masked() -> None:
    d = evaluate_visibility(_Widget, _row(), _scope())
    assert "unit_cost" in d.masked_fields
    assert "customer_email" in d.masked_fields
    assert "internal_note" in d.masked_fields


def test_classification_in_scope_visible() -> None:
    d = evaluate_visibility(
        _Widget, _row(),
        _scope(classifications={Classification.TRADE_SECRET, Classification.PII, Classification.INTERNAL}),
    )
    assert d.masked_fields == frozenset()
    assert "unit_cost" in d.visible_fields
    assert "customer_email" in d.visible_fields


def test_row_filter_match() -> None:
    d = evaluate_visibility(
        _Widget, _row(), _scope(row_filters={"region": "US-WEST"}),
    )
    assert d.row_visible
    assert d.row_filter_reason is None


def test_row_filter_mismatch() -> None:
    d = evaluate_visibility(
        _Widget, _row(), _scope(row_filters={"region": "EU-EAST"}),
    )
    assert not d.row_visible
    assert d.row_filter_reason is not None
    assert "region" in d.row_filter_reason


def test_row_filter_missing_column_fails_closed() -> None:
    d = evaluate_visibility(
        _Widget, _row(), _scope(row_filters={"missing_column": "X"}),
    )
    assert not d.row_visible
