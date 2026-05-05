"""AXLECML Genealogy entity — lot / serial traceability edge."""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class GenealogyDirection(StrEnum):
    FORWARD = "forward"      # parent (raw) → child (processed)
    REVERSE = "reverse"      # child (finished) → parent (raw input)


class Genealogy(CanonicalEntity):
    """A single traceability edge linking input material to output material / unit.

    A finished unit's full genealogy is the transitive closure of these edges;
    the edge-record shape keeps the write-path cheap and append-only.
    """

    parent_id: str = Field(..., description="Upstream lot / batch / unit identifier.")
    child_id: str = Field(..., description="Downstream lot / batch / unit identifier.")
    relationship: str = Field(
        "consumed_in",
        description="e.g. 'consumed_in', 'produced_by', 'assembled_into'.",
    )
    equipment_key: str | None = None
    quantity: float | None = None
    unit_of_measure: str | None = None
