"""ISA-95 Equipment objects (EquipmentClass + Equipment)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

_ISA95_CONFIG = ConfigDict(extra="forbid")


class Isa95EquipmentClass(BaseModel):
    """Equipment class — a category of equipment with shared capabilities."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    description: str = ""
    capabilities: list[str] = Field(default_factory=list)


class Isa95Equipment(BaseModel):
    """A specific equipment instance — a concrete machine / instrument."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    equipment_class_id: str | None = Field(None, description="FK → Isa95EquipmentClass.id.")
    work_unit_id: str | None = Field(None, description="Where this equipment is hosted.")
    serial_number: str | None = None
    capabilities: list[str] = Field(default_factory=list)
