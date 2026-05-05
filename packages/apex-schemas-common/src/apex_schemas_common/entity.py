"""Canonical-entity base class + SCD Type 2 mixin.

Every APEX canonical Silver row inherits :class:`CanonicalEntity`. Entities
whose history must be tracked also mix in :class:`ScdType2Fields`.

See ``docs/APEX - Design and Build/APEX_Design.md`` §5.3, §6.4.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from apex_core.envelope import CanonicalEnvelope


class CanonicalEntity(CanonicalEnvelope):
    """Base class for every APEX canonical Silver entity.

    Inherits the five-field envelope (``event_id``, ``event_ts``, ``entity_id``,
    ``source_system``, ``source_system_ts``) and relaxes the envelope's
    ``frozen=True`` so subclasses may extend.

    Subclasses declare additional attributes as typed Pydantic fields, optionally
    :class:`typing.Annotated` with a :class:`apex_core.types.Classification`
    marker for DLP/Purview and with a
    :class:`apex_schemas_common.standards.types.StandardRef` marker for
    industry-standard identifier fields.
    """

    model_config = ConfigDict(extra="forbid")


class ScdType2Fields(BaseModel):
    """SCD Type 2 history fields for entities whose business change matters.

    Mix into an entity::

        class SKU(CanonicalEntity, ScdType2Fields): ...

    Semantics (APEX_Design §6.4):

    - ``scd2_valid_from`` — inclusive start of this row's validity.
    - ``scd2_valid_to`` — exclusive end; ``None`` if currently valid.
    - ``scd2_is_current`` — convenience flag matching ``scd2_valid_to is None``.
    - ``row_hash`` — content hash used for change detection.
    """

    model_config = ConfigDict(extra="forbid")

    scd2_valid_from: datetime = Field(
        ..., description="Inclusive start of this row's validity."
    )
    scd2_valid_to: datetime | None = Field(
        None, description="Exclusive end; None while currently valid."
    )
    scd2_is_current: bool = Field(
        True, description="True iff scd2_valid_to is None."
    )
    row_hash: Annotated[str, StringConstraints(min_length=1, max_length=128)] = Field(
        ..., description="Content hash for change detection."
    )
