"""APEX Master Registries framework — Sprint 19.

Sprint 19 delivers the normative reference set (Appendices A-K) and the
per-Practice Wave delivery playbooks. The package contains *registries*
— small Pydantic models with per-entry YAML manifests under
``src/apex_registries/{registry}/`` — and *playbooks / discovery /
pre-clearance* artifacts which are markdown documents.

Registries shipped:

- :class:`KpiEntry` (Appendix C) — KPI master registry
- :class:`PersonaEntry` (Appendix E) — Persona catalog
- :class:`McpToolEntry` (Appendix F) — MCP tool catalog
- :class:`SchemaEntry` (Appendix A) — Canonical schema reference
- :class:`ArchetypeEntry` (Appendix D) — Orchestration archetype catalog (47 archetypes)
- :class:`ProductEntry` (Appendix G) — Microsoft product & SKU reference
- :class:`PartnerEntry` (Appendix H) — Partner ecosystem catalog
- :class:`CompetitiveEntry` (Appendix K) — Independence & competitive posture
- :class:`ExerciseEntry` (Appendix J) — Exercise solutions

Cross-reference: APEX Orchestrator Sprint 16 (agents), Sprint 17
(services), Sprint 18 (reference deployments). KPI / persona / MCP-tool
registries cross-validate against the live Sprint 16 / 17 catalogs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PRACTICE_CODES: tuple[str, ...] = (
    "rc", "hls", "er", "axle", "tmt", "th", "ice", "cross",
)
"""Includes ``cross`` for cross-Practice registry entries."""


# ---------------------------------------------------------------------------
# KPI master registry — Appendix C
# ---------------------------------------------------------------------------


class KpiEntry(BaseModel):
    """One KPI in the master registry.

    Appendix C. Every KPI named in any agent (Sprint 16), service
    (Sprint 17), or reference deployment (Sprint 18) should resolve here.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["kpi"] = "kpi"
    kpi_id: str
    """Stable identifier (e.g., ``kpi.rc.gross-margin``)."""

    name: str
    """Canonical KPI name as it appears in services/agents."""

    practice: str
    direction: Literal["up", "down", "money", "neutral"]
    description: str
    measurement_pattern: str = ""
    """Standard measurement methodology (sample method, attribution, etc.)."""

    typical_baseline: str = ""
    typical_wave2_target: str = ""
    typical_wave3_target: str = ""

    units: str = ""
    cadence: Literal["realtime", "shift", "daily", "weekly", "monthly", "quarterly", "annual"] = "monthly"

    appendix_c_section: str = ""
    """Optional cross-link to Sellers Guide Appendix C subsection."""

    @field_validator("practice", mode="before")
    @classmethod
    def _validate_practice(cls, v: str) -> str:
        if v.lower() not in PRACTICE_CODES:
            raise ValueError(
                f"practice must be one of {PRACTICE_CODES}, got {v!r}"
            )
        return v.lower()


# ---------------------------------------------------------------------------
# Persona catalog — Appendix E
# ---------------------------------------------------------------------------


