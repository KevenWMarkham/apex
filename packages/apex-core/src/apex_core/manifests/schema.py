"""Schema manifest — canonical entity declaration.

See ``docs/APEX - Design and Build/APEX_Design.md`` §5.5.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from apex_core.manifests.base import BaseManifest
from apex_core.types import Classification, ManifestName


class AttributeSpec(BaseModel):
    """A typed attribute on a canonical entity."""

    model_config = ConfigDict(extra="forbid")

    name: ManifestName
    data_type: str = Field(..., description="Canonical type (string/int/decimal/timestamp/...).")
    nullable: bool = False
    description: str = ""
    classification: Classification = Classification.INTERNAL
    enum: list[str] | None = Field(None, description="Allowed values for closed enums.")
    business_term: str | None = Field(
        None, description="Purview Unified Catalog glossary term binding."
    )


class RelationshipSpec(BaseModel):
    """A foreign-key link to another canonical entity."""

    model_config = ConfigDict(extra="forbid")

    name: ManifestName
    target_entity: ManifestName
    cardinality: Literal["1:1", "1:N", "N:1", "N:N"]
    temporal: bool = Field(False, description="Whether validity is time-bounded.")


class EntitySpec(BaseModel):
    """Specification of a single canonical entity within a SchemaManifest."""

    model_config = ConfigDict(extra="forbid")

    name: ManifestName
    natural_key: list[ManifestName]
    surrogate_key: ManifestName = "entity_id"
    attributes: list[AttributeSpec]
    pre_measures: list[AttributeSpec] = Field(default_factory=list)
    post_measures: list[AttributeSpec] = Field(default_factory=list)
    relationships: list[RelationshipSpec] = Field(default_factory=list)
    scd2: bool = Field(False, description="Maintain Slowly Changing Dimension Type 2 history.")
    classification: Classification = Classification.INTERNAL


class SchemaManifest(BaseManifest):
    """Canonical schema manifest — a family of related entities.

    Example: SCML (Supply Chain) is one SchemaManifest containing entities
    ``sku``, ``location``, ``lot``, ``shipment``, ``supplier``, ``item``.
    """

    kind: Literal["schema"] = "schema"
    family: ManifestName = Field(..., description="Schema family name (scml/merml/cxml/...).")
    entities: list[EntitySpec]
    standards: list[str] = Field(
        default_factory=list,
        description="Industry standards this schema aligns with (GS1, FHIR, ISA-95, ...).",
    )
