"""APEX Service Catalog framework — Sprint 17.

Every productized service ships as a YAML manifest declaring:

- Service code (RC-E2E-03, HLS-LS-03, etc. per Sellers Guide §1.1A.5 convention)
- Practice + Track classification
- Display name + brief
- Lead persona + secondary personas
- KPIs with baseline / Wave-2 target / Wave-3 mature target
- SLOs (latency, availability, audit-row emission)
- Wave envelope (Wave-1, Wave-2, Wave-3 commercial bands)
- Linked agents from the Sprint 16 catalog
- Linked archetype IDs from the 47-archetype library
- Linked canonical schemas
- Commercial model (fixed_fee / value_share / hybrid)

The framework parses, validates, indexes, and cross-references against
Sprint 16 agents and Sprint 28 service codes.

Cross-reference: Sellers Guide §2.2A (envelopes), §2.2B (value-delivery
chain), §9.11–§15.9 (Practice deep-dives).
"""

from __future__ import annotations

import re
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

#: Canonical APEX service-code pattern (matches Sprint 28 validate-scenarios).
SERVICE_CODE_RE = re.compile(
    r"^(RC|HLS|ER|AXLE|TMT|TH|ICE)-"
    r"([A-Za-z][A-Za-z0-9]{1,14}(?:-[A-Za-z][A-Za-z0-9]{1,14}){0,2})"
    r"-\d{2,3}$"
)


class CommercialModel(str, Enum):
    """How a service is sold."""

    FIXED_FEE = "fixed_fee"
    """Wave-1 / Wave-2 fixed-fee delivery."""

    VALUE_SHARE = "value_share"
    """Outcome-attributed share of measured KPI delta. Markdown / shrink / recovery services."""

    HYBRID = "hybrid"
    """Fixed fee for foundation services + value-share on attribution-clean services."""


class Wave(str, Enum):
    WAVE_1 = "wave_1"  # Envision & Land
    WAVE_2 = "wave_2"  # Enable & Scale
    WAVE_3 = "wave_3"  # Sustain & Transform


# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------


