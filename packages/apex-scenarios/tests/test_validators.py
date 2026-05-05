"""Tests for apex_scenarios.validators — Sprint 28 Tasks 28.1.6 + 28.7.2-5."""

from __future__ import annotations

from pathlib import Path

from apex_scenarios.library import load_featured_chains, load_scenario_library
from apex_scenarios.models import FeaturedChain, Scenario
from apex_scenarios.validators import (
    classify_library_bump,
    extract_agent_references,
    extract_kpi_name,
    validate_agent_references,
    validate_kpis,
    validate_service_codes,
    validate_wave_data_presence,
)

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Wave-data presence (Task 28.1.6)
# ---------------------------------------------------------------------------


def test_wave_data_presence_fails_on_empty_fixture() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    report = validate_wave_data_presence(scenarios)
    assert not report.ok
    assert report.exit_code == 1
    assert len(report.errors) == 3
    assert all(i.code == "WAVE_MISSING" for i in report.errors)


def test_wave_data_presence_passes_when_complete() -> None:
    scenarios = [
        Scenario(
            title="t", service_code="RC-E2E-03", brief="b", kpi="+2pp GM",
            kpi_direction="up", practice="RC",
            w1="W1", w2="W2", w3="W3",
        )
    ]
    assert validate_wave_data_presence(scenarios).ok


def test_wave_data_presence_partial_missing_one_wave() -> None:
    scenarios = [
        Scenario(
            title="t", service_code="s", brief="b", kpi="k", kpi_direction="up",
            w1="W1", w2="", w3="W3",
        )
    ]
    report = validate_wave_data_presence(scenarios)
    assert len(report.errors) == 1
    assert "w2" in report.errors[0].message


# ---------------------------------------------------------------------------
# Service codes (Task 28.7.2)
# ---------------------------------------------------------------------------


def test_service_codes_structural_passes_on_canonical() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    # No catalog passed → structural check (regex pattern)
    report = validate_service_codes(scenarios)
    assert report.ok


def test_service_codes_structural_rejects_malformed() -> None:
    scenarios = [
        Scenario(
            title="t", service_code="not-canonical", brief="b",
            kpi="+2pp GM", kpi_direction="up",
        )
    ]
    report = validate_service_codes(scenarios)
    assert len(report.errors) == 1
    assert report.errors[0].code == "SERVICE_CODE_MALFORMED"


def test_service_codes_with_catalog_resolves() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    catalog = {"RC-E2E-03", "RC-E2E-06", "HLS-E2E-04"}
    assert validate_service_codes(scenarios, service_catalog_codes=catalog).ok


def test_service_codes_with_catalog_misses() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    catalog = {"RC-E2E-03"}  # missing RC-E2E-06 and HLS-E2E-04
    report = validate_service_codes(scenarios, service_catalog_codes=catalog)
    assert len(report.errors) == 2
    assert all(i.code == "SERVICE_CODE_UNRESOLVED" for i in report.errors)


# NOTE: Empty service_code is rejected at Pydantic-model construction time
# (min_length=1 + str_strip_whitespace), so the validator's SERVICE_CODE_EMPTY
# branch is defense-in-depth only. We do not test it via the model — it's
# unreachable when Scenarios are constructed via the public API.


# ---------------------------------------------------------------------------
# Agent references (Task 28.7.3)
# ---------------------------------------------------------------------------


def test_extract_agent_references_finds_phrases() -> None:
    refs = extract_agent_references(
        "Real-time perishables-integrity agent fuses signals and the recall response agent triggers."
    )
    # The regex captures the full noun phrase preceding "agent". Determiners
    # ("the", "a", "an") are stripped. Adjectives ("real-time") stay attached.
    assert any("perishables-integrity" in r for r in refs)
    assert "recall response" in refs


def test_extract_agent_references_strips_leading_determiners() -> None:
    refs = extract_agent_references("The recall response agent fires.")
    assert "recall response" in refs
    # "the" was stripped
    assert not any(r.startswith("the ") for r in refs)


def test_extract_agent_references_empty_when_no_match() -> None:
    refs = extract_agent_references("No automation here.")
    assert refs == []


def test_validate_agent_references_warns_when_no_phrase() -> None:
    chain = FeaturedChain(
        title="t", Scenario="x", Solution="No automation in this Solution.", **{"Use Case": "u"}
    )
    report = validate_agent_references([chain])
    # No agents named → warning, not error
    assert len(report.warnings) == 1
    assert report.warnings[0].code == "AGENT_REF_MISSING"
    assert report.ok


