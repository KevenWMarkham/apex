"""AXLECML Equipment entity — Pattern C over ISA-95 Equipment."""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class EquipmentStatus(StrEnum):
    IN_SERVICE = "in_service"
    IDLE = "idle"
    SETUP = "setup"
    PRODUCING = "producing"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"
    RETIRED = "retired"


class Equipment(CanonicalEntity, ScdType2Fields):
    """A plant-floor asset participating in production."""

    isa95_id: str = Field(..., description="ISA-95 Equipment id.")
    name: str
    equipment_class_id: str | None = None
    work_unit_id: str | None = Field(
        None, description="ISA-95 WorkUnit this Equipment is hosted in."
    )
    work_center_key: str | None = Field(
        None, description="FK → AXLECML WorkCenter.entity_id."
    )
    serial_number: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    status: EquipmentStatus = EquipmentStatus.IN_SERVICE
    capabilities: list[str] = Field(default_factory=list)
