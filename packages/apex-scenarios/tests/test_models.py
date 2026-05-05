"""Tests for apex_scenarios.models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from apex_scenarios.models import (
    PRACTICE_CODES,
    Scenario,
    ScenarioCompact,
    compact_to_extended,
    extended_to_compact,
)


def test_compact_required_fields() -> None:
    s = ScenarioCompact(
        t="Title", s="RC-E2E-03", b="Brief", k="+2pp GM", kk="up"
    )
    assert s.t == "Title"
    assert s.kk == "up"


def test_compact_normalizes_direction_case() -> None:
    s = ScenarioCompact(t="t", s="s", b="b", k="k", kk="UP")
    assert s.kk == "up"


def test_compact_rejects_unknown_direction() -> None:
    with pytest.raises(ValidationError):
        ScenarioCompact(t="t", s="s", b="b", k="k", kk="sideways")


def test_extended_default_wave_fields_empty() -> None:
    s = Scenario(
        title="t", service_code="RC-E2E-03", brief="b", kpi="k", kpi_direction="up"
    )
    assert s.w1 == s.w2 == s.w3 == ""
    assert not s.has_full_wave_data()


def test_extended_has_full_wave_data() -> None:
    s = Scenario(
        title="t", service_code="RC-E2E-03", brief="b", kpi="k", kpi_direction="up",
        w1="W1 narrative", w2="W2 narrative", w3="W3 narrative",
    )
    assert s.has_full_wave_data()


def test_extended_partial_wave_data_returns_false() -> None:
    s = Scenario(
        title="t", service_code="s", brief="b", kpi="k", kpi_direction="up",
        w1="x", w2="", w3="z",
    )
    assert not s.has_full_wave_data()


def test_extended_practice_normalizes_to_uppercase() -> None:
    s = Scenario(
        title="t", service_code="s", brief="b", kpi="k", kpi_direction="up",
        practice="rc",
    )
    assert s.practice == "RC"


def test_extended_practice_rejects_unknown() -> None:
    with pytest.raises(ValidationError):
        Scenario(
            title="t", service_code="s", brief="b", kpi="k", kpi_direction="up",
            practice="marketing",
        )


def test_compact_to_extended_round_trip() -> None:
    c = ScenarioCompact(
        t="Cold-chain", s="RC-E2E-06", b="Real-time", k="+18% margin", kk="up"
    )
    e = compact_to_extended(c, practice="RC")
    assert e.title == "Cold-chain"
    assert e.service_code == "RC-E2E-06"
    assert e.practice == "RC"
    back = extended_to_compact(e)
    assert back == c


def test_practice_codes_canonical_seven() -> None:
    assert set(PRACTICE_CODES) == {"RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"}
