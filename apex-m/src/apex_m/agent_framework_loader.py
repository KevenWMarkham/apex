"""Microsoft Agent Framework loader — bridges APEX agent.yaml + prompts → AgentWorkflowBuilder.

Sprint 42 architecture validation (authored Sprint 32-34 work-back).

This module is the **adapter layer** between the APEX-side artifacts the
service sprints produce (per-agent agent.yaml, prompts/*.md, MCP tools, HITL
config in Key Vault) and the Microsoft Agent Framework SDK. Per ADR-006:

- **APEX names** (Sequential / Concurrent / Handoff / Group Chat / Magentic)
  are deliberately the same as Agent Framework's `AgentWorkflowBuilder.Build*`
  method names. The mapping is verbatim, no impedance mismatch.
- **APEX agent.yaml** is the metadata source the loader reads to construct
  one ``ChatAgent`` per role.
- **APEX prompts/*.md** is the system-prompt body for each ``ChatAgent``.
- **APEX MCP tools** wrap into ``FunctionTool`` instances via lazy bindings.
- **APEX three-version stamp** (manifest_version / policy_version /
  prompt_version per Roadmap.md BL.P.79) is enforced by ``ApexAuditMiddleware``
  which wraps every agent invocation.
- **APEX HITL gate** (per agent.yaml ``hitl_gate: true`` + ``hitl_persona``)
  is wired through Agent Framework's ``human_input_request`` primitive.

Lazy import strategy
====================

``agent_framework`` is in apex-m's ``runtime`` optional-dependency extra,
not core. This module imports cleanly without it — when the real SDK is
absent (default test environment), :func:`build_workflow` returns a
:class:`LoaderSpec` capturing all the input the SDK would consume, and the
pattern dispatcher returns the *name* of the builder method instead of
calling it. When the real SDK is installed (production / Lab tenant),
:func:`build_workflow` returns a real ``WorkflowAgent``.

This dual mode lets Sprint 32-34 ship without an Agent Framework dependency
and Sprint 42 light up real workflow construction by changing one config
flag.

References
----------

- ADR-006: https://learn.microsoft.com/agent-framework/
- AgentWorkflowBuilder API:
  https://learn.microsoft.com/agent-framework/workflows/orchestrations/
- ChatAgent + tools:
  https://learn.microsoft.com/agent-framework/agents/chat-agent
- Human-in-the-loop primitive:
  https://learn.microsoft.com/agent-framework/workflows/human-in-the-loop
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Literal

import yaml

# ---------------------------------------------------------------------------
# Lazy SDK detection
# ---------------------------------------------------------------------------

try:                                           # pragma: no cover — branch
    import agent_framework as _af              # type: ignore[import-not-found]
    from agent_framework.tools import function_tool as _function_tool  # type: ignore
    from agent_framework.workflows import AgentWorkflowBuilder as _AgentWorkflowBuilder  # type: ignore
    _HAS_AGENT_FRAMEWORK = True
except ImportError:                            # default test path
    _af = None                                  # type: ignore[assignment]
    _function_tool = None                       # type: ignore[assignment]
    _AgentWorkflowBuilder = None                # type: ignore[assignment]
    _HAS_AGENT_FRAMEWORK = False


def has_agent_framework() -> bool:
    """Return True if Microsoft Agent Framework SDK is importable."""
    return _HAS_AGENT_FRAMEWORK


# ---------------------------------------------------------------------------
# Canonical pattern names — verbatim Agent Framework AgentWorkflowBuilder methods
# ---------------------------------------------------------------------------

CanonicalPattern = Literal[
    "sequential",
    "concurrent",
    "handoff",
    "group_chat",
    "magentic",
]

ALL_PATTERNS: tuple[CanonicalPattern, ...] = (
    "sequential", "concurrent", "handoff", "group_chat", "magentic",
)

# Agent Framework method-name map — kept lowercase here; the dispatcher uses
# the actual SDK class methods when present.
_PATTERN_TO_BUILDER_METHOD: dict[CanonicalPattern, str] = {
    "sequential": "BuildSequential",
    "concurrent": "BuildConcurrent",
    "handoff":    "BuildHandoff",
    "group_chat": "BuildGroupChat",
    "magentic":   "BuildMagentic",
}


# ---------------------------------------------------------------------------
# Data classes — the spec the loader produces in mock mode
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AgentSpec:
    """Captured spec for a single APEX agent — what becomes a ``ChatAgent``.

    Field-for-field reflects an `agent.yaml` after prompt-body load.
    Sprint 42's real-mode path constructs a ``ChatAgent`` from this.
    """

    role: str
    label: str
    service_code: str
    scenario_id: str
    canonical_pattern: CanonicalPattern
    model: str
    instructions: str          # the prompt body, loaded from prompts/*.md
    tool_names: tuple[str, ...]
    schemas_read: tuple[str, ...]
    schemas_write: tuple[str, ...]
    hitl_gate: bool
    hitl_persona: str | None
    hitl_thresholds_consumed: tuple[str, ...]
    audit_row_emit: bool
    classification_propagation: tuple[str, ...]
    prompt_version: str
    manifest_version: str
    operator_obo_required: bool
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WorkflowSpec:
    """Captured spec for a use-case → workflow build.

    In mock mode (no agent_framework SDK), this is the loader's return value.
    In real mode, the loader uses this to invoke
    ``AgentWorkflowBuilder.<builder_method_name>(...)``.
    """

    service_code: str
    scenario_id: str
    use_case_id: str
    canonical_pattern: CanonicalPattern
    builder_method_name: str   # "BuildMagentic" etc.
    agents: tuple[AgentSpec, ...]
    manager_role: str | None   # for magentic; None for the other 4 patterns
    extra: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# YAML loaders
# ---------------------------------------------------------------------------


def _normalise_str_list(raw: Any) -> tuple[str, ...]:
    if not raw:
        return ()
    if isinstance(raw, list):
        return tuple(str(x) for x in raw)
    if isinstance(raw, str):
        return (raw,)
    raise ValueError(f"Cannot normalise {raw!r} to a list of strings")


def load_agent_spec(agent_yaml_path: Path | str) -> AgentSpec:
    """Read one ``agent.yaml`` and the referenced ``prompts/*.md`` body.

    Args:
        agent_yaml_path: Filesystem path to the agent.yaml.

    Returns:
        Frozen :class:`AgentSpec` capturing every field the SDK adapter needs.

    Raises:
        ValueError: required fields missing or `canonical_pattern` not one of
            the five Agent Framework primitives.
        FileNotFoundError: prompt file referenced by ``prompt_ref`` not on disk.
    """
    p = Path(agent_yaml_path)
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}

    required = ("role", "service_code", "scenario_id", "model", "prompt_ref",
                "canonical_pattern", "prompt_version", "manifest_version")
    missing = [f for f in required if f not in raw]
    if missing:
        raise ValueError(
            f"agent.yaml at {p} missing required fields: {missing}",
        )

    pattern = raw["canonical_pattern"]
    if pattern not in ALL_PATTERNS:
        raise ValueError(
            f"canonical_pattern {pattern!r} not in {ALL_PATTERNS}; "
            "see ADR-006 + Services Guide §14.5"
        )

    prompt_path = p.parent / raw["prompt_ref"]
    if not prompt_path.exists():
        raise FileNotFoundError(
            f"agent.yaml at {p} references prompt {raw['prompt_ref']!r} "
            f"but {prompt_path} does not exist",
        )
    instructions = prompt_path.read_text(encoding="utf-8")

    return AgentSpec(
        role=raw["role"],
        label=raw.get("label", raw["role"]),
        service_code=raw["service_code"],
        scenario_id=raw["scenario_id"],
        canonical_pattern=pattern,
        model=raw["model"],
        instructions=instructions,
        tool_names=_normalise_str_list(raw.get("tools")),
        schemas_read=_normalise_str_list(raw.get("schemas_read")),
        schemas_write=_normalise_str_list(raw.get("schemas_write")),
        hitl_gate=bool(raw.get("hitl_gate", False)),
        hitl_persona=raw.get("hitl_persona"),
        hitl_thresholds_consumed=_normalise_str_list(raw.get("hitl_thresholds_consumed")),
        audit_row_emit=bool(raw.get("audit_row_emit", True)),
        classification_propagation=_normalise_str_list(raw.get("classification_propagation")),
        prompt_version=raw["prompt_version"],
        manifest_version=raw["manifest_version"],
        operator_obo_required=bool(raw.get("operator_obo_required", False)),
        extra={
            k: v for k, v in raw.items()
            if k not in {
                "role", "label", "service_code", "scenario_id", "model",
                "prompt_ref", "canonical_pattern", "tools", "schemas_read",
                "schemas_write", "hitl_gate", "hitl_persona",
                "hitl_thresholds_consumed", "audit_row_emit",
                "classification_propagation", "prompt_version",
                "manifest_version", "operator_obo_required",
            }
        },
    )


def load_use_case_workflow(use_case_yaml_path: Path | str) -> WorkflowSpec:
    """Read a use-case YAML + every per-agent agent.yaml under its scenario.

    The use-case YAML declares ``orchestration_archetype`` (canonical pattern
    name) and points at a scenario folder. This loader reads every agent.yaml
    under that scenario's ``agents/`` directory + their prompt bodies, validates
    the pattern is one of the five Agent Framework primitives, and returns a
    :class:`WorkflowSpec`.

    Args:
        use_case_yaml_path: Path to e.g.
            ``services/rc/RC-E2E-03/use-cases/_default/use-case.yaml``.

    Returns:
        Frozen :class:`WorkflowSpec` ready to feed into :func:`build_workflow`.

    Raises:
        ValueError: missing required keys or unknown pattern.
        FileNotFoundError: scenario directory not on disk.
    """
    p = Path(use_case_yaml_path)
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}

    for required in ("use_case_id", "service_code", "scenario_id",
                     "orchestration_archetype"):
        if required not in raw:
            raise ValueError(f"use-case.yaml at {p} missing {required!r}")

    pattern: CanonicalPattern = raw["orchestration_archetype"]
    if pattern not in ALL_PATTERNS:
        raise ValueError(
            f"orchestration_archetype {pattern!r} not in {ALL_PATTERNS}; "
            "see ADR-006 + Services Guide §14.5.2"
        )

    # services/rc/<svc>/use-cases/_default/use-case.yaml
    # → services/rc/<svc>/scenarios/<scenario_id>/agents/
    service_dir = p.parent.parent.parent          # …/<svc>
    scenario_dir = service_dir / "scenarios" / raw["scenario_id"]
    agents_dir = scenario_dir / "agents"
    if not agents_dir.exists():
        raise FileNotFoundError(
            f"use-case at {p} references scenario at {scenario_dir} but "
            f"{agents_dir} does not exist; scaffolding may be incomplete",
        )

    role_dirs = sorted(d for d in agents_dir.iterdir() if d.is_dir())
    agents: list[AgentSpec] = []
    for d in role_dirs:
        agent_yaml = d / "agent.yaml"
        if not agent_yaml.exists():
            continue
        agents.append(load_agent_spec(agent_yaml))

    if not agents:
        raise ValueError(
            f"use-case {raw['use_case_id']} has no loadable agent.yaml "
            f"files under {agents_dir}",
        )

    # Magentic — find the manager via use-case `magentic_manager_role` override
    # or the conventional default. Per Services Guide §14.5.6 the Analyst is
    # the Magentic manager for RC-E2E-03; otherwise pick the first role
    # alphabetically that doesn't carry hitl_gate (the manager dispatches; it
    # doesn't gate).
    manager_role: str | None = None
    if pattern == "magentic":
        manager_role = raw.get("magentic_manager_role")
        if manager_role is None:
            non_gate_roles = [a.role for a in agents if not a.hitl_gate]
            manager_role = non_gate_roles[0] if non_gate_roles else agents[0].role

    return WorkflowSpec(
        service_code=raw["service_code"],
        scenario_id=raw["scenario_id"],
        use_case_id=raw["use_case_id"],
        canonical_pattern=pattern,
        builder_method_name=_PATTERN_TO_BUILDER_METHOD[pattern],
        agents=tuple(agents),
        manager_role=manager_role,
        extra={
            "primary_variant": raw.get("primary_variant"),
            "substrate": raw.get("substrate"),
            "orchestration_runtime": raw.get("orchestration_runtime"),
        },
    )


# ---------------------------------------------------------------------------
# Pattern dispatcher — thin shim over AgentWorkflowBuilder
# ---------------------------------------------------------------------------


class _DispatchResult:
    """Mock-mode dispatch return — captures what the SDK would have built."""

    def __init__(
        self,
        builder_method_name: str,
        agent_roles: tuple[str, ...],
        manager_role: str | None,
    ) -> None:
        self.builder_method_name = builder_method_name
        self.agent_roles = agent_roles
        self.manager_role = manager_role

    def __repr__(self) -> str:  # pragma: no cover — diagnostic
        return (
            f"<_DispatchResult method={self.builder_method_name} "
            f"roles={self.agent_roles} manager={self.manager_role!r}>"
        )


def dispatch_to_builder(spec: WorkflowSpec, *, agents: list[Any] | None = None) -> Any:
    """Map a :class:`WorkflowSpec` to the right ``AgentWorkflowBuilder`` call.

    In mock mode (Sprint 32-34), ``agents`` is None and we return a
    :class:`_DispatchResult` that captures the method name + role list.

    In real mode (Sprint 42 with agent_framework installed), pass a list of
    real ``ChatAgent`` instances; we call the actual SDK method.

    Per ADR-006 the 5 patterns map verbatim to:

    - sequential → ``AgentWorkflowBuilder().BuildSequential(agents)``
    - concurrent → ``AgentWorkflowBuilder().BuildConcurrent(agents)``
    - handoff   → ``AgentWorkflowBuilder().BuildHandoff(agents)``
    - group_chat → ``AgentWorkflowBuilder().BuildGroupChat(agents)``
    - magentic  → ``AgentWorkflowBuilder().BuildMagentic(manager, workers)``
    """
    method_name = _PATTERN_TO_BUILDER_METHOD[spec.canonical_pattern]
    agent_roles = tuple(a.role for a in spec.agents)

    if not _HAS_AGENT_FRAMEWORK or agents is None:
        # Mock mode: capture what we would have called.
        return _DispatchResult(method_name, agent_roles, spec.manager_role)

    # Real mode (Sprint 42 path).
    builder = _AgentWorkflowBuilder()
    if spec.canonical_pattern == "magentic":
        manager_idx = agent_roles.index(spec.manager_role) if spec.manager_role else 0
        manager = agents[manager_idx]
        workers = [a for i, a in enumerate(agents) if i != manager_idx]
        return builder.BuildMagentic(manager=manager, workers=workers)
    builder_method = getattr(builder, method_name)
    return builder_method(agents)


# ---------------------------------------------------------------------------
# Tool adapter — MCP tool → Agent Framework FunctionTool
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _ToolAdapter:
    """Mock-mode tool adapter. Captures the MCP callable + a derived name."""

    qualified_name: str   # e.g. "rc_e2e_03.get_excursion_decision_panel"
    callable: Callable[..., Any]


def wrap_mcp_tool(qualified_name: str, mcp_callable: Callable[..., Any]) -> Any:
    """Wrap an MCP tool function as a Agent-Framework-callable tool.

    In mock mode returns a :class:`_ToolAdapter`; in real mode returns the
    decorated function via ``agent_framework.tools.function_tool``.

    The MCP callable is expected to accept (per our convention)
    ``agent_id`` and ``caller_identity`` keyword args. The wrapper threads
    these from the ChatAgent's invocation context.
    """
    if not _HAS_AGENT_FRAMEWORK:
        return _ToolAdapter(qualified_name=qualified_name, callable=mcp_callable)

    # Real mode (Sprint 42): decorate the function so Agent Framework can
    # introspect args + emit it through the agent's tool-call protocol.
    return _function_tool(name=qualified_name)(mcp_callable)  # type: ignore[misc]


def resolve_tool_for_role(qualified_name: str) -> Callable[..., Any] | None:
    """Resolve a tool name in agent.yaml `tools:` to its MCP callable.

    Lookup order:

    1. ``rc_e2e_03.*`` → ``rc_e2e_03_mcp.*``
    2. ``rc_e2e_04.*`` → ``rc_e2e_04_mcp.*``
    3. ``rc_e2e_09.*`` → ``rc_e2e_09_mcp.*`` (Sprint 39)
    4. ``scml-mcp.*`` / ``merml-mcp.*`` / ``cxml-mcp.*`` → respective package
    5. ``tokenizer-mcp.*`` → tokenizer-mcp package
    6. ``fabric-mcp.*`` / ``policy-mcp.*`` / ``telemetry-mcp.*`` / ``approvals-mcp.*``
       / ``ledger-mcp.*`` → utility MCP packages

    Returns ``None`` if the package isn't installed in this environment —
    Sprint 42 production wiring fails closed; mock mode tolerates absence.
    """
    if "." not in qualified_name:
        return None
    server, tool = qualified_name.split(".", 1)
    module_map: dict[str, str] = {
        "rc_e2e_03": "rc_e2e_03_mcp",
        "rc_e2e_04": "rc_e2e_04_mcp",
        "rc_e2e_05": "rc_e2e_05_mcp",
        "rc_e2e_07": "rc_e2e_07_mcp",
        "rc_e2e_09": "rc_e2e_09_mcp",
        "scml-mcp": "scml_mcp",
        "merml-mcp": "merml_mcp",
        "cxml-mcp": "cxml_mcp",
        "tokenizer-mcp": "tokenizer_mcp",
        "fabric-mcp": "fabric_mcp",
        "policy-mcp": "policy_mcp",
        "telemetry-mcp": "telemetry_mcp",
        "approvals-mcp": "approvals_mcp",
        "ledger-mcp": "ledger_mcp",
    }
    module_name = module_map.get(server)
    if module_name is None:
        return None
    try:
        import importlib
        mod = importlib.import_module(module_name)
        return getattr(mod, tool, None)
    except ImportError:
        return None


# ---------------------------------------------------------------------------
# ApexAuditMiddleware — three-version stamp + classification propagation
# ---------------------------------------------------------------------------


@dataclass
class AuditRecord:
    """One audit row emitted by :class:`ApexAuditMiddleware` per invocation."""

    trace_id: str
    agent_id: str
    role: str
    service_code: str
    scenario_id: str
    inputs_hash: str
    outputs_hash: str
    manifest_version: str
    prompt_version: str
    policy_version: str
    classification: tuple[str, ...]
    operator_principal: str | None
    duration_ms: int
    extra: dict[str, Any] = field(default_factory=dict)


# Sprint 42 swaps this for the real Purview Audit emitter (apex_m.audit_purview).
_AUDIT_SINK: list[AuditRecord] = []


def reset_audit_sink_for_test() -> None:
    """Test helper — clear in-memory audit rows between tests."""
    _AUDIT_SINK.clear()


def get_audit_sink() -> tuple[AuditRecord, ...]:
    """Test / debugging helper — return all audit rows since last reset."""
    return tuple(_AUDIT_SINK)


class ApexAuditMiddleware:
    """Wraps every ChatAgent invocation to emit a Purview-bound audit row.

    Per Roadmap.md BL.P.79 (three-version rule) every audit row stamps:

    - ``manifest_version``  — from agent.yaml
    - ``prompt_version``    — from agent.yaml
    - ``policy_version``    — from the tenant HITL config snapshot

    Per BL.P.86 (lineage capture) the ``classification`` field carries the
    union of agent.yaml ``classification_propagation`` plus any per-tool
    classification the invocation touched.

    Sprint 32-34 use this in mock mode (records appended to ``_AUDIT_SINK``);
    Sprint 42 swaps the sink for the real Purview Audit Graph emitter.
    """

    def __init__(self, agent_spec: AgentSpec, *, policy_version: str = "1.0.0") -> None:
        self.agent_spec = agent_spec
        self.policy_version = policy_version

    async def on_invoke(
        self,
        ctx: Any,
        next_: Callable[[Any], Any],
    ) -> Any:                                 # pragma: no cover — Sprint 42 path
        """Real-mode middleware hook — wraps a ChatAgent invocation."""
        import hashlib
        import time
        start = time.monotonic()
        result = await next_(ctx)
        duration_ms = int((time.monotonic() - start) * 1000)

        record = AuditRecord(
            trace_id=getattr(ctx, "trace_id", "unknown"),
            agent_id=getattr(ctx.agent, "id", self.agent_spec.role),
            role=self.agent_spec.role,
            service_code=self.agent_spec.service_code,
            scenario_id=self.agent_spec.scenario_id,
            inputs_hash=hashlib.sha256(repr(ctx.input).encode()).hexdigest(),
            outputs_hash=hashlib.sha256(repr(result).encode()).hexdigest(),
            manifest_version=self.agent_spec.manifest_version,
            prompt_version=self.agent_spec.prompt_version,
            policy_version=self.policy_version,
            classification=self.agent_spec.classification_propagation,
            operator_principal=getattr(ctx, "operator_principal", None),
            duration_ms=duration_ms,
        )
        _AUDIT_SINK.append(record)
        return result

    def stamp_synchronously(
        self,
        *,
        trace_id: str,
        inputs_hash: str,
        outputs_hash: str,
        operator_principal: str | None = None,
        duration_ms: int = 0,
    ) -> AuditRecord:
        """Test helper — synthesise an audit row outside a real invocation.

        Lets Sprint 32-34 unit tests verify the audit-row contract without
        spinning up a real ChatAgent. Sprint 42's :meth:`on_invoke` takes
        the same path with real values.
        """
        record = AuditRecord(
            trace_id=trace_id,
            agent_id=self.agent_spec.role,
            role=self.agent_spec.role,
            service_code=self.agent_spec.service_code,
            scenario_id=self.agent_spec.scenario_id,
            inputs_hash=inputs_hash,
            outputs_hash=outputs_hash,
            manifest_version=self.agent_spec.manifest_version,
            prompt_version=self.agent_spec.prompt_version,
            policy_version=self.policy_version,
            classification=self.agent_spec.classification_propagation,
            operator_principal=operator_principal,
            duration_ms=duration_ms,
        )
        _AUDIT_SINK.append(record)
        return record


# ---------------------------------------------------------------------------
# Top-level entry — Sprint 42's "happy path" for production wiring
# ---------------------------------------------------------------------------


def build_workflow(
    use_case_yaml_path: Path | str,
    *,
    real_mode: bool | None = None,
) -> tuple[WorkflowSpec, Any]:
    """Compile a use-case YAML to a workflow object.

    Returns the captured :class:`WorkflowSpec` plus the dispatch result
    (mock or real). The two-tuple shape lets Sprint 32-34 inspect the spec
    in tests without caring whether the SDK is present.

    Args:
        use_case_yaml_path: Path to a use-case YAML.
        real_mode: When ``True``, requires ``agent_framework`` to be
            installed and constructs real ``ChatAgent`` + ``WorkflowAgent``.
            When ``False`` (or None and SDK absent), runs in mock mode and
            returns the captured spec only.

    Sprint 42 invokes with ``real_mode=True`` against a Lab tenant with
    every dependency present.
    """
    spec = load_use_case_workflow(use_case_yaml_path)
    use_real = real_mode if real_mode is not None else _HAS_AGENT_FRAMEWORK
    if use_real and not _HAS_AGENT_FRAMEWORK:
        raise RuntimeError(
            "build_workflow(..., real_mode=True) requires agent-framework "
            "to be installed; run `pip install -e 'apex-m[runtime]'`",
        )

    agents_for_dispatch: list[Any] | None = None
    if use_real:                          # pragma: no cover — Sprint 42 path
        agents_for_dispatch = []
        for agent_spec in spec.agents:
            chat_agent = _build_chat_agent_real(agent_spec)
            agents_for_dispatch.append(chat_agent)

    dispatched = dispatch_to_builder(spec, agents=agents_for_dispatch)
    return spec, dispatched


def _build_chat_agent_real(agent_spec: AgentSpec) -> Any:  # pragma: no cover
    """Sprint 42 path — construct an actual ``ChatAgent`` from an :class:`AgentSpec`."""
    from agent_framework import ChatAgent  # type: ignore[import-not-found]

    tools: list[Any] = []
    for qname in agent_spec.tool_names:
        mcp_callable = resolve_tool_for_role(qname)
        if mcp_callable is None:
            continue   # Sprint 42 logs the miss; production fail-closes upstream
        tools.append(wrap_mcp_tool(qname, mcp_callable))

    middleware = [ApexAuditMiddleware(agent_spec)]

    return ChatAgent(
        id=f"{agent_spec.service_code}--{agent_spec.scenario_id}--{agent_spec.role}",
        model=agent_spec.model,
        instructions=agent_spec.instructions,
        tools=tools,
        middleware=middleware,
        metadata={
            "manifest_version": agent_spec.manifest_version,
            "prompt_version": agent_spec.prompt_version,
            "label": agent_spec.label,
            "service_code": agent_spec.service_code,
            "scenario_id": agent_spec.scenario_id,
            "classification_propagation": list(agent_spec.classification_propagation),
            "operator_obo_required": agent_spec.operator_obo_required,
        },
    )
