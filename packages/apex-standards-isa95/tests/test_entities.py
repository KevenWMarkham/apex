"""Tests for ISA-95 personnel, equipment, and material entities."""

from __future__ import annotations

from apex_standards_isa95 import (
    Isa95Equipment,
    Isa95EquipmentClass,
    Isa95Material,
    Isa95MaterialClass,
    Isa95Person,
    Isa95PersonnelClass,
    MaterialType,
)


class TestPersonnel:
    def test_person_with_class(self) -> None:
        cls = Isa95PersonnelClass(id="pc-operator", name="Operator")
        p = Isa95Person(
            id="op1", name="Alice",
            personnelClassId=cls.id,
            qualifications=["fork-lift", "confined-space"],
        )
        assert p.personnel_class_id == "pc-operator"
        assert "fork-lift" in p.qualifications

    def test_person_without_class(self) -> None:
        p = Isa95Person(id="op2", name="Bob")
        assert p.personnel_class_id is None


class TestEquipment:
    def test_equipment_class_capabilities(self) -> None:
        ec = Isa95EquipmentClass(
            id="ec-conveyor", name="Conveyor",
            capabilities=["transport", "queue"],
        )
        assert len(ec.capabilities) == 2

    def test_equipment_binds_to_work_unit(self) -> None:
        eq = Isa95Equipment(
            id="eq1", name="Conveyor 001",
            equipment_class_id="ec-conveyor",
            work_unit_id="u1",
            serial_number="SN-12345",
        )
        assert eq.serial_number == "SN-12345"
        assert eq.work_unit_id == "u1"


class TestMaterial:
    def test_raw_material(self) -> None:
        mc = Isa95MaterialClass(id="mc-steel", name="Steel")
        m = Isa95Material(
            id="mat1", name="A36 Steel Plate",
            material_class_id=mc.id,
            material_type=MaterialType.RAW,
            unit_of_measure="kg",
        )
        assert m.material_type is MaterialType.RAW

    def test_all_material_types_enumerated(self) -> None:
        types = {t.value for t in MaterialType}
        assert types == {"raw", "work_in_process", "finished", "consumable"}
