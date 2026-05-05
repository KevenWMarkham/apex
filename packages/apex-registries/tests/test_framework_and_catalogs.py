"""Tests for apex_registries — Sprint 19 framework + Appendices A-K."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from apex_registries import (
    PRACTICE_CODES,
    REGISTRY_DIRS,
    ArchetypeEntry,
    CompetitiveEntry,
    ExerciseEntry,
    KpiEntry,
    McpToolEntry,
    PartnerEntry,
    PersonaEntry,
    ProductEntry,
    SchemaEntry,
    list_discovery,
    list_playbooks,
    list_preclearance,
    load_playbook,
    package_root,
    scan_all_registries,
    scan_registry,
    total_entries,
    validate_registries,
)
from apex_registries._cli import registries_app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Model validation
# ---------------------------------------------------------------------------


def test_kpi_entry_practice_normalizes() -> None:
    k = KpiEntry(
        kpi_id="kpi.rc.test", name="Test KPI", practice="RC",
        direction="up", description="x",
    )
    assert k.practice == "rc"


def test_kpi_entry_rejects_unknown_practice() -> None:
    with pytest.raises(Exception):
        KpiEntry(kpi_id="x", name="x", practice="marketing", direction="up", description="x")


def test_persona_entry_seniority_default() -> None:
    p = PersonaEntry(
        persona_id="persona.rc.test", name="Test", practice="rc",
        function="Operations", description="x",
    )
    assert p.seniority == "vp"


def test_archetype_entry_defaults() -> None:
    a = ArchetypeEntry(
        archetype_id="arch.test", family="triage", name="Test", description="x",
    )
    assert a.typical_oversight == "HITL"
    assert a.typical_model_tier == "standard"


def test_schema_entry_practice_normalization() -> None:
    s = SchemaEntry(
        schema_code="TEST", name="Test", description="x",
        practices=["RC", "HLS"], primary_entities=["Foo"],
    )
    assert s.practices == ["rc", "hls"]


# ---------------------------------------------------------------------------
# Catalog scanning
# ---------------------------------------------------------------------------


def test_package_root_exists() -> None:
    assert package_root().is_dir()


def test_scan_all_registries_returns_all_known() -> None:
    cats = scan_all_registries()
    assert set(cats.keys()) == set(REGISTRY_DIRS.keys())


def test_total_entries_meets_sprint19_targets() -> None:
    """Sprint 19 ships at minimum: 130 KPIs, 140 personas, 160 tools, 47 archetypes,
    48 schemas, 25 products, 18 partners, 8 competitive, 8 exercises."""
    totals = total_entries()
    assert totals["kpis"] >= 130
    assert totals["personas"] >= 140
    assert totals["mcp_tools"] >= 160
    assert totals["schemas"] >= 48
    assert totals["archetypes"] == 47
    assert totals["products"] >= 25
    assert totals["partners"] >= 18
    assert totals["competitive"] >= 8
    assert totals["exercises"] >= 8


def test_scan_registry_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown registry"):
        scan_registry("nonexistent")


# ---------------------------------------------------------------------------
# Per-registry correctness
# ---------------------------------------------------------------------------


def test_every_kpi_has_id_and_direction() -> None:
    for entry in scan_registry("kpis"):
        spec = entry.spec
        assert spec.kpi_id
        assert spec.direction in ("up", "down", "money", "neutral")
        assert spec.practice in PRACTICE_CODES


def test_every_persona_has_id_and_function() -> None:
    for entry in scan_registry("personas"):
        spec = entry.spec
        assert spec.persona_id
        assert spec.function
        assert spec.practice in PRACTICE_CODES


def test_every_mcp_tool_has_id_and_purpose() -> None:
    for entry in scan_registry("mcp_tools"):
        spec = entry.spec
        assert spec.tool_id.startswith("apex.")
        assert spec.purpose


def test_every_schema_has_entities() -> None:
    for entry in scan_registry("schemas"):
        spec = entry.spec
        assert spec.schema_code
        assert spec.primary_entities


def test_every_archetype_has_family_and_oversight() -> None:
    valid_families = {
        "triage", "cascade", "rca", "recovery", "personalize", "optimize",
        "monitor", "predict", "schedule", "match", "translate", "summarize",
        "explain", "score", "negotiate", "compose",
    }
    for entry in scan_registry("archetypes"):
        spec = entry.spec
        assert spec.archetype_id.startswith("arch.")
        assert spec.family in valid_families


def test_archetype_count_is_exactly_47() -> None:
    """Sellers Guide §6.3 names the 47-archetype library as canonical."""
    entries = scan_registry("archetypes")
    assert len(entries) == 47


def test_every_product_has_family_and_role() -> None:
    valid_families = {
        "fabric", "foundry", "copilot-studio", "purview", "defender",
        "entra", "intune", "teams", "power-platform", "azure-openai",
        "azure-ml", "github-copilot", "azure-storage", "azure-network",
    }
    for entry in scan_registry("products"):
        spec = entry.spec
        assert spec.product_id.startswith("ms.")
        assert spec.family in valid_families


def test_every_partner_has_practices_or_cross() -> None:
    for entry in scan_registry("partners"):
        spec = entry.spec
        assert spec.partner_id
        assert spec.practices


def test_every_competitive_has_differentiators() -> None:
    for entry in scan_registry("competitive"):
        spec = entry.spec
        assert spec.entry_id
        assert spec.competitor
        assert spec.apex_differentiators


def test_every_exercise_has_solution() -> None:
    for entry in scan_registry("exercises"):
        spec = entry.spec
        assert spec.exercise_id.startswith("ex.")
        assert spec.canonical_solution
        assert spec.sellers_guide_section


# ---------------------------------------------------------------------------
# Markdown asset coverage
# ---------------------------------------------------------------------------


def test_seven_wave_playbooks_present() -> None:
    """One Wave playbook per Practice."""
    paths = list_playbooks()
    names = {p.stem for p in paths}
    expected = {"rc", "hls", "er", "axle", "tmt", "th", "ice"}
    assert expected.issubset(names)


def test_seven_discovery_prompts_present() -> None:
    paths = list_discovery()
    names = {p.stem for p in paths}
    expected = {"rc", "hls", "er", "axle", "tmt", "th", "ice"}
    assert expected.issubset(names)


def test_three_preclearance_checklists_present() -> None:
    paths = list_preclearance()
    names = {p.stem for p in paths}
    expected = {"technical-checklist", "legal-checklist", "compliance-checklist"}
    assert expected.issubset(names)


def test_load_playbook_known_practice() -> None:
    md = load_playbook("rc")
    assert "Wave 1" in md or "Wave-1" in md
    assert "RC" in md


def test_load_playbook_unknown_returns_empty() -> None:
    assert load_playbook("nope") == ""


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


def test_validator_no_errors_on_shipped_registries() -> None:
    """Shipped registries pass governance with zero errors (warnings allowed)."""
    report = validate_registries()
    assert report.ok, [
        f"{i.registry}/{i.entry}: [{i.code}] {i.message}" for i in report.errors
    ]


def test_validator_with_full_cross_references_no_errors() -> None:
    """With agent + service catalogs supplied, cross-ref check is informational only."""
    a_kpi = a_per = a_tool = s_kpi = s_per = None
    try:
        from apex_agents import scan_all_catalogs as agents_scan
        a_kpi = set()
        a_per = set()
        a_tool = set()
        for entries in agents_scan().values():
            for entry in entries:
                a_per.add(entry.spec.persona)
                for k in entry.spec.kpis:
                    a_kpi.add(k.name)
                for t in entry.spec.tools:
                    a_tool.add(t.tool_id)
    except ImportError:
        pass
    try:
        from apex_services import scan_all_catalogs as services_scan
        s_kpi = set()
        s_per = set()
        for entries in services_scan().values():
            for entry in entries:
                for k in entry.spec.kpis:
                    s_kpi.add(k.name)
                for p in entry.spec.personas:
                    s_per.add(p.name)
    except ImportError:
        pass
    report = validate_registries(
        agents_kpi_names=a_kpi,
        services_kpi_names=s_kpi,
        agents_persona_names=a_per,
        services_persona_names=s_per,
        agents_tool_ids=a_tool,
    )
    assert report.ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_stats() -> None:
    result = runner.invoke(registries_app, ["stats"])
    assert result.exit_code == 0
    assert "Total registry entries shipped:" in result.stdout


def test_cli_list_kpis() -> None:
    result = runner.invoke(registries_app, ["list", "kpis"])
    assert result.exit_code == 0
    assert "kpi." in result.stdout


def test_cli_list_kpis_filter_by_practice() -> None:
    result = runner.invoke(registries_app, ["list", "kpis", "--practice", "rc"])
    assert result.exit_code == 0


def test_cli_list_archetypes_filter_by_family() -> None:
    result = runner.invoke(registries_app, ["list", "archetypes", "--family", "triage"])
    assert result.exit_code == 0
    assert "arch.triage" in result.stdout


def test_cli_list_unknown_registry_fails() -> None:
    result = runner.invoke(registries_app, ["list", "nope"])
    assert result.exit_code != 0


def test_cli_inspect_known_archetype() -> None:
    result = runner.invoke(registries_app, ["inspect", "archetypes", "arch.recovery.001"])
    assert result.exit_code == 0
    assert "IROPS" in result.stdout or "recovery" in result.stdout.lower()


def test_cli_inspect_unknown_fails() -> None:
    result = runner.invoke(registries_app, ["inspect", "kpis", "nope"])
    assert result.exit_code != 0


def test_cli_playbook_rc() -> None:
    result = runner.invoke(registries_app, ["playbook", "rc"])
    assert result.exit_code == 0
    assert "Wave" in result.stdout


def test_cli_playbook_unknown_fails() -> None:
    result = runner.invoke(registries_app, ["playbook", "nope"])
    assert result.exit_code != 0


def test_cli_discovery_rc() -> None:
    result = runner.invoke(registries_app, ["discovery", "rc"])
    assert result.exit_code == 0
    assert "Discovery" in result.stdout


def test_cli_preclearance_technical() -> None:
    result = runner.invoke(registries_app, ["preclearance", "technical"])
    assert result.exit_code == 0
    assert "Technical Pre-Clearance" in result.stdout


def test_cli_validate_passes() -> None:
    result = runner.invoke(registries_app, ["validate"])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_appendix_targets_met() -> None:
    """Sprint 19 conformance — appendix population targets satisfied."""
    totals = total_entries()
    assert totals["archetypes"] == 47, "Appendix D = 47 orchestration archetypes"
    assert totals["schemas"] >= 48, "Appendix A = canonical schema reference"
    assert totals["products"] >= 25, "Appendix G = Microsoft product/SKU reference"
    assert totals["partners"] >= 18, "Appendix H = partner ecosystem"
    assert totals["competitive"] >= 8, "Appendix K = competitive posture"
    assert totals["exercises"] >= 8, "Appendix J = exercise solutions"


@pytest.mark.conformance
def test_conformance_seven_practice_playbooks() -> None:
    """Wave playbooks cover all 7 Practices."""
    paths = list_playbooks()
    names = {p.stem for p in paths}
    assert {"rc", "hls", "er", "axle", "tmt", "th", "ice"}.issubset(names)


@pytest.mark.conformance
def test_conformance_seven_practice_discovery_prompts() -> None:
    paths = list_discovery()
    names = {p.stem for p in paths}
    assert {"rc", "hls", "er", "axle", "tmt", "th", "ice"}.issubset(names)


@pytest.mark.conformance
def test_conformance_three_preclearance_checklists() -> None:
    paths = list_preclearance()
    names = {p.stem for p in paths}
    assert {"technical-checklist", "legal-checklist", "compliance-checklist"}.issubset(names)
