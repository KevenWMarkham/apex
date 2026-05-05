"""Tests for axlecml-mcp tools."""

from __future__ import annotations

import pytest

from axlecml_mcp import (
    CONTRACTS,
    get_equipment_by_key,
    list_production_events,
    list_recent_quality_results,
)
from fabric_mcp import InMemoryFabricBackend, set_fabric_backend


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_fabric_backend(InMemoryFabricBackend(
        entities={
            ("equipment", "eq-1"): {"name": "CNC Lathe 01", "isa95_id": "EQ-1"},
        },
        views={
            "gold_axlecml.production_event": [
                {"event_type": "BATCH_START", "equipment_key": "eq-1"},
                {"event_type": "BATCH_END", "equipment_key": "eq-1"},
            ],
            "gold_axlecml.quality_result": [
                {"test_code": "TENSILE", "equipment_key": "eq-1", "status": "pass"},
            ],
        },
    ))


def test_get_equipment() -> None:
    row = get_equipment_by_key("eq-1")
    assert row["name"] == "CNC Lathe 01"


def test_list_production_events() -> None:
    rows = list_production_events("eq-1")
    assert len(rows) == 2


def test_list_quality_results() -> None:
    rows = list_recent_quality_results("eq-1")
    assert rows[0]["test_code"] == "TENSILE"


def test_axle_scope() -> None:
    for c in CONTRACTS:
        assert "practice:axle" in c.required_scopes
