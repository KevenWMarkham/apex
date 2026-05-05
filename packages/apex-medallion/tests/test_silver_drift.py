"""Tests for ``apex_medallion.silver.drift``."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from apex_schemas_common import CanonicalEntity
from apex_medallion.silver import DriftReport, detect_drift, expected_columns


class _Widget(CanonicalEntity):
    widget_natural: str = Field(..., description="Natural key.")
    qty: int | None = None
    price: Decimal | None = None
    is_active: bool = True


class TestExpectedColumns:
    def test_includes_envelope(self) -> None:
        cols = expected_columns(_Widget)
        for env in ("event_id", "event_ts", "entity_id", "source_system", "source_system_ts"):
            assert env in cols

    def test_user_columns_typed(self) -> None:
        cols = expected_columns(_Widget)
        assert cols["widget_natural"] == "STRING"
        assert cols["qty"] == "BIGINT"
        assert cols["price"] == "DECIMAL(18, 6)"
        assert cols["is_active"] == "BOOLEAN"


class TestDetectDrift:
    def _actual_matching(self) -> dict[str, str]:
        return dict(expected_columns(_Widget))

    def test_no_drift(self) -> None:
        report = detect_drift(_Widget, self._actual_matching())
        assert report.clean
        assert "[OK]" in report.summary()

    def test_added_column_detected(self) -> None:
        actual = self._actual_matching()
        actual["new_field"] = "STRING"
        report = detect_drift(_Widget, actual)
        assert not report.clean
        assert "new_field" in report.added

    def test_removed_column_detected(self) -> None:
        actual = self._actual_matching()
        del actual["qty"]
        report = detect_drift(_Widget, actual)
        assert "qty" in report.removed

    def test_type_mismatch_detected(self) -> None:
        actual = self._actual_matching()
        actual["qty"] = "STRING"  # wrong type
        report = detect_drift(_Widget, actual)
        assert report.type_mismatches
        col, expected, got = report.type_mismatches[0]
        assert col == "qty"
        assert expected == "BIGINT"
        assert got == "STRING"

    def test_long_alias_accepted(self) -> None:
        actual = self._actual_matching()
        actual["qty"] = "LONG"  # Spark-ism for BIGINT
        report = detect_drift(_Widget, actual)
        assert not report.type_mismatches

    def test_summary_contains_counts(self) -> None:
        actual = self._actual_matching()
        actual["extra_col"] = "STRING"
        del actual["qty"]
        report = detect_drift(_Widget, actual)
        summary = report.summary()
        assert "[DRIFT]" in summary
        assert "1 added" in summary
        assert "1 removed" in summary
