"""Tests for ``apex_core.envelope``."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from apex_core.envelope import (
    CORE_ENVELOPE_FIELDS,
    ENVELOPE_FIELDS,
    CanonicalEnvelope,
)
from apex_core.quality import DataQualityMetadata


def _sample_kwargs() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "sku_00112233",
        "source_system": "oracle-retail",
        "source_system_ts": datetime.now(UTC),
    }


def test_core_envelope_fields_exact() -> None:
    """The five pre-Sprint-22 core fields are preserved."""
    assert CORE_ENVELOPE_FIELDS == {
        "event_id",
        "event_ts",
        "entity_id",
        "source_system",
        "source_system_ts",
    }


def test_envelope_fields_includes_quality_block() -> None:
    """Sprint 22 Task 22.6 added the quality field; full set is six."""
    assert ENVELOPE_FIELDS == CORE_ENVELOPE_FIELDS | {"quality"}


def test_valid_envelope() -> None:
    env = CanonicalEnvelope(**_sample_kwargs())  # type: ignore[arg-type]
    assert env.entity_id == "sku_00112233"
    assert env.source_system == "oracle-retail"


def test_envelope_quality_defaults_to_empty_block() -> None:
    """Backward-compat: callers that don't pass ``quality`` get a blank block."""
    env = CanonicalEnvelope(**_sample_kwargs())  # type: ignore[arg-type]
    assert isinstance(env.quality, DataQualityMetadata)
    assert env.quality.completeness is None
    assert env.quality.composite_score() is None
    assert not env.quality.is_fully_assessed()


def test_envelope_accepts_explicit_quality_block() -> None:
    kwargs = _sample_kwargs()
    kwargs["quality"] = DataQualityMetadata(
        completeness=0.95,
        consistency=0.9,
        accuracy=0.85,
        currency=1.0,
        provenance=0.9,
        conformance=1.0,
    )
    env = CanonicalEnvelope(**kwargs)  # type: ignore[arg-type]
    assert env.quality.is_fully_assessed()
    score = env.quality.composite_score()
    assert score is not None
    assert 0.9 <= score <= 0.95


def test_missing_field_rejected() -> None:
    kwargs = _sample_kwargs()
    kwargs.pop("entity_id")
    with pytest.raises(ValidationError):
        CanonicalEnvelope(**kwargs)  # type: ignore[arg-type]


def test_extra_field_rejected() -> None:
    kwargs = _sample_kwargs()
    kwargs["extra_field"] = "nope"
    with pytest.raises(ValidationError):
        CanonicalEnvelope(**kwargs)  # type: ignore[arg-type]


def test_envelope_is_frozen() -> None:
    env = CanonicalEnvelope(**_sample_kwargs())  # type: ignore[arg-type]
    with pytest.raises(ValidationError):
        env.entity_id = "other"  # type: ignore[misc]
