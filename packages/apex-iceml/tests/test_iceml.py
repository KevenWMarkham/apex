"""Tests for ICEML entities + AEMP translator."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from apex_iceml import (
    AempSnapshotInput,
    FleetMember,
    IceEquipment,
    IceEquipmentKind,
    MaintenanceKind,
    MaintenanceRecord,
    ServiceEvent,
    ServiceEventSeverity,
    TelemetryQuality,
    TelemetryReading,
    telemetry_reading_from_aemp,
)


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test",
        "source_system": "aemp",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "abc",
    }


class TestEquipment:
    def test_truck_with_vin(self) -> None:
        eq = IceEquipment(
            aemp_equipment_id="EQ-001",
            vin17="1HGCM82633A004352",
            serial_number="SN-00001",
            kind=IceEquipmentKind.TRUCK,
            make="Freightliner", model="Cascadia", model_year=2024,
            in_service_date=date(2024, 6, 1),
            **_envelope(), **_scd2(),
        )  # type: ignore[arg-type]
        assert eq.vin17 == "1HGCM82633A004352"

    def test_rejects_invalid_vin(self) -> None:
        with pytest.raises(ValidationError):
            IceEquipment(
                aemp_equipment_id="EQ-002",
                vin17="TOO_SHORT",
                serial_number="SN-2",
                **_envelope(), **_scd2(),
            )  # type: ignore[arg-type]


class TestTelemetry:
    def test_reading_with_gps(self) -> None:
        tr = TelemetryReading(
            equipment_key="equipment:EQ-001",
            captured_at=datetime.now(UTC),
            latitude=37.7749, longitude=-122.4194,
            engine_hours=Decimal("1234.5"),
            odometer_km=Decimal("187500"),
            fuel_level_pct=Decimal("45.0"),
            quality=TelemetryQuality.DECODED,
            **_envelope(),
        )  # type: ignore[arg-type]
        assert tr.fuel_level_pct == Decimal("45.0")

    def test_fuel_pct_bounds(self) -> None:
        with pytest.raises(ValidationError):
            TelemetryReading(
                equipment_key="equipment:EQ-001",
                captured_at=datetime.now(UTC),
                fuel_level_pct=Decimal("125"),
                **_envelope(),
            )  # type: ignore[arg-type]


class TestServiceEvent:
    def test_critical_with_spn(self) -> None:
        ev = ServiceEvent(
            equipment_key="equipment:EQ-001",
            occurred_at=datetime.now(UTC),
            oem_fault_code="P0300",
            j1939_spn=190,
            severity=ServiceEventSeverity.CRITICAL,
            description="Engine speed sensor out of range",
            **_envelope(),
        )  # type: ignore[arg-type]
        assert ev.severity is ServiceEventSeverity.CRITICAL


class TestMaintenance:
    def test_scheduled(self) -> None:
        mr = MaintenanceRecord(
            equipment_key="equipment:EQ-001",
            kind=MaintenanceKind.SCHEDULED,
            scheduled_at=datetime.now(UTC),
            work_description="500-hr service",
            parts_replaced=["oil_filter", "air_filter"],
            labor_hours=Decimal("2.5"),
            cost_usd=Decimal("425.00"),
            **_envelope(),
        )  # type: ignore[arg-type]
        assert mr.labor_hours == Decimal("2.5")
        assert "oil_filter" in mr.parts_replaced


class TestFleetMember:
    def test_active(self) -> None:
        fm = FleetMember(
            equipment_key="equipment:EQ-001",
            fleet_id="fleet-west",
            assigned_from=date(2026, 1, 1),
            **_envelope(),
        )  # type: ignore[arg-type]
        assert fm.is_active is True


@pytest.mark.conformance
class TestAempTranslator:
    def test_snapshot_to_reading(self) -> None:
        aemp = AempSnapshotInput(
            equipment_id="EQ-001",
            timestamp=datetime(2026, 4, 20, 10, 0, tzinfo=UTC),
            latitude=37.77, longitude=-122.42,
            engine_hours=Decimal("1234.5"),
            odometer_km=Decimal("187500"),
            fuel_level_pct=Decimal("45"),
        )
        tr = telemetry_reading_from_aemp(aemp, equipment_key="equipment:EQ-001")
        assert tr.equipment_key == "equipment:EQ-001"
        assert tr.engine_hours == Decimal("1234.5")
        assert tr.quality is TelemetryQuality.DECODED
