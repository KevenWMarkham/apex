"""Scenario library data models — Sprint 28.

The legacy scenario library JSON uses compact keys (``t``, ``s``, ``b``,
``k``, ``kk``) to keep the on-the-wire payload small for the Stacked
Architecture HTML. This module ships:

- :class:`ScenarioCompact` — the legacy 5-key shape, read from
  ``docs/scenarios/_catalog/scenario-library.json``.
- :class:`Scenario` — the **extended** v2 shape that adds the
  Sprint 28 wave fields (``w1``, ``w2``, ``w3``) plus optional metadata.
- :func:`compact_to_extended` — round-trip migrator preserving the
  short keys' values into the extended model.

Cross-reference: APEX Orchestrator Sprint 28 Task 28.1.2; Sellers Guide
§2.2A envelope framework (Wave 1 / 2 / 3 are the contractable boundaries).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


PRACTICE_CODES: tuple[str, ...] = ("RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE")
#: Canonical KPI directions found in the live scenario library.
#: - ``up``      — metric should increase (margin, accuracy, attainment)
#: - ``down``    — metric should decrease (cycle time, MAPE, mortality)
#: - ``money``   — dollar-quantified improvement (revenue, cost, write-off)
#: - ``neutral`` — qualitative outcome (regulator-ready, defensibility)
KPI_DIRECTIONS: tuple[str, ...] = ("up", "down", "money", "neutral")


# ---------------------------------------------------------------------------
# Compact shape (legacy v1)
# ---------------------------------------------------------------------------


class ScenarioCompact(BaseModel):
    """Compact 5-key shape used by the Stacked Architecture HTML."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    t: str = Field(..., description="Title.")
    s: str = Field(..., description="Service code (e.g., RC-E2E-03).")
    b: str = Field(..., description="Brief — one-line scenario description.")
    k: str = Field(..., description="KPI delta (e.g., '+2.4pp GM').")
    kk: Literal["up", "down", "money", "neutral"] = Field(..., description="KPI direction.")

    @field_validator("kk", mode="before")
    @classmethod
    def _normalize_direction(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v


# ---------------------------------------------------------------------------
# Extended shape (Sprint 28 v2)
# ---------------------------------------------------------------------------


class Scenario(BaseModel):
    """Extended v2 scenario with Wave 1 / Wave 2 / Wave 3 content.

    All v1 fields are preserved under their long names (``title``,
    ``service_code``, ``brief``, ``kpi``, ``kpi_direction``). The three
    Wave fields are required after Sprint 28; the validator that enforces
    presence is in :mod:`apex_scenarios.validators`.

    Optional fields that accumulate as Sprint 28 progresses:

    - ``personas`` — list of persona codes (e.g., ``["chief-merchant", "vp-pricing"]``)
    - ``schemas_touched`` — canonical schemas referenced
        (e.g., ``["SCML.Lot", "MERML.Price"]``)
    - ``archetype_id`` — orchestration archetype the scenario realizes
    - ``mesh_id`` — W3 fusion-mesh membership (Task 28.3)
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    title: str = Field(..., min_length=1)
    service_code: str = Field(..., min_length=1)
    brief: str = Field(..., min_length=1)
    kpi: str = Field(..., min_length=1)
    kpi_direction: Literal["up", "down", "money", "neutral"]

    # Sprint 28 Wave fields
    w1: str = Field(default="", description="Wave 1 (Envision & Land) one-sentence content.")
    w2: str = Field(default="", description="Wave 2 (Enable & Scale) one-sentence content.")
    w3: str = Field(default="", description="Wave 3 (Sustain & Transform) one-sentence content.")

    # Optional metadata accumulated through the sprint
    personas: list[str] = Field(default_factory=list)
    schemas_touched: list[str] = Field(default_factory=list)
    archetype_id: str | None = None
    mesh_id: str | None = None
    practice: str | None = None

    @field_validator("practice", mode="before")
    @classmethod
    def _validate_practice(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if v.upper() not in PRACTICE_CODES:
            raise ValueError(
                f"practice must be one of {PRACTICE_CODES}, got {v!r}"
            )
        return v.upper()

    @field_validator("kpi_direction", mode="before")
    @classmethod
    def _normalize_direction(cls, v: str) -> str:
        return v.strip().lower() if isinstance(v, str) else v

    def has_full_wave_data(self) -> bool:
        """Return True iff all three Wave fields are populated (non-empty)."""
        return all([self.w1.strip(), self.w2.strip(), self.w3.strip()])


# ---------------------------------------------------------------------------
# Migrators
# ---------------------------------------------------------------------------


def compact_to_extended(compact: ScenarioCompact, *, practice: str | None = None) -> Scenario:
    """Convert a legacy compact scenario to the extended Sprint 28 shape."""
    return Scenario(
        title=compact.t,
        service_code=compact.s,
        brief=compact.b,
        kpi=compact.k,
        kpi_direction=compact.kk,
        practice=practice,
    )


def extended_to_compact(scenario: Scenario) -> ScenarioCompact:
    """Round-trip back to the compact JSON form (drops Wave fields)."""
    return ScenarioCompact(
        t=scenario.title,
        s=scenario.service_code,
        b=scenario.brief,
        k=scenario.kpi,
        kk=scenario.kpi_direction,
    )


# ---------------------------------------------------------------------------
# Featured chains (separate, richer schema)
# ---------------------------------------------------------------------------


class FeaturedChain(BaseModel):
    """One row of the featured-chains catalog.

    Each row is a richer scenario narrative including the full
    Scenario / Solution / Use Case chain (per Sellers Guide §2.2B).
    Sprint 28 Task 28.7.3 validates the Solution string for agent
    references that resolve to the Agent Catalog.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    title: str
    Scenario: str
    Solution: str
    Use_Case: str = Field(alias="Use Case")
    Service: str | None = None
    Persona: str | None = None
    KPI: str | None = None
    practice: str | None = None
