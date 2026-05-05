"""Tests for ``apex_medallion.bronze.partitioning``."""

from __future__ import annotations

from apex_medallion import default_partition_columns


def test_default() -> None:
    assert default_partition_columns() == ["ingest_date"]


def test_recall_trace() -> None:
    cols = default_partition_columns(recall_trace=True)
    assert cols[0] == "lot_id"
    assert "ingest_date" in cols


def test_event_time() -> None:
    cols = default_partition_columns(event_time=True)
    assert cols[0] == "event_date"
    assert "ingest_date" in cols


def test_recall_overrides_event_time() -> None:
    cols = default_partition_columns(recall_trace=True, event_time=True)
    assert cols[0] == "lot_id"
