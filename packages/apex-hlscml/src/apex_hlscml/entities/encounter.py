"""HLSCML Encounter entity — Pattern C over FHIR R4 Encounter."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class EncounterStatus(StrEnum):
    PLANNED = "planned"
    ARRIVED = "arrived"
    TRIAGED = "triaged"
    IN_PROGRESS = "in-progress"
    ONLEAVE = "onleave"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class Encounter(CanonicalEntity):
    """An interaction between a patient and healthcare provider(s)."""

    fhir_id: str = Field(..., description="FHIR Encounter.id.")
    status: EncounterStatus
    encounter_class: str | None = Field(
        None, description="v3 ActCode — 'AMB' (ambulatory), 'IMP' (inpatient), 'EMER', …"
    )
    patient_key: str = Field(..., description="FK → HLSCML Patient.entity_id.")
    start_ts: datetime
    end_ts: datetime | None = None
    reason_codes: list[str] = Field(
        default_factory=list,
        description="ICD-10 / SNOMED codes for the reason(s) of this encounter.",
    )
    service_provider: str | None = Field(
        None, description="Name or identifier of the organisation providing service."
    )