def test_validate_agent_references_fails_unresolved() -> None:
    chain = FeaturedChain(
        title="t", Scenario="x",
        Solution="The recall response agent triggers downstream.",
        **{"Use Case": "u"},
    )
    catalog = {"perishables-integrity"}  # 'recall response' not registered
    report = validate_agent_references([chain], agent_catalog_names=catalog)
    assert len(report.errors) == 1
    assert report.errors[0].code == "AGENT_REF_UNRESOLVED"


def test_validate_agent_references_passes_resolved() -> None:
    chain = FeaturedChain(
        title="t", Scenario="x",
        Solution="The perishables-integrity agent runs.",
        **{"Use Case": "u"},
    )
    catalog = {"perishables-integrity"}
    assert validate_agent_references([chain], agent_catalog_names=catalog).ok


def test_validate_agent_references_against_real_fixture() -> None:
    chains = load_featured_chains(FIXTURES / "featured-chains-mini.json")
    report = validate_agent_references(chains)
    # Both fixture rows mention "... agent"; structural check passes
    assert report.ok


# ---------------------------------------------------------------------------
# KPIs (Task 28.7.4)
# ---------------------------------------------------------------------------


def test_extract_kpi_name_from_pp() -> None:
    assert extract_kpi_name("+2.4pp GM") == "GM"


def test_extract_kpi_name_from_percent() -> None:
    assert extract_kpi_name("+18% margin") == "margin"


def test_extract_kpi_name_from_negative() -> None:
    assert extract_kpi_name("-15% MAPE") == "MAPE"


def test_extract_kpi_name_unparseable() -> None:
    assert extract_kpi_name("nothing here") is None


def test_validate_kpis_structural_passes() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    assert validate_kpis(scenarios).ok


def test_validate_kpis_with_registry() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    registry = {"GM", "margin", "mortality"}
    assert validate_kpis(scenarios, kpi_registry_names=registry).ok


def test_validate_kpis_with_registry_misses() -> None:
    scenarios = load_scenario_library(FIXTURES / "scenario-library-mini.json")
    registry = {"GM"}  # missing margin + mortality
    report = validate_kpis(scenarios, kpi_registry_names=registry)
    assert len(report.errors) == 2


def test_validate_kpis_unparseable() -> None:
    bad = [
        Scenario(
            title="t", service_code="RC-E2E-03", brief="b",
            kpi="vague aspirational", kpi_direction="up",
        )
    ]
    report = validate_kpis(bad)
    assert len(report.errors) == 1
    assert report.errors[0].code == "KPI_DELTA_UNPARSEABLE"


# ---------------------------------------------------------------------------
# Versioning (Task 28.7.5)
# ---------------------------------------------------------------------------


def _row(title: str, **extra) -> Scenario:
    return Scenario(
        title=title, service_code=extra.get("service_code", "RC-E2E-03"),
        brief="b", kpi=extra.get("kpi", "+2pp GM"),
        kpi_direction="up", practice=extra.get("practice", "RC"),
        **{k: v for k, v in extra.items() if k not in ("service_code", "kpi", "practice")},
    )


def test_versioning_patch_when_no_diff() -> None:
    rows = [_row("a"), _row("b")]
    result = classify_library_bump(rows, rows)
    assert result.bump == "PATCH"


def test_versioning_patch_on_kpi_remeasurement() -> None:
    before = [_row("a", kpi="+2pp GM")]
    after = [_row("a", kpi="+2.4pp GM")]
    result = classify_library_bump(before, after)
    assert result.bump == "PATCH"


def test_versioning_minor_on_added_scenario() -> None:
    before = [_row("a")]
    after = [_row("a"), _row("b")]
    result = classify_library_bump(before, after)
    assert result.bump == "MINOR"
    assert len(result.added) == 1
    assert result.removed == []


def test_versioning_minor_on_removed_scenario() -> None:
    before = [_row("a"), _row("b")]
    after = [_row("a")]
    result = classify_library_bump(before, after)
    assert result.bump == "MINOR"
    assert len(result.removed) == 1


def test_versioning_major_on_field_schema_change() -> None:
    before = [_row("a")]
    # New field exposed via model_dump(exclude_unset=True): w1 set
    after = [_row("a", w1="filled in")]
    result = classify_library_bump(before, after)
    assert result.bump == "MAJOR"
    assert result.field_schema_changed
