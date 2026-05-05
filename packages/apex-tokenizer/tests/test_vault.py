"""Tests for vault backends."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from apex_core.types import Classification
from apex_tokenizer import (
    DeltaVaultBackend,
    InMemoryVaultBackend,
    VaultBackend,
    VaultEntry,
    vault_ddl,
)
from apex_tokenizer.vault import new_vault_entry


def test_in_memory_implements_protocol() -> None:
    backend = InMemoryVaultBackend()
    assert isinstance(backend, VaultBackend)


def test_store_and_resolve() -> None:
    backend = InMemoryVaultBackend()
    entry = new_vault_entry(
        token="tok_abc", cleartext="hello",
        classification=Classification.PHI,
        tenant_id="t1", source_system="epic", created_by="svc",
    )
    backend.store(entry)
    assert backend.has("tok_abc")
    resolved = backend.resolve("tok_abc")
    assert resolved is not None
    assert resolved.cleartext == "hello"


def test_store_is_idempotent_on_token() -> None:
    backend = InMemoryVaultBackend()
    e1 = VaultEntry(token="tok_x", cleartext="first",
                    classification=Classification.PII,
                    tenant_id="t", source_system=None,
                    created_ts=datetime.now(UTC), created_by="svc")
    e2 = VaultEntry(token="tok_x", cleartext="second",
                    classification=Classification.PII,
                    tenant_id="t", source_system=None,
                    created_ts=datetime.now(UTC), created_by="svc")
    backend.store(e1)
    backend.store(e2)
    resolved = backend.resolve("tok_x")
    assert resolved is not None
    assert resolved.cleartext == "first"  # first-wins
    assert backend.size() == 1


def test_resolve_unknown_returns_none() -> None:
    backend = InMemoryVaultBackend()
    assert backend.resolve("tok_missing") is None


def test_delta_backend_methods_not_yet_wired() -> None:
    delta = DeltaVaultBackend(table_name="silver_vault_tokens")
    with pytest.raises(NotImplementedError):
        delta.store(new_vault_entry(
            token="tok_x", cleartext="v", classification=Classification.PII,
            tenant_id="t", source_system=None, created_by="svc",
        ))


def test_vault_ddl_structure() -> None:
    ddl = vault_ddl()
    assert "CREATE TABLE silver_vault_tokens" in ddl
    for col in ("token", "cleartext", "classification", "tenant_id", "created_ts"):
        assert col in ddl
    assert "PARTITIONED BY (tenant_id, classification)" in ddl


def test_vault_ddl_qualified() -> None:
    ddl = vault_ddl(database="silver_hls")
    assert "CREATE TABLE silver_hls.silver_vault_tokens" in ddl
