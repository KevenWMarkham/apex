"""Silver-transform helpers — tokenise classified fields + stamp SCD2 history.

These functions operate on Pydantic instances (one canonical row at a time).
The PySpark notebook template in ``notebooks/silver/transform_template.py``
maps them over a DataFrame via ``spark.udf.register`` or row-by-row collect.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TypeVar

from pydantic import BaseModel

from apex_medallion.silver.scd2 import Scd2Config, compute_row_hash

_ModelT = TypeVar("_ModelT", bound=BaseModel)


def tokenise_and_stamp(
    instance: _ModelT,
    *,
    source_system: str | None = None,
) -> _ModelT:
    """Apply the full Silver transform to a single Pydantic instance.

    1. Tokenise every classified field via apex-tokenizer's default service.
    2. (Caller is responsible for envelope fields — they should already be
       populated by the Bronze landing step or the caller.)

    If ``apex_tokenizer`` isn't installed, the instance is returned unchanged
    — preserves backward-compat for packages that haven't adopted the runtime.
    """
    try:
        from apex_tokenizer import tokenize_classified_fields
    except ImportError:  # pragma: no cover — only when apex-tokenizer absent
        return instance
    return tokenize_classified_fields(instance, source_system=source_system)


def add_scd2_fields_to_instance(
    instance: _ModelT,
    *,
    config: Scd2Config,
    existing_row_hash: str | None = None,
    now: datetime | None = None,
) -> _ModelT:
    """Stamp SCD2 fields onto a Pydantic instance.

    - Computes ``row_hash`` from the instance's dict.
    - If ``existing_row_hash`` matches the new hash, returns the instance
      unchanged (no-op — caller should skip writing this row).
    - Otherwise sets ``scd2_valid_from = now``, ``scd2_valid_to = None``,
      ``scd2_is_current = True``, ``row_hash = computed``.

    Returns the updated instance (or the input if it's a no-op).
    """
    ts = now or datetime.now(UTC)
    payload = instance.model_dump()
    new_hash = compute_row_hash(payload, config)

    if existing_row_hash is not None and existing_row_hash == new_hash:
        return instance

    return instance.model_copy(update={
        "scd2_valid_from": ts,
        "scd2_valid_to": None,
        "scd2_is_current": True,
        "row_hash": new_hash,
    })
