"""Row signing + tamper-evidence verification (BL.P.84).

Every row is HMAC-SHA256 signed before seal. Production pulls the key from
Key Vault keyed by ``tenant_id``; this reference implementation accepts any
``bytes`` key.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any


def _canonical(row: dict[str, Any]) -> bytes:
    return json.dumps(
        {k: v for k, v in row.items() if k != "signature"},
        sort_keys=True,
        default=str,
        ensure_ascii=False,
    ).encode("utf-8")


def sign_row(row: dict[str, Any], *, key: bytes) -> str:
    """Compute HMAC-SHA256 hex digest over the row (excluding ``signature``)."""
    return hmac.new(key, _canonical(row), hashlib.sha256).hexdigest()


def verify_row(row: dict[str, Any], *, key: bytes) -> bool:
    """Constant-time verify a stored row's signature."""
    stored = row.get("signature")
    if not isinstance(stored, str) or not stored:
        return False
    recomputed = sign_row(row, key=key)
    return hmac.compare_digest(stored, recomputed)
