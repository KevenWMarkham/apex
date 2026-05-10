"""Tests for ``apex_m.agent_framework_loader`` — Sprint 42 architecture validation.

Authored Sprint 32-34 work-back. Validates that the agent.yaml + prompts
+ MCP tools authored in Sprints 32 + 34 actually compile through the
Microsoft Agent Framework loader. When the SDK is absent (default test
environment), the loader runs in mock mode and returns a captured
:class:`WorkflowSpec` we can inspect directly.

These tests prove the spec-level production-readiness of every artifact
the service sprints have shipped — Sprint 42 swaps the mock dispatch for
real ``AgentWorkflowBuilder`` calls without re-touching anything below.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from apex_m.agent_framework_loader import (
    ALL_PATTERNS,
    AgentSpec,
    ApexAuditMiddleware,
    WorkflowSpec,
    _DispatchResult,
    _PATTERN_TO_BUILDER_METHOD,
    _ToolAdapter,
    build_workflow,
    dispatch_to_builder,
    get_audit_sink,
    has_agent_framework,
    load_agent_spec,
    load_use_case_workflow,
    reset_audit_sink_for_test,
    resolve_tool_for_role,
    wrap_mcp_tool,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SERVICES_DIR = REPO_ROOT / "services" / "rc"

RC_E2E_03_USE_CASE = SERVICES_DIR / "RC-E2E-03" / "use-cases" / "_default" / "use-case.yaml"
RC_E2E_04_USE_CASE = SERVICES_DIR / "RC-E2E-04" / "use-cases" / "_default" / "use-case.yaml"

RC_E2E_03_AGENTS_DIR = (
    SERVICES_DIR / "RC-E2E-03" / "scenarios"
    / "rc-cold-chain-excursion-mid-shift" / "agents"
)
RC_E2E_04_AGENTS_DIR = (
    SERVICES_DIR / "RC-E2E-04" / "scenarios"
    / "rc-loyalty-churn-prediction-winback" / "agents"
)


@pytest.fixture(autouse=True)
def _reset_audit() -> None:
    reset_audit_sink_for_test()


# ---------------------------------------------------------------------------
# 5-pattern surface
# ---------------------------------------------------------------------------


def test_all_patterns_match_agent_framework_builder_method_names() -> None:
    """ADR-006 — APEX names map verbatim to AgentWorkflowBuilder.Build*."""
    expected = {
        "sequential": "BuildSequential",
        "concurrent": "BuildConcurrent",
        "handoff":    "BuildHandoff",
        "group_chat": "BuildGroupChat",
        "magentic":   "BuildMagentic",
    }
    assert set(ALL_PATTERNS) == set(expected)
    for pattern, method in expected.items():
        assert _PATTERN_TO_BUILDER_METHOD[pattern] == method


# ---------------------------------------------------------------------------
# Per-agent.yaml load
# ---------------------------------------------------------------------------


def test_load_agent_spec_for_rc_e2e_03_pricing() -> None:
    """The Pricer agent.yaml + pricing.md compile to a complete AgentSpec."""
    spec = load_agent_spec(RC_E2E_03_AGENTS_DIR / "pricing" / "agent.yaml")
    assert isinstance(spec, AgentSpec)
    assert spec.role == "pricing"
    assert spec.label == "The Pricer"
    assert spec.canonical_pattern == "magentic"
    assert spec.model == "gpt-4o-2024-11-20"
    assert spec.hitl_gate is True
    assert spec.audit_row_emit is True
    assert "trade_secret" in spec.classification_propagation
    assert "rc_e2e_03.get_pricing_recommendation_basis" in spec.tool_names
    assert "PROML.Pricing" in spec.schemas_read
    assert spec.prompt_version == "1.0.0"
    assert spec.manifest_version == "1.0.0"
    # Prompt body loaded — has the strict JSON contract section
    assert "Pricing Agent" in spec.instructions
    assert "MUST NOT" in spec.instructions


def test_load_agent_spec_rejects_missing_required_field(tmp_path: Path) -> None:
    bad = tmp_path / "agent.yaml"
    bad.write_text("role: x\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required fields"):
        load_agent_spec(bad)


def test_load_agent_spec_rejects_unknown_canonical_pattern(tmp_path: Path) -> None:
    """Pattern names must be one of the five Agent Framework primitives."""
    bad = tmp_path / "agent.yaml"
    bad.write_text(
        "role: x\nservice_code: x\nscenario_id: x\nmodel: gpt-4o\n"
        "prompt_ref: prompts/x.md\ncanonical_pattern: orchestral\n"
        "prompt_version: 1.0.0\nmanifest_version: 1.0.0\n",
        encoding="utf-8",
    )
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "x.md").write_text("body\n", encoding="utf-8")
    with pytest.raises(ValueError, match="canonical_pattern"):
        load_agent_spec(bad)


def test_load_agent_spec_rejects_missing_prompt_file(tmp_path: Path) -> None:
    bad = tmp_path / "agent.yaml"
    bad.write_text(
        "role: x\nservice_code: x\nscenario_id: x\nmodel: gpt-4o\n"
        "prompt_ref: prompts/missing.md\ncanonical_pattern: sequential\n"
        "prompt_version: 1.0.0\nmanifest_version: 1.0.0\n",
        encoding="utf-8",
    )
    with pytest.raises(FileNotFoundError, match="missing.md"):
        load_agent_spec(bad)


# ---------------------------------------------------------------------------
# Use-case → workflow round-trip (the headline test)
# ---------------------------------------------------------------------------


def test_rc_e2e_03_use_case_compiles_to_magentic_workflow() -> None:
    """RC-E2E-03 default use-case → Magentic workflow with 7 agents.

    This is the headline architecture-validation test. If the use-case YAML +
    every agent.yaml + every prompt.md round-trip cleanly through the loader,
    Sprint 42's real-mode dispatch is mechanical (it only swaps the agent
    constructors).
    """
    spec, dispatched = build_workflow(RC_E2E_03_USE_CASE)

    # Spec inspection
    assert isinstance(spec, WorkflowSpec)
    assert spec.use_case_id == "rc-e2e-03--default"
    assert spec.service_code == "RC-E2E-03"
    assert spec.scenario_id == "rc-cold-chain-excursion-mid-shift"
    assert spec.canonical_pattern == "magentic"
    assert spec.builder_method_name == "BuildMagentic"

    # All 7 cold-chain agents present
    roles = sorted(a.role for a in spec.agents)
    assert roles == ["act", "assess", "classify", "decide", "learn", "pricing", "quantify"]

    # Magentic manager: first non-gate role alphabetically. assess + classify
    # + learn + quantify + act all hitl_gate=false; sorted: act < assess.
    assert spec.manager_role == "act"  # canonical first non-gate role

    # Dispatch (mock mode) captures the right Build* method name
    assert isinstance(dispatched, _DispatchResult)
    assert dispatched.builder_method_name == "BuildMagentic"
    assert set(dispatched.agent_roles) == set(roles)


def test_rc_e2e_04_use_case_compiles_to_sequential_workflow() -> None:
    """RC-E2E-04 default use-case → Sequential workflow with 6 agents."""
    spec, dispatched = build_workflow(RC_E2E_04_USE_CASE)

    assert spec.canonical_pattern == "sequential"
    assert spec.builder_method_name == "BuildSequential"
    assert spec.use_case_id == "rc-e2e-04--default"

    roles = sorted(a.role for a in spec.agents)
    assert roles == ["act", "assess", "classify", "decide", "learn", "quantify"]

    # Sequential pattern → no manager_role (only Magentic uses one)
    assert spec.manager_role is None

    assert isinstance(dispatched, _DispatchResult)
    assert dispatched.builder_method_name == "BuildSequential"
    assert dispatched.manager_role is None


def test_every_agent_in_rc_e2e_03_carries_three_version_stamp() -> None:
    """Roadmap.md BL.P.79 — manifest_version, policy_version, prompt_version."""
    spec, _ = build_workflow(RC_E2E_03_USE_CASE)
    for agent in spec.agents:
        assert agent.prompt_version == "1.0.0"
        assert agent.manifest_version == "1.0.0"
        # policy_version is provided by the tenant config snapshot; not
        # captured per-agent in the YAML — middleware injects it.


def test_rc_e2e_03_pricer_carries_classification_propagation() -> None:
    """The Pricer touches TRADE_SECRET data — must declare propagation."""
    spec, _ = build_workflow(RC_E2E_03_USE_CASE)
    pricer = next(a for a in spec.agents if a.role == "pricing")
    assert "trade_secret" in pricer.classification_propagation


def test_rc_e2e_04_decide_declares_hitl_persona() -> None:
    """RC-E2E-04 Decide routes to Maya Patel."""
    spec, _ = build_workflow(RC_E2E_04_USE_CASE)
    decide = next(a for a in spec.agents if a.role == "decide")
    assert decide.hitl_gate is True
    assert decide.hitl_persona == "maya-patel-loyalty-crm-director"


def test_rc_e2e_04_decide_declares_tier3_pii_unlock_in_extra() -> None:
    """Sprint 34.3 — Tier-3 PII fields preserved in agent.extra."""
    spec, _ = build_workflow(RC_E2E_04_USE_CASE)
    decide = next(a for a in spec.agents if a.role == "decide")
    assert decide.extra.get("tier3_pii_unlock_ttl_seconds") == 60
    purposes = decide.extra.get("tier3_pii_unlock_authorised_purposes", [])
    assert "winback_offer_distribution" in purposes


# ---------------------------------------------------------------------------
# Pattern dispatcher
# ---------------------------------------------------------------------------


def _make_dummy_spec(pattern: str, agent_count: int = 3) -> WorkflowSpec:
    return WorkflowSpec(
        service_code="X",
        scenario_id="x",
        use_case_id="x--default",
        canonical_pattern=pattern,  # type: ignore[arg-type]
        builder_method_name=_PATTERN_TO_BUILDER_METHOD[pattern],  # type: ignore[index]
        agents=tuple(
            AgentSpec(
                role=f"r{i}", label=f"R{i}", service_code="X", scenario_id="x",
                canonical_pattern=pattern,  # type: ignore[arg-type]
                model="gpt-4o", instructions="x", tool_names=(),
                schemas_read=(), schemas_write=(),
                hitl_gate=False, hitl_persona=None,
                hitl_thresholds_consumed=(),
                audit_row_emit=True, classification_propagation=("internal",),
                prompt_version="1.0.0", manifest_version="1.0.0",
                operator_obo_required=False,
            )
            for i in range(agent_count)
        ),
        manager_role="r0" if pattern == "magentic" else None,
    )


@pytest.mark.parametrize("pattern", list(ALL_PATTERNS))
def test_dispatch_to_builder_returns_correct_method_name(pattern: str) -> None:
    """All 5 patterns route to the right AgentWorkflowBuilder.Build* method."""
    spec = _make_dummy_spec(pattern)
    result = dispatch_to_builder(spec)
    assert isinstance(result, _DispatchResult)
    assert result.builder_method_name == _PATTERN_TO_BUILDER_METHOD[pattern]
    assert result.agent_roles == ("r0", "r1", "r2")


def test_dispatch_to_builder_magentic_carries_manager_role() -> None:
    spec = _make_dummy_spec("magentic")
    result = dispatch_to_builder(spec)
    assert result.builder_method_name == "BuildMagentic"
    assert result.manager_role == "r0"


# ---------------------------------------------------------------------------
# Tool wrapper
# ---------------------------------------------------------------------------


def test_wrap_mcp_tool_returns_adapter_in_mock_mode() -> None:
    """Without agent_framework installed, wrapper captures name + callable."""
    def my_tool(x: int) -> int:
        return x + 1

    wrapped = wrap_mcp_tool("rc_e2e_03.fake_tool", my_tool)
    if has_agent_framework():
        # Real mode — wrapped is the decorated function; we just assert callable.
        assert callable(wrapped)
    else:
        assert isinstance(wrapped, _ToolAdapter)
        assert wrapped.qualified_name == "rc_e2e_03.fake_tool"
        assert wrapped.callable is my_tool


def test_resolve_tool_for_role_finds_rc_e2e_03_tool() -> None:
    """Sprint 32 — `rc_e2e_03.get_excursion_decision_panel` resolves."""
    fn = resolve_tool_for_role("rc_e2e_03.get_excursion_decision_panel")
    assert fn is not None
    assert callable(fn)


def test_resolve_tool_for_role_finds_rc_e2e_04_tool() -> None:
    """Sprint 34 — `rc_e2e_04.commit_winback_offer` resolves."""
    fn = resolve_tool_for_role("rc_e2e_04.commit_winback_offer")
    assert fn is not None
    assert callable(fn)


def test_resolve_tool_for_role_returns_none_for_unknown_server() -> None:
    assert resolve_tool_for_role("not-an-mcp.tool") is None


def test_resolve_tool_for_role_returns_none_for_missing_function() -> None:
    """Tool name resolves to a real package but the function doesn't exist."""
    assert resolve_tool_for_role("rc_e2e_03.no_such_tool") is None


