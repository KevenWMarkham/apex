"""Walk a Pydantic instance, tokenise every classified string field."""

from __future__ import annotations

from types import NoneType, UnionType
from typing import Annotated, Any, TypeVar, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from apex_core.types import Classification

from apex_tokenizer.service import TokenService, get_default_service

_TOKENISED_CLASSIFICATIONS: frozenset[Classification] = frozenset({
    Classification.PII,
    Classification.PHI,
    Classification.PCI,
    Classification.TRADE_SECRET,
    Classification.MEMBER_ONLY,
})

_ModelT = TypeVar("_ModelT", bound=BaseModel)


def _find_classification(annotation: Any) -> Classification | None:
    """Return the first ``Classification`` metadata on ``annotation``, if any."""
    origin = get_origin(annotation)
    if origin is UnionType or origin is Union:
        for arg in get_args(annotation):
            if arg is NoneType:
                continue
            found = _find_classification(arg)
            if found is not None:
                return found
        return None
    if origin is Annotated:
        for meta in get_args(annotation)[1:]:
            if isinstance(meta, Classification):
                return meta
    return None


def tokenize_classified_fields(
    instance: _ModelT,
    *,
    service: TokenService | None = None,
    source_system: str | None = None,
) -> _ModelT:
    """Return a copy of ``instance`` with every classified string field tokenised.

    Only classifications in :data:`_TOKENISED_CLASSIFICATIONS` are tokenised
    (PII / PHI / PCI / TRADE_SECRET / MEMBER_ONLY). Fields that already hold
    an APEX token (start with ``tok_``) are skipped — idempotent. Non-string
    classified fields are left untouched; the caller is responsible for
    stringifying before calling if needed.
    """
    svc = service or get_default_service()
    hints = get_type_hints(type(instance), include_extras=True)
    updates: dict[str, Any] = {}

    for field_name in type(instance).model_fields:
        classification = _find_classification(hints.get(field_name, str))
        if classification is None or classification not in _TOKENISED_CLASSIFICATIONS:
            continue
        current = getattr(instance, field_name)
        if current is None or not isinstance(current, str):
            continue
        if current.startswith("tok_"):
            continue  # already tokenised
        updates[field_name] = svc.tokenize(
            current, classification, source_system=source_system,
        )

    if not updates:
        return instance
    return instance.model_copy(update=updates)
