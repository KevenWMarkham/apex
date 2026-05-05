"""Vault backends — pluggable storage for token ↔ cleartext mappings."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol, runtime_checkable

from apex_core.types import Classification


@dataclass(frozen=True, slots=True)
class VaultEntry:
    """One vault row — an immutable mapping from token to cleartext."""

    token: str
    cleartext: str
    classification: Classification
    tenant_id: str
    source_system: str | None
    created_ts: datetime
    created_by: str


@runtime_checkable
class VaultBackend(Protocol):
    """Protocol every vault backend must implement."""

    def store(self, entry: VaultEntry) -> None:
        """Persist an entry. Implementations should be idempotent on ``token``."""
        ...

    def resolve(self, token: str) -> VaultEntry | None:
        """Return the entry for ``token``, or ``None`` if not found."""
        ...

    def has(self, token: str) -> bool:
        """Return True iff ``token`` has an entry (cheaper than resolve)."""
        ...


@dataclass
class InMemoryVaultBackend:
    """In-memory backend — dev, tests, and single-process runs only."""

    _store: dict[str, VaultEntry] = field(default_factory=dict)

    def store(self, entry: VaultEntry) -> None:
        self._store.setdefault(entry.token, entry)

    def resolve(self, token: str) -> VaultEntry | None:
        return self._store.get(token)

    def has(self, token: str) -> bool:
        return token in self._store

    def size(self) -> int:
        """Test helper — number of stored entries."""
        return len(self._store)


class DeltaVaultBackend:
    """Fabric Delta-backed vault (Sprint 5 stub).

    The real implementation uses the OneLake Delta writer + a SparkSession;
    it lives in the Silver notebook pipeline. Sprint 5 ships the interface
    and structural placeholders so the service + classifier_hook work without
    a live Spark environment.
    """

    def __init__(self, table_name: str, spark: Any = None) -> None:
        self.table_name = table_name
        self.spark = spark

    def store(self, entry: VaultEntry) -> None:  # pragma: no cover - Spark-only
        raise NotImplementedError(
            "DeltaVaultBackend.store is wired by the Silver-transform notebook."
        )

    def resolve(self, token: str) -> VaultEntry | None:  # pragma: no cover
        raise NotImplementedError(
            "DeltaVaultBackend.resolve is wired by the Silver-transform notebook."
        )

    def has(self, token: str) -> bool:  # pragma: no cover
        raise NotImplementedError(
            "DeltaVaultBackend.has is wired by the Silver-transform notebook."
        )


def new_vault_entry(
    *,
    token: str,
    cleartext: str,
    classification: Classification,
    tenant_id: str,
    source_system: str | None,
    created_by: str,
) -> VaultEntry:
    """Convenience constructor — stamps ``created_ts`` with UTC now."""
    return VaultEntry(
        token=token,
        cleartext=cleartext,
        classification=classification,
        tenant_id=tenant_id,
        source_system=source_system,
        created_ts=datetime.now(UTC),
        created_by=created_by,
    )
