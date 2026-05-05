"""Tests for the T-SQL / KQL / Direct Lake generators."""

from __future__ import annotations

import re

from pydantic import Field

from apex_medallion.gold import (
    MeasureDefinition,
    MeasureKind,
    MeasureLanguage,
    SemanticModelSpec,
    TableSpec,
    generate_kql_function,
    generate_warehouse_view,
    render_tmdl,
)
from apex_medallion.gold.rc_measures import (
    EFFECTIVE_MARGIN_PCT,
    PERIOD_OVER_PERIOD_PCT_DAX,
    RECENT_EVENTS_KQL,
    ROLLING_AVG_14_DAY_TSQL,
)
from apex_medallion.gold.warehouse import view_definition_sha
from apex_schemas_common import CanonicalEntity


class _Widget(CanonicalEntity):
    widget_natural: str = Field(..., description="Natural key.")
    on_hand_qty: int | None = None


class TestWarehouseView:
    def test_minimal(self) -> None:
        ddl = generate_warehouse_view(
            _Widget,
            view_name="v_widget",
            silver_table="silver_rc.widget",
        )
        assert ddl.startswith("CREATE OR ALTER VIEW gold.v_widget AS")
        assert "FROM silver_rc.widget" in ddl
        assert "widget_natural" in ddl
        assert "_classification" in ddl

    def test_with_tsql_measure(self) -> None:
        ddl = generate_warehouse_view(
            _Widget,
            view_name="v_widget",
            silver_table="silver_rc.widget",
            measures=[ROLLING_AVG_14_DAY_TSQL],
        )
        assert "rolling_avg_14_day" in ddl
        assert re.search(r"AVG\(base_metric\) OVER", ddl)

    def test_filters_non_tsql_measures(self) -> None:
        ddl = generate_warehouse_view(
            _Widget,
            view_name="v_widget",
            silver_table="silver_rc.widget",
            measures=[PERIOD_OVER_PERIOD_PCT_DAX, ROLLING_AVG_14_DAY_TSQL, RECENT_EVENTS_KQL],
        )
        # Only the TSQL measure ends up in the view.
        assert "rolling_avg_14_day" in ddl
        assert "period_over_period_pct" not in ddl
        assert "events_last_15_min" not in ddl

    def test_sha_is_stable(self) -> None:
        ddl = generate_warehouse_view(
            _Widget, view_name="v_widget", silver_table="silver_rc.widget",
        )
        a = view_definition_sha(ddl)
        b = view_definition_sha(ddl)
        assert a == b
        assert len(a) == 64


class TestKqlFunction:
    def test_minimal(self) -> None:
        kql = generate_kql_function(
            _Widget,
            function_name="fn_widget",
            silver_table="silver_rc_widget",
        )
        assert kql.startswith(".create-or-alter function fn_widget()")
        assert "silver_rc_widget" in kql
        assert "| project" in kql

    def test_with_kql_measure(self) -> None:
        kql = generate_kql_function(
            _Widget,
            function_name="fn_widget",
            silver_table="silver_rc_widget",
            measures=[RECENT_EVENTS_KQL],
        )
        assert "events_last_15_min" in kql
        assert "bin(event_ts, 15m)" in kql

    def test_filters_non_kql_measures(self) -> None:
        kql = generate_kql_function(
            _Widget,
            function_name="fn_widget",
            silver_table="silver_rc_widget",
            measures=[ROLLING_AVG_14_DAY_TSQL, PERIOD_OVER_PERIOD_PCT_DAX, RECENT_EVENTS_KQL],
        )
        assert "events_last_15_min" in kql
        assert "rolling_avg_14_day" not in kql
        assert "period_over_period_pct" not in kql


class TestDirectLakeSpec:
    def test_render_tmdl_structure(self) -> None:
        spec = SemanticModelSpec(
            model_name="RcSemanticModel",
            tables=(
                TableSpec(
                    name="Widget",
                    silver_delta_path="onelake://silver/rc/widget",
                    columns=("widget_natural", "on_hand_qty"),
                    measures=(PERIOD_OVER_PERIOD_PCT_DAX,),
                ),
            ),
            notes="Sprint 6 anchor.",
        )
        tmdl = render_tmdl(spec)
        assert "model RcSemanticModel" in tmdl
        assert "table Widget" in tmdl
        assert "source onelake://silver/rc/widget" in tmdl
        assert "measure period_over_period_pct" in tmdl
        assert "-- Sprint 6 anchor." in tmdl

    def test_dax_only_measures_in_model(self) -> None:
        spec = SemanticModelSpec(
            model_name="Mixed",
            tables=(
                TableSpec(
                    name="Widget",
                    silver_delta_path="onelake://x/y",
                    columns=("a",),
                    measures=(PERIOD_OVER_PERIOD_PCT_DAX, RECENT_EVENTS_KQL),
                ),
            ),
        )
        # Only DAX measures counted
        assert spec.total_measures() == 1

    def test_empty_model_renders(self) -> None:
        spec = SemanticModelSpec(model_name="Empty", tables=())
        tmdl = render_tmdl(spec)
        assert "model Empty" in tmdl


class TestMeasureLanguageExclusivity:
    def test_pre_measure_formula_uses_f_col(self) -> None:
        # Pre-measures are PySpark — formula should reference F.col
        assert "F.col(" in EFFECTIVE_MARGIN_PCT.formula
