"""Tests for apex_services — Sprint 17 framework + 61 service manifests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

from apex_services import (
    PRACTICE_CODES,
    SERVICE_CODE_RE,
    CommercialModel,
    KpiCommitment,
    Persona,
    ServiceSpec,
    Wave,
    WaveEnvelope,
    all_service_codes,
    catalogs_root,
    scan_all_catalogs,
    scan_practice_catalog,
    total_services,
    validate_service_catalogs,
)
from apex_services._cli import services_app

runner = CliRunner()


# ---------------------------------------------------------------------------
# ServiceSpec
# ---------------------------------------------------------------------------


def _minimal(**overrides) -> ServiceSpec:
    base = dict(
        service_code="RC-E2E-99",
        practice="rc",
        display_name="Test Service",
        brief="A test service.",
        personas=[Persona(name="Tester")],
        kpis=[KpiCommitment(name="test", direction="up")],
        waves=[WaveEnvelope(wave=Wave.WAVE_1, duration="4 weeks",
                           fee_band_low_usd=100_000, fee_band_high_usd=500_000)],
    )
    base.update(overrides)
    return ServiceSpec(**base)


def test_service_code_canonical_pattern() -> None:
    for code in [
        "RC-E2E-03", "HLS-LS-03", "ER-PU-01", "AXLE-Connected-Factory-01",
        "TMT-MED-03", "TH-AIR-01", "ICE-EaaS-01",
    ]:
        assert SERVICE_CODE_RE.match(code), f"Should match: {code}"


def test_service_code_rejects_malformed() -> None:
    with pytest.raises(ValidationError):
        _minimal(service_code="not-canonical")


def test_practice_normalizes_to_lower() -> None:
    spec = _minimal(practice="RC")
    assert spec.practice == "rc"


def test_practice_rejects_unknown() -> None:
    with pytest.raises(ValidationError):
        _minimal(practice="marketing")


def test_primary_persona_returns_first_primary() -> None:
    spec = _minimal(personas=[
        Persona(name="A", role="secondary"),
        Persona(name="B", role="primary"),
    ])
    assert spec.primary_persona().name == "B"


def test_has_value_share_via_eligible_flag() -> None:
    spec = _minimal(value_share_eligible=True)
    assert spec.has_value_share()


def test_has_value_share_via_commercial_model() -> None:
    spec = _minimal(commercial_model=CommercialModel.VALUE_SHARE)
    assert spec.has_value_share()


def test_wave_envelope_lookup() -> None:
    spec = _minimal(waves=[
        WaveEnvelope(wave=Wave.WAVE_1, duration="d", fee_band_low_usd=1, fee_band_high_usd=2),
        WaveEnvelope(wave=Wave.WAVE_2, duration="d", fee_band_low_usd=3, fee_band_high_usd=4),
    ])
    w1 = spec.wave_envelope(Wave.WAVE_1)
    assert w1 is not None and w1.fee_band_low_usd == 1
    w3 = spec.wave_envelope(Wave.WAVE_3)
    assert w3 is None


# ---------------------------------------------------------------------------
# Catalog scanning
# ---------------------------------------------------------------------------


def test_catalogs_root_exists() -> None:
    assert catalogs_root().is_dir()


def test_total_services_meets_61() -> None:
    """Sprint 17 ships 13 RC + 8 each for HLS/ER/AXLE/TMT/TH/ICE = 61 anchors."""
    assert total_services() == 61


def test_rc_has_thirteen_services() -> None:
    assert len(scan_practice_catalog("rc")) == 13


def test_other_practices_have_at_least_eight() -> None:
    for p in ("hls", "er", "axle", "tmt", "th", "ice"):
        assert len(scan_practice_catalog(p)) >= 8


def test_scan_all_returns_seven_practices() -> None:
    cats = scan_all_catalogs()
    assert set(cats.keys()) == set(PRACTICE_CODES)


def test_all_service_codes_returns_canonical_set() -> None:
    codes = all_service_codes()
    # Spot-check known codes
    assert "RC-E2E-03" in codes
    assert "RC-E2E-06" in codes
    assert "HLS-E2E-04" in codes
    assert "TH-AIR-01" in codes
    assert "ICE-Aftermarket-01" in codes
    assert len(codes) == 61


# ---------------------------------------------------------------------------
# Manifest correctness
# ---------------------------------------------------------------------------


def test_every_service_code_matches_canonical_pattern() -> None:
    for entries in scan_all_catalogs().values():
        for entry in entries:
            assert SERVICE_CODE_RE.match(entry.spec.service_code), \
                f"Bad service_code: {entry.spec.service_code}"


def test_every_service_practice_matches_code_prefix() -> None:
    for practice, entries in scan_all_catalogs().items():
        for entry in entries:
            assert entry.spec.service_code.upper().startswith(practice.upper() + "-")


def test_every_service_has_persona_kpi_and_wave() -> None:
    for entries in scan_all_catalogs().values():
        for entry in entries:
            assert entry.spec.personas
            assert entry.spec.kpis
            assert entry.spec.waves


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


def test_validate_passes_for_shipped_catalogs() -> None:
    report = validate_service_catalogs()
    if report.errors:
        for e in report.errors:
            print(f"{e.practice}/{e.service_code}: [{e.code}] {e.message}")
    assert report.ok


def test_validate_with_agent_catalog_resolves() -> None:
    """Cross-reference linked_agents against the Sprint 16 agent catalog."""
    from apex_agents.framework import scan_all_catalogs as agent_scan

    agent_names = set()
    for entries in agent_scan().values():
        for e in entries:
            agent_names.add(e.spec.name)

    report = validate_service_catalogs(agent_catalog=agent_names)
    # Show any unresolved agents for debug
    unresolved = [i for i in report.errors if i.code == "AGENT_NOT_FOUND"]
    for u in unresolved:
        print(f"  {u.service_code}: {u.message}")
    assert not unresolved, f"{len(unresolved)} services link to non-existent agents"


def test_validate_flags_no_persona() -> None:
    bad = ServiceSpec(
        service_code="RC-E2E-99",
        practice="rc",
        display_name="t",
        brief="b",
        personas=[],
        kpis=[KpiCommitment(name="k", direction="up")],
        waves=[WaveEnvelope(wave=Wave.WAVE_1, duration="d", fee_band_low_usd=1, fee_band_high_usd=2)],
    )
    from apex_services.framework import CatalogEntry, validate_service_catalogs
    from pathlib import Path

    fake = {p: [] for p in PRACTICE_CODES}
    fake["rc"] = [CatalogEntry(path=Path("/dev/null"), spec=bad)]
    report = validate_service_catalogs(fake)
    codes = {i.code for i in report.errors}
    assert "NO_PERSONAS" in codes


def test_validate_flags_value_share_without_money_kpi() -> None:
    spec = ServiceSpec(
        service_code="RC-E2E-99",
        practice="rc", display_name="t", brief="b",
        personas=[Persona(name="P")],
        kpis=[KpiCommitment(name="k", direction="up")],
        waves=[WaveEnvelope(wave=Wave.WAVE_1, duration="d", fee_band_low_usd=1, fee_band_high_usd=2)],
        value_share_eligible=True,
    )
    from apex_services.framework import CatalogEntry, validate_service_catalogs
    from pathlib import Path

    fake = {p: [] for p in PRACTICE_CODES}
    fake["rc"] = [CatalogEntry(path=Path("/dev/null"), spec=spec)]
    report = validate_service_catalogs(fake)
    codes = {i.code for i in report.issues}
    assert "VALUE_SHARE_WITHOUT_MONEY_KPI" in codes


# ---------------------------------------------------------------------------
# Specific anchor presence
# ---------------------------------------------------------------------------


def test_rc_anchor_services_present() -> None:
    """The five priority RC services per Sellers Guide §9.3 must ship."""
    codes = {entry.spec.service_code for entry in scan_practice_catalog("rc")}
    must_have = {"RC-E2E-03", "RC-E2E-05", "RC-E2E-09", "RC-TTP-02", "RC-TTP-07"}
    assert must_have.issubset(codes)


def test_hls_anchor_services_present() -> None:
    codes = {entry.spec.service_code for entry in scan_practice_catalog("hls")}
    must_have = {"HLS-E2E-04", "HLS-E2E-02", "HLS-E2E-03", "HLS-LS-03"}
    assert must_have.issubset(codes)


def test_th_irops_recovery_present() -> None:
    """TH IROPs recovery is the reference TH service per §14.8."""
    codes = {entry.spec.service_code for entry in scan_practice_catalog("th")}
    assert "TH-AIR-01" in codes


def test_axle_connected_factory_present() -> None:
    """AXLE Connected Factory is the lead service per §12.10."""
    codes = {entry.spec.service_code for entry in scan_practice_catalog("axle")}
    assert "AXLE-Connected-Factory-01" in codes


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_stats() -> None:
    result = runner.invoke(services_app, ["stats"])
    assert result.exit_code == 0
    assert "Total services shipped: 61" in result.stdout


def test_cli_list_one_practice() -> None:
    result = runner.invoke(services_app, ["list", "--practice", "rc"])
    assert result.exit_code == 0
    assert "RC-E2E-06" in result.stdout


def test_cli_list_value_share_filter() -> None:
    result = runner.invoke(services_app, ["list", "--value-share"])
    assert result.exit_code == 0
    assert "[value-share]" in result.stdout


def test_cli_inspect() -> None:
    result = runner.invoke(services_app, ["inspect", "RC-E2E-06"])
    assert result.exit_code == 0
    assert "Cold Chain" in result.stdout
    assert "Store Manager" in result.stdout


def test_cli_inspect_unknown_fails() -> None:
    result = runner.invoke(services_app, ["inspect", "RC-E2E-999"])
    assert result.exit_code != 0


def test_cli_validate_passes() -> None:
    result = runner.invoke(services_app, ["validate"])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Sprint 28 integration — service codes feed scenario validator
# ---------------------------------------------------------------------------


def test_all_service_codes_are_consumable_by_scenario_validator() -> None:
    """The scenario-library validator (Sprint 28 Task 28.7.2) accepts a
    service_catalog_codes set; this catalog provides it."""
    from apex_scenarios.validators import validate_service_codes
    from apex_scenarios.models import Scenario

    catalog = all_service_codes()
    # Pick a scenario whose service_code is in the shipped catalog
    scenarios = [
        Scenario(
            title="t", service_code="RC-E2E-06", brief="b",
            kpi="+18% margin", kpi_direction="up", practice="RC",
        )
    ]
    report = validate_service_codes(scenarios, service_catalog_codes=catalog)
    assert report.ok


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_all_61_anchor_services() -> None:
    assert total_services() == 61
    report = validate_service_catalogs()
    assert report.ok
