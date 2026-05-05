"""Canonical envelope enforced on every Silver row.

The envelope is the universal primary-key + provenance + quality contract
that makes cross-entity joins, temporal analysis, and quality-aware
downstream filtering possible regardless of schema family.

See ``docs/APEX - Design and Build/APEX_Design.md`` §5.3 (envelope fields)
and `apex_core.quality` for the ISO-8000-aligned `DataQualityMetadata`
attached at the envelope level (Sprint 22 Task 22.6, BL.P.154).
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from apex_core.quality import DataQualityMetadata


class CanonicalEnvelope(BaseModel):
    """Universal envelope on every canonical Silver row.

    Silver tables *must* include every field in this model. Downstream Gold
    views, MCP tool outputs, and agent-safe views inherit these fields as-is.

    Sprint 22 Task 22.6 added :attr:`quality` (ISO 8000-aligned
    :class:`DataQualityMetadata`). The field defaults to a fresh empty
    :class:`DataQualityMetadata` (all dimensions ``None``) so existing
    callers keep working — assessors populate dimensions as they're
    measured.
    """

    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)

    event_id: UUID = Field(
        ...,
        description="Unique event identifier (UUID).",
    )
    event_ts: datetime = Field(
        ...,
        description="When the event occurred (source system timestamp).",
    )
    entity_id: Annotated[str, StringConstraints(min_length=1, max_length=255)] = Field(
        ...,
        description="Canonical entity key (surrogate + natural compound).",
    )
    source_system: Annotated[str, StringConstraints(min_length=1, max_length=80)] = Field(
        ...,
        description="Which SOR emitted this row.",
    )
    source_system_ts: datetime = Field(
        ...,
        description="Source system's timestamp (for audit and change detection).",
    )
    quality: DataQualityMetadata = Field(
        default_factory=DataQualityMetadata,
        description=(
            "ISO 8000-aligned per-row data quality scores. Defaults to "
            "an empty (all-None) block — assessors populate dimensions "
            "as they're measured. Sprint 22 Task 22.6 / BL.P.154."
        ),
    )


ENVELOPE_FIELDS: frozenset[str] = frozenset(CanonicalEnvelope.model_fields)
"""The names of the envelope fields, used by Silver-DDL validators.

As of Sprint 22 Task 22.6, includes ``quality`` alongside the original
five (event_id / event_ts / entity_id / source_system / source_system_ts).
"""

CORE_ENVELOPE_FIELDS: frozenset[str] = frozenset({
    "event_id", "event_ts", "entity_id", "source_system", "source_system_ts",
})
"""The pre-Sprint-22 five core fields. Used where downstream code wants to
distinguish provenance fields from the quality block."""
