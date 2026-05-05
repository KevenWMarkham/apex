"""ISO 8000-aligned data-quality metadata — Sprint 22 Task 22.6 (BL.P.154).

Every Silver row carries a :class:`DataQualityMetadata` block that scores the
six ISO-8000-recognized data-quality dimensions for the row. Downstream Gold
views, MCP tools, and agent-safe materializations propagate the block.

ISO 8000 part 61:2016 governs information and data quality management. APEX
implements the **dimension semantics in code only** — no ISO 8000 text is
redistributed (per workspace `LICENSE-ATTRIBUTION.md`).

Dimensions APEX scores (per Sellers Guide §6.7):

- **completeness** — fraction of required fields populated
- **consistency** — fraction of cross-field invariants satisfied
- **accuracy** — agreement with an authoritative reference (where one exists)
- **currency** — staleness measure (event_ts vs. ingest_ts)
- **provenance** — strength of source-system + transformation chain attestation
- **conformance** — agreement with bound canonical / industry-standard schema

Each score is a float in ``[0.0, 1.0]``. ``None`` means "not measured" — agents
must treat ``None`` as "unknown" and apply the appropriate HOTL escalation
when the score gates a downstream decision.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class QualityDimension(StrEnum):
    """The six ISO-8000-aligned dimensions APEX scores per row."""

    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"
    ACCURACY = "accuracy"
    CURRENCY = "currency"
    PROVENANCE = "provenance"
    CONFORMANCE = "conformance"


QualityScore = Annotated[float, Field(ge=0.0, le=1.0)]
"""A scalar in [0.0, 1.0]. None permitted at row level for "not measured"."""


class DataQualityMetadata(BaseModel):
    """ISO 8000-aligned per-row quality block.

    Embedded in :class:`apex_core.envelope.CanonicalEnvelope`. Every Silver
    row has it; Gold views inherit it; MCP tool outputs propagate it.
    """

    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)

    completeness: QualityScore | None = Field(
        default=None,
        description="Fraction of required fields populated, [0,1].",
    )
    consistency: QualityScore | None = Field(
        default=None,
        description="Fraction of cross-field invariants satisfied, [0,1].",
    )
    accuracy: QualityScore | None = Field(
        default=None,
        description="Agreement with authoritative reference where one exists, [0,1].",
    )
    currency: QualityScore | None = Field(
        default=None,
        description="Currency / freshness score: 1.0 = real-time, decays with staleness, [0,1].",
    )
    provenance: QualityScore | None = Field(
        default=None,
        description="Strength of source + transformation-chain attestation, [0,1].",
    )
    conformance: QualityScore | None = Field(
        default=None,
        description="Agreement with bound canonical / industry-standard schema, [0,1].",
    )

    iso8000_pinned_version: str = Field(
        default="8000-61:2016",
        description="ISO 8000 part:year APEX is pinned to.",
    )
    quality_assessed_at: datetime | None = Field(
        default=None,
        description="When this row's quality block was last computed.",
    )

    def composite_score(self) -> float | None:
        """Equal-weight mean of the six dimensions, ignoring ``None``.

        Returns ``None`` if no dimensions were measured.
        """
        scored = [
            v
            for v in (
                self.completeness,
                self.consistency,
                self.accuracy,
                self.currency,
                self.provenance,
                self.conformance,
            )
            if v is not None
        ]
        if not scored:
            return None
        return sum(scored) / len(scored)

    def is_fully_assessed(self) -> bool:
        """True iff every dimension was measured (no ``None``)."""
        return all(
            v is not None
            for v in (
                self.completeness,
                self.consistency,
                self.accuracy,
                self.currency,
                self.provenance,
                self.conformance,
            )
        )

    def degraded_dimensions(self, threshold: float = 0.7) -> list[QualityDimension]:
        """Return dimensions scoring below ``threshold`` (default 0.7).

        ``None``-scored dimensions are NOT considered degraded — they're
        unknown, surfaced via :meth:`is_fully_assessed`.
        """
        out: list[QualityDimension] = []
        pairs = [
            (QualityDimension.COMPLETENESS, self.completeness),
            (QualityDimension.CONSISTENCY, self.consistency),
            (QualityDimension.ACCURACY, self.accuracy),
            (QualityDimension.CURRENCY, self.currency),
            (QualityDimension.PROVENANCE, self.provenance),
            (QualityDimension.CONFORMANCE, self.conformance),
        ]
        for dim, score in pairs:
            if score is not None and score < threshold:
                out.append(dim)
        return out


QUALITY_FIELDS: frozenset[str] = frozenset(DataQualityMetadata.model_fields)
"""Field names DataQualityMetadata exposes; used by Silver-DDL validators."""
