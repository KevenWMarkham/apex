"""Tests for ``apex_schemas_common.standards``."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, Field, ValidationError

from apex_core.types import Practice
from apex_schemas_common.standards import (
    GLN,
    GTIN14,
    SSCC,
    STANDARDS,
    Icd10Code,
    LoincCode,
    audit_model,
    find_standard_refs,
    list_standards,
    lookup,
)


class _Box(BaseModel):
    gtin: GTIN14
    sscc: SSCC
    gln: GLN
    loinc: LoincCode | None = Field(None)
    icd10: Icd10Code | None = Field(None)


class TestIdentifierRegex:
    def test_gtin14_accepts_14_digits(self) -> None:
        _Box(gtin="12345678901234", sscc="123456789012345678", gln="1234567890123")

    def test_gtin14_rejects_non_14_digits(self) -> None:
        with pytest.raises(ValidationError):
            _Box(gtin="123", sscc="123456789012345678", gln="1234567890123")

    def test_sscc_18_digits(self) -> None:
        with pytest.raises(ValidationError):
            _Box(gtin="12345678901234", sscc="123", gln="1234567890123")

    def test_loinc_format(self) -> None:
        _Box(
            gtin="12345678901234", sscc="123456789012345678",
            gln="1234567890123", loinc="1234-5",
        )
        with pytest.raises(ValidationError):
            _Box(
                gtin="12345678901234", sscc="123456789012345678",
                gln="1234567890123", loinc="invalid",
            )

    def test_icd10_format(self) -> None:
        _Box(
            gtin="12345678901234", sscc="123456789012345678",
            gln="1234567890123", icd10="E11.9",
        )
        with pytest.raises(ValidationError):
            _Box(
                gtin="12345678901234", sscc="123456789012345678",
                gln="1234567890123", icd10="not-a-code",
            )


class TestRegistry:
    def test_lookup_known(self) -> None:
        spec = lookup("gs1-gtin")
        assert spec.authority == "GS1"
        assert spec.pattern == "A"

    def test_lookup_unknown_raises(self) -> None:
        with pytest.raises(KeyError):
            lookup("not-a-real-standard")

    def test_list_standards_all(self) -> None:
        specs = list_standards()
        assert len(specs) > 5
        ids = {s.id for s in specs}
        assert "gs1-gtin" in ids
        assert "hl7-fhir" in ids

    def test_list_standards_filter_by_practice(self) -> None:
        rc_specs = list_standards(Practice.RC)
        assert all(Practice.RC in s.practices for s in rc_specs)
        assert any(s.id == "gs1-gtin" for s in rc_specs)

    def test_redistribution_flag_for_restricted(self) -> None:
        snomed = STANDARDS.get("snomed-ct")
        assert snomed is not None
        assert snomed.license == "restricted"
        assert snomed.redistribution_ok is False


@pytest.mark.conformance
class TestIntrospection:
    def test_find_refs_on_box(self) -> None:
        refs = find_standard_refs(_Box)
        assert set(refs) == {"gtin", "sscc", "gln", "loinc", "icd10"}
        assert refs["gtin"].identifier == "GTIN-14"

    def test_audit_model_all_registered(self) -> None:
        entries = audit_model(_Box)
        by_field = {e.field: e for e in entries}
        # GTIN-14, SSCC, GLN all in registry
        assert by_field["gtin"].registered
        assert by_field["sscc"].registered
        assert by_field["gln"].registered
        assert by_field["icd10"].registered

    def test_audit_version_matches_for_known_standards(self) -> None:
        entries = audit_model(_Box)
        by_field = {e.field: e for e in entries}
        assert by_field["gtin"].version_matches
