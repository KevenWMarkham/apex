"""ISA-95 five-level hierarchy + validator.

Levels: Enterprise → Site → Area → WorkCenter → WorkUnit.

See ANSI/ISA-95.00.02 §5.3 (Role-Based Equipment Hierarchy).
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field

_ISA95_CONFIG = ConfigDict(extra="forbid")


class Isa95Enterprise(BaseModel):
    """Enterprise — top of the ISA-95 hierarchy."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    description: str = ""


class Isa95Site(BaseModel):
    """Site — a geographic location belonging to an enterprise."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    enterprise_id: str = Field(..., description="FK → Isa95Enterprise.id.")
    location: str | None = Field(None, description="Physical address or geographic label.")


class Isa95Area(BaseModel):
    """Area — a logical grouping within a site (e.g. packaging area, utilities)."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    site_id: str = Field(..., description="FK → Isa95Site.id.")
    description: str = ""


class Isa95WorkCenter(BaseModel):
    """WorkCenter — a collection of related work units within an area."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    area_id: str = Field(..., description="FK → Isa95Area.id.")
    description: str = ""


class Isa95WorkUnit(BaseModel):
    """WorkUnit — a single production-capable location (machine / cell)."""

    model_config = _ISA95_CONFIG
    id: str
    name: str
    work_center_id: str = Field(..., description="FK → Isa95WorkCenter.id.")
    equipment_class_id: str | None = Field(
        None, description="Optional link to an EquipmentClass."
    )


@dataclass(frozen=True, slots=True)
class HierarchyValidation:
    """Result of validating a collection of ISA-95 entities for FK integrity."""

    ok: bool
    errors: list[str]


def validate_hierarchy(
    *,
    enterprises: list[Isa95Enterprise] | None = None,
    sites: list[Isa95Site] | None = None,
    areas: list[Isa95Area] | None = None,
    work_centers: list[Isa95WorkCenter] | None = None,
    work_units: list[Isa95WorkUnit] | None = None,
) -> HierarchyValidation:
    """Validate parent / child FK integrity across a set of ISA-95 entities.

    Every child must reference a parent that exists in the supplied sets.
    Returns a :class:`HierarchyValidation` with ``ok`` and error details.
    """
    ent_ids = {e.id for e in enterprises or []}
    site_ids = {s.id for s in sites or []}
    area_ids = {a.id for a in areas or []}
    wc_ids = {w.id for w in work_centers or []}

    errors: list[str] = []

    for s in sites or []:
        if s.enterprise_id not in ent_ids:
            errors.append(
                f"Site {s.id!r} references unknown enterprise {s.enterprise_id!r}"
            )
    for a in areas or []:
        if a.site_id not in site_ids:
            errors.append(f"Area {a.id!r} references unknown site {a.site_id!r}")
    for w in work_centers or []:
        if w.area_id not in area_ids:
            errors.append(
                f"WorkCenter {w.id!r} references unknown area {w.area_id!r}"
            )
    for u in work_units or []:
        if u.work_center_id not in wc_ids:
            errors.append(
                f"WorkUnit {u.id!r} references unknown work center {u.work_center_id!r}"
            )

    return HierarchyValidation(ok=not errors, errors=errors)
