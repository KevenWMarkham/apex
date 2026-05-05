"""Tests for ``apex_schemas_common.ddl.generate_delta_ddl``."""

from __future__ import annotations

import re
from decimal import Decimal

from pydantic import Field

from apex_schemas_common import CanonicalEntity, generate_delta_ddl
from apex_schemas_common.standards import GTIN14


class _SKU(CanonicalEntity):
    sku_natural: str = Field(..., description="Source natural key.")
    gtin: GTIN14 | None = Field(None, description="GS1 GTIN-14.")
    unit_retail: Decimal | None = Field(None, description="Retail price.")
    case_pack: int | None = Field(None, description="Units per case.")
    is_active: bool = Field(True, description="Active flag.")
    tags: list[str] = Field(default_factory=list, description="Free-form tags.")


def _match(pattern: str, text: str) -> re.Match[str] | None:
    return re.search(pattern, text, re.MULTILINE)


def test_ddl_has_create_delta_skeleton() -> None:
    ddl = generate_delta_ddl(_SKU, database="silver_scml", partition_by=["is_active"])
    assert ddl.startswith("CREATE TABLE silver_scml._sku (")
    assert "USING DELTA" in ddl
    assert "PARTITIONED BY (is_active)" in ddl
    assert "TBLPROPERTIES" in ddl


def test_ddl_has_required_envelope_fields() -> None:
    ddl = generate_delta_ddl(_SKU)
    for field in ("event_id", "event_ts", "entity_id", "source_system", "source_system_ts"):
        assert field in ddl


def test_ddl_types_map_correctly() -> None:
    ddl = generate_delta_ddl(_SKU)
    assert _match(r"sku_natural\s+STRING NOT NULL", ddl)
    assert _match(r"gtin\s+STRING(?! NOT NULL)", ddl)  # GTIN14 collapses to STRING, nullable
    assert _match(r"unit_retail\s+DECIMAL\(18, 6\)", ddl)
    assert _match(r"case_pack\s+BIGINT", ddl)
    assert _match(r"is_active\s+BOOLEAN", ddl)
    assert _match(r"tags\s+ARRAY<STRING>", ddl)


def test_optional_fields_are_nullable() -> None:
    ddl = generate_delta_ddl(_SKU)
    # Required → NOT NULL
    assert _match(r"sku_natural\s+STRING NOT NULL", ddl)
    # Optional → not NOT NULL
    gtin_line = [line for line in ddl.splitlines() if "gtin" in line and "STRING" in line][0]
    assert "NOT NULL" not in gtin_line

