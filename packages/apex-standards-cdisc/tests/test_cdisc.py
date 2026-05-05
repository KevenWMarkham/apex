"""Tests for CDISC ODM + SDTM skeletons."""

from __future__ import annotations

from datetime import date

from apex_standards_cdisc import (
    CdiscFormData,
    CdiscStudy,
    CdiscSubject,
    SdtmAdverseEvent,
    SdtmAeSeverity,
    SdtmDemographics,
    SdtmLabResult,
)


class TestOdm:
    def test_study_minimal(self) -> None:
        s = CdiscStudy(study_oid="STUDY-001", protocol_name="APX-001")
        assert s.study_oid == "STUDY-001"

    def test_subject_links_to_study(self) -> None:
        subj = CdiscSubject(
            subject_key="SUBJ-001",
            study_oid="STUDY-001",
            enrolled_date=date(2026, 3, 15),
        )
        assert subj.status == "enrolled"
        assert subj.study_oid == "STUDY-001"

    def test_form_data_captures_items(self) -> None:
        from datetime import datetime

        fd = CdiscFormData(
            form_oid="F-DEMO",
            subject_key="SUBJ-001",
            study_event_oid="SE-SCREEN",
            collected_at=datetime.now(),
            data={"BIRTH_YEAR": 1985, "SEX": "F"},
        )
        assert fd.data["SEX"] == "F"


class TestSdtm:
    def test_demographics_minimal(self) -> None:
        dm = SdtmDemographics(studyid="S-001", usubjid="S-001-0001", age=42, sex="F")
        assert dm.age == 42

    def test_ae_severity_controlled(self) -> None:
        ae = SdtmAdverseEvent(
            studyid="S-001", usubjid="S-001-0001", aeseq=1,
            aeterm="Headache", aesev=SdtmAeSeverity.MILD,
        )
        assert ae.aesev is SdtmAeSeverity.MILD

    def test_lab_result_numeric(self) -> None:
        lb = SdtmLabResult(
            studyid="S-001", usubjid="S-001-0001", lbseq=1,
            lbtestcd="GLUC", lbtest="Glucose",
            lborres="105", lborresu="mg/dL",
            lbstresn=105.0, lbstresu="mg/dL",
        )
        assert lb.lbstresn == 105.0

    def test_ae_sequence_must_be_positive(self) -> None:
        import pytest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            SdtmAdverseEvent(
                studyid="S-001", usubjid="S-001-0001", aeseq=0, aeterm="x",
            )
