"""Tests for FHIR primitive datatypes."""

from __future__ import annotations

from apex_standards_fhir import (
    FhirAddress,
    FhirCodeableConcept,
    FhirCoding,
    FhirContactPoint,
    FhirHumanName,
    FhirIdentifier,
    FhirPeriod,
    FhirQuantity,
    FhirReference,
)


class TestAliasRoundTrip:
    def test_human_name_accepts_snake_or_camel(self) -> None:
        a = FhirHumanName.model_validate({"family": "Smith", "given": ["Jane"]})
        assert a.family == "Smith"
        # Same via FHIR-native dict:
        b = FhirHumanName.model_validate({"family": "Smith", "given": ["Jane"]})
        assert a == b

    def test_address_postal_code_alias(self) -> None:
        addr = FhirAddress.model_validate({"postalCode": "90210", "city": "Beverly Hills"})
        assert addr.postal_code == "90210"
        dumped = addr.model_dump(by_alias=True, exclude_none=True)
        assert dumped["postalCode"] == "90210"
        assert "postal_code" not in dumped


class TestUnknownFieldsIgnored:
    def test_coding_silently_drops_unknown(self) -> None:
        coding = FhirCoding.model_validate(
            {"system": "http://loinc.org", "code": "1234-5", "someWildFutureField": "x"}
        )
        assert coding.code == "1234-5"


class TestContactPoint:
    def test_phone_email_constructs(self) -> None:
        p = FhirContactPoint(system="phone", value="555-1234", use="work")
        e = FhirContactPoint(system="email", value="j@example.com", use="home")
        assert p.value == "555-1234"
        assert e.use == "home"


class TestCodeableConceptAndIdentifier:
    def test_codeable_concept_nesting(self) -> None:
        cc = FhirCodeableConcept(
            coding=[FhirCoding(system="http://loinc.org", code="1234-5")],
            text="Blood test",
        )
        assert cc.coding[0].code == "1234-5"
        assert cc.text == "Blood test"

    def test_identifier_with_type(self) -> None:
        cc = FhirCodeableConcept(
            coding=[FhirCoding(system="http://terminology.hl7.org/CodeSystem/v2-0203", code="MR")]
        )
        ident = FhirIdentifier(use="official", system="urn:oid:1.2.3", value="MRN-42", type=cc)
        assert ident.type is not None
        assert ident.type.coding[0].code == "MR"


class TestPeriodAndQuantity:
    def test_period(self) -> None:
        p = FhirPeriod.model_validate({"start": "2026-01-01T00:00:00Z"})
        assert p.start is not None
        assert p.end is None

    def test_quantity(self) -> None:
        q = FhirQuantity(value=98.6, unit="degF", system="http://unitsofmeasure.org", code="[degF]")
        assert q.value == 98.6


class TestReference:
    def test_reference_roundtrip(self) -> None:
        ref = FhirReference(reference="Patient/example", type="Patient")
        dumped = ref.model_dump(exclude_none=True)
        assert dumped["reference"] == "Patient/example"
