"""Tests for ISA-95 → AXLECML and J1939 → AXLECML translators."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from apex_axlecml import (
    Equipment,
    EquipmentStatus,
    J1939Signal,
    equipment_from_isa95,
    j1939_signal_from_frame,
)
from apex_standards_isa95 import Isa95Equipment
from apex_standards_j1939 import CanFrame

pytestmark = pytest.mark.conformance


def test_equipment_from_isa95_basic() -> None:
    isa = Isa95Equipment(
        id="EQ-100", name="CNC Lathe",
        equipment_class_id="ec-cnc",
        work_unit_id="WU-1",
        serial_number="SN-12345",
        capabilities=["turning", "facing"],
    )
    eq = equipment_from_isa95(isa, work_center_key="wc:42")
    assert isinstance(eq, Equipment)
    assert eq.isa95_id == "EQ-100"
    assert eq.work_unit_id == "WU-1"
    assert eq.work_center_key == "wc:42"
    assert eq.status is EquipmentStatus.IN_SERVICE
    assert "turning" in eq.capabilities


def test_j1939_signal_from_frame_with_known_spn() -> None:
    frame = CanFrame(
        pgn=61444, source_address=0, priority=3,
        data=b"\x00\x00\x00\x00\x00\x00\x00\x00",
        timestamp=datetime.now(UTC),
    )
    sig = j1939_signal_from_frame(
        frame, spn=190, value=Decimal("1800.0"),
        equipment_key="equipment:truck-01",
    )
    assert isinstance(sig, J1939Signal)
    assert sig.spn == 190
    assert sig.signal_name == "Engine Speed"
    assert sig.unit == "rpm"
    assert sig.equipment_key == "equipment:truck-01"


def test_j1939_signal_from_frame_unknown_spn_falls_back_to_generic() -> None:
    frame = CanFrame(
        pgn=0xFFFF, source_address=0,
        data=b"",
        timestamp=datetime.now(UTC),
    )
    sig = j1939_signal_from_frame(frame, spn=999999, value=Decimal("0"))
    assert sig.signal_name == "SPN-999999"
    assert sig.unit == ""
