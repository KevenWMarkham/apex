"""HLSCML DiagnosticReport entity — Pattern C over FHIR R4 DiagnosticReport."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class DiagnosticReportStatus(StrEnum):
    REGISTERED = "registered"
    PARTIAL = "partial"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CANCELLED = "cancelled"


class DiagnosticReport(CanonicalEntity):
    """A clinical findings report — ties together related Observations."""

    fhir_id: str = Field(..., description="FHIR DiagnosticReport.id.")
    status: DiagnosticReportStatus
    category: str | None = Field(
        None, description="e.g. 'LAB', 'RAD', 'PAT', …"
    )
    code_display: str = Field(
        "", description="Human-readable name of the report."
    )
    patient_key: str = Field(..., description="FK → HLSCML Patient.entity_id.")
    encounter_key: str | None = None
    effective_ts: datetime | None = None
    issued_ts: datetime | None = None
    observation_keys: list[str] = Field(
        default_factory=list,
        description="FKs → HLSCML Observation.entity_id.",
    )
    conclusion: str = Field(
        "", description="Free-text conclusion / impression."
    )
