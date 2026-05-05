"""Tests for HLSCML entities."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from apex_hlscml import (
    AdverseEvent,
    ClaimHeader,
    ClaimLine,
    DiagnosticReport,
    Encounter,
    EncounterStatus,
    MedicationRequest,
    MedicationRequestIntent,
    MedicationRequestStatus,
    Observation,
    ObservationStatus,
    Patient,
    Practitioner,
    Study,
    StudyEnrollment,
    StudyPhase,
)
from apex_hlscml.entities.adverse_event import AeSeverity
from apex_hlscml.entities.claim import ClaimStatus, ClaimType
from apex_hlscml.entities.diagnostic_report import DiagnosticReportStatus


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test",
        "source_system": "fhir",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "abc123",
    }


class TestPatient:
    def test_minimal(self) -> None:
        p = Patient(fhir_id="ex1", **_envelope(), **_scd2())  # type: ignore[arg-type]
        assert p.fhir_id == "ex1"
        assert p.source_fhir_version == "R4"

    def test_tokenised_fields(self) -> None:
        p = Patient(
            fhir_id="ex2",
            mrn_token="tok_mrn_123",
            name_family_token="tok_smith",
            gender="female",
            birth_date=date(1980, 1, 1),
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        assert p.mrn_token == "tok_mrn_123"
        assert p.gender == "female"

    def test_rejects_invalid_gender(self) -> None:
        with pytest.raises(ValidationError):
            Patient(
                fhir_id="bad", gender="invalid",  # type: ignore[arg-type]
                **_envelope(), **_scd2(),
            )


class TestPractitioner:
    def test_minimal(self) -> None:
        p = Practitioner(fhir_id="dr1", **_envelope(), **_scd2())  # type: ignore[arg-type]
        assert p.active is True

    def test_with_qualification(self) -> None:
        p = Practitioner(
            fhir_id="dr2", qualifications=["MD", "BoardCertified"],
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        assert "MD" in p.qualifications


class TestEncounter:
    def test_ambulatory(self) -> None:
        enc = Encounter(
            fhir_id="enc1", status=EncounterStatus.FINISHED,
            encounter_class="AMB", patient_key="patient:ex1",
            start_ts=datetime.now(UTC),
            **_envelope(),
        )  # type: ignore[arg-type]
        assert enc.status is EncounterStatus.FINISHED


class TestObservation:
    def test_with_loinc(self) -> None:
        obs = Observation(
            fhir_id="obs1", status=ObservationStatus.FINAL,
            loinc_code="85354-9", code_display="Blood pressure",
            patient_key="patient:ex1",
            effective_ts=datetime.now(UTC),
            value_numeric=Decimal("120"), value_unit="mmHg",
            **_envelope(),
        )  # type: ignore[arg-type]
        assert obs.loinc_code == "85354-9"

    def test_rejects_invalid_loinc(self) -> None:
        with pytest.raises(ValidationError):
            Observation(
                fhir_id="obs-bad", status=ObservationStatus.FINAL,
                loinc_code="not-a-code",
                code_display="x", patient_key="patient:ex1",
                effective_ts=datetime.now(UTC),
                **_envelope(),
            )  # type: ignore[arg-type]


class TestDiagnosticReport:
    def test_with_observations(self) -> None:
        dr = DiagnosticReport(
            fhir_id="dr1", status=DiagnosticReportStatus.FINAL,
            patient_key="patient:ex1",
            observation_keys=["obs1", "obs2"],
            conclusion="No abnormalities detected.",
            **_envelope(),
        )  # type: ignore[arg-type]
        assert len(dr.observation_keys) == 2


class TestMedicationRequest:
    def test_with_rxnorm(self) -> None:
        mr = MedicationRequest(
            fhir_id="mr1",
            status=MedicationRequestStatus.ACTIVE,
            intent=MedicationRequestIntent.ORDER,
            rxnorm_code="1049630",
            medication_display="Acetaminophen 325 MG Oral Tablet",
            patient_key="patient:ex1",
            **_envelope(),
        )  # type: ignore[arg-type]
        assert mr.rxnorm_code == "1049630"


class TestClaims:
    def test_header_and_line(self) -> None:
        header = ClaimHeader(
            fhir_id="clm1",
            status=ClaimStatus.ACTIVE,
            claim_type=ClaimType.PROFESSIONAL,
            patient_key="patient:ex1",
            provider_key="prac:dr1",
            created_ts=datetime.now(UTC),
            total_amount=Decimal("250.00"),
            **_envelope(),
        )  # type: ignore[arg-type]
        line = ClaimLine(
            fhir_id="clm1-1",
            claim_header_key=header.entity_id,
            sequence=1,
            cpt_code="99213",
            unit_price=Decimal("250.00"),
            net_amount=Decimal("250.00"),
            **_envelope(),
        )  # type: ignore[arg-type]
        assert line.cpt_code == "99213"


class TestStudyAndEnrollment:
    def test_study(self) -> None:
        s = Study(
            study_oid="ODM.STUDY-42",
            protocol_name="APX-042",
            phase=StudyPhase.PHASE_2,
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        assert s.phase is StudyPhase.PHASE_2

    def test_enrollment_requires_token(self) -> None:
        with pytest.raises(ValidationError):
            StudyEnrollment(
                study_key="study:42",
                **_envelope(), **_scd2(),
            )  # type: ignore[call-arg,arg-type]

    def test_enrollment(self) -> None:
        e = StudyEnrollment(
            subject_key_token="tok_subj_001",
            study_key="study:42",
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        assert e.subject_key_token == "tok_subj_001"


class TestAdverseEvent:
    def test_mild(self) -> None:
        ae = AdverseEvent(
            subject_key_token="tok_subj_001",
            study_key="study:42",
            ae_sequence=1,
            ae_term="Headache",
            severity=AeSeverity.MILD,
            **_envelope(),
        )  # type: ignore[arg-type]
        assert ae.severity is AeSeverity.MILD
        assert ae.serious is False
