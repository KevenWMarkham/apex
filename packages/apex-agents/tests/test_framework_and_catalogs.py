"""Tests for apex_agents — Sprint 16 framework + catalogs."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from apex_agents import (
    PRACTICE_CODES,
    AgentSpec,
    HITLGate,
    KpiTarget,
    ModelTier,
    OversightMode,
    ToolBinding,
    catalogs_root,
    load_agent_spec,
    scan_all_catalogs,
    scan_practice_catalog,
    total_agents,
    validate_catalogs,
)
from apex_agents._cli import agents_app

runner = CliRunner()


# ---------------------------------------------------------------------------
# AgentSpec model
# ---------------------------------------------------------------------------


def _minimal_spec(**overrides) -> AgentSpec:
    base = dict(
        name="apex.rc.agents.test",
        practice="rc",
        persona="Test Persona",
        service_codes=["RC-E2E-99"],
        model_tier=ModelTier.STANDARD,
        model_pin="gpt-4o-2024-11-20",
    )
    base.update(overrides)
    return AgentSpec(**base)


def test_agent_spec_practice_normalizes_to_lower() -> None:
    spec = _minimal_spec(practice="RC")
    assert spec.practice == "rc"


def test_agent_spec_rejects_unknown_practice() -> None:
    with pytest.raises(Exception):
        _minimal_spec(practice="marketing")


def test_agent_spec_write_tools_filter() -> None:
    spec = _minimal_spec(tools=[
        ToolBinding(tool_id="t1", purpose="read"),
        ToolBinding(tool_id="t2", purpose="write", write=True),
        ToolBinding(tool_id="t3", purpose="write", write=True),
    ])
    assert len(spec.write_tools()) == 2


def test_agent_spec_has_hitl() -> None:
    spec1 = _minimal_spec()
    assert not spec1.has_hitl()
    spec2 = _minimal_spec(hitl_gates=[HITLGate(name="g", description="d", fires_when="x")])
    assert spec2.has_hitl()


# ---------------------------------------------------------------------------
# Catalog scanning
# ---------------------------------------------------------------------------


def test_catalogs_root_exists() -> None:
    assert catalogs_root().is_dir()


def test_scan_all_catalogs_returns_seven_practices() -> None:
    cats = scan_all_catalogs()
    assert set(cats.keys()) == set(PRACTICE_CODES)


def test_scan_all_catalogs_total_agents_meets_sprint16_anchor_target() -> None:
    """Sprint 16 anchor target is 10 per Practice — 70 total."""
    assert total_agents() >= 70


def test_each_practice_has_at_least_anchor_10() -> None:
    cats = scan_all_catalogs()
    for practice in PRACTICE_CODES:
        assert len(cats[practice]) >= 10, f"Practice {practice} has fewer than 10 agents"


def test_scan_practice_catalog_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown practice"):
        scan_practice_catalog("marketing")


# ---------------------------------------------------------------------------
# Manifest correctness
# ---------------------------------------------------------------------------


def test_every_manifest_loads_cleanly() -> None:
    cats = scan_all_catalogs()
    for practice, entries in cats.items():
        for entry in entries:
            assert entry.spec.kind == "agent"
            assert entry.spec.practice == practice


def test_every_agent_name_uses_canonical_prefix() -> None:
    cats = scan_all_catalogs()
    for practice, entries in cats.items():
        for entry in entries:
            expected = f"apex.{practice}.agents."
            assert entry.spec.name.startswith(expected), \
                f"{entry.spec.name} should start with {expected}"


def test_every_agent_has_at_least_one_tool() -> None:
    cats = scan_all_catalogs()
    for entries in cats.values():
        for entry in entries:
            assert entry.spec.tools, f"Agent {entry.spec.name} has no tools declared"


def test_every_agent_has_persona_and_service_codes() -> None:
    cats = scan_all_catalogs()
    for entries in cats.values():
        for entry in entries:
            assert entry.spec.persona
            assert entry.spec.service_codes


# ---------------------------------------------------------------------------
# Catalog validator
# ---------------------------------------------------------------------------


def test_validate_catalogs_passes_for_shipped_anchors() -> None:
    """The 70 anchor agents pass governance rules."""
    report = validate_catalogs()
    if report.errors:
        # Show details on failure to make CI-debug easy
        for e in report.errors:
            print(f"{e.practice}/{e.agent_name}: [{e.code}] {e.message}")
    assert report.ok, f"Catalog validation produced {len(report.errors)} error(s)"


def test_validate_catalogs_flags_write_tool_without_hitl() -> None:
    bad = _minimal_spec(
        name="apex.rc.agents.test",
        tools=[ToolBinding(tool_id="t1", purpose="write thing", write=True)],
    )
    # Build a fake catalog with this bad spec to exercise the validator
    from apex_agents.framework import CatalogEntry, validate_catalogs

    fake = {"rc": [CatalogEntry(path=Path("/dev/null"), spec=bad)]}
    for p in PRACTICE_CODES:
        fake.setdefault(p, [])
    report = validate_catalogs(fake)
    codes = {i.code for i in report.errors}
    assert "MISSING_HITL_FOR_WRITE" in codes


def test_validate_catalogs_flags_reasoning_without_kpi() -> None:
    bad = _minimal_spec(
        name="apex.rc.agents.test",
        model_tier=ModelTier.REASONING,
        tools=[ToolBinding(tool_id="t1", purpose="read")],
    )
    from apex_agents.framework import CatalogEntry, validate_catalogs

    fake = {"rc": [CatalogEntry(path=Path("/dev/null"), spec=bad)]}
    for p in PRACTICE_CODES:
        fake.setdefault(p, [])
    report = validate_catalogs(fake)
    warnings = [i for i in report.issues if i.severity == "warning"]
    codes = {i.code for i in warnings}
    assert "REASONING_TIER_NO_KPI" in codes


def test_validate_catalogs_flags_noncanonical_name() -> None:
    bad = _minimal_spec(
        name="apex.rc.foo.test",  # missing 'agents' segment
        tools=[ToolBinding(tool_id="t", purpose="x")],
    )
    from apex_agents.framework import CatalogEntry, validate_catalogs

    fake = {"rc": [CatalogEntry(path=Path("/dev/null"), spec=bad)]}
    for p in PRACTICE_CODES:
        fake.setdefault(p, [])
    report = validate_catalogs(fake)
    codes = {i.code for i in report.errors}
    assert "AGENT_NAME_NONCANONICAL" in codes


def test_validate_catalogs_flags_invalid_hitl_sla() -> None:
    bad = _minimal_spec(
        tools=[ToolBinding(tool_id="t1", purpose="write thing", write=True)],
        hitl_gates=[HITLGate(name="g", description="d", fires_when="x", sla_minutes=-1)],
    )
    from apex_agents.framework import CatalogEntry, validate_catalogs

    fake = {"rc": [CatalogEntry(path=Path("/dev/null"), spec=bad)]}
    for p in PRACTICE_CODES:
        fake.setdefault(p, [])
    report = validate_catalogs(fake)
    codes = {i.code for i in report.errors}
    assert "HITL_SLA_INVALID" in codes


# ---------------------------------------------------------------------------
# Specific anchor-agent presence
# ---------------------------------------------------------------------------


def test_rc_anchor_agents_present() -> None:
    """Sprint 16 Task 16.1.1 names ten specific anchors; verify they're shipped."""
    cats = scan_practice_catalog("rc")
    names = {entry.spec.name for entry in cats}
    must_have = {
        "apex.rc.agents.assortment-pricing",
        "apex.rc.agents.demand-sensing",
        "apex.rc.agents.markdown-cadence",
        "apex.rc.agents.cold-chain-response",
        "apex.rc.agents.shrink-detection",
        "apex.rc.agents.customer-identity",
        "apex.rc.agents.substitution-recommendation",
        "apex.rc.agents.inventory-replenishment",
        "apex.rc.agents.store-ops-intelligence",
    }
    assert must_have.issubset(names)


