"""Tests for the dev-only mock terminology service."""

from __future__ import annotations

from apex_standards_fhir.terminology import MockTerminologyService


def test_lookup_known_loinc() -> None:
    svc = MockTerminologyService()
    result = svc.lookup("http://loinc.org", "85354-9")
    assert result is not None
    assert result.system == "http://loinc.org"
    assert result.code == "85354-9"
    assert "Blood pressure" in result.display


def test_lookup_missing_returns_none() -> None:
    svc = MockTerminologyService()
    assert svc.lookup("http://loinc.org", "not-in-mock") is None


def test_is_active_gates_unknown_codes() -> None:
    svc = MockTerminologyService()
    assert svc.is_active("http://loinc.org", "85354-9") is True
    assert svc.is_active("http://loinc.org", "not-in-mock") is False


def test_snomed_seed_present() -> None:
    svc = MockTerminologyService()
    assert svc.lookup("http://snomed.info/sct", "386661006") is not None


def test_rxnorm_seed_present() -> None:
    svc = MockTerminologyService()
    result = svc.lookup("http://www.nlm.nih.gov/research/umls/rxnorm", "1049630")
    assert result is not None
    assert "acetaminophen" in result.display.lower()