def test_pricer_tools_resolve_through_loader() -> None:
    """The Pricer's declared tools resolve to actual MCP callables."""
    spec, _ = build_workflow(RC_E2E_03_USE_CASE)
    pricer = next(a for a in spec.agents if a.role == "pricing")
    resolved = [resolve_tool_for_role(t) for t in pricer.tool_names]
    # `rc_e2e_03.get_pricing_recommendation_basis` MUST resolve (Sprint 32.8 ships it).
    pricing_basis = next(
        (r for r, name in zip(resolved, pricer.tool_names)
         if name == "rc_e2e_03.get_pricing_recommendation_basis"),
        None,
    )
    assert pricing_basis is not None and callable(pricing_basis)


# ---------------------------------------------------------------------------
# ApexAuditMiddleware — three-version stamp + classification propagation
# ---------------------------------------------------------------------------


def test_apex_audit_middleware_stamps_three_versions() -> None:
    """BL.P.79 — manifest / policy / prompt versions emit on every audit row."""
    pricer = load_agent_spec(RC_E2E_03_AGENTS_DIR / "pricing" / "agent.yaml")
    middleware = ApexAuditMiddleware(pricer, policy_version="1.0.0")
    inputs_hash = hashlib.sha256(b"in").hexdigest()
    outputs_hash = hashlib.sha256(b"out").hexdigest()

    record = middleware.stamp_synchronously(
        trace_id="trace-test-001",
        inputs_hash=inputs_hash,
        outputs_hash=outputs_hash,
        operator_principal="marisol.reyes@labtenant.onmicrosoft.com",
        duration_ms=42,
    )

    assert record.manifest_version == "1.0.0"
    assert record.prompt_version == "1.0.0"
    assert record.policy_version == "1.0.0"
    assert record.role == "pricing"
    assert record.service_code == "RC-E2E-03"
    assert record.scenario_id == "rc-cold-chain-excursion-mid-shift"
    assert record.inputs_hash == inputs_hash
    assert record.outputs_hash == outputs_hash
    assert record.duration_ms == 42


