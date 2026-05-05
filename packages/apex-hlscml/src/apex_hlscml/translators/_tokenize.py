"""Thin delegator to the real ``apex-tokenizer`` service.

Sprint 3 shipped an in-module placeholder that prepended ``tok_placeholder_``.
Sprint 5 replaces it with delegation to ``apex_tokenizer``, whose default
service uses an in-memory vault (so unit tests still round-trip without a
Spark / Delta environment). Production swaps the default service to the
Delta-backed vault via :func:`apex_tokenizer.set_default_service`.
"""

from __future__ import annotations

from apex_core.types import Classification
from apex_tokenizer import detokenize as _svc_detokenize
from apex_tokenizer import tokenize as _svc_tokenize


def tokenize(
    value: str | None,
    *,
    classification: Classification = Classification.PHI,
) -> str | None:
    """Tokenise ``value`` using the apex-tokenizer default service."""
    if value is None:
        return None
    return _svc_tokenize(value, classification)


def detokenize(token: str | None) -> str | None:
    """Resolve ``token`` via the apex-tokenizer default service."""
    if token is None:
        return None
    return _svc_detokenize(token)
