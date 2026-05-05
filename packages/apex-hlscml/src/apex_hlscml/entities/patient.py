"""HLSCML Patient entity — Pattern C over FHIR R4 Patient."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Literal

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class Patient(CanonicalEntity, ScdType2Fields):
    """HLSCML canonical Patient — FHIR R4 Patient extended with APEX governance.

    Every direct identifier is tokenised at the Bronze→Silver boundary; this
    entity only ever holds tokens. Cleartext detokenisation is gated by the
    ``tokenizer-mcp`` service and only granted to authorised identities.
    """

    # --- FHIR-carried (subset agents consume) -------------------------------
    fhir_id: str = Field(..., description="FHIR Patient.id.")
    mrn_token: Annotated[str, Classification.PHI] | None = Field(
        None, description="Tokenised Medical Record Number."
    )
    mrn_system: str | None = Field(
        None, description="OID / URI of the identifier system that issued the MRN."
    )
    name_family_token: Annotated[str, Classification.PHI] | None = Field(
        None, description="Tokenised family / surname."
    )
    name_given_token: Annotated[str, Classification.PHI] | None = Field(
        None, description="Tokenised first given name."
    )
    gender: Literal["male", "female", "other", "unknown"] | None = None
    birth_date: date | None = None
    deceased: bool | None = None
    address_token: Annotated[str, Classification.PHI] | None = Field(
        None, description="Tokenised structured address."
    )
    phone_token: Annotated[str, Classification.PHI] | None = Field(
        None, description="Tokenised phone."
    )
    email_token: Annotated[str, Classification.PHI] | None = Field(
        None, description="Tokenised email."
    )

    # --- APEX governance additions ------------------------------------------
    source_fhir_version: Literal["R4", "R5"] = Field(
        "R4", description="FHIR version the record was ingested from."
    )
    consent_pointer: str | None = Field(
        None, description="Reference into the consent ledger (Sprint 13)."
    )
