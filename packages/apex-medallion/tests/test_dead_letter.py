"""Tests for ``apex_medallion.bronze.dead_letter``."""

from __future__ import annotations

import re
from datetime import UTC, datetime

from apex_medallion import DeadLetterRecord, dead_letter_ddl


def test_record_minimal() -> None:
    r = DeadLetterRecord(
        source_system="oracle-retail",
        source_pattern="mirrored_database",
        target_table="bronze_scml.sku",
        occurred_at=datetime.now(UTC),
        error_class="ParseError",
        error_message="Column 'gtin' expected STRING, got INT",
    )
    assert r.retry_count == 0
    assert r.run_id is None


def test_ddl_includes_required_columns() -> None:
    ddl = dead_letter_ddl()
    for col in (
        "dead_letter_id", "source_system", "source_pattern",
        "target_table", "occurred_at", "error_class", "error_message",
        "retry_count", "payload_raw", "run_id",
    ):
        assert re.search(rf"\b{col}\b", ddl), f"missing column {col}"


def test_ddl_qualified_with_database() -> None:
    ddl = dead_letter_ddl(database="bronze_ops")
    assert "bronze_ops.bronze_raw_deadletter" in ddl


def test_ddl_partitioned_by_source_system() -> None:
    ddl = dead_letter_ddl()
    assert "PARTITIONED BY (source_system)" in ddl
