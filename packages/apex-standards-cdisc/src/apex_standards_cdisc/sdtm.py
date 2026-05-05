"""CDISC SDTM — DM / AE / LB domain skeletons."""

from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

_SDTM_CONFIG = ConfigDict(extra="forbid")


class SdtmAeSeverity(StrEnum):
    """CDISC-controlled severity for AE.AESEV."""

    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"


class SdtmDemographics(BaseModel):
    """SDTM DM — Demographics domain (one row per subject)."""

    model_config = _SDTM_CONFIG
    studyid: str
    usubjid: str = Field(..., description="Unique Subject Identifier.")
    subjid: str | None = None
    siteid: str | None = None
    age: int | None = Field(None, ge=0, le=150)
    ageu: str | None = Field(None, description="Age unit: YEARS, MONTHS, etc.")
    sex: str | None = Field(None, description="M / F / U / UNDIFFERENTIATED.")
    race: str | None = None
    ethnic: str | None = None
    country: str | None = Field(None, min_length=2, max_length=3)


class SdtmAdverseEvent(BaseModel):
    """SDTM AE — Adverse Event domain row."""

    model_config = _SDTM_CONFIG
    studyid: str
    usubjid: str
    aeseq: int = Field(..., ge=1, description="Sequence number within subject.")
    aeterm: str = Field(..., description="Reported term for the AE.")
    aedecod: str | None = Field(None, description="Dictionary-derived term (MedDRA).")
    aebodsys: str | None = Field(None, description="Body system / MedDRA SOC.")
    aesev: SdtmAeSeverity | None = None
    aeser: str | None = Field(None, description="Serious flag: Y/N.")
    aestdtc: date | None = Field(None, description="Start date.")
    aeendtc: date | None = Field(None, description="End date.")
    aerel: str | None = Field(None, description="Relationship to study treatment.")


class SdtmLabResult(BaseModel):
    """SDTM LB — Lab Result domain row."""

    model_config = _SDTM_CONFIG
    studyid: str
    usubjid: str
    lbseq: int = Field(..., ge=1)
    lbtestcd: str = Field(..., description="Lab test code (standardised).")
    lbtest: str | None = None
    lborres: str | None = Field(None, description="Original result as collected.")
    lborresu: str | None = Field(None, description="Original result units.")
    lbstresn: float | None = Field(None, description="Numeric standardised result.")
    lbstresu: str | None = Field(None, description="Standardised units.")
    lbdtc: date | None = None
