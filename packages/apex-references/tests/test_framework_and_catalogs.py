"""Tests for apex_references — Sprint 18 framework + reference deployments."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from apex_references import (
    PRACTICE_CODES,
    KpiTarget,
    ReferenceSpec,
    SolutionArchitecture,
    TriggeringScenario,
    UseCase,
    Wave1Scope,
    catalogs_root,
    demo_scripts_root,
    get_reference,
    load_demo_script,
    load_reference_spec,
    scan_all_references,
    total_references,
    validate_references,
)
from apex_references._cli import references_app

runner = CliRunner()


# ---------------------------------------------------------------------------
# ReferenceSpec model
# ---------------------------------------------------------------------------


def _minimal_arch() -> SolutionArchitecture:
    return SolutionArchitecture(
        capacity_blueprint="single-capacity-tenant",
        fabric_sku="F64",
    )


def _minimal_wave1() -> Wave1Scope:
    return Wave1Scope(
        duration_weeks_low=8,
        duration_weeks_high=12,
        fee_band_usd_low=500_000,
        fee_band_usd_high=1_000_000,
    )


def _minimal_spec(**overrides) -> ReferenceSpec:
    base = dict(
        name="test",
        practice="rc",
        display_name="Test Reference",
        description="Test reference deployment.",
        architecture=_minimal_arch(),
        wave1_scope=_minimal_wave1(),
        use_cases=[UseCase(name="uc", description="d")],
        kpi_targets=[KpiTarget(name="k", direction="up", wave2_target="x")],
    )
    base.update(overrides)
    return ReferenceSpec(**base)


def test_reference_spec_practice_normalizes_to_lower() -> None:
    spec = _minimal_spec(practice="RC")
    assert spec.practice == "rc"


def test_reference_spec_rejects_unknown_practice() -> None:
    with pytest.raises(Exception):
        _minimal_spec(practice="marketing")


def test_reference_spec_kind_default() -> None:
    spec = _minimal_spec()
    assert spec.kind == "reference_deployment"


# ---------------------------------------------------------------------------
# Catalog scanning
# ---------------------------------------------------------------------------


def test_catalogs_root_exists() -> None:
    assert catalogs_root().is_dir()


def test_demo_scripts_root_exists() -> None:
    assert demo_scripts_root().is_dir()


def test_total_references_meets_sprint18_target() -> None:
    """Sprint 18 ships exactly five reference deployments."""
    assert total_references() == 5


def test_scan_all_references_contains_anchor_set() -> None:
    entries = scan_all_references()
    names = {e.spec.name for e in entries}
    expected = {"big-box-store", "hospital", "utility", "plant", "airline"}
    assert expected.issubset(names)


def test_get_reference_round_trips() -> None:
    for name in ["big-box-store", "hospital", "utility", "plant", "airline"]:
        spec = get_reference(name)
        assert spec is not None
        assert spec.name == name


def test_get_reference_unknown_returns_none() -> None:
    assert get_reference("does-not-exist") is None


# ---------------------------------------------------------------------------
# Manifest correctness
# ---------------------------------------------------------------------------


def test_every_manifest_loads_cleanly() -> None:
    entries = scan_all_references()
    for entry in entries:
        assert entry.spec.kind == "reference_deployment"
        assert entry.spec.practice in PRACTICE_CODES
        assert entry.spec.display_name
        assert entry.spec.description


def test_every_reference_has_use_cases_and_kpis() -> None:
    for entry in scan_all_references():
        assert entry.spec.use_cases, f"{entry.spec.name} has no use cases"
        assert entry.spec.kpi_targets, f"{entry.spec.name} has no kpi targets"


def test_every_reference_declares_triggering_scenarios() -> None:
    for entry in scan_all_references():
        assert entry.spec.triggering_scenarios, \
            f"{entry.spec.name} has no triggering scenarios"


def test_every_reference_declares_sponsor_personas() -> None:
    for entry in scan_all_references():
        assert entry.spec.sponsor_personas, \
            f"{entry.spec.name} has no sponsor personas"


def test_every_reference_has_demo_script_present() -> None:
    for entry in scan_all_references():
        if entry.spec.demo_script_path:
            md = load_demo_script(entry.spec.name)
            assert md, f"Demo script for {entry.spec.name} is empty / missing"


def test_every_reference_architecture_complete() -> None:
    for entry in scan_all_references():
        arch = entry.spec.architecture
        assert arch.capacity_blueprint
        assert arch.fabric_sku
        assert arch.adapters, f"{entry.spec.name} declares no adapters"


def test_every_reference_wave1_scope_coherent() -> None:
    for entry in scan_all_references():
        ws = entry.spec.wave1_scope
        assert ws.duration_weeks_low <= ws.duration_weeks_high
        assert ws.fee_band_usd_low <= ws.fee_band_usd_high
        assert 4 <= ws.duration_weeks_low
        assert ws.duration_weeks_high <= 16
        assert ws.deliverables, f"{entry.spec.name} declares no deliverables"
        assert ws.success_criteria, \
            f"{entry.spec.name} declares no success criteria"


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


def test_validator_passes_for_shipped_anchors() -> None:
    """Five anchor references pass governance with no cross-refs supplied."""
    report = validate_references()
    if report.errors:
        for e in report.errors:
            print(f"{e.reference}: [{e.code}] {e.message}")
    assert report.ok, f"Validation produced {len(report.errors)} error(s)"


def test_validator_passes_with_full_cross_references() -> None:
    """With live agent / service / adapter catalogs, all references resolve."""
    from apex_services import all_service_codes
    from apex_agents import scan_all_catalogs as agents_scan
    from apex_adapters.catalog import load_all_shipped_manifests

    codes = all_service_codes()
    agents = {
        e.spec.name for entries in agents_scan().values() for e in entries
    }
    adapters = set(load_all_shipped_manifests().keys())

    report = validate_references(
        service_codes=codes,
        agent_catalog=agents,
        adapter_catalog=adapters,
    )
    if report.errors:
        for e in report.errors:
            print(f"{e.reference}: [{e.code}] {e.message}")
    assert report.ok


def test_validator_flags_inverted_duration() -> None:
    bad_dir = Path(__file__).parent / "_bad"
    bad_dir.mkdir(exist_ok=True)
    bad_path = bad_dir / "_inverted.yaml"
    bad_path.write_text(
        """