class PersonaEntry(BaseModel):
    """One persona in the catalog.

    Appendix E. Every persona named on any agent / service / reference
    should resolve here.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["persona"] = "persona"
    persona_id: str
    """Stable identifier (e.g., ``persona.rc.chief-merchant``)."""

    name: str
    practice: str
    seniority: Literal["c-suite", "svp", "vp", "director", "manager", "individual-contributor"] = "vp"
    function: str
    """E.g., 'Merchandising', 'Operations', 'Revenue Cycle'."""

    description: str
    typical_decisions: list[str] = Field(default_factory=list)
    pains: list[str] = Field(default_factory=list)
    metrics_owned: list[str] = Field(default_factory=list)
    """KPI names this persona is held accountable to."""

    appendix_e_section: str = ""

    @field_validator("practice", mode="before")
    @classmethod
    def _validate_practice(cls, v: str) -> str:
        if v.lower() not in PRACTICE_CODES:
            raise ValueError(f"practice must be one of {PRACTICE_CODES}, got {v!r}")
        return v.lower()


# ---------------------------------------------------------------------------
# MCP tool catalog — Appendix F
# ---------------------------------------------------------------------------


class McpToolEntry(BaseModel):
    """One MCP tool in the catalog.

    Appendix F. Every ``ToolBinding.tool_id`` named on a Sprint 16 agent
    should resolve to one of these entries.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["mcp_tool"] = "mcp_tool"
    tool_id: str
    """Qualified MCP tool id (e.g., ``apex.rc.mcp.scml.get_lot_trace``)."""

    practice: str
    sor_or_layer: str
    """E.g., 'sap-s4hana', 'silver-curated', 'gold-mart', 'fabric-data-warehouse'."""

    purpose: str
    write: bool = False
    """If True, the tool produces side effects (a downstream write)."""

    inputs_schema: str = ""
    outputs_schema: str = ""
    classification_required: list[str] = Field(default_factory=list)
    """Classifications a caller must hold to invoke this tool."""

    related_canonical_schemas: list[str] = Field(default_factory=list)
    appendix_f_section: str = ""

    @field_validator("practice", mode="before")
    @classmethod
    def _validate_practice(cls, v: str) -> str:
        if v.lower() not in PRACTICE_CODES:
            raise ValueError(f"practice must be one of {PRACTICE_CODES}, got {v!r}")
        return v.lower()


# ---------------------------------------------------------------------------
# Schema reference — Appendix A
# ---------------------------------------------------------------------------


class SchemaEntry(BaseModel):
    """One canonical schema family in the reference.

    Appendix A. SCML, MERML, CXML, PatientML, etc. Cross-reference to
    the Sprint 13 governance + Sprint 22-24 schema package implementations.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["schema"] = "schema"
    schema_code: str
    """Short canonical code (e.g., ``SCML``, ``MERML``)."""

    name: str
    description: str
    practices: list[str] = Field(default_factory=list)
    """Practices that consume / produce this schema family."""

    primary_entities: list[str] = Field(default_factory=list)
    """Top-level entities (e.g., ``Lot``, ``Movement``, ``Trace`` for SCML)."""

    standards_alignment: list[str] = Field(default_factory=list)
    """Industry standards this schema family aligns with."""

    governance_classification: str = ""
    """Default Purview classification family for this schema."""

    appendix_a_section: str = ""
    package_implementation: str = ""
    """Name of the apex-* package that implements this schema (e.g., ``apex-scml``)."""

    @field_validator("practices", mode="before")
    @classmethod
    def _validate_practices(cls, v: list[str]) -> list[str]:
        out = []
        for p in v:
            if p.lower() not in PRACTICE_CODES:
                raise ValueError(f"practice must be one of {PRACTICE_CODES}, got {p!r}")
            out.append(p.lower())
        return out


# ---------------------------------------------------------------------------
# Archetype catalog — Appendix D — 47 orchestration archetypes
# ---------------------------------------------------------------------------


class ArchetypeEntry(BaseModel):
    """One orchestration archetype.

    Appendix D. The library of 47 reusable orchestration patterns
    (Triage, Cascade, RCA, Recovery, Personalize, Optimize, etc.)
    that agents implement.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["archetype"] = "archetype"
    archetype_id: str
    """E.g., ``arch.triage.001``, ``arch.recovery.012``."""

    family: Literal[
        "triage", "cascade", "rca", "recovery", "personalize", "optimize",
        "monitor", "predict", "schedule", "match", "translate", "summarize",
        "explain", "score", "negotiate", "compose",
    ]
    name: str
    description: str
    canonical_inputs: list[str] = Field(default_factory=list)
    canonical_outputs: list[str] = Field(default_factory=list)
    typical_hitl_gate: str = ""
    typical_oversight: Literal["HITL", "HOTL", "HIC"] = "HITL"
    typical_model_tier: Literal["lightweight", "standard", "reasoning"] = "standard"
    example_agents: list[str] = Field(default_factory=list)
    """Agent names from Sprint 16 that exemplify this archetype."""

    appendix_d_section: str = ""


