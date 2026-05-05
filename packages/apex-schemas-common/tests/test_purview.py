"""Tests for ``apex_schemas_common.purview.build_purview_payload``."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, build_purview_payload
from apex_schemas_common.standards import GTIN14


class _SKU(CanonicalEntity):
    sku_natural: str = Field(..., description="Source natural key.")
    gtin: GTIN14 | None = Field(None)
    unit_cost_token: Annotated[str, Classification.TRADE_SECRET] | None = Field(None)


def test_payload_has_entity_and_family() -> None:
    payload = build_purview_payload(_SKU, family="scml")
    assert payload["entity"] == "_sku"
    assert payload["family"] == "scml"


def test_classification_is_discovered() -> None:
    payload = build_purview_payload(_SKU)
    by_name = {f["name"]: f for f in payload["fields"]}
    assert by_name["unit_cost_token"]["classification"] == "trade_secret"


def test_default_classification_applied() -> None:
    payload = build_purview_payload(_SKU)
    by_name = {f["name"]: f for f in payload["fields"]}
    assert by_name["sku_natural"]["classification"] == "internal"


def test_standard_ref_is_discovered() -> None:
    payload = build_purview_payload(_SKU)
    by_name = {f["name"]: f for f in payload["fields"]}
    assert "standard" in by_name["gtin"]
    assert by_name["gtin"]["standard"]["standard_id"] == "gs1-gtin"
    assert by_name["gtin"]["standard"]["identifier"] == "GTIN-14"


def test_required_vs_optional() -> None:
    payload = build_purview_payload(_SKU)
    by_name = {f["name"]: f for f in payload["fields"]}
    assert by_name["sku_natural"]["required"] is True
    assert by_name["gtin"]["required"] is False
