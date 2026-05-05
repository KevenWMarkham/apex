"""Tests for the Pydantic classified-fields walker."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field

from apex_core.types import Classification
from apex_tokenizer import (
    InMemoryVaultBackend,
    TokenService,
    detokenize,
    reset_default_service,
    set_default_service,
    tokenize_classified_fields,
)


def _setup() -> InMemoryVaultBackend:
    reset_default_service()
    backend = InMemoryVaultBackend()
    set_default_service(TokenService(backend=backend))
    return backend


class _Model(BaseModel):
    id: int
    name_token: Annotated[str, Classification.PII] | None = None
    email_token: Annotated[str, Classification.PII] | None = None
    dob: str | None = None  # not classified
    internal_note: Annotated[str, Classification.INTERNAL] | None = None  # internal → not tokenised


def test_classified_fields_tokenised() -> None:
    _setup()
    before = _Model(id=1, name_token="Alice", email_token="alice@example.com", dob="1990-01-01")
    after = tokenize_classified_fields(before)
    assert after.name_token is not None and after.name_token.startswith("tok_")
    assert after.email_token is not None and after.email_token.startswith("tok_")


def test_non_classified_fields_pass_through() -> None:
    _setup()
    before = _Model(id=1, name_token="Bob", dob="1985-06-15")
    after = tokenize_classified_fields(before)
    assert after.dob == "1985-06-15"
    assert after.id == 1


def test_internal_classification_not_tokenised() -> None:
    _setup()
    before = _Model(id=1, internal_note="just a note")
    after = tokenize_classified_fields(before)
    assert after.internal_note == "just a note"


def test_idempotent_on_already_tokenised() -> None:
    _setup()
    before = _Model(id=1, name_token="Carol")
    once = tokenize_classified_fields(before)
    twice = tokenize_classified_fields(once)
    assert once.name_token == twice.name_token


def test_none_fields_left_alone() -> None:
    _setup()
    before = _Model(id=1)  # all optional classified fields None
    after = tokenize_classified_fields(before)
    assert after.name_token is None
    assert after.email_token is None


def test_round_trip_via_default_service() -> None:
    _setup()
    before = _Model(id=1, email_token="carol@example.com")
    after = tokenize_classified_fields(before)
    assert detokenize(after.email_token or "") == "carol@example.com"
