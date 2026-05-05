"""Tests for apex_scenarios.exporters."""

from __future__ import annotations

import csv
import datetime as dt
import io
from pathlib import Path

from apex_scenarios.exporters import (
    CSV_COLUMNS,
    csv_filename,
    write_csv,
    write_csv_string,
)
from apex_scenarios.library import load_scenario_library

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# csv_filename (Task 28.4.3)
# ---------------------------------------------------------------------------


def test_filename_default_is_all() -> None:
    name = csv_filename(when=dt.date(2026, 5, 4))
    assert name == "APEX-scenarios-all-2026-05-04.csv"


def test_filename_single_practice() -> None:
    name = csv_filename(practices=["RC"], when=dt.date(2026, 5, 4))
    assert name == "APEX-scenarios-rc-2026-05-04.csv"


def test_filename_multi_practice_collapses_to_multi() -> None:
    name = csv_filename(practices=["RC", "HLS"], when=dt.date(2026, 5, 4))
    assert name == "APEX-scenarios-multi-2026-05-04.csv"


def test_filename_all_seven_practices_canonical() -> None:
    seven = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
    name = csv_filename(practices=seven, when=dt.date(2026, 5, 4))
    assert name == "APEX-scenarios-all-2026-05-04.csv"


def test_filename_with_label() -> None:
    name = csv_filename(
        practices=["RC"], when=dt.date(2026, 5, 4), label="wave-incomplete"
    )
    assert name == "APEX-scenarios-rc-wave-incomplete-2026-05-04.csv"


def test_filename_empty_practices_segment() -> None:
    name = csv_filename(practices=[], when=dt.date(2026, 5, 4))
    assert name == "APEX-scenarios-empty-2026-05-04.csv"


def test_filename_lowercases_practice() -> None:
    name = csv_filename(practices=["RC"], when=dt.date(2026, 5, 4))
    assert "rc" in name
    assert "RC" not in name


# ---------------------------------------------------------------------------
# write_csv_string (Task 28.4.1)
# ---------------------------------------------------------------------------


def test_csv_string_has_header_and_rows() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    output = write_csv_string(scenarios)
    reader = csv.DictReader(io.StringIO(output))
    assert list(reader.fieldnames or []) == list(CSV_COLUMNS)
    rows = list(reader)
    assert len(rows) == 3


def test_csv_string_preserves_practice() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    output = write_csv_string(scenarios)
    reader = csv.DictReader(io.StringIO(output))
    rows = list(reader)
    practices = {r["practice"] for r in rows}
    assert practices == {"RC", "HLS"}


def test_csv_columns_complete() -> None:
    expected = {
        "practice", "service_code", "title", "brief", "kpi", "kpi_direction",
        "w1", "w2", "w3", "archetype_id", "mesh_id",
    }
    assert set(CSV_COLUMNS) == expected


# ---------------------------------------------------------------------------
# write_csv (file)
# ---------------------------------------------------------------------------


def test_write_csv_creates_file_with_bom(tmp_path: Path) -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    out = tmp_path / "out.csv"
    written = write_csv(scenarios, out)
    assert written == 3
    assert out.exists()
    content_bytes = out.read_bytes()
    # UTF-8 BOM for Excel friendliness
    assert content_bytes.startswith(b"\xef\xbb\xbf")


def test_write_csv_round_trip(tmp_path: Path) -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    out = tmp_path / "out.csv"
    write_csv(scenarios, out)
    with out.open("r", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 3
    titles = {r["title"] for r in rows}
    assert "Cold-chain excursion response" in titles
