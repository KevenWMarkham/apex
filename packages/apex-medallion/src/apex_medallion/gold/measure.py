"""Measure definition + registry.

Every measure APEX ships is a first-class ``MeasureDefinition`` — owned,
versioned, typed to a target language (PySpark / T-SQL / KQL / DAX). Pre-
measures compute at Silver→Gold transform time; post-measures compute at
query time in Gold / semantic-model surfaces.

See ``APEX_Design.md`` §6.6.
"""

from __future__ import annotations

from enum import StrEnum

from apex_core.types import Classification
from pydantic import BaseModel, ConfigDict, Field


class MeasureKind(StrEnum):
    """Where a measure is computed."""

    PRE_MEASURE = "pre_measure"
    """Computed in the Silver→Gold transform; embodied as a Gold column."""

    POST_MEASURE = "post_measure"
    """Computed at query time in Gold / semantic model."""


class MeasureLanguage(StrEnum):
    """The target language for the measure's formula."""

    PYSPARK = "pyspark"
    TSQL = "tsql"
    KQL = "kql"
    DAX = "dax"


class MeasureDefinition(BaseModel):
    """A single measure, first-class governed artefact."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., min_length=1, description="Snake-case measure identifier.")
    kind: MeasureKind
    language: MeasureLanguage
    owner: str = Field(..., min_length=1)
    description: str = ""
    classification: Classification = Classification.INTERNAL
    formula: str = Field(
        ...,
        min_length=1,
        description="Language-specific expression. See language-specific generators.",
    )
    depends_on: list[str] = Field(
        default_factory=list,
        description="Source columns / measures this formula requires.",
    )
    consumer_map: list[str] = Field(
        default_factory=list,
        description="Agents / services that consume this measure.",
    )
    version: str = Field("1.0", description="Measure-level SemVer.")
    deprecated_from: str | None = Field(
        None,
        description=(
            "Set to the APEX version that deprecated this measure. Silver/"
            "Gold continue to emit until the removal window (2 quarters)."
        ),
    )


class MeasureRegistry:
    """In-memory registry of measures — one per Practice typically."""

    def __init__(self) -> None:
        """Initialise an empty name-to-measure index."""
        self._by_name: dict[str, MeasureDefinition] = {}

    def register(self, measure: MeasureDefinition) -> None:
        """Register a measure. Duplicate names are rejected."""
        if measure.name in self._by_name:
            raise ValueError(f"Measure {measure.name!r} already registered.")
        self._by_name[measure.name] = measure

    def register_many(self, measures: list[MeasureDefinition]) -> None:
        """Register each measure in order; stops at the first duplicate name (``ValueError``)."""
        for m in measures:
            self.register(m)

    def get(self, name: str) -> MeasureDefinition:
        """Look up a measure by name."""
        try:
            return self._by_name[name]
        except KeyError as exc:
            raise KeyError(f"Unknown measure {name!r}") from exc

    def list_by_kind(self, kind: MeasureKind) -> list[MeasureDefinition]:
        """Return measures of ``kind``, sorted by name."""
        return sorted(
            (m for m in self._by_name.values() if m.kind is kind),
            key=lambda m: m.name,
        )

    def list_by_language(self, language: MeasureLanguage) -> list[MeasureDefinition]:
        """Return measures written in ``language``, sorted by name."""
        return sorted(
            (m for m in self._by_name.values() if m.language is language),
            key=lambda m: m.name,
        )

    def __len__(self) -> int:
        """Return the number of registered measures."""
        return len(self._by_name)

    def __contains__(self, name: str) -> bool:
        """Return True if a measure named ``name`` is registered."""
        return name in self._by_name

    def names(self) -> list[str]:
        """Return all registered measure names, sorted."""
        return sorted(self._by_name)
