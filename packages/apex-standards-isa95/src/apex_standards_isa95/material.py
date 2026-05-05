"""ISA-95 Material objects (MaterialClass + Material)."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

_ISA95_CONFIG = ConfigDict(extra="forbid")


class MaterialType(StrEnum):
    RAW = "raw"
    WORK_IN_PROCESS = "work_in_process"
    FINISHED = "finished"
    CONSUMABLE = "consumable"


class Isa95MaterialClass(BaseModel):
    """Material class — a category of materials sharing properties."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    description: str = ""


class Isa95Material(BaseModel):
    """A specific material — with type + optional class + unit of measure."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    material_class_id: str | None = Field(None, description="FK → Isa95MaterialClass.id.")
    material_type: MaterialType | None = None
    unit_of_measure: str | None = None
