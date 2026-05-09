"""SecretStore protocol — secrets, keys, certificates with rotation.

APEX-M satisfies via Azure Key Vault (Premium HSM).
APEX-G satisfies via Google Secret Manager.
APEX-A satisfies via AWS Secrets Manager + KMS.

Adapters: HashiCorp Vault, CyberArk, Thycotic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class SecretReference:
    """Pointer to a secret, never the value itself."""
    store_id: str       # variant-specific (KV name, Secret Manager project, etc.)
    secret_name: str
    version: str | None = None  # None = latest


@dataclass(frozen=True)
class Secret:
    """A retrieved secret value + metadata."""
    reference: SecretReference
    value: str          # caller is responsible for not logging this
    version: str
    expires_at: str | None = None  # ISO 8601


@runtime_checkable
class SecretStore(Protocol):
    """Get, put, version, and rotate secrets."""

    variant: str

    def get(self, ref: SecretReference) -> Secret:
        """Retrieve a secret. Raises on missing or unauthorized."""
        ...

    def put(self, *, name: str, value: str, expires_at: str | None = None) -> SecretReference:
        """Store a new secret or new version of an existing secret."""
        ...

    def list_versions(self, name: str) -> list[str]:
        """All versions of the named secret."""
        ...

    def rotate(self, name: str, *, new_value: str) -> SecretReference:
        """Atomically rotate to a new value. Returns the new ref (latest)."""
        ...
