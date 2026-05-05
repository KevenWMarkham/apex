"""CDISC ODM — Study / Subject / FormData skeleton."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

_ODM_CONFIG = ConfigDict(extra="forbid")


class CdiscStudy(BaseModel):
    """ODM Study metadata — protocol ID + sponsor + phase."""

    model_config = _ODM_CONFIG
    study_oid: str = Field(..., description="ODM StudyOID.")
    protocol_name: str
    sponsor: str | None = None
    phase: str | None = Field(None, description="e.g. '1', '2', '3', '4', 'NA'.")
    therapeutic_area: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class CdiscSubject(BaseModel):
    """ODM Subject — a trial participant."""

    model_config = _ODM_CONFIG
    subject_key: str = Field(..., description="ODM SubjectKey — usually pseudonymised.")
    study_oid: str = Field(..., description="FK → CdiscStudy.study_oid.")
    investigator_id: str | None = None
    site_id: str | None = None
    enrolled_date: date | None = None
    status: str = Field("enrolled", description="e.g. 'enrolled', 'screen_failure', 'completed', 'withdrawn'.")


class CdiscFormData(BaseModel):
    """ODM FormData — captured form at a specific visit/event."""

    model_config = _ODM_CONFIG
    form_oid: str
    subject_key: str
    study_event_oid: str
    collected_at: datetime
    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Item-OID → value map (thin; real ODM uses ItemGroupData).",
    )