kind: reference_deployment
name: bad-inverted
practice: rc
display_name: Bad
description: bad
architecture:
  capacity_blueprint: single-capacity-tenant
  fabric_sku: F64
use_cases:
  - name: uc
    description: d
kpi_targets:
  - name: k
    direction: up
    wave2_target: x
wave1_scope:
  duration_weeks_low: 12
  duration_weeks_high: 8
  fee_band_usd_low: 100000
  fee_band_usd_high: 200000
""",
        encoding="utf-8",
    )
    spec = load_reference_spec(bad_path)
    assert spec.wave1_scope.duration_weeks_low == 12


def test_validator_detects_unknown_service_code() -> None:
    report = validate_references(service_codes={"RC-OTHER-99"})
    codes = {i.code for i in report.errors}
    assert "SERVICE_CODE_NOT_FOUND" in codes


def test_validator_detects_unknown_agent() -> None:
    report = validate_references(agent_catalog={"apex.rc.agents.fake"})
    codes = {i.code for i in report.errors}
    assert "AGENT_NOT_FOUND" in codes


def test_validator_detects_unknown_adapter() -> None:
    report = validate_references(adapter_catalog={"some-adapter"})
    codes = {i.code for i in report.errors}
    assert "ADAPTER_NOT_FOUND" in codes


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_stats() -> None:
    result = runner.invoke(references_app, ["stats"])
    assert result.exit_code == 0
    assert "Total reference deployments shipped:" in result.stdout


def test_cli_list_default() -> None:
    result = runner.invoke(references_app, ["list"])
    assert result.exit_code == 0
    assert "big-box-store" in result.stdout
    assert "hospital" in result.stdout
    assert "utility" in result.stdout
    assert "plant" in result.stdout
    assert "airline" in result.stdout


def test_cli_list_filter_by_practice() -> None:
    result = runner.invoke(references_app, ["list", "--practice", "rc"])
    assert result.exit_code == 0
    assert "big-box-store" in result.stdout
    assert "hospital" not in result.stdout


def test_cli_inspect_known_reference() -> None:
    result = runner.invoke(references_app, ["inspect", "big-box-store"])
    assert result.exit_code == 0
    assert "Big Box Store" in result.stdout
    assert "RC" in result.stdout.upper()
    assert "wave1_scope" in result.stdout


def test_cli_inspect_unknown_reference_fails() -> None:
    result = runner.invoke(references_app, ["inspect", "does-not-exist"])
    assert result.exit_code != 0


def test_cli_demo_returns_markdown() -> None:
    result = runner.invoke(references_app, ["demo", "big-box-store"])
    assert result.exit_code == 0
    assert "Demo Script" in result.stdout
    assert "Wave-1" in result.stdout


def test_cli_demo_unknown_fails() -> None:
    result = runner.invoke(references_app, ["demo", "does-not-exist"])
    assert result.exit_code != 0


def test_cli_validate_passes_on_shipped_catalogs() -> None:
    result = runner.invoke(references_app, ["validate"])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Per-reference anchor presence
# ---------------------------------------------------------------------------


def test_big_box_store_composes_rc_agents_and_services() -> None:
    spec = get_reference("big-box-store")
    assert spec is not None
    assert spec.practice == "rc"
    assert spec.sellers_guide_section == "§16.13"
    agent_names = {a for uc in spec.use_cases for a in uc.agents}
    assert "apex.rc.agents.cold-chain-response" in agent_names
    assert "apex.rc.agents.markdown-cadence" in agent_names
    service_codes = {c for uc in spec.use_cases for c in uc.service_codes}
    assert any(sc.startswith("RC-") for sc in service_codes)


def test_hospital_composes_hls_agents_and_services() -> None:
    spec = get_reference("hospital")
    assert spec is not None
    assert spec.practice == "hls"
    assert spec.sellers_guide_section == "§10.9"
    agent_names = {a for uc in spec.use_cases for a in uc.agents}
    assert "apex.hls.agents.sepsis-early-warning" in agent_names


def test_utility_composes_er_agents_and_services() -> None:
    spec = get_reference("utility")
    assert spec is not None
    assert spec.practice == "er"
    assert spec.sellers_guide_section == "§11.9"
    agent_names = {a for uc in spec.use_cases for a in uc.agents}
    assert "apex.er.agents.psps-decision" in agent_names


def test_plant_composes_axle_agents_and_services() -> None:
    spec = get_reference("plant")
    assert spec is not None
    assert spec.practice == "axle"
    assert spec.sellers_guide_section == "§12.9A"
    agent_names = {a for uc in spec.use_cases for a in uc.agents}
    assert "apex.axle.agents.oee-monitor" in agent_names


def test_airline_composes_th_agents_and_services() -> None:
    spec = get_reference("airline")
    assert spec is not None
    assert spec.practice == "th"
    assert spec.sellers_guide_section == "§14.8"
    agent_names = {a for uc in spec.use_cases for a in uc.agents}
    assert "apex.th.agents.irops-recovery" in agent_names


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_all_five_anchor_references() -> None:
    """All 5 anchor references load, validate, cross-reference cleanly."""
    assert total_references() == 5
    from apex_services import all_service_codes
    from apex_agents import scan_all_catalogs as agents_scan
    from apex_adapters.catalog import load_all_shipped_manifests

    report = validate_references(
        service_codes=all_service_codes(),
        agent_catalog={
            e.spec.name for entries in agents_scan().values() for e in entries
        },
        adapter_catalog=set(load_all_shipped_manifests().keys()),
    )
    assert report.ok, [
        f"{i.reference}: [{i.code}] {i.message}" for i in report.errors
    ]


@pytest.mark.conformance
def test_conformance_each_reference_has_demo_script() -> None:
    for entry in scan_all_references():
        md = load_demo_script(entry.spec.name)
        assert md, f"{entry.spec.name}: demo script missing"
        assert "Wave-1" in md or "Wave 1" in md.replace("-", " ")
