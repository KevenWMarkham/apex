"""Response signing — HMAC over agent outputs keyed on (agent_id, tenant_id).

Sprint 10 ships a deterministic HMAC-SHA256. Sprint 13 swaps in
RSA-SHA256 with Key-Vault-stored tenant private keys.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any

_DEFAULT_SECRET_ENV = "APEX_SIGNING_SECRET"
_DEV_SECRET = b"apex-signing-dev-secret-change-me"


def _base_secret() -> bytes:
    value = os.environ.get(_DEFAULT_SECRET_ENV)
    if value:
        return value.encode("utf-8")
    return _DEV_SECRET


def _derive_key(agent_id: str, tenant_id: str) -> bytes:
    """Derive a per-(agent, tenant) HMAC key from the base secret."""
    base = _base_secret()
    return hmac.new(
        base, f"{tenant_id}|{agent_id}".encode("utf-8"), hashlib.sha256
    ).digest()


def sign_response(
    payload: Any,
    *,
    agent_id: str,
    tenant_id: str,
) -> str:
    """Compute an HMAC-SHA256 signature over ``payload``."""
    key = _derive_key(agent_id, tenant_id)
    blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hmac.new(key, blob, hashlib.sha256).hexdigest()


def verify_response(
    payload: Any,
    signature: str,
    *,
    agent_id: str,
    tenant_id: str,
) -> bool:
    """Recompute + compare a signature. Constant-time via ``hmac.compare_digest``."""
    expected = sign_response(payload, agent_id=agent_id, tenant_id=tenant_id)
    return hmac.compare_digest(expected, signature)
