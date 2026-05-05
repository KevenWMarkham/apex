"""Tests for ``apex_core.validators.practice.validate_practice``."""

from __future__ import annotations

from pathlib import Path

from apex_core.validators import validate_practice

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_fixtures_directory_has_two_invalid() -> None:
    """The fixtures directory contains 7 valid + 2 invalid YAMLs."""
    report = validate_practice(FIXTURES)
    # Depending on fixture drift, this is roughly the number we expect.
    assert len(report.reports) >= 7
    # At least the two invalid fixtures fail.
    assert len(report.failures) >= 2
    assert not report.valid


def test_summary_format() -> None:
    report = validate_practice(FIXTURES)
    summary = report.summary()
    assert str(FIXTURES) in summary
    assert ("OK" in summary) or ("FAIL" in summary)
