"""HLSCML Observation entity — Pattern C over FHIR R4 Observation."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity
from apex_schemas_common.standards import LoincCode


class ObservationStatus(StrEnum):
    REGISTERED = "registered"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"


class Observation(CanonicalEntity):
    """A measurement / lab result / vital sign."""

    fhir_id: str = Field(..., description="FHIR Observation.id.")
    status: ObservationStatus
    loinc_code: LoincCode | None = Field(
        None, description="LOINC code for what is observed."
    )
    code_display: str = Field(
        "", description="Human-readable name of the observed concept."
    )
    patient_key: str = Field(..., description="FK → HLSCML Patient.entity_id.")
    encounter_key: str | None = Field(
        None, description="FK → HLSCML Encounter.entity_id."
    )
    effective_ts: datetime

    # FHIR Observation has multiple value[x]; APEX models the three most-used.
    value_numeric: Decimal | None = Field(
        None, description="Numeric value (maps to FHIR valueQuantity.value)."
    )
    value_unit: str | None = Field(
        None, description="Unit string (maps to FHIR valueQuantity.unit)."
    )
    value_code: str | None = Field(
        None, description="Coded value (maps to FHIR valueCodeableConcept)."
    )
    value_string: str | None = Field(
        None, description="Free-text value (maps to FHIR valueString)."
    )
    interpretation: str | None = Field(
        None, description="Interpretation code (e.g. 'H' for high, 'N' for normal)."
    )