def test_apex_audit_middleware_propagates_classification_to_audit_row() -> None:
    """BL.P.86 lineage — classification flows from agent.yaml to audit row."""
    pricer = load_agent_spec(RC_E2E_03_AGENTS_DIR / "pricing" / "agent.yaml")
    middleware = ApexAuditMiddleware(pricer)
    record = middleware.stamp_synchronously(
        trace_id="t", inputs_hash="i", outputs_hash="o",
    )
    assert "trade_secret" in record.classification


def test_audit_sink_collects_records_across_calls() -> None:
    pricer = load_agent_spec(RC_E2E_03_AGENTS_DIR / "pricing" / "agent.yaml")
    mw = ApexAuditMiddleware(pricer)
    mw.stamp_synchronously(trace_id="t1", inputs_hash="a", outputs_hash="b")
    mw.stamp_synchronously(trace_id="t2", inputs_hash="c", outputs_hash="d")
    sink = get_audit_sink()
    assert len(sink) == 2
    assert sink[0].trace_id == "t1"
    assert sink[1].trace_id == "t2"


# ---------------------------------------------------------------------------
# Real-mode guard
# ---------------------------------------------------------------------------


def test_build_workflow_real_mode_raises_when_sdk_absent() -> None:
    """real_mode=True without agent_framework installed must fail clearly."""
    if has_agent_framework():
        pytest.skip("agent_framework is installed; real mode is exercisable")
    with pytest.raises(RuntimeError, match="agent-framework"):
        build_workflow(RC_E2E_03_USE_CASE, real_mode=True)


def test_default_mode_works_without_sdk_for_rc_e2e_03() -> None:
    """Mock-mode default: no SDK required, full spec captured."""
    spec, dispatched = build_workflow(RC_E2E_03_USE_CASE)
    assert spec.builder_method_name == "BuildMagentic"
    assert dispatched is not None
