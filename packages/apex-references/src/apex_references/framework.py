"""APEX Reference Deployment framework — Sprint 18.

A reference deployment is a turnkey Wave-1 engagement blueprint composing
Sprint 14 (capacity), 15 (adapters), 16 (agents), 17 (services) into a
named, scoped, demo-able pattern. Five ship per Sprint 18 — one per
"flagship" Practice anchor:

- Big Box Store (RC) per Sellers Guide §16.13 reference deployment
- Hospital (HLS) per §10.9 hospital reference deployment
- Utility (ER) per §11.9 reference deployment
- Plant (AXLE) per §12.9A reference deployment
- Airline (TH) per §14.8 reference deployment

Each ReferenceSpec captures:

- Triggering scenario (executive event that drives the engagement)
- Solution architecture (which Microsoft platform pieces compose)
- Use cases (specific decisions the deployment makes)
- Personas (who's served)
- KPI targets (Wave-1 vs Wave-2 vs Wave-3)
- Wave-1 scope document (4-12 week deliverable plan)
- Adapter / service / agent linkages
- Demo script reference

Cross-reference: APEX Orchestrator Sprint 14 (capacity blueprints),
Sprint 15 (SOR adapters), Sprint 16 (agent catalog), Sprint 17
(service catalog).
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

PRACTICE_CODES: tuple[str, ...] = ("rc", "hls", "er", "axle", "tmt", "th", "ice")


# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------


class TriggeringScenario(BaseModel):
    """Executive event that drives the engagement."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str
    """Short label for the scenario (e.g., 'Cold-chain excursion')."""

    description: str
    """1-2 sentence narrative of the event sequence."""

    pain: str
    """The pain the event represents (regulatory, operational, financial)."""

    sponsor_persona: str
    """Executive who would commission the engagement after seeing this."""


class SolutionArchitecture(BaseModel):
    """The Microsoft platform composition this reference deploys."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    capacity_blueprint: Literal[
        "single-capacity-tenant", "dev-prod-split", "per-workload-isolation"
    ]
    """Sprint 14 Terraform blueprint to provision the Fabric capacity."""

    fabric_sku: str
    """Recommended F-SKU (e.g., 'F64', 'F128')."""

    bronze_workspaces: list[str] = Field(default_factory=list)
    silver_workspaces: list[str] = Field(default_factory=list)
    gold_workspaces: list[str] = Field(default_factory=list)
    governance_workspace: str = ""

    adapters: list[str] = Field(default_factory=list)
    """Sprint 15 adapter names (e.g., 'sap-s4hana', 'epic-clarity')."""

    canonical_schemas: list[str] = Field(default_factory=list)
    """Schema families instantiated (SCML, MERML, PatientML, etc.)."""

    foundry_model_pins: list[str] = Field(default_factory=list)
    """Specific model deployments used by the agents."""

    purview_classifications: list[str] = Field(default_factory=list)
    """Classifications applied to Bronze/Silver/Gold (Sprint 13)."""


class UseCase(BaseModel):
    """One specific decision the deployment makes."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str
    description: str
    service_codes: list[str] = Field(default_factory=list)
    """Sprint 17 service codes invoked."""

    agents: list[str] = Field(default_factory=list)
    """Sprint 16 agent names invoked."""

    triggering_event: str = ""
    expected_decision_latency: str = ""
    """End-to-end SLA from trigger event to HITL gate ready."""


class KpiTarget(BaseModel):
    """KPI commitment with Wave-1 / Wave-2 / Wave-3 bands."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str
    direction: Literal["up", "down", "money", "neutral"]
    wave1_commitment: str = ""
    """Wave-1 typically establishes baseline and infrastructure;
    measurable KPI movement comes in Wave-2."""

    wave2_target: str
    wave3_target: str = ""
    measurement_pattern: str = ""


class Wave1Scope(BaseModel):
    """4-12 week Wave-1 deliverable plan."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    duration_weeks_low: int
    duration_weeks_high: int
    fee_band_usd_low: int
    fee_band_usd_high: int
    deliverables: list[str] = Field(default_factory=list)
    """Specific named artifacts produced in Wave-1."""

    success_criteria: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# ReferenceSpec — top-level
# ---------------------------------------------------------------------------