# ---------------------------------------------------------------------------
# Microsoft product & SKU reference — Appendix G
# ---------------------------------------------------------------------------


class ProductEntry(BaseModel):
    """One Microsoft product or SKU reference.

    Appendix G. Captures Fabric SKUs, Foundry model deployments, Copilot
    Studio editions, Purview tiers, Defender add-ons, Teams Premium,
    Intune, etc., with commercial implications.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["product"] = "product"
    product_id: str
    """E.g., ``ms.fabric.f128``, ``ms.foundry.gpt4o``, ``ms.copilot-studio.standard``."""

    family: Literal[
        "fabric", "foundry", "copilot-studio", "purview", "defender",
        "entra", "intune", "teams", "power-platform", "azure-openai",
        "azure-ml", "github-copilot", "azure-storage", "azure-network",
    ]
    display_name: str
    sku_or_tier: str = ""
    description: str
    list_price_basis: str = ""
    """E.g., 'consumption', 'per-user/month', 'reserved-capacity-monthly'."""

    typical_use: str = ""
    apex_role: str = ""
    """Where this product fits in the APEX stack."""

    appendix_g_section: str = ""


# ---------------------------------------------------------------------------
# Partner ecosystem — Appendix H
# ---------------------------------------------------------------------------


class PartnerEntry(BaseModel):
    """One partner in the ecosystem.

    Appendix H. Covers SOR vendors, ISVs, model providers, and
    delivery-partner relationships referenced in the Sellers Guide.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["partner"] = "partner"
    partner_id: str
    name: str
    category: Literal[
        "sor-vendor", "isv", "model-provider", "data-provider",
        "delivery-partner", "infrastructure", "specialty",
    ]
    practices: list[str] = Field(default_factory=list)
    description: str
    apex_integration_pattern: str = ""
    """E.g., 'mirrored-db-via-Sprint15-adapter', 'direct-API'."""

    contracts_in_place: list[str] = Field(default_factory=list)
    appendix_h_section: str = ""

    @field_validator("practices", mode="before")
    @classmethod
    def _validate_practices(cls, v: list[str]) -> list[str]:
        out = []
        for p in v:
            if p.lower() not in PRACTICE_CODES:
                raise ValueError(f"practice must be one of {PRACTICE_CODES}, got {p!r}")
            out.append(p.lower())
        return out


# ---------------------------------------------------------------------------
# Independence & competitive posture — Appendix K
# ---------------------------------------------------------------------------


class CompetitiveEntry(BaseModel):
    """One competitive-posture entry.

    Appendix K. How APEX positions vs. each named competitor
    (Accenture+CFC, IBM+watsonx, Capgemini+gen-AI, etc.).
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["competitive"] = "competitive"
    entry_id: str
    competitor: str
    competitor_offering: str
    apex_differentiators: list[str] = Field(default_factory=list)
    independence_concerns: list[str] = Field(default_factory=list)
    """Auditor-independence + DSE rules that bound APEX engagement scope."""

    win_themes: list[str] = Field(default_factory=list)
    appendix_k_section: str = ""


# ---------------------------------------------------------------------------
# Exercise solutions — Appendix J
# ---------------------------------------------------------------------------


class ExerciseEntry(BaseModel):
    """One Sellers Guide exercise + its solution.

    Appendix J. Sellers Guide chapters end in exercises; this catalogs
    the canonical solutions for training + sales-enablement use.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["exercise"] = "exercise"
    exercise_id: str
    """E.g., ``ex.10.3.a``."""

    sellers_guide_section: str
    chapter: str
    prompt: str
    """The exercise prompt as it appears in the Sellers Guide."""

    canonical_solution: str
    teaching_points: list[str] = Field(default_factory=list)
    related_kpi_ids: list[str] = Field(default_factory=list)
    related_archetype_ids: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Loaders + scanners
