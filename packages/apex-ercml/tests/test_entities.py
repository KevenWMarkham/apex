"""Tests for ERCML entities."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from apex_ercml import (
    Asset,
    AssetLifecycleState,
    GridEvent,
    GridEventType,
    Meter,
    MeterKind,
    MeterReading,
    ReadingQuality,
    ReliabilityRecord,
    WorkOrder,
    WorkOrderStatus,
)
from apex_standards_iso14224 import (
    Iso14224EquipmentClass,
    Iso14224FailureMode,
)


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test",
        "source_system": "cim",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "abc",
    }


class TestMeter:
    def test_electricity_default(self) -> None:
        m = Meter(cim_mrid="mrid-1", serial_number="AMI-001",
                  **_envelope(), **_scd2())  # type: ignore[arg-type]
        assert m.kind is MeterKind.ELECTRICITY

    def test_gas_meter(self) -> None:
        m = Meter(cim_mrid="mrid-2", serial_number="GAS-001",
                  kind=MeterKind.GAS, **_envelope(), **_scd2())  # type: ignore[arg-type]
        assert m.kind is MeterKind.GAS


class TestMeterReading:
    def test_with_measured_quality(self) -> None:
        r = MeterReading(
            meter_key="meter:1", timestamp=datetime.now(UTC),
            value=Decimal("125.42"), unit="kWh",
            quality=ReadingQuality.MEASURED,
            **_envelope(),
        )  # type: ignore[arg-type]
        assert r.quality is ReadingQuality.MEASURED
        assert r.value == Decimal("125.42")


class TestGridEvent:
    def test_outage(self) -> None:
        ev = GridEvent(
            event_type=GridEventType.OUTAGE,
            occurred_start=datetime.now(UTC),
            severity=1,
            customers_affected=150,
            **_envelope(),
        )  # type: ignore[arg-type]
        assert ev.event_type is GridEventType.OUTAGE
        assert ev.severity == 1

    def test_rejects_bad_severity(self) -> None:
        with pytest.raises(ValidationError):
            GridEvent(
                event_type=GridEventType.OUTAGE,
                occurred_start=datetime.now(UTC),
                severity=99,
                **_envelope(),
            )  # type: ignore[arg-type]


class TestAsset:
    def test_lifecycle_default(self) -> None:
        a = Asset(cim_mrid="mrid-5", name="Transformer T1",
                  **_envelope(), **_scd2())  # type: ignore[arg-type]
        assert a.lifecycle_state is AssetLifecycleState.IN_SERVICE


class TestWorkOrder:
    def test_priority_bounds(self) -> None:
        wo = WorkOrder(
            work_order_number="WO-2026-0001",
            status=WorkOrderStatus.OPEN,
            priority=2,
            created=datetime.now(UTC),
            **_envelope(),
        )  # type: ignore[arg-type]
        assert wo.priority == 2


class TestReliabilityRecord:
    def test_minimal(self) -> None:
        rr = ReliabilityRecord(
            equipment_key="asset:1",
            equipment_class=Iso14224EquipmentClass.ELECTRIC_MOTOR,
            **_envelope(),
        )  # type: ignore[arg-type]
        assert rr.equipment_class is Iso14224EquipmentClass.ELECTRIC_MOTOR

    def test_with_failure(self) -> None:
        rr = ReliabilityRecord(
            equipment_key="asset:1",
            equipment_class=Iso14224EquipmentClass.TRANSFORMER,
            failure_mode=Iso14224FailureMode.OVERHEATING,
            downtime_hours=4.5,
            is_critical=True,
            **_envelope(),
        )  # type: ignore[arg-type]
        assert rr.failure_mode is Iso14224FailureMode.OVERHEATING
        assert rr.is_critical is True
