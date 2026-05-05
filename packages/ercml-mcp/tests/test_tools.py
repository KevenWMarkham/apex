"""Tests for ercml-mcp tools."""

from __future__ import annotations

import pytest

from ercml_mcp import (
    CONTRACTS,
    get_meter_by_key,
    list_grid_events_by_type,
    list_recent_readings,
)
from fabric_mcp import InMemoryFabricBackend, set_fabric_backend


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_fabric_backend(InMemoryFabricBackend(
        entities={
            ("meter", "m-1"): {"serial_number": "AMI-1"},
        },
        views={
            "gold_ercml.meter_reading": [
                {"meter_key": "m-1", "value": 10.0},
                {"meter_key": "m-1", "value": 11.0},
            ],
            "gold_ercml.grid_event": [
                {"event_type": "outage", "severity": 1},
                {"event_type": "outage", "severity": 2},
                {"event_type": "fault", "severity": 3},
            ],
        },
    ))


def test_get_meter() -> None:
    row = get_meter_by_key("m-1")
    assert row["serial_number"] == "AMI-1"


def test_list_readings() -> None:
    rows = list_recent_readings("m-1")
    assert len(rows) == 2


def test_list_outages_only() -> None:
    rows = list_grid_events_by_type("outage")
    assert len(rows) == 2
    assert all(r["event_type"] == "outage" for r in rows)


def test_er_scope() -> None:
    for c in CONTRACTS:
        assert "practice:er" in c.required_scopes