def test_hls_anchor_agents_present() -> None:
    cats = scan_practice_catalog("hls")
    names = {entry.spec.name for entry in cats}
    must_have = {
        "apex.hls.agents.sepsis-early-warning",
        "apex.hls.agents.clinical-decision-support",
        "apex.hls.agents.utilization-management",
        "apex.hls.agents.claim-triage",
        "apex.hls.agents.study-enrollment",
        "apex.hls.agents.drug-interaction",
        "apex.hls.agents.readmission-risk",
        "apex.hls.agents.patient-identity",
        "apex.hls.agents.adverse-event",
        "apex.hls.agents.supply-cold-chain",
    }
    assert must_have.issubset(names)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_stats() -> None:
    result = runner.invoke(agents_app, ["stats"])
    assert result.exit_code == 0
    assert "Total agents shipped:" in result.stdout


def test_cli_list_one_practice() -> None:
    result = runner.invoke(agents_app, ["list", "--practice", "rc"])
    assert result.exit_code == 0
    assert "apex.rc.agents." in result.stdout


def test_cli_list_all_practices() -> None:
    result = runner.invoke(agents_app, ["list"])
    assert result.exit_code == 0
    for p in PRACTICE_CODES:
        assert p.upper() in result.stdout


def test_cli_inspect_known_agent() -> None:
    result = runner.invoke(agents_app, ["inspect", "apex.rc.agents.cold-chain-response"])
    assert result.exit_code == 0
    assert "Store Manager" in result.stdout


def test_cli_inspect_unknown_agent_fails() -> None:
    result = runner.invoke(agents_app, ["inspect", "apex.rc.agents.does-not-exist"])
    assert result.exit_code != 0


def test_cli_validate_passes_on_shipped_catalogs() -> None:
    result = runner.invoke(agents_app, ["validate"])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_all_70_anchor_agents() -> None:
    """The 70 anchor manifests load, validate, and pass governance."""
    assert total_agents() >= 70
    report = validate_catalogs()
    assert report.ok


@pytest.mark.conformance
def test_conformance_oversight_modes_only_canonical_values() -> None:
    cats = scan_all_catalogs()
    valid = {OversightMode.HITL, OversightMode.HOTL, OversightMode.HIC}
    for entries in cats.values():
        for entry in entries:
            for mode in entry.spec.oversight_modes:
                assert mode in valid
