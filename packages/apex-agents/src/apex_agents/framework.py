"""APEX Agent Catalog framework — Sprint 16.

Every Sprint-16 agent ships as a YAML manifest under
``apex_agents/catalogs/{practice}/{agent_name}.yaml``. The manifest declares:

- Identity (name, version, owner, persona, service code)
- Model configuration (tier, model pin, prompt SHA, temperature, max tokens)
- Capability boundaries (allowed MCP tools, forbidden classifications)
- HITL gate placement (which decisions require human approval)
- KPI references (what outcomes the agent targets)
- Audit-row contract (what fields the agent emits)
- Manifest provenance (Git SHA, signing, immutable_during_run)

The framework here parses, validates, and indexes those manifests. The
*execution* runtime (Foundry / SK / Copilot Studio) is out of scope —
this is the L1 contract layer per Sellers Guide §1.6 + §6.10 + §6.13.

Cross-reference: Sellers Guide §6.10 (audit row), §6.11 (Microsoft
orchestrator types), §9.11–§15.9 (per-Practice deep-dives).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PRACTICE_CODES: tuple[str, ...] = ("rc", "hls", "er", "axle", "tmt", "th", "ice")


class ModelTier(str, Enum):
    """Three-tier APEX model strategy from Sellers Guide §6.2.

    Choosing the right tier is the single largest cost lever per service.
    The Practice deep-dives recommend tier per service.
    """

    LIGHTWEIGHT = "lightweight"  # GPT-4o-mini class, <2k tokens, simple classification
    STANDARD = "standard"        # GPT-4o / Claude Sonnet, most agent reasoning
    REASONING = "reasoning"      # o-series / Claude Opus, multi-step planning + elasticity


class OversightMode(str, Enum):
    """Sellers Guide §2.2C oversight spectrum."""

    HITL = "HITL"  # Human-in-the-Loop — checkpoint per consequential decision
    HOTL = "HOTL"  # Human-on-the-Loop — exception-based monitoring of routine
    HIC = "HIC"    # Human-in-Command — strategic governance


# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------


class HITLGate(BaseModel):
    """One HITL gate declared on the agent."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str
    description: str
    fires_when: str
    """Plain-language condition — when this gate intercepts the decision."""

    surface: Literal["teams_card", "copilot_studio", "dashboard", "mobile"] = "teams_card"
    sla_minutes: int = 60
    """Maximum minutes before escalation if no human response."""


class ToolBinding(BaseModel):
    """One MCP tool the agent is authorized to call."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    tool_id: str
    """MCP tool qualified name (e.g., ``apex.rc.mcp.scml.get_lot_trace``)."""

    purpose: str
    write: bool = False
    """If True, the tool produces side effects (a downstream write)."""


class KpiTarget(BaseModel):
    """One KPI the agent targets."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str
    """KPI canonical name (matches Appendix C / Appendix T entries)."""

    direction: Literal["up", "down", "money", "neutral"]
    target_band: str = ""
    """Wave-2-mature target range (e.g., ``+2-4pp GM`` or ``-15% MAPE``)."""


# ---------------------------------------------------------------------------
# AgentSpec — top-level manifest
# ---------------------------------------------------------------------------


class AgentSpec(BaseModel):
    """Top-level agent manifest.

    Validated at load time; engagement specs override fields as needed.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["agent"] = "agent"
    name: str
    """Agent ID. Convention: ``apex.{practice}.agents.{snake_case_name}``."""

    version: str = "0.1.0"
    practice: str
    """One of PRACTICE_CODES."""

    persona: str
    """Primary persona served (e.g., ``Chief Merchant``, ``Charge Nurse``)."""

    service_codes: list[str]
    """APEX Service codes this agent contributes to (e.g., ``RC-E2E-03``)."""

    model_tier: ModelTier
    model_pin: str
    """Specific model deployment id (e.g., ``gpt-4o-2024-11-20``)."""

    prompt_sha: str = ""
    """Content-hash of the agent's system-prompt bundle. Empty during draft."""

    tools: list[ToolBinding] = Field(default_factory=list)
    hitl_gates: list[HITLGate] = Field(default_factory=list)
    kpis: list[KpiTarget] = Field(default_factory=list)

    oversight_modes: list[OversightMode] = Field(default_factory=list)
    """Modes the agent operates under, ordered (e.g., [HITL, HOTL])."""

    forbidden_classifications: list[str] = Field(default_factory=list)
    """Sensitivity classifications this agent must never receive."""

    description: str = ""
    archetype_id: str | None = None
    """Optional reference to an archetype from the 47-archetype library."""

    primary_contact: str = ""
    """Owner UPN or team alias responsible for this agent."""

    notes: str = ""

    @field_validator("practice", mode="before")
    @classmethod
    def _validate_practice(cls, v: str) -> str:
        if v.lower() not in PRACTICE_CODES:
            raise ValueError(
                f"practice must be one of {PRACTICE_CODES}, got {v!r}"
            )
        return v.lower()

    def write_tools(self) -> list[ToolBinding]:
        return [t for t in self.tools if t.write]

    def has_hitl(self) -> bool:
        return len(self.hitl_gates) > 0


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------


