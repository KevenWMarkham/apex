"""Unified Catalog registration emitter — Sprint 13 Task 13.5.

Generates Atlas v2 business-glossary terms (one per attribute carrying
a description) and cross-entity relationship payloads (foreign-key style
edges declared in canonical schemas).

Subtasks
--------
- **13.5.1** — business-glossary term registration per attribute
- **13.5.2** — cross-entity relationship registration

API references
--------------
- ``POST /api/atlas/v2/glossary``       — create glossary
- ``POST /api/atlas/v2/glossary/term``  — create term
- ``POST /api/atlas/v2/relationship``   — create relationship between entities

Cross-reference: Sellers Guide §8.8.5 Unified Catalog registration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GlossaryTerm:
    """One Atlas glossary term."""

    name: str
    """Display name. Convention: ``{Entity}.{Attribute}`` (e.g., ``SKU.unit_cost_token``)."""

    qualified_name: str
    """Globally unique identifier for the term inside the glossary."""

    short_description: str
    long_description: str = ""

    related_entity_qnames: tuple[str, ...] = ()
    """Entity qualified names this term annotates."""

    glossary_qname: str = "APEX@apex-glossary"

    def to_atlas(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "name": self.name,
            "qualifiedName": self.qualified_name,
            "shortDescription": self.short_description,
            "longDescription": self.long_description,
            "anchor": {
                "glossaryGuid": "",  # resolved at POST time
                "relationGuid": "",
                "displayText": self.glossary_qname,
            },
        }
        if self.related_entity_qnames:
            body["assignedEntities"] = [
                {"typeName": "apex_silver_attribute", "uniqueAttributes": {"qualifiedName": q}}
                for q in self.related_entity_qnames
            ]
        return body


@dataclass(frozen=True)
class GlossaryDef:
    """Top-level Atlas glossary container."""

    qualified_name: str = "APEX@apex-glossary"
    name: str = "APEX Business Glossary"
    short_description: str = (
        "APEX-canonical business terms keyed by Practice. Each term annotates one or more "
        "Silver / Gold entity attributes registered in Purview."
    )
    language: str = "English"
    usage: str = "Production"

    def to_atlas(self) -> dict[str, Any]:
        return {
            "qualifiedName": self.qualified_name,
            "name": self.name,
            "shortDescription": self.short_description,
            "language": self.language,
            "usage": self.usage,
        }


@dataclass(frozen=True)
class EntityRelationship:
    """One cross-entity relationship — Subtask 13.5.2."""

    relationship_type: str
    """Atlas relationshipDef name. APEX uses ``apex_fk`` and ``apex_join``."""

    end1_type: str
    end1_qualified_name: str
    end2_type: str
    end2_qualified_name: str

    cardinality: str = "N:1"
    """One of ``1:1``, ``1:N``, ``N:1``, ``N:M``."""

    label: str = ""

    def to_atlas(self) -> dict[str, Any]:
        return {
            "typeName": self.relationship_type,
            "end1": {
                "typeName": self.end1_type,
                "uniqueAttributes": {"qualifiedName": self.end1_qualified_name},
            },
            "end2": {
                "typeName": self.end2_type,
                "uniqueAttributes": {"qualifiedName": self.end2_qualified_name},
            },
            "attributes": {
                "cardinality": self.cardinality,
                "label": self.label,
            },
        }


# ---------------------------------------------------------------------------
# Emitters
# ---------------------------------------------------------------------------


def emit_glossary_def() -> dict[str, Any]:
    """Emit the top-level APEX glossary container payload."""
    return GlossaryDef().to_atlas()


def emit_glossary_terms_from_schema(schema: dict[str, Any]) -> list[GlossaryTerm]:
    """Emit one glossary term per attribute that has a ``description``.

    Args:
        schema: Parsed APEX schema YAML dict.

    Returns:
        List of :class:`GlossaryTerm` ready to POST to
        ``/api/atlas/v2/glossary/term``.
    """
    practice = schema.get("practice", "unknown")
    family = schema.get("family", schema.get("name", "unknown"))

    terms: list[GlossaryTerm] = []
    for entity in schema.get("entities", []) or []:
        entity_name = entity.get("name", "unknown")
        entity_qname = f"apex.{practice}.{family}.{entity_name}".lower()

        # Entity-level term
        if entity.get("description"):
            terms.append(
                GlossaryTerm(
                    name=entity_name,
                    qualified_name=f"{entity_qname}@apex-glossary",
                    short_description=entity["description"][:200],
                    long_description=entity["description"],
                    related_entity_qnames=(entity_qname,),
                )
            )

        for attr in entity.get("attributes", []) or []:
            attr_name = attr.get("name", "unknown")
            if attr.get("description"):
                attr_qname = f"{entity_qname}.{attr_name}".lower()
                terms.append(
                    GlossaryTerm(
                        name=f"{entity_name}.{attr_name}",
                        qualified_name=f"{attr_qname}@apex-glossary",
                        short_description=attr["description"][:200],
                        long_description=attr["description"],
                        related_entity_qnames=(attr_qname,),
                    )
                )

    return terms


def emit_relationships_from_schema(
    schema: dict[str, Any],
) -> list[EntityRelationship]:
    """Emit one EntityRelationship per declared schema relationship.

    APEX schemas declare ``relationships`` per entity:

    .. code-block:: yaml

        entities:
          - name: sku
            relationships:
              - name: supplier
                target_entity: supplier
                cardinality: N:1

    Each is emitted as an apex_fk relationship between the qualified names.
    """
    practice = schema.get("practice", "unknown")
    family = schema.get("family", schema.get("name", "unknown"))

    rels: list[EntityRelationship] = []
    for entity in schema.get("entities", []) or []:
        from_name = entity.get("name", "unknown")
        from_qname = f"apex.{practice}.{family}.{from_name}".lower()

        for rel in entity.get("relationships", []) or []:
            target = rel.get("target_entity", "unknown")
            target_qname = f"apex.{practice}.{family}.{target}".lower()
            rels.append(
                EntityRelationship(
                    relationship_type="apex_fk",
                    end1_type="apex_silver_table",
                    end1_qualified_name=from_qname,
                    end2_type="apex_silver_table",
                    end2_qualified_name=target_qname,
                    cardinality=rel.get("cardinality", "N:1"),
                    label=rel.get("name", ""),
                )
            )

    return rels


def emit_catalog_bundle(schema: dict[str, Any]) -> dict[str, Any]:
    """Emit the full catalog-registration bundle for one schema.

    Combines the glossary container, all glossary terms, and all
    cross-entity relationships into a single object that callers can
    iterate to make the appropriate POSTs to Atlas / Purview.
    """
    return {
        "glossary": emit_glossary_def(),
        "terms": [t.to_atlas() for t in emit_glossary_terms_from_schema(schema)],
        "relationships": [r.to_atlas() for r in emit_relationships_from_schema(schema)],
    }


def emit_relationship_typedefs() -> dict[str, Any]:
    """Emit Atlas v2 relationshipDef payload for APEX's two relationship types."""
    return {
        "enumDefs": [],
        "structDefs": [],
        "classificationDefs": [],
        "entityDefs": [],
        "businessMetadataDefs": [],
        "relationshipDefs": [
            {
                "category": "RELATIONSHIP",
                "name": "apex_fk",
                "description": "APEX foreign-key relationship between two Silver tables.",
                "typeVersion": "1.0",
                "relationshipCategory": "ASSOCIATION",
                "endDef1": {
                    "type": "apex_silver_table",
                    "name": "from",
                    "isContainer": False,
                    "cardinality": "SINGLE",
                },
                "endDef2": {
                    "type": "apex_silver_table",
                    "name": "to",
                    "isContainer": False,
                    "cardinality": "SINGLE",
                },
                "attributeDefs": [
                    {"name": "cardinality", "typeName": "string", "isOptional": False, "cardinality": "SINGLE"},
                    {"name": "label", "typeName": "string", "isOptional": True, "cardinality": "SINGLE"},
                ],
            },
            {
                "category": "RELATIONSHIP",
                "name": "apex_join",
                "description": "APEX semantic join between two Silver or Gold entities.",
                "typeVersion": "1.0",
                "relationshipCategory": "ASSOCIATION",
                "endDef1": {
                    "type": "apex_silver_table",
                    "name": "left",
                    "isContainer": False,
                    "cardinality": "SINGLE",
                },
                "endDef2": {
                    "type": "apex_silver_table",
                    "name": "right",
                    "isContainer": False,
                    "cardinality": "SINGLE",
                },
                "attributeDefs": [
                    {"name": "cardinality", "typeName": "string", "isOptional": False, "cardinality": "SINGLE"},
                    {"name": "label", "typeName": "string", "isOptional": True, "cardinality": "SINGLE"},
                ],
            },
        ],
    }
