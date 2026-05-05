"""HLSCML MedicationRequest entity — Pattern C over FHIR R4 MedicationRequest."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity
from apex_schemas_common.standards import NdcCode, RxNormConceptId


class MedicationRequestStatus(StrEnum):
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered-in-error"
    STOPPED = "stopped"
    DRAFT = "draft"


class MedicationRequestIntent(StrEnum):
    PROPOSAL = "proposal"
    PLAN = "plan"
    ORDER = "order"
    ORIGINAL_ORDER = "original-order"
    REFLEX_ORDER = "reflex-order"
    FILLER_ORDER = "filler-order"
    INSTANCE_ORDER = "instance-order"


class MedicationRequest(CanonicalEntity):
    """A prescription / medication order."""

    fhir_id: str = Field(..., description="FHIR MedicationRequest.id.")
    status: MedicationRequestStatus
    intent: MedicationRequestIntent
    rxnorm_code: RxNormConceptId | None = Field(
        None, description="RxNorm concept ID for the medication."
    )
    ndc_code: NdcCode | None = Field(
        None, description="National Drug Code for the product."
    )
    medication_display: str = Field(
        "", description="Human-readable medication name."
    )
    patient_key: str = Field(..., description="FK → HLSCML Patient.entity_id.")
    encounter_key: str | None = None
    practitioner_key: str | None = Field(
        None, description="FK → HLSCML Practitioner.entity_id (the prescriber)."
    )
    authored_on: datetime | None = None
    dosage_text: str = Field("", description="Free-text dosage instructions.")
    as_needed: bool = False
