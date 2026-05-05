"""HLSCML Study + StudyEnrollment entities — Pattern C over CDISC ODM."""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class StudyPhase(StrEnum):
    PRECLINICAL = "preclinical"
    PHASE_1 = "1"
    PHASE_1_2 = "1/2"
    PHASE_2 = "2"
    PHASE_2_3 = "2/3"
    PHASE_3 = "3"
    PHASE_4 = "4"
    NA = "NA"


class StudyStatus(StrEnum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    TERMINATED = "terminated"
    WITHDRAWN = "withdrawn"


class Study(CanonicalEntity, ScdType2Fields):
    """CDISC-aligned clinical trial / study record."""

    study_oid: str = Field(..., description="CDISC ODM StudyOID.")
    protocol_name: str
    sponsor: str | None = None
    phase: StudyPhase = StudyPhase.NA
    therapeutic_area: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: StudyStatus = StudyStatus.PLANNED


class EnrollmentStatus(StrEnum):
    SCREENING = "screening"
    ENROLLED = "enrolled"
    SCREEN_FAILURE = "screen_failure"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"


class StudyEnrollment(CanonicalEntity, ScdType2Fields):
    """A subject's enrolment in a specific study."""

    subject_key_token: Annotated[str, Classification.PHI] = Field(
        ..., description="Tokenised CDISC SubjectKey / USUBJID."
    )
    study_key: str = Field(..., description="FK → HLSCML Study.entity_id.")
    investigator_key: str | None = Field(
        None, description="FK → HLSCML Practitioner.entity_id."
    )
    site_id: str | None = None
    enrolled_date: date | None = None
    status: EnrollmentStatus = EnrollmentStatus.SCREENING
