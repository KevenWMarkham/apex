"""Tests for ``apex_core.quality`` — Sprint 22 Task 22.6 (BL.P.154)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from apex_core.envelope import CanonicalEnvelope
from apex_core.quality import (
    QUALITY_FIELDS,
    DataQualityMetadata,
    QualityDimension,
)


# ---------------------------------------------------------------------------
# Model basics
# ---------------------------------------------------------------------------


def test_quality_dimension_values() -> None:
    """Six ISO-8000-aligned dimensions, lowercased."""
    assert {d.value for d in QualityDimension} == {
        "completeness",
        "consistency",
        "accuracy",
        "currency",
        "provenance",
        "conformance",
    }


def test_quality_fields_includes_all_dimensions() -> None:
    expected = {d.value for d in QualityDimension} | {
        "iso8000_pinned_version",
        "quality_assessed_at",
    }
    assert QUALITY_FIELDS == expected


def test_default_metadata_has_all_none_dimensions() -> None:
    md = DataQualityMetadata()
    for dim in QualityDimension:
        assert getattr(md, dim.value) is None
    assert md.iso8000_pinned_version == "8000-61:2016"
    assert md.composite_score() is None
    assert not md.is_fully_assessed()


# ---------------------------------------------------------------------------
# Score range validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("dim", [d.value for d in QualityDimension])
def test_dimension_rejects_score_below_zero(dim: str) -> None:
    with pytest.raises(ValidationError):
        DataQualityMetadata(**{dim: -0.01})


@pytest.mark.parametrize("dim", [d.value for d in QualityDimension])
def test_dimension_rejects_score_above_one(dim: str) -> None:
    with pytest.raises(ValidationError):
        DataQualityMetadata(**{dim: 1.01})


@pytest.mark.parametrize("score", [0.0, 0.5, 1.0])
def test_dimension_accepts_in_range_score(score: float) -> None:
    md = DataQualityMetadata(completeness=score)
    assert md.completeness == score


# ---------------------------------------------------------------------------
# Composite + helper methods
# ---------------------------------------------------------------------------


def test_composite_score_equal_weight_mean() -> None:
    md = DataQualityMetadata(
        completeness=1.0,
        consistency=0.5,
        accuracy=0.0,
    )
    # Three measured: (1.0 + 0.5 + 0.0) / 3 = 0.5
    assert md.composite_score() == pytest.approx(0.5)


def test_composite_score_ignores_unmeasured_dimensions() -> None:
    md = DataQualityMetadata(
        completeness=0.9,
        # rest are None
    )
    assert md.composite_score() == pytest.approx(0.9)


def test_is_fully_assessed_true_when_all_measured() -> None:
    md = DataQualityMetadata(
        completeness=1.0,
        consistency=1.0,
        accuracy=1.0,
        currency=1.0,
        provenance=1.0,
        conformance=1.0,
    )
    assert md.is_fully_assessed()


def test_is_fully_assessed_false_with_any_none() -> None:
    md = DataQualityMetadata(
        completeness=1.0,
        consistency=1.0,
        accuracy=1.0,
        currency=1.0,
        provenance=1.0,
        # conformance None
    )
    assert not md.is_fully_assessed()


def test_degraded_dimensions_returns_below_threshold() -> None:
    md = DataQualityMetadata(
        completeness=0.95,   # OK
        consistency=0.6,     # degraded
        accuracy=0.5,        # degraded
        currency=0.7,        # exactly threshold — NOT degraded
    )
    degraded = md.degraded_dimensions(threshold=0.7)
    assert QualityDimension.CONSISTENCY in degraded
    assert QualityDimension.ACCURACY in degraded
    assert QualityDimension.COMPLETENESS not in degraded
    assert QualityDimension.CURRENCY not in degraded


def test_degraded_dimensions_skips_unmeasured() -> None:
    """None-scored dimensions are unknown, not degraded."""
    md = DataQualityMetadata(completeness=0.5)
    degraded = md.degraded_dimensions(threshold=0.7)
    assert QualityDimension.COMPLETENESS in degraded
    assert QualityDimension.CONSISTENCY not in degraded


# ---------------------------------------------------------------------------
# Frozen / extra=forbid
# ---------------------------------------------------------------------------


def test_metadata_is_frozen() -> None:
    md = DataQualityMetadata(completeness=0.5)
    with pytest.raises(ValidationError):
        md.completeness = 0.9  # type: ignore[misc]


def test_metadata_rejects_extra_field() -> None:
    with pytest.raises(ValidationError):
        DataQualityMetadata(unknown_dimension=0.5)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Conformance — every Silver row carries quality block
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_envelope_carries_quality_block() -> None:
    """BL.P.154 / Task 22.6.3 exit criterion: every envelope row has the block."""
    from uuid import uuid4

    env = CanonicalEnvelope(
        event_id=uuid4(),
        event_ts=datetime.now(UTC),
        entity_id="x",
        source_system="s",
        source_system_ts=datetime.now(UTC),
    )
    assert hasattr(env, "quality")
    assert isinstance(env.quality, DataQualityMetadata)


@pytest.mark.conformance
def test_conformance_iso_8000_in_standards_registry() -> None:
    """ISO 8000 binding is registered alongside the rest of the catalog."""
    from apex_schemas_common.standards import STANDARDS

    assert "iso-8000" in STANDARDS
    spec = STANDARDS["iso-8000"]
    assert spec.authority == "ISO"
    assert spec.pattern == "B"
    # Spans every Practice — quality is universal
    assert len(spec.practices) >= 7


@pytest.mark.conformance
def test_conformance_iso_8000_pinned_version_matches_metadata() -> None:
    """Drift-detection: registry pin == DataQualityMetadata default pin."""
    from apex_schemas_common.standards import STANDARDS

    md = DataQualityMetadata()
    assert md.iso8000_pinned_version == STANDARDS["iso-8000"].apex_pinned_version
