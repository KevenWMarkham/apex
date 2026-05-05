"""Tests for CIM IEC 61970 + IEC 61968 mirrors."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from apex_standards_cim import (
    CimAsset,
    CimCustomer,
    CimEnergyEvent,
    CimEquipment,
    CimLocation,
    CimMeter,
    CimReading,
    CimWorkOrder,
    DateTimeInterval,
    UnitSymbol,
)


class TestIec61970:
    def test_asset_location_linkage(self) -> None:
        loc = CimLocation(m_rid=str(uuid4()), name="Substation A", latitude=37.7, longitude=-122.4)
        asset = CimAsset(
            m_rid=str(uuid4()), name="Transformer T1",
            asset_type="PowerTransformer", location_mrid=loc.m_rid,
        )
        assert asset.location_mrid == loc.m_rid

    def test_equipment_in_service_defaults_true(self) -> None:
        eq = CimEquipment(m_rid=str(uuid4()), name="Breaker 123")
        assert eq.in_service is True

    def test_energy_event_severity_range(self) -> None:
        ev = CimEnergyEvent(
            m_rid=str(uuid4()),
            event_type="outage",
            occurred=DateTimeInterval(start=datetime.now(UTC)),
            severity=1,
        )
        assert ev.severity == 1

    def test_energy_event_rejects_bad_severity(self) -> None:
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            CimEnergyEvent(
                m_rid=str(uuid4()),
                event_type="outage",
                occurred=DateTimeInterval(start=datetime.now(UTC)),
                severity=99,
            )


class TestIec61968:
    def test_meter_with_default_kind(self) -> None:
        m = CimMeter(m_rid=str(uuid4()), serial_number="AMI-00001")
        assert m.kind.value == "electricity"

    def test_reading_with_unit(self) -> None:
        r = CimReading(
            meter_mrid=str(uuid4()),
            timestamp=datetime.now(UTC),
            value=Decimal("125.42"),
            unit=UnitSymbol.KWH,
        )
        assert r.unit is UnitSymbol.KWH
        assert r.value == Decimal("125.42")

    def test_customer_roundtrip(self) -> None:
        c = CimCustomer(m_rid=str(uuid4()), name="Acme Industrial", kind="industrial")
        assert c.kind == "industrial"

    def test_work_order_priority_bounds(self) -> None:
        wo = CimWorkOrder(
            m_rid=str(uuid4()),
            work_order_number="WO-2026-00042",
            status="open",
            priority=2,
            created=datetime.now(UTC),
        )
        assert wo.priority == 2


class TestSharedPrimitives:
    def test_unit_symbol_covers_energy(self) -> None:
        values = {u.value for u in UnitSymbol}
        assert "kWh" in values
        assert "MWh" in values

    def test_mrid_accepts_uuid_like_strings(self) -> None:
        # Validated via CimMeter which declares m_rid: MRID
        CimMeter(m_rid=str(uuid4()), serial_number="AMI-1")