def load_agent_spec(path: str | Path) -> AgentSpec:
    """Parse one agent-manifest YAML."""
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"Agent spec {path}: expected mapping, got {type(data).__name__}")
    return AgentSpec.model_validate(data)


# ---------------------------------------------------------------------------
# Catalog scanner
# ---------------------------------------------------------------------------


@dataclass
class CatalogEntry:
    """One catalog entry — manifest + filesystem path."""

    path: Path
    spec: AgentSpec


def catalogs_root() -> Path:
    """Return the directory holding the shipped reference catalogs."""
    return Path(__file__).parent / "catalogs"


def scan_practice_catalog(practice: str) -> list[CatalogEntry]:
    """Load every agent manifest in one Practice's catalog."""
    if practice.lower() not in PRACTICE_CODES:
        raise ValueError(f"Unknown practice {practice!r}. Allowed: {PRACTICE_CODES}")
    practice_dir = catalogs_root() / practice.lower()
    if not practice_dir.exists():
        return []
    entries: list[CatalogEntry] = []
    for yaml_path in sorted(practice_dir.glob("*.yaml")):
        spec = load_agent_spec(yaml_path)
        entries.append(CatalogEntry(path=yaml_path, spec=spec))
    return entries


def scan_all_catalogs() -> dict[str, list[CatalogEntry]]:
    """Load every catalog across all 7 Practices."""
    return {p: scan_practice_catalog(p) for p in PRACTICE_CODES}


def total_agents() -> int:
    """Total agents shipped across all Practice catalogs."""
    return sum(len(v) for v in scan_all_catalogs().values())


# ---------------------------------------------------------------------------
# Validation report
# ---------------------------------------------------------------------------


@dataclass
class CatalogValidationIssue:
    practice: str
    agent_name: str
    code: str
    severity: str = "error"
    message: str = ""


@dataclass
class CatalogValidationReport:
    issues: list[CatalogValidationIssue] = field(default_factory=list)
    agents_checked: int = 0

    @property
    def errors(self) -> list[CatalogValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1


def validate_catalogs(
    catalogs: dict[str, list[CatalogEntry]] | None = None,
) -> CatalogValidationReport:
    """Validate every agent manifest in every catalog.

    Checks:

    - Every write-tool agent declares at least one HITL gate.
    - Agents with model_tier=reasoning declare ≥ 1 KPI.
    - HITL gate sla_minutes > 0.
    - Every agent name follows ``apex.{practice}.agents.{...}`` convention.
    """
    cats = catalogs if catalogs is not None else scan_all_catalogs()
    report = CatalogValidationReport()

    for practice, entries in cats.items():
        for entry in entries:
            spec = entry.spec
            report.agents_checked += 1

            # Naming convention
            expected_prefix = f"apex.{practice.lower()}.agents."
            if not spec.name.startswith(expected_prefix):
                report.issues.append(
                    CatalogValidationIssue(
                        practice=practice,
                        agent_name=spec.name,
                        code="AGENT_NAME_NONCANONICAL",
                        message=f"Agent name should start with {expected_prefix!r}",
                    )
                )

            # Write-tool agents must declare HITL UNLESS their oversight
            # is explicitly purely HOTL (Human-on-the-Loop — exception-based
            # supervisory monitoring per Sellers Guide §2.2C). Pure-HOTL
            # writes are routine and reversible by design (e.g., sending a
            # coaching prompt, logging a usage event).
            pure_hotl_or_hic = (
                bool(spec.oversight_modes)
                and OversightMode.HITL not in spec.oversight_modes
                and all(m in (OversightMode.HOTL, OversightMode.HIC) for m in spec.oversight_modes)
            )
            if spec.write_tools() and not spec.has_hitl() and not pure_hotl_or_hic:
                report.issues.append(
                    CatalogValidationIssue(
                        practice=practice,
                        agent_name=spec.name,
                        code="MISSING_HITL_FOR_WRITE",
                        message=(
                            "Agent has write tools but declares no HITL gate "
                            "and oversight_modes does not assert pure HOTL/HIC. "
                            "Per Sellers Guide §2.2C, consequential write decisions require HITL."
                        ),
                    )
                )

            # Reasoning-tier agents should declare ≥ 1 KPI
            if spec.model_tier == ModelTier.REASONING and not spec.kpis:
                report.issues.append(
                    CatalogValidationIssue(
                        practice=practice,
                        agent_name=spec.name,
                        code="REASONING_TIER_NO_KPI",
                        severity="warning",
                        message="Reasoning-tier agents are expensive; should declare measurable KPI(s).",
                    )
                )

            # HITL SLA sanity
            for gate in spec.hitl_gates:
                if gate.sla_minutes <= 0:
                    report.issues.append(
                        CatalogValidationIssue(
                            practice=practice,
                            agent_name=spec.name,
                            code="HITL_SLA_INVALID",
                            message=f"HITL gate {gate.name!r} has non-positive SLA",
                        )
                    )

    return report
