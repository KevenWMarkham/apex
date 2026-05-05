"""Tests for ISO 14224 taxonomy, failure modes, and ReliabilityRecord."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from apex_standards_iso14224 import (
    Iso14224EquipmentClass,
    Iso14224EquipmentSubclass,
    Iso14224FailureMechanism,
    Iso14224FailureMode,
    ReliabilityRecord,
)


class TestTaxonomy:
    def test_top_level_classes_cover_core(self) -> None:
        names = {c.value for c in Iso14224EquipmentClass}
        assert "pump" in names
        assert "compressor" in names
        assert "heat_exchanger" in names

    def test_subclasses_nest_under_classes(self) -> None:
        # Subclass enum is documentational only; this test catches typos
        names = {s.value for s in Iso14224EquipmentSubclass}
        assert "centrifugal_pump" in names
        assert "shell_and_tube" in names


class TestFailureTaxonomy:
    def test_core_failure_modes(self) -> None:
        values = {m.value for m in Iso14224FailureMode}
        for expected in ("leakage", "vibration", "fail_to_start"):
            assert expected in values

    def test_core_mechanisms(self) -> None:
        values = {m.value for m in Iso14224FailureMechanism}
        for expected in ("corrosion", "fatigue", "overload"):
            assert expected in values


@pytest.mark.conformance
class TestReliabilityRecord:
    def test_minimal(self) -> None:
        r = ReliabilityRecord(
            equipment_id="eq-42",
            equipment_class=Iso14224EquipmentClass.PUMP,
        )
        assert r.equipment_class is Iso14224EquipmentClass.PUMP
        assert r.failure_mode is None

    def test_full_event(self) -> None:
        t0 = datetime.now(UTC)
        r = ReliabilityRecord(
            equipment_id="eq-42",
            equipment_class=Iso14224EquipmentClass.PUMP,
            equipment_subclass=Iso14224EquipmentSubclass.CENTRIFUGAL_PUMP,
            failure_mode=Iso14224FailureMode.VIBRATION,
            failure_mechanism=Iso14224FailureMechanism.FATIGUE,
            detected_at=t0,
            repair_started_at=t0 + timedelta(hours=2),
            repair_completed_at=t0 + timedelta(hours=8),
            downtime_hours=6.0,
            cause_description="Bearing fatigue confirmed via vibration spectrum.",
            corrective_action="Replace bearing; re-balance impeller.",
            cost_usd=4200.0,
            is_critical=True,
        )
        assert r.downtime_hours == 6.0
        assert r.is_critical is True
        assert r.failure_mode is Iso14224FailureMode.VIBRATION

    def test_negative_downtime_rejected(self) -> None:
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            ReliabilityRecord(
                equipment_id="eq-1",
                equipment_class=Iso14224EquipmentClass.PUMP,
                downtime_hours=-1.0,
            )
