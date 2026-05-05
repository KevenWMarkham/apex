"""Tests for CIM ↔ ERCML translators."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from apex_ercml import (
    AssetLifecycleState,
    GridEventType,
    MeterKind,
    ReadingQuality,
    WorkOrderStatus,
    asset_from_cim,
    asset_to_cim,
    grid_event_from_cim,
    meter_from_cim,
    meter_reading_from_cim,
    meter_to_cim,
    work_order_from_cim,
)
from apex_standards_cim import (
    CimAsset,
    CimEnergyEvent,
    CimMeter,
    CimMeterKind,
    CimReading,
    CimWorkOrder,
    DateTimeInterval,
    UnitSymbol,
)

pytestmark = pytest.mark.conformance


def _mrid() -> str:
    return str(uuid4())


class TestMeterRoundTrip:
    def test_forward(self) -> None:
        cim = CimMeter(
            m_rid=_mrid(),
            serial_number="AMI-00001",
            kind=CimMeterKind.ELECTRICITY,
            install_date=datetime(2026, 1, 1, tzinfo=UTC),
        )
        meter = meter_from_cim(cim)
        assert meter.kind is MeterKind.ELECTRICITY
        assert meter.serial_number == "AMI-00001"
        assert meter.cim_mrid == cim.m_rid

    def test_round_trip(self) -> None:
        cim = CimMeter(
            m_rid=_mrid(), serial_number="GAS-99",
            kind=CimMeterKind.GAS,
            install_date=datetime(2026, 1, 1, tzinfo=UTC),
            customer_mrid=_mrid(), location_mrid=_mrid(),
        )
        meter = meter_from_cim(cim)
        back = meter_to_cim(meter)
        assert back.m_rid == cim.m_rid
        assert back.serial_number == cim.serial_number
        assert back.kind is cim.kind
        assert back.customer_mrid == cim.customer_mrid
        assert back.location_mrid == cim.location_mrid


class TestReading:
    def test_from_cim_with_quality(self) -> None:
        cim = CimReading(
            meter_mrid=_mrid(),
            timestamp=datetime.now(UTC),
            value=Decimal("42.5"),
            unit=UnitSymbol.KWH,
            quality_flag="measured",
        )
        r = meter_reading_from_cim(cim, meter_key="meter:1")
        assert r.value == Decimal("42.5")
        assert r.quality is ReadingQuality.MEASURED
        assert r.unit == "kWh"

    def test_unknown_quality_falls_back_to_measured(self) -> None:
        cim = CimReading(
            meter_mrid=_mrid(), timestamp=datetime.now(UTC),
            value=Decimal("1"), unit=UnitSymbol.KWH,
            quality_flag="something-weird",
        )
        r = meter_reading_from_cim(cim, meter_key="meter:1")
        assert r.quality is ReadingQuality.MEASURED


class TestGridEvent:
    def test_outage_classified(self) -> None:
        cim = CimEnergyEvent(
            m_rid=_mrid(),
            event_type="outage",
            occurred=DateTimeInterval(start=datetime.now(UTC)),
            description="Feeder 42 lockout",
            severity=1,
        )
        ev = grid_event_from_cim(cim)
        assert ev.event_type is GridEventType.OUTAGE

    def test_unknown_event_type_falls_back(self) -> None:
        cim = CimEnergyEvent(
            m_rid=_mrid(),
            event_type="cosmic_ray_spike",
            occurred=DateTimeInterval(start=datetime.now(UTC)),
        )
        ev = grid_event_from_cim(cim)
        assert ev.event_type is GridEventType.OTHER


class TestAssetRoundTrip:
    def test_round_trip(self) -> None:
        cim = CimAsset(
            m_rid=_mrid(), name="Transformer T1",
            asset_type="PowerTransformer",
            in_service_date=datetime(2020, 6, 15, tzinfo=UTC),
            lifecycle_state="in_service",
        )
        asset = asset_from_cim(cim)
        assert asset.lifecycle_state is AssetLifecycleState.IN_SERVICE
        back = asset_to_cim(asset)
        assert back.m_rid == cim.m_rid
        assert back.name == cim.name
        assert back.asset_type == cim.asset_type


class TestWorkOrder:
    def test_open_status(self) -> None:
        cim = CimWorkOrder(
            m_rid=_mrid(),
            work_order_number="WO-001",
            status="open",
            priority=3,
            created=datetime.now(UTC),
            description="Inspect breaker.",
        )
        wo = work_order_from_cim(cim)
        assert wo.status is WorkOrderStatus.OPEN

    def test_unknown_status_falls_back(self) -> None:
        cim = CimWorkOrder(
            m_rid=_mrid(), work_order_number="WO-2",
            status="mysterious", created=datetime.now(UTC),
        )
        wo = work_order_from_cim(cim)
        assert wo.status is WorkOrderStatus.OPEN
