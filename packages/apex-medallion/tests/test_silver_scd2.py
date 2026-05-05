"""Tests for ``apex_medallion.silver.scd2``."""

from __future__ import annotations

from datetime import UTC, datetime

from apex_medallion.silver import (
    Scd2Config,
    compute_row_hash,
    next_scd2_fields,
)


def _config() -> Scd2Config:
    return Scd2Config(
        key_columns=("sku_natural",),
        hashable_columns=("sku_natural", "status", "unit_price"),
    )


class TestComputeRowHash:
    def test_deterministic(self) -> None:
        cfg = _config()
        record = {"sku_natural": "sku-1", "status": "ACTIVE", "unit_price": "10.00"}
        h1 = compute_row_hash(record, cfg)
        h2 = compute_row_hash(record, cfg)
        assert h1 == h2

    def test_value_change_changes_hash(self) -> None:
        cfg = _config()
        a = {"sku_natural": "sku-1", "status": "ACTIVE", "unit_price": "10.00"}
        b = {"sku_natural": "sku-1", "status": "INACTIVE", "unit_price": "10.00"}
        assert compute_row_hash(a, cfg) != compute_row_hash(b, cfg)

    def test_none_values_stable(self) -> None:
        cfg = _config()
        record = {"sku_natural": "sku-1", "status": None, "unit_price": None}
        assert len(compute_row_hash(record, cfg)) == 64  # sha256 hex length

    def test_ignored_columns_dont_affect_hash(self) -> None:
        cfg = _config()
        base = {"sku_natural": "sku-1", "status": "ACTIVE", "unit_price": "10"}
        with_ignored = dict(base) | {"ingest_ts": "2026-01-01T00:00:00Z"}
        # ingest_ts is in ignore_columns but NOT in hashable_columns, so both
        # paths produce the same hash.
        assert compute_row_hash(base, cfg) == compute_row_hash(with_ignored, cfg)


class TestNextScd2Fields:
    def test_new_entity_first_write(self) -> None:
        cfg = _config()
        result = next_scd2_fields(
            incoming={"sku_natural": "sku-1", "status": "ACTIVE", "unit_price": "10.00"},
            existing=None,
            config=cfg,
            now=datetime(2026, 4, 20, 12, 0, tzinfo=UTC),
        )
        assert result is not None
        new_row = result["new_row"]
        assert new_row["scd2_is_current"] is True
        assert new_row["scd2_valid_to"] is None
        assert result["closed_row"] is None

    def test_same_content_is_noop(self) -> None:
        cfg = _config()
        incoming = {"sku_natural": "sku-1", "status": "ACTIVE", "unit_price": "10.00"}
        existing = {**incoming, "row_hash": compute_row_hash(incoming, cfg)}
        assert next_scd2_fields(incoming=incoming, existing=existing, config=cfg) is None

    def test_content_change_closes_and_opens(self) -> None:
        cfg = _config()
        now = datetime(2026, 4, 20, 12, 0, tzinfo=UTC)
        incoming = {"sku_natural": "sku-1", "status": "INACTIVE", "unit_price": "10.00"}
        existing = {
            "sku_natural": "sku-1", "status": "ACTIVE", "unit_price": "10.00",
            "row_hash": compute_row_hash(
                {"sku_natural": "sku-1", "status": "ACTIVE", "unit_price": "10.00"},
                cfg,
            ),
        }
        result = next_scd2_fields(incoming=incoming, existing=existing, config=cfg, now=now)
        assert result is not None
        assert result["closed_row"] is not None
        assert result["closed_row"]["scd2_valid_to"] == now
        assert result["closed_row"]["scd2_is_current"] is False
        assert result["new_row"]["scd2_valid_from"] == now
        assert result["new_row"]["row_hash"] != existing["row_hash"]
