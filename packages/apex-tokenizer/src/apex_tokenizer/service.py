"""``TokenService`` — the tokenise / detokenise runtime.

Tokens are shaped ``tok_<base64url-16>`` where the 16-char suffix is a
URL-safe encoding of the first 12 bytes of ``HMAC-SHA256(secret,
tenant|classification|value)``. The HMAC ensures determinism + collision
resistance; cleartext is recovered only by looking the token up in the
backend vault — not by reversing the hash.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os

from apex_core.types import Classification

from apex_tokenizer.vault import (
    InMemoryVaultBackend,
    VaultBackend,
    new_vault_entry,
)

TOKEN_PREFIX = "tok_"
_DEFAULT_TENANT = "default"
_DEFAULT_SECRET_ENV = "APEX_TOKENIZER_SECRET"
_DEV_PLACEHOLDER_SECRET = b"apex-dev-secret-change-me"


def _resolve_secret(explicit: bytes | None) -> bytes:
    """Pick the HMAC secret: explicit arg > env var > dev placeholder."""
    if explicit is not None:
        return explicit
    from_env = os.environ.get(_DEFAULT_SECRET_ENV)
    if from_env:
        return from_env.encode("utf-8")
    return _DEV_PLACEHOLDER_SECRET


class TokenService:
    """Tokenise / detokenise against a configured vault backend."""

    def __init__(
        self,
        backend: VaultBackend,
        *,
        tenant_id: str = _DEFAULT_TENANT,
        secret: bytes | None = None,
    ) -> None:
        self.backend = backend
        self.tenant_id = tenant_id
        self._secret = _resolve_secret(secret)

    def _compute_token(self, *, value: str, classification: Classification) -> str:
        msg = f"{self.tenant_id}|{classification.value}|{value}".encode("utf-8")
        digest = hmac.new(self._secret, msg, hashlib.sha256).digest()[:12]
        suffix = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
        return f"{TOKEN_PREFIX}{suffix}"

    def tokenize(
        self,
        value: str,
        classification: Classification,
        *,
        source_system: str | None = None,
        created_by: str = "system",
    ) -> str:
        """Tokenise ``value``; idempotent — repeat calls return the same token."""
        if not value:
            return value
        token = self._compute_token(value=value, classification=classification)
        if not self.backend.has(token):
            self.backend.store(
                new_vault_entry(
                    token=token,
                    cleartext=value,
                    classification=classification,
                    tenant_id=self.tenant_id,
                    source_system=source_system,
                    created_by=created_by,
                )
            )
        return token

    def detokenize(self, token: str) -> str | None:
        """Resolve ``token`` to its cleartext via the vault.

        Sprint 5 ships unconditional detokenise. The visibility-lattice check
        (per APEX_Design §8.3) is wired in Sprint 10.

        Returns ``None`` if ``token`` is unknown, empty, or not a valid APEX
        token shape. If ``token`` is not an APEX token (no prefix), it is
        returned as-is — handles rows that carry cleartext during migration.
        """
        if not token:
            return token
        if not token.startswith(TOKEN_PREFIX):
            return token  # cleartext pass-through
        entry = self.backend.resolve(token)
        return entry.cleartext if entry is not None else None


# --- Module-level default service -------------------------------------------

_default_service: TokenService | None = None


def set_default_service(svc: TokenService) -> None:
    """Replace the module-level default service (e.g. to swap to DeltaVaultBackend)."""
    global _default_service
    _default_service = svc


def get_default_service() -> TokenService:
    """Return the module-level default service, creating one if necessary."""
    global _default_service
    if _default_service is None:
        _default_service = TokenService(backend=InMemoryVaultBackend())
    return _default_service


def reset_default_service() -> None:
    """Test helper — clear the module-level default."""
    global _default_service
    _default_service = None


def tokenize(
    value: str,
    classification: Classification,
    *,
    source_system: str | None = None,
    created_by: str = "system",
) -> str:
    """Convenience — delegate to the default service."""
    return get_default_service().tokenize(
        value, classification,
        source_system=source_system, created_by=created_by,
    )


def detokenize(token: str) -> str | None:
    """Convenience — delegate to the default service."""
    return get_default_service().detokenize(token)
