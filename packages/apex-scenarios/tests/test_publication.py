"""Tests for apex_scenarios.publication."""

from __future__ import annotations

from pathlib import Path

from apex_scenarios.library import ScenarioIndex, load_scenario_library
from apex_scenarios.publication import (
    PRACTICE_LONG_NAME,
    publish_master_catalog,
    render_index_markdown,
    render_practice_markdown,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_render_practice_includes_long_name_and_count() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    md = render_practice_markdown(idx, "RC")
    assert "Retail & Consumer" in md
    assert "**Total scenarios:** 2" in md


def test_render_practice_lists_each_scenario_with_service_code() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    md = render_practice_markdown(idx, "RC")
    assert "RC-E2E-03" in md
    assert "RC-E2E-06" in md


def test_render_practice_handles_pipe_in_title() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    md = render_practice_markdown(idx, "RC")
    # Markdown table doesn't break: every row has 4 pipes plus newline
    body_lines = [line for line in md.splitlines() if line.startswith("|") and not line.startswith("|---")]
    for line in body_lines:
        # 5 pipes per row (start, between 4 columns, end)
        assert line.count("|") == 5


def test_render_index_includes_all_seven_practices() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    md = render_index_markdown(idx)
    for practice in ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]:
        assert practice in md
        assert PRACTICE_LONG_NAME[practice] in md


def test_render_index_total_row() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    md = render_index_markdown(idx)
    assert "**TOTAL**" in md
    assert "**3**" in md


def test_render_index_wave_completion_warning_when_incomplete() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    md = render_index_markdown(idx)
    assert "Wave-data completion" in md
    assert "Sprint 28 Task 28.1.6 gates" in md


def test_publish_master_catalog_writes_index_plus_seven_files(tmp_path: Path) -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    written = publish_master_catalog(idx, tmp_path / "catalog")
    # 1 index + 7 practices = 8 files
    assert len(written) == 8
    assert (tmp_path / "catalog" / "index.md").exists()
    for p in ["rc", "hls", "er", "axle", "tmt", "th", "ice"]:
        assert (tmp_path / "catalog" / f"{p}.md").exists()


def test_publish_master_catalog_files_round_trip_to_unicode(tmp_path: Path) -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    idx = ScenarioIndex(scenarios)
    publish_master_catalog(idx, tmp_path / "catalog")
    rc_md = (tmp_path / "catalog" / "rc.md").read_text(encoding="utf-8")
    assert "Cold-chain excursion response" in rc_md
