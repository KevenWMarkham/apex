"""HLSCML Practitioner entity — Pattern C over FHIR R4 Practitioner."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class Practitioner(CanonicalEntity, ScdType2Fields):
    """HLSCML canonical Practitioner — clinician identity with APEX governance."""

    fhir_id: str = Field(..., description="FHIR Practitioner.id.")
    npi_token: Annotated[str, Classification.PII] | None = Field(
        None, description="Tokenised National Provider Identifier (US NPI)."
    )
    name_family_token: Annotated[str, Classification.PII] | None = None
    name_given_token: Annotated[str, Classification.PII] | None = None
    qualifications: list[str] = Field(
        default_factory=list,
        description="Qualification codes (e.g. 'MD', 'PA', 'RN').",
    )
    active: bool = True
