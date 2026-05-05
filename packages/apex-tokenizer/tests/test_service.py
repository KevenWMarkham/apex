"""Tests for ``apex_tokenizer.service``."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from apex_tokenizer import (
    InMemoryVaultBackend,
    TokenService,
    detokenize,
    reset_default_service,
    set_default_service,
    tokenize,
)


@pytest.fixture(autouse=True)
def _reset_default() -> None:
    reset_default_service()


def _svc() -> TokenService:
    return TokenService(backend=InMemoryVaultBackend())


class TestTokenize:
    def test_shape(self) -> None:
        svc = _svc()
        t = svc.tokenize("Alice Doe", Classification.PHI)
        assert t.startswith("tok_")
        assert len(t) > len("tok_")

    def test_deterministic(self) -> None:
        svc = _svc()
        a = svc.tokenize("alice@example.com", Classification.PII)
        b = svc.tokenize("alice@example.com", Classification.PII)
        assert a == b

    def test_classification_separation(self) -> None:
        svc = _svc()
        a = svc.tokenize("acme", Classification.PII)
        b = svc.tokenize("acme", Classification.TRADE_SECRET)
        assert a != b  # same value, different classifications → different tokens

    def test_tenant_separation(self) -> None:
        svc1 = TokenService(backend=InMemoryVaultBackend(), tenant_id="t1")
        svc2 = TokenService(backend=InMemoryVaultBackend(), tenant_id="t2")
        assert svc1.tokenize("v", Classification.PII) != svc2.tokenize("v", Classification.PII)

    def test_empty_passthrough(self) -> None:
        svc = _svc()
        assert svc.tokenize("", Classification.PII) == ""

    def test_vault_populated(self) -> None:
        backend = InMemoryVaultBackend()
        svc = TokenService(backend=backend)
        svc.tokenize("secret", Classification.PHI)
        assert backend.size() == 1


class TestDetokenize:
    def test_roundtrip(self) -> None:
        svc = _svc()
        original = "Jane Doe"
        token = svc.tokenize(original, Classification.PHI)
        assert svc.detokenize(token) == original

    def test_unknown_token_returns_none(self) -> None:
        svc = _svc()
        assert svc.detokenize("tok_nonexistent_token") is None

    def test_cleartext_pass_through(self) -> None:
        svc = _svc()
        # Not an APEX token — return as-is (migration safety).
        assert svc.detokenize("plain-cleartext") == "plain-cleartext"

    def test_empty_returns_empty(self) -> None:
        svc = _svc()
        assert svc.detokenize("") == ""


class TestModuleLevelDefault:
    def test_module_tokenize_uses_default(self) -> None:
        token = tokenize("hello", Classification.PII)
        assert detokenize(token) == "hello"

    def test_set_default_service(self) -> None:
        backend = InMemoryVaultBackend()
        set_default_service(TokenService(backend=backend))
        tokenize("x", Classification.PCI)
        assert backend.size() == 1

    def test_idempotent_across_calls(self) -> None:
        t1 = tokenize("same", Classification.PII)
        t2 = tokenize("same", Classification.PII)
        assert t1 == t2