# ---------------------------------------------------------------------------


REGISTRY_DIRS = {
    "kpis": "kpis",
    "personas": "personas",
    "mcp_tools": "mcp_tools",
    "schemas": "schemas",
    "archetypes": "archetypes",
    "products": "products",
    "partners": "partners",
    "competitive": "competitive",
    "exercises": "exercises",
}

REGISTRY_MODELS: dict[str, type[BaseModel]] = {
    "kpis": KpiEntry,
    "personas": PersonaEntry,
    "mcp_tools": McpToolEntry,
    "schemas": SchemaEntry,
    "archetypes": ArchetypeEntry,
    "products": ProductEntry,
    "partners": PartnerEntry,
    "competitive": CompetitiveEntry,
    "exercises": ExerciseEntry,
}


def package_root() -> Path:
    return Path(__file__).parent


def registry_root(registry: str) -> Path:
    if registry not in REGISTRY_DIRS:
        raise ValueError(f"Unknown registry {registry!r}. Allowed: {list(REGISTRY_DIRS)}")
    return package_root() / REGISTRY_DIRS[registry]


def load_entry(registry: str, path: str | Path) -> BaseModel:
    model = REGISTRY_MODELS[registry]
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(
            f"{registry}/{path}: expected mapping, got {type(data).__name__}"
        )
    return model.model_validate(data)


@dataclass
class RegistryEntry:
    path: Path
    spec: BaseModel


def scan_registry(registry: str) -> list[RegistryEntry]:
    """Load every YAML manifest in the named registry."""
    root = registry_root(registry)
    if not root.exists():
        return []
    out: list[RegistryEntry] = []
    for p in sorted(root.glob("*.yaml")):
        out.append(RegistryEntry(path=p, spec=load_entry(registry, p)))
    return out


def scan_all_registries() -> dict[str, list[RegistryEntry]]:
    return {name: scan_registry(name) for name in REGISTRY_DIRS}


def total_entries() -> dict[str, int]:
    return {n: len(v) for n, v in scan_all_registries().items()}


# ---------------------------------------------------------------------------
# Markdown asset loaders (Wave playbooks + discovery + preclearance)
# ---------------------------------------------------------------------------


def playbooks_root() -> Path:
    return package_root() / "playbooks"


def discovery_root() -> Path:
    return package_root() / "discovery"


def preclearance_root() -> Path:
    return package_root() / "preclearance"


def list_playbooks() -> list[Path]:
    if not playbooks_root().exists():
        return []
    return sorted(playbooks_root().glob("*.md"))


def list_discovery() -> list[Path]:
    if not discovery_root().exists():
        return []
    return sorted(discovery_root().glob("*.md"))


def list_preclearance() -> list[Path]:
    if not preclearance_root().exists():
        return []
    return sorted(preclearance_root().glob("*.md"))


def load_playbook(name: str) -> str:
    """Load one playbook by basename without `.md`."""
    p = playbooks_root() / f"{name}.md"
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


@dataclass
class RegistryIssue:
    registry: str
    entry: str
    code: str
    severity: str = "error"
    message: str = ""


