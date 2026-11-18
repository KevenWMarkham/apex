"""AXLECML WorkCenter entity — Pattern C over ISA-95 WorkCenter."""

from __future__ import annotations

from apex_schemas_common import CanonicalEntity, ScdType2Fields
from pydantic import Field


class WorkCenter(CanonicalEntity, ScdType2Fields):
    """A group of related work units (production cell / line)."""

    isa95_id: str = Field(..., description="ISA-95 WorkCenter id.")
    name: str
    area_id: str = Field(..., description="ISA-95 Area this work center belongs to.")
    site_id: str | None = Field(None, description="Convenience; parent Area's Site.")
    description: str = ""
    active: bool = True
