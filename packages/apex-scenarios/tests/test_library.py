"""Tests for apex_scenarios.library."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from apex_scenarios.library import (
    ScenarioIndex,
    load_featured_chains,
    load_scenario_library,
    write_extended_library,
)
from apex_scenarios.models import Scenario

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_mini_library_parses_three_scenarios() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    assert len(scenarios) == 3
    practices = {s.practice for s in scenarios}
    assert practices == {"RC", "HLS"}


def test_load_mini_library_stamps_practice_from_dict_key() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    rc = [s for s in scenarios if s.practice == "RC"]
    hls = [s for s in scenarios if s.practice == "HLS"]
    assert len(rc) == 2
    assert len(hls) == 1
    assert rc[0].title == "Assortment rationalization"


def test_load_mini_library_rejects_unknown_practice(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"BAD_PRACTICE": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="unknown practice key"):
        load_scenario_library(bad)


def test_load_mini_library_rejects_non_mapping(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps([]), encoding="utf-8")
    with pytest.raises(ValueError, match="expected mapping"):
        load_scenario_library(bad)


def test_index_basic_counts() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    assert idx.total == 3
    counts = idx.practice_counts()
    assert counts["RC"] == 2
    assert counts["HLS"] == 1
    # Practices with no scenarios still appear with count 0
    assert counts["ER"] == 0


def test_index_by_service_code() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    matches = idx.by_service("RC-E2E-06")
    assert len(matches) == 1
    assert matches[0].title == "Cold-chain excursion response"


def test_index_filter_combinations() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    rc_matching = idx.filter(practice="RC", title_contains="cold")
    assert len(rc_matching) == 1
    none_matching = idx.filter(practice="HLS", service_code="RC-E2E-03")
    assert len(none_matching) == 0


def test_index_wave_completion_status() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    # Initially all rows have empty W1/W2/W3
    idx = ScenarioIndex(scenarios)
    assert len(idx.with_full_wave_data()) == 0
    assert len(idx.missing_wave_data()) == 3


def test_index_wave_completion_after_population() -> None:
    populated = [
        Scenario(
            title="t", service_code="RC-E2E-03", brief="b", kpi="k", kpi_direction="up",
            practice="RC", w1="x", w2="y", w3="z",
        ),
        Scenario(
            title="t2", service_code="RC-E2E-04", brief="b", kpi="k", kpi_direction="up",
            practice="RC", w1="x", w2="", w3="z",
        ),
    ]
    idx = ScenarioIndex(populated)
    assert len(idx.with_full_wave_data()) == 1
    assert len(idx.missing_wave_data()) == 1


def test_load_featured_chains_mini() -> None:
    chains = load_featured_chains(FIXTURES / "featured-chains-mini.json")
    assert len(chains) == 2
    assert chains[0].Service == "RC-E2E-06"
    assert chains[0].Use_Case.startswith("Excursion")


def test_write_extended_library_round_trip(tmp_path: Path) -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    out = tmp_path / "extended.json"
    write_extended_library(scenarios, out)
    assert out.exists()
    # Read back and verify structure
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "RC" in data
    assert len(data["RC"]) == 2
    assert data["RC"][0]["title"] == "Assortment rationalization"
    # Wave fields present (empty strings)
    assert "w1" in data["RC"][0]