class Persona(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str
    role: Literal["primary", "secondary"] = "primary"


class KpiCommitment(BaseModel):
    """Service KPI with baseline + Wave 2/3 targets."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str
    direction: Literal["up", "down", "money", "neutral"]
    baseline: str = ""
    """Typical pre-engagement metric value."""

    wave2_target: str = ""
    """What Wave-2 implementation typically achieves."""

    wave3_target: str = ""
    """What mature operations reach (2+ year horizon)."""

    measurement_pattern: str = ""
    """How the KPI is measured (audit-row attribution, sample method, etc.)."""


class SLO(BaseModel):
    """Service-level objective declaration."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str
    target: str
    """Target value, e.g., '99.5% monthly availability', 'p95 latency < 2s'."""

    enforcement: Literal["soft", "hard", "regulatory"] = "soft"


class WaveEnvelope(BaseModel):
    """Commercial envelope for one Wave."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    wave: Wave
    duration: str
    """E.g., '4-12 weeks', '6-12 months'."""

    fee_band_low_usd: int
    fee_band_high_usd: int
    deliverables: list[str] = Field(default_factory=list)
    description: str = ""


# ---------------------------------------------------------------------------
# ServiceSpec — top-level manifest
# ---------------------------------------------------------------------------


class ServiceSpec(BaseModel):
    """Top-level Service Catalog manifest.

    Validated at load time. Cross-references to Sprint 16 agents and
    Sprint 28 scenario service-codes are checked separately by
    :func:`apex_services.validators`.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["service"] = "service"
    service_code: str
    """Canonical service code (e.g., RC-E2E-03)."""

    version: str = "0.1.0"
    practice: str
    """One of PRACTICE_CODES."""

    display_name: str
    brief: str
    """One-sentence description for proposals + decks."""

    description: str = ""
    """Longer description for service-catalog entries."""

    personas: list[Persona] = Field(default_factory=list)
    kpis: list[KpiCommitment] = Field(default_factory=list)
    slos: list[SLO] = Field(default_factory=list)
    waves: list[WaveEnvelope] = Field(default_factory=list)

    commercial_model: CommercialModel = CommercialModel.FIXED_FEE
    value_share_eligible: bool = False
    """If True, the service can be sold value-share (per Sellers Guide §2.6)."""

    linked_agents: list[str] = Field(default_factory=list)
    """Agent names from the apex-agents catalog (e.g., apex.rc.agents.cold-chain-response)."""

    linked_archetypes: list[str] = Field(default_factory=list)
    """Archetype IDs from the 47-archetype library."""

    schemas_touched: list[str] = Field(default_factory=list)
    """Canonical schemas the service reads/writes (e.g., SCML, MERML, CXML)."""

    standards: list[str] = Field(default_factory=list)
    """Industry standards referenced (e.g., FSMA 204, HIPAA, FERC)."""

    primary_contact: str = ""
    """Practice lead UPN or alias."""

    @field_validator("practice", mode="before")
    @classmethod
    def _validate_practice(cls, v: str) -> str:
        if v.lower() not in PRACTICE_CODES:
            raise ValueError(
                f"practice must be one of {PRACTICE_CODES}, got {v!r}"
            )
        return v.lower()

    @field_validator("service_code", mode="before")
    @classmethod
    def _validate_service_code(cls, v: str) -> str:
        if not SERVICE_CODE_RE.match(v):
            raise ValueError(
                f"service_code {v!r} does not match canonical pattern "
                "{PRACTICE}-{Track}-{NN}."
            )
        return v

    def primary_persona(self) -> Persona | None:
        for p in self.personas:
            if p.role == "primary":
                return p
        return self.personas[0] if self.personas else None

    def has_value_share(self) -> bool:
        return (
            self.value_share_eligible
            or self.commercial_model in (CommercialModel.VALUE_SHARE, CommercialModel.HYBRID)
        )

    def wave_envelope(self, wave: Wave) -> WaveEnvelope | None:
        for w in self.waves:
            if w.wave == wave:
                return w
        return None


# ---------------------------------------------------------------------------
# Loader + scanner
# ---------------------------------------------------------------------------


def load_service_spec(path: str | Path) -> ServiceSpec:
    """Parse one service-manifest YAML."""
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(
            f"Service spec {path}: expected mapping, got {type(data).__name__}"
        )
    return ServiceSpec.model_validate(data)


@dataclass
class CatalogEntry:
    path: Path
    spec: ServiceSpec


def catalogs_root() -> Path:
    return Path(__file__).parent / "catalogs"


def scan_practice_catalog(practice: str) -> list[CatalogEntry]:
    if practice.lower() not in PRACTICE_CODES:
        raise ValueError(f"Unknown practice {practice!r}.")
    practice_dir = catalogs_root() / practice.lower()
    if not practice_dir.exists():
        return []
    entries: list[CatalogEntry] = []
    for yaml_path in sorted(practice_dir.glob("*.yaml")):
        spec = load_service_spec(yaml_path)
        entries.append(CatalogEntry(path=yaml_path, spec=spec))
    return entries


def scan_all_catalogs() -> dict[str, list[CatalogEntry]]:
    return {p: scan_practice_catalog(p) for p in PRACTICE_CODES}


def total_services() -> int:
    return sum(len(v) for v in scan_all_catalogs().values())


def all_service_codes() -> set[str]:
    """Return every shipped service code (used by Sprint 28 validators)."""
    codes: set[str] = set()
    for entries in scan_all_catalogs().values():
        for entry in entries:
            codes.add(entry.spec.service_code)
    return codes


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


@dataclass
class CatalogIssue:
    practice: str
    service_code: str
    code: str
    severity: str = "error"
    message: str = ""


@dataclass
class CatalogReport:
    issues: list[CatalogIssue] = field(default_factory=list)
    services_checked: int = 0

    @property
    def errors(self) -> list[CatalogIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1


def validate_service_catalogs(
    catalogs: dict[str, list[CatalogEntry]] | None = None,
    *,
    agent_catalog: set[str] | None = None,
) -> CatalogReport:
    """Validate every service manifest against governance rules.

    Checks:

    - Service code matches the canonical regex
    - Service code's practice prefix matches the manifest's practice field
    - At least one persona declared
    - At least one KPI declared
    - Wave envelope declared (≥1 wave)
    - Linked agents (if any) resolve in the agent catalog (when supplied)
    - Value-share-eligible services have at least one money-direction KPI
    """
    cats = catalogs if catalogs is not None else scan_all_catalogs()
    report = CatalogReport()

    for practice, entries in cats.items():
        for entry in entries:
            spec = entry.spec
            report.services_checked += 1

            # Service-code prefix matches practice
            expected_prefix = practice.upper() + "-"
            if not spec.service_code.startswith(expected_prefix):
                report.issues.append(CatalogIssue(
                    practice=practice,
                    service_code=spec.service_code,
                    code="PRACTICE_PREFIX_MISMATCH",
                    message=f"Code should start with {expected_prefix!r}",
                ))

            # Personas present
            if not spec.personas:
                report.issues.append(CatalogIssue(
                    practice=practice, service_code=spec.service_code,
                    code="NO_PERSONAS",
                    message="Every productized service must declare at least one persona.",
                ))

            # KPIs present
            if not spec.kpis:
                report.issues.append(CatalogIssue(
                    practice=practice, service_code=spec.service_code,
                    code="NO_KPIS",
                    message="Every productized service must declare at least one KPI.",
                ))

            # Wave envelope present
            if not spec.waves:
                report.issues.append(CatalogIssue(
                    practice=practice, service_code=spec.service_code,
                    code="NO_WAVE_ENVELOPE",
                    message="Service must declare at least one Wave envelope.",
                ))

            # Value-share-eligible services need money-direction KPIs
            if spec.has_value_share():
                money_kpis = [k for k in spec.kpis if k.direction == "money"]
                if not money_kpis:
                    report.issues.append(CatalogIssue(
                        practice=practice, service_code=spec.service_code,
                        code="VALUE_SHARE_WITHOUT_MONEY_KPI",
                        severity="warning",
                        message=(
                            "Value-share commercial model usually requires a "
                            "money-direction KPI for clean attribution."
                        ),
                    ))

            # Linked agents resolve
            if agent_catalog is not None and spec.linked_agents:
                unresolved = [a for a in spec.linked_agents if a not in agent_catalog]
                for u in unresolved:
                    report.issues.append(CatalogIssue(
                        practice=practice, service_code=spec.service_code,
                        code="AGENT_NOT_FOUND",
                        message=f"linked_agent {u!r} is not in the agent catalog.",
                    ))

    return report