class ReferenceSpec(BaseModel):
    """Top-level Reference Deployment manifest."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["reference_deployment"] = "reference_deployment"
    name: str
    """Reference id (e.g., 'big-box-store', 'hospital', 'utility')."""

    version: str = "0.1.0"
    practice: str
    display_name: str
    """Human-readable name (e.g., 'Big Box Store — Retail Operations')."""

    description: str
    sponsor_personas: list[str] = Field(default_factory=list)
    """Executive personas who commission this deployment."""

    triggering_scenarios: list[TriggeringScenario] = Field(default_factory=list)
    architecture: SolutionArchitecture
    use_cases: list[UseCase] = Field(default_factory=list)
    kpi_targets: list[KpiTarget] = Field(default_factory=list)
    wave1_scope: Wave1Scope

    sellers_guide_section: str = ""
    """Cross-reference to the Sellers Guide narrative section."""

    demo_script_path: str = ""
    """Relative path to the demo script markdown."""

    primary_contact: str = ""

    @field_validator("practice", mode="before")
    @classmethod
    def _validate_practice(cls, v: str) -> str:
        if v.lower() not in PRACTICE_CODES:
            raise ValueError(
                f"practice must be one of {PRACTICE_CODES}, got {v!r}"
            )
        return v.lower()


# ---------------------------------------------------------------------------
# Loader + scanner
# ---------------------------------------------------------------------------


def load_reference_spec(path: str | Path) -> ReferenceSpec:
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(
            f"Reference spec {path}: expected mapping, got {type(data).__name__}"
        )
    return ReferenceSpec.model_validate(data)


@dataclass
class CatalogEntry:
    path: Path
    spec: ReferenceSpec


def catalogs_root() -> Path:
    return Path(__file__).parent / "catalogs"


def scan_all_references() -> list[CatalogEntry]:
    """Load every shipped reference manifest."""
    root = catalogs_root()
    if not root.exists():
        return []
    entries: list[CatalogEntry] = []
    for yaml_path in sorted(root.glob("*.yaml")):
        spec = load_reference_spec(yaml_path)
        entries.append(CatalogEntry(path=yaml_path, spec=spec))
    return entries


def total_references() -> int:
    return len(scan_all_references())


def get_reference(name: str) -> ReferenceSpec | None:
    for entry in scan_all_references():
        if entry.spec.name == name:
            return entry.spec
    return None


# ---------------------------------------------------------------------------
# Demo-script loader
# ---------------------------------------------------------------------------


def demo_scripts_root() -> Path:
    return Path(__file__).parent / "demo_scripts"


def load_demo_script(reference_name: str) -> str:
    """Load the markdown demo script for a reference deployment."""
    path = demo_scripts_root() / f"{reference_name}.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


@dataclass
class CatalogIssue:
    reference: str
    code: str
    severity: str = "error"
    message: str = ""


@dataclass
class CatalogReport:
    issues: list[CatalogIssue] = field(default_factory=list)
    references_checked: int = 0

    @property
    def errors(self) -> list[CatalogIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1


def validate_references(
    *,
    service_codes: set[str] | None = None,
    agent_catalog: set[str] | None = None,
    adapter_catalog: set[str] | None = None,
) -> CatalogReport:
    """Validate every reference deployment manifest."""
    report = CatalogReport()
    for entry in scan_all_references():
        spec = entry.spec
        report.references_checked += 1

        # Wave 1 scope coherence: low <= high, and within reasonable bounds
        ws = spec.wave1_scope
        if ws.duration_weeks_low > ws.duration_weeks_high:
            report.issues.append(CatalogIssue(
                reference=spec.name, code="WAVE1_DURATION_INVERTED",
                message=f"duration_weeks_low ({ws.duration_weeks_low}) > high ({ws.duration_weeks_high})",
            ))
        if ws.fee_band_usd_low > ws.fee_band_usd_high:
            report.issues.append(CatalogIssue(
                reference=spec.name, code="WAVE1_FEE_INVERTED",
                message=f"fee_band low ({ws.fee_band_usd_low}) > high ({ws.fee_band_usd_high})",
            ))
        if ws.duration_weeks_low < 4 or ws.duration_weeks_high > 16:
            report.issues.append(CatalogIssue(
                reference=spec.name, code="WAVE1_DURATION_OUT_OF_RANGE",
                severity="warning",
                message=(
                    f"Wave-1 typical duration is 4-12 weeks per Sellers Guide §2.2; "
                    f"this reference declares {ws.duration_weeks_low}-{ws.duration_weeks_high} weeks"
                ),
            ))

        # Cross-reference check: every linked service code resolves
        if service_codes is not None:
            for use_case in spec.use_cases:
                for code in use_case.service_codes:
                    if code not in service_codes:
                        report.issues.append(CatalogIssue(
                            reference=spec.name,
                            code="SERVICE_CODE_NOT_FOUND",
                            message=(
                                f"Use case {use_case.name!r} references "
                                f"unknown service_code {code!r}"
                            ),
                        ))

        # Agent linkage check
        if agent_catalog is not None:
            for use_case in spec.use_cases:
                for agent in use_case.agents:
                    if agent not in agent_catalog:
                        report.issues.append(CatalogIssue(
                            reference=spec.name,
                            code="AGENT_NOT_FOUND",
                            message=(
                                f"Use case {use_case.name!r} references "
                                f"unknown agent {agent!r}"
                            ),
                        ))

        # Adapter linkage check
        if adapter_catalog is not None:
            for adapter in spec.architecture.adapters:
                if adapter not in adapter_catalog:
                    report.issues.append(CatalogIssue(
                        reference=spec.name,
                        code="ADAPTER_NOT_FOUND",
                        message=f"architecture references unknown adapter {adapter!r}",
                    ))

        # Demo script presence
        if spec.demo_script_path:
            demo_path = demo_scripts_root() / spec.demo_script_path
            if not demo_path.exists():
                report.issues.append(CatalogIssue(
                    reference=spec.name,
                    code="DEMO_SCRIPT_MISSING",
                    message=f"demo_script_path {spec.demo_script_path!r} not found",
                ))

        # Coverage essentials
        if not spec.use_cases:
            report.issues.append(CatalogIssue(
                reference=spec.name, code="NO_USE_CASES",
                message="Reference must declare at least one use case",
            ))
        if not spec.kpi_targets:
            report.issues.append(CatalogIssue(
                reference=spec.name, code="NO_KPI_TARGETS",
                message="Reference must declare at least one KPI target",
            ))

    return report
