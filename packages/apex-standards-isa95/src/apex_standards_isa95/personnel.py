"""ISA-95 Personnel objects (PersonnelClass + Person)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

_ISA95_CONFIG = ConfigDict(extra="forbid")


class Isa95PersonnelClass(BaseModel):
    """Personnel class — defines a role / skill category."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    description: str = ""


class Isa95Person(BaseModel):
    """A specific person / operator with optional class + qualifications."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    personnel_class_id: str | None = Field(None, alias="personnelClassId")
    qualifications: list[str] = Field(default_factory=list)
