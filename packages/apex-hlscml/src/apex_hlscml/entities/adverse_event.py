"""HLSCML AdverseEvent entity — Pattern C over CDISC SDTM AE domain."""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity


class AeSeverity(StrEnum):
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"


class AdverseEvent(CanonicalEntity):
    """An adverse event reported against a trial subject."""

    subject_key_token: Annotated[str, Classification.PHI] = Field(
        ..., description="Tokenised CDISC USUBJID."
    )
    study_key: str = Field(..., description="FK → HLSCML Study.entity_id.")
    ae_sequence: int = Field(..., ge=1, description="SDTM AESEQ — sequence within subject.")
    ae_term: str = Field(..., description="Reported adverse event term (AETERM).")
    ae_decoded: str | None = Field(
        None, description="Dictionary-derived term (AEDECOD, typically MedDRA)."
    )
    ae_body_system: str | None = Field(
        None, description="MedDRA System Organ Class (AEBODSYS)."
    )
    severity: AeSeverity | None = None
    serious: bool = Field(
        False,
        description="Y/N on serious-AE criteria (death / life-threat / hospitalisation / …).",
    )
    start_date: date | None = None
    end_date: date | None = None
    relationship_to_treatment: Literal[
        "related", "possibly_related", "unlikely_related", "not_related", "unknown"
    ] | None = None
    outcome: str | None = Field(
        None, description="e.g. 'recovered', 'ongoing', 'fatal', 'unknown'."
    )
