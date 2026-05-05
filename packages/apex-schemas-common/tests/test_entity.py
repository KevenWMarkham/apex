"""Tests for ``apex_schemas_common.entity``."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import Field, ValidationError

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class _SampleEntity(CanonicalEntity):
    sku_natural: str = Field(..., description="Natural key from source.")
    description: str = ""


class _SampleScd2Entity(CanonicalEntity, ScdType2Fields):
    sku_natural: str


def _envelope_kwargs() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "sku_0001",
        "source_system": "test",
        "source_system_ts": datetime.now(UTC),
    }


def test_canonical_entity_requires_envelope() -> None:
    with pytest.raises(ValidationError):
        _SampleEntity(sku_natural="abc")  # type: ignore[call-arg]


def test_canonical_entity_construction() -> None:
    entity = _SampleEntity(sku_natural="abc", **_envelope_kwargs())  # type: ignore[arg-type]
    assert entity.sku_natural == "abc"
    assert entity.source_system == "test"


def test_scd2_mixin_adds_history_fields() -> None:
    now = datetime.now(UTC)
    entity = _SampleScd2Entity(
        sku_natural="abc",
        scd2_valid_from=now,
        row_hash="deadbeef",
        **_envelope_kwargs(),
    )  # type: ignore[arg-type]
    assert entity.scd2_is_current is True
    assert entity.scd2_valid_to is None
    assert entity.row_hash == "deadbeef"


def test_scd2_requires_row_hash() -> None:
    with pytest.raises(ValidationError):
        _SampleScd2Entity(
            sku_natural="abc",
            scd2_valid_from=datetime.now(UTC),
            **_envelope_kwargs(),
        )  # type: ignore[call-arg,arg-type]