@dataclass
class RegistryReport:
    issues: list[RegistryIssue] = field(default_factory=list)
    entries_checked: int = 0

    @property
    def errors(self) -> list[RegistryIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1


def validate_registries(
    *,
    agents_kpi_names: set[str] | None = None,
    services_kpi_names: set[str] | None = None,
    agents_persona_names: set[str] | None = None,
    services_persona_names: set[str] | None = None,
    agents_tool_ids: set[str] | None = None,
) -> RegistryReport:
    """Validate every registry manifest + cross-reference upstream catalogs.

    The cross-reference check is best-effort: pass ``None`` for any
    catalog that is unavailable, and that check is skipped.
    """
    report = RegistryReport()
    cats = scan_all_registries()
    for name, entries in cats.items():
        for entry in entries:
            report.entries_checked += 1
            spec = entry.spec
            # Per-registry coverage essentials
            if name == "kpis":
                k: KpiEntry = spec  # type: ignore[assignment]
                if not k.description:
                    report.issues.append(RegistryIssue(
                        registry=name, entry=k.kpi_id,
                        code="KPI_NO_DESCRIPTION",
                        severity="warning",
                        message="KPI entry has no description",
                    ))
            elif name == "personas":
                p: PersonaEntry = spec  # type: ignore[assignment]
                if not p.typical_decisions:
                    report.issues.append(RegistryIssue(
                        registry=name, entry=p.persona_id,
                        code="PERSONA_NO_DECISIONS",
                        severity="warning",
                        message="Persona has no typical_decisions listed",
                    ))
            elif name == "mcp_tools":
                t: McpToolEntry = spec  # type: ignore[assignment]
                if t.write and not t.classification_required:
                    report.issues.append(RegistryIssue(
                        registry=name, entry=t.tool_id,
                        code="WRITE_TOOL_NO_CLASSIFICATION",
                        severity="warning",
                        message="Write-effecting MCP tool should declare required classification",
                    ))
            elif name == "schemas":
                s: SchemaEntry = spec  # type: ignore[assignment]
                if not s.primary_entities:
                    report.issues.append(RegistryIssue(
                        registry=name, entry=s.schema_code,
                        code="SCHEMA_NO_ENTITIES",
                        severity="warning",
                        message="Schema entry should declare ≥1 primary entity",
                    ))

    # Cross-reference: every KPI named on agents/services must resolve to a registry kpi.name
    kpi_names_in_registry = {e.spec.name for e in cats.get("kpis", [])}  # type: ignore[attr-defined]
    persona_names_in_registry = {e.spec.name for e in cats.get("personas", [])}  # type: ignore[attr-defined]
    tool_ids_in_registry = {e.spec.tool_id for e in cats.get("mcp_tools", [])}  # type: ignore[attr-defined]

    if agents_kpi_names is not None:
        for n in agents_kpi_names:
            if n not in kpi_names_in_registry:
                report.issues.append(RegistryIssue(
                    registry="kpis", entry=n,
                    code="KPI_REFERENCED_BY_AGENT_NOT_IN_REGISTRY",
                    severity="warning",
                    message=f"agents reference KPI {n!r} not present in KPI registry",
                ))
    if services_kpi_names is not None:
        for n in services_kpi_names:
            if n not in kpi_names_in_registry:
                report.issues.append(RegistryIssue(
                    registry="kpis", entry=n,
                    code="KPI_REFERENCED_BY_SERVICE_NOT_IN_REGISTRY",
                    severity="warning",
                    message=f"services reference KPI {n!r} not present in KPI registry",
                ))
    if agents_persona_names is not None:
        for n in agents_persona_names:
            if n not in persona_names_in_registry:
                report.issues.append(RegistryIssue(
                    registry="personas", entry=n,
                    code="PERSONA_REFERENCED_BY_AGENT_NOT_IN_REGISTRY",
                    severity="warning",
                    message=f"agents reference persona {n!r} not present in Persona catalog",
                ))
    if services_persona_names is not None:
        for n in services_persona_names:
            if n not in persona_names_in_registry:
                report.issues.append(RegistryIssue(
                    registry="personas", entry=n,
                    code="PERSONA_REFERENCED_BY_SERVICE_NOT_IN_REGISTRY",
                    severity="warning",
                    message=f"services reference persona {n!r} not present in Persona catalog",
                ))
    if agents_tool_ids is not None:
        for tid in agents_tool_ids:
            if tid not in tool_ids_in_registry:
                report.issues.append(RegistryIssue(
                    registry="mcp_tools", entry=tid,
                    code="TOOL_REFERENCED_BY_AGENT_NOT_IN_REGISTRY",
                    severity="warning",
                    message=f"agents reference MCP tool {tid!r} not present in tool catalog",
                ))

    return report
