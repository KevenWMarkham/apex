"""Tests for ``BronzeLandingConfig`` + ``generate_bronze_ddl``."""

from __future__ import annotations

import re

import pytest
from pydantic import ValidationError

from apex_core.types import Classification, Practice
from apex_medallion import (
    BronzeLandingConfig,
    RetentionPolicy,
    SourcePattern,
    generate_bronze_ddl,
)


def _cfg(**overrides: object) -> BronzeLandingConfig:
    base: dict[str, object] = {
        "source_system": "oracle-retail",
        "source_pattern": SourcePattern.MIRRORED_DATABASE,
        "source_connection_name": "oracle-retail-mirror",
        "workspace_id": "ws-1",
        "lakehouse_id": "lh-1",
        "target_table": "bronze_scml.sku",
        "practice": Practice.RC,
    }
    base.update(overrides)
    return BronzeLandingConfig(**base)  # type: ignore[arg-type]


class TestConfig:
    def test_defaults(self) -> None:
        c = _cfg()
        assert c.partition_columns == ["ingest_date"]
        assert c.classification is Classification.INTERNAL
        assert c.max_retries == 3
        assert c.deadletter_table == "bronze_raw_deadletter"

    def test_rejects_invalid_max_retries(self) -> None:
        with pytest.raises(ValidationError):
            _cfg(max_retries=99)

    def test_accepts_pattern_detail(self) -> None:
        c = _cfg(pattern_detail={"mirror_item_id": "mi-42"})
        assert c.pattern_detail["mirror_item_id"] == "mi-42"

    def test_retention_for_hls(self) -> None:
        c = _cfg(
            practice=Practice.HLS,
            retention=RetentionPolicy.default_for_practice(Practice.HLS),
        )
        assert c.retention.duration_days == 10 * 365


class TestDdlGeneration:
    def test_skeleton(self) -> None:
        ddl = generate_bronze_ddl(_cfg())
        assert ddl.startswith("CREATE TABLE bronze_scml.sku")
        assert "USING DELTA" in ddl
        assert "PARTITIONED BY (ingest_date)" in ddl
        assert "'apex.medallion.layer' = 'bronze'" in ddl
        assert "'apex.source_system' = 'oracle-retail'" in ddl
        assert "'apex.source_pattern' = 'mirrored_database'" in ddl

    def test_envelope_columns_present(self) -> None:
        ddl = generate_bronze_ddl(_cfg())
        for col in (
            "event_id", "event_ts", "entity_id", "source_system", "source_system_ts",
            "ingest_ts", "ingest_date", "run_id", "_raw_payload", "_classification",
        ):
            assert re.search(rf"\b{col}\b", ddl), f"Bronze DDL missing {col}"

    def test_user_columns_injected(self) -> None:
        ddl = generate_bronze_ddl(
            _cfg(),
            user_columns={"sku_natural": "STRING", "gtin": "STRING"},
        )
        assert re.search(r"sku_natural\s+STRING", ddl)
        assert re.search(r"gtin\s+STRING", ddl)

    def test_database_prefix(self) -> None:
        ddl = generate_bronze_ddl(_cfg(), database="fabric_bronze")
        assert "CREATE TABLE fabric_bronze.bronze_scml.sku" in ddl
