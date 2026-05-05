"""Content-addressed I/O store (Section 11.3, BL.P.82).

Inputs and tool-call results are hashed and stored by their content hash.
The audit row carries only the hash reference (``inputs_ref``, ``result_hash``)
- the actual payload lives in the Gold immutable store and is resolved on
demand by auditors.

This is the in-memory reference implementation; production wires it to a
Delta-backed store with retention + WORM policy.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def content_hash(payload: Any) -> str:
    """Return ``sha256:<hex>`` for a JSON-serialisable payload.

    Canonicalised via ``json.dumps(..., sort_keys=True)`` so semantically
    equal payloads hash identically.
    """
    blob = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False)
    digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


class ContentAddressedStore:
    """Append-once, read-many store keyed by ``content_hash``."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def put(self, payload: Any) -> str:
        h = content_hash(payload)
        if h in self._store:
            # Same hash -> same content (by definition). Idempotent.
            return h
        self._store[h] = payload
        return h

    def get(self, ref: str) -> Any:
        if ref not in self._store:
            raise KeyError(f"No payload for content ref {ref!r}")
        return self._store[ref]

    def __contains__(self, ref: str) -> bool:
        return ref in self._store

    def __len__(self) -> int:
        return len(self._store)
