"""Tests for ``apex_medallion.silver.transform``."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from pydantic import Field

from apex_core.types import Classification
from apex_medallion.silver import Scd2Config, add_scd2_fields_to_instance, tokenise_and_stamp
from apex_schemas_common import CanonicalEntity, ScdType2Fields
from apex_tokenizer import (
    InMemoryVaultBackend,
    TokenService,
    reset_default_service,
    set_default_service,
)


class _ExampleEntity(CanonicalEntity, ScdType2Fields):
    natural: str = Field(..., description="Natural key.")
    email_token: Annotated[str, Classification.PII] | None = None
    status: str = "ACTIVE"


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
        "row_hash": "placeholder",
    }


def _reset() -> InMemoryVaultBackend:
    reset_default_service()
    backend = InMemoryVaultBackend()
    set_default_service(TokenService(backend=backend))
    return backend


class TestTokeniseAndStamp:
    def test_tokenises_pii_field(self) -> None:
        _reset()
        ent = _ExampleEntity(
            natural="e-1", email_token="alice@example.com",
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        out = tokenise_and_stamp(ent)
        assert out.email_token is not None and out.email_token.startswith("tok_")

    def test_idempotent_on_already_tokenised(self) -> None:
        _reset()
        ent = _ExampleEntity(
            natural="e-1", email_token="alice@example.com",
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        once = tokenise_and_stamp(ent)
        twice = tokenise_and_stamp(once)
        assert once.email_token == twice.email_token


class TestAddScd2Fields:
    def test_stamps_when_no_existing_hash(self) -> None:
        _reset()
        ent = _ExampleEntity(
            natural="e-1", status="ACTIVE",
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        config = Scd2Config(
            key_columns=("natural",),
            hashable_columns=("natural", "status"),
        )
        out = add_scd2_fields_to_instance(ent, config=config)
        assert out.row_hash != "placeholder"  # updated to real hash
        assert out.scd2_is_current is True
        assert out.scd2_valid_to is None

    def test_noop_when_hash_unchanged(self) -> None:
        _reset()
        ent = _ExampleEntity(
            natural="e-1", status="ACTIVE",
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        config = Scd2Config(
            key_columns=("natural",),
            hashable_columns=("natural", "status"),
        )
        out = add_scd2_fields_to_instance(ent, config=config)
        # Re-apply with the computed hash treated as 'existing'
        again = add_scd2_fields_to_instance(
            out, config=config, existing_row_hash=out.row_hash,
        )
        assert again is out  # identity — no-op
