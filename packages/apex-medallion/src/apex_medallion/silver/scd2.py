"""SCD Type 2 helpers — content hashing + next-state resolver."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class Scd2Config:
    """Configuration for an SCD Type 2 resolution step."""

    key_columns: tuple[str, ...]
    """Natural / surrogate key columns — the 'entity identity' columns."""

    hashable_columns: tuple[str, ...]
    """Columns whose values participate in ``row_hash``."""

    ignore_columns: frozenset[str] = frozenset({
        "event_id", "event_ts", "ingest_ts", "ingest_date", "run_id",
        "scd2_valid_from", "scd2_valid_to", "scd2_is_current", "row_hash",
    })
    """Columns explicitly excluded from ``row_hash`` even if named in ``hashable_columns``."""


def compute_row_hash(record: dict[str, Any], config: Scd2Config) -> str:
    """Compute a deterministic content hash over the SCD2-relevant columns.

    The hash is SHA-256 over a stable, ``|``-separated projection of the
    named hashable columns (minus ignored ones). ``None`` serialises as the
    literal string ``__NONE__``; values are ``str()`` cast for stability.
    """
    effective_cols = tuple(
        c for c in config.hashable_columns if c not in config.ignore_columns
    )
    payload = "|".join(
        "__NONE__" if record.get(col) is None else str(record.get(col))
        for col in effective_cols
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def next_scd2_fields(
    incoming: dict[str, Any],
    existing: dict[str, Any] | None,
    config: Scd2Config,
    *,
    now: datetime | None = None,
) -> dict[str, Any] | None:
    """Return the SCD2 field updates for ``incoming`` vs ``existing`` (if any).

    Args:
        incoming: The new source row (dict of column → value).
        existing: The currently-valid row for the same entity key(s), or None.
        config: SCD2 configuration.
        now: Override the timestamp (tests). Defaults to ``datetime.now(UTC)``.

    Returns:
        - ``None`` if ``existing`` has the same content-hash as ``incoming``
          (no-op; writing SCD2 history would be wasteful).
        - Otherwise a dict with ``scd2_valid_from``, ``scd2_valid_to``,
          ``scd2_is_current``, ``row_hash`` ready to stamp onto the new row
          (and onto the existing row, which closes out).
    """
    ts = now or datetime.now(UTC)
    incoming_hash = compute_row_hash(incoming, config)

    if existing is not None and existing.get("row_hash") == incoming_hash:
        return None

    return {
        "new_row": {
            "scd2_valid_from": ts,
            "scd2_valid_to": None,
            "scd2_is_current": True,
            "row_hash": incoming_hash,
        },
        "closed_row": (
            {
                "scd2_valid_to": ts,
                "scd2_is_current": False,
            }
            if existing is not None
            else None
        ),
    }
