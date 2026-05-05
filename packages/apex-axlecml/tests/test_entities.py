"""Tests for AXLECML entities."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from apex_axlecml import (
    AxleReliabilityRecord,
    BillOfMaterials,
    BomLine,
    Equipment,
    EquipmentStatus,
    Genealogy,
    J1939Signal,
    ProductionEvent,
    ProductionEventType,
    QualityResult,
    QualityStatus,
    WorkCenter,
)
from apex_standards_iso14224 import Iso14224EquipmentClass


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test",
        "source_system": "isa95",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "abc",
    }


def test_equipment_status_default() -> None:
    eq = Equipment(isa95_id="EQ1", name="CNC Lathe 01",
                   **_envelope(), **_scd2())  # type: ignore[arg-type]
    assert eq.status is EquipmentStatus.IN_SERVICE


def test_work_center() -> None:
    wc = WorkCenter(isa95_id="WC1", name="Assembly Line A", area_id="AREA-1",
                    **_envelope(), **_scd2())  # type: ignore[arg-type]
    assert wc.active is True


def test_production_event_batch_start() -> None:
    ev = ProductionEvent(
        event_type=ProductionEventType.BATCH_START,
        equipment_key="equipment:EQ1",
        batch_id="BATCH-0042",
        occurred_at=datetime.now(UTC),
        **_envelope(),
    )  # type: ignore[arg-type]
    assert ev.event_type is ProductionEventType.BATCH_START


def test_quality_result_pass_fail() -> None:
    qr = QualityResult(
        test_code="TENSILE",
        batch_id="B-1", measured_at=datetime.now(UTC),
        measurement_value=Decimal("550"),
        target_value=Decimal("500"),
        upper_limit=Decimal("600"),
        status=QualityStatus.PASS,
        **_envelope(),
    )  # type: ignore[arg-type]
    assert qr.status is QualityStatus.PASS


def test_genealogy_edge() -> None:
    g = Genealogy(
        parent_id="lot:raw-001",
        child_id="unit:finished-042",
        relationship="consumed_in",
        quantity=2.5, unit_of_measure="kg",
        **_envelope(),
    )  # type: ignore[arg-type]
    assert g.quantity == 2.5


def test_bom_header_and_lines() -> None:
    bom = BillOfMaterials(
        product_id="PROD-1", version="1.2",
        description="Widget v1.2",
        **_envelope(), **_scd2(),
    )  # type: ignore[arg-type]
    line = BomLine(
        bom_id=bom.entity_id,
        parent_product_id="PROD-1",
        child_product_id="COMP-A",
        quantity=Decimal("2"),
        **_envelope(),
    )  # type: ignore[arg-type]
    assert line.quantity == Decimal("2")


def test_bom_line_rejects_zero_quantity() -> None:
    with pytest.raises(ValidationError):
        BomLine(
            bom_id="bom:1",
            parent_product_id="P",
            child_product_id="C",
            quantity=Decimal("0"),
            **_envelope(),
        )  # type: ignore[arg-type]


def test_j1939_signal() -> None:
    sig = J1939Signal(
        spn=190, pgn=61444, signal_name="Engine Speed",
        value=Decimal("1800.0"), unit="rpm",
        equipment_key="equipment:EQ-truck-01",
        captured_at=datetime.now(UTC),
        **_envelope(),
    )  # type: ignore[arg-type]
    assert sig.spn == 190


def test_reliability_record() -> None:
    rr = AxleReliabilityRecord(
        equipment_key="equipment:EQ1",
        equipment_class=Iso14224EquipmentClass.GEARBOX,
        downtime_hours=3.5,
        production_impact_units=42,
        **_envelope(),
    )  # type: ignore[arg-type]
    assert rr.production_impact_units == 42
