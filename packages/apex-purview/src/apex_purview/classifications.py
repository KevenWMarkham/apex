"""Purview classification emitter.

Reads APEX canonical schema YAMLs and emits Microsoft Purview /
Apache Atlas v2 API payloads for:

1. **Classification type-defs** — `POST /api/atlas/v2/types/typedefs` body
   declaring the classifications APEX uses (trade_secret, pii, phi, pci,
   restricted, etc.).
2. **Entity classification attachments** — per-entity
   `PUT /api/atlas/v2/entity/guid/{guid}/classifications` body listing
   the classifications that apply to a registered entity or attribute.

Canonical schema input shape (per Sprint 2 apex-scml, apex-merml, apex-cxml):

```yaml
kind: schema
name: scml
version: 1.0.0
practice: rc
family: scml
entities:
  - name: sku
    classification: internal         # entity-level classification
    attributes:
      - name: sku_natural
        data_type: string
      - name: unit_cost_token
        data_type: string
        classification: trade_secret  # attribute-level classification
```

The emitter handles:
- Unique collection of classifications referenced in the schema.
- APEX-prefixed Purview classification type names (e.g. ``APEX.TradeSecret``).
- Round-trip-safe emission: running the emitter twice produces the same bytes.
- Conformance with the Atlas v2 type-def schema subset Purview accepts.

Sprint 13 Task 13.1.1. Source of truth: Sellers Guide §8.8 and §9.11.7.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Canonical APEX classifications
# ---------------------------------------------------------------------------

#: Canonical APEX classification set. Every classification an APEX schema
#: declares must map to one of these keys. Adding a new classification
#: is a MAJOR bump of apex-core conventions per ``schema-versioning.md``.
APEX_CLASSIFICATIONS: dict[str, dict[str, str]] = {
    "public": {
        "type_name": "APEX.Public",
        "description": (
            "Public data. No DLP or access restrictions. Published assets, "
            "public filings, marketing artifacts."
        ),
    },
    "internal": {
        "type_name": "APEX.Internal",
        "description": (
            "Internal enterprise data. Not PII, not trade-secret, not "
            "regulator-restricted. Default for most Silver/Gold columns."
        ),
    },
    "trade_secret": {
        "type_name": "APEX.TradeSecret",
        "description": (
            "Trade-secret / commercially sensitive data — pricing rules, "
            "supplier cost, assortment strategy, vendor contracts. DLP blocks "
            "external sharing; masking in cross-category views."
        ),
    },
    "pii": {
        "type_name": "APEX.PII",
        "description": (
            "Personally Identifiable Information. Name, email, phone, "
            "address, device IDs. Tokenized at Silver; PIM-gated detokenization."
        ),
    },
    "phi": {
        "type_name": "APEX.PHI",
        "description": (
            "Protected Health Information (HIPAA §164). Patient, encounter, "
            "clinical observation, claim. Tokenized; break-glass gated; "
            "10-year retention minimum."
        ),
    },
    "pci": {
        "type_name": "APEX.PCI",
        "description": (
            "Payment Card Industry data. Never in Gold; tokenized reference "
            "only; PCI DSS Requirement 10 audit applies."
        ),
    },
    "genetic": {
        "type_name": "APEX.Genetic",
        "description": (
            "Genetic / hereditary data (GINA). Stricter scope than PHI; "
            "separate consent; no pooled views."
        ),
    },
    "behavioral_health": {
        "type_name": "APEX.BehavioralHealth",
        "description": (
            "Substance use / psychiatric data (42 CFR Part 2). "
            "Double-consent; separate token vault; tighter retention."
        ),
    },
    "restricted": {
        "type_name": "APEX.Restricted",
        "description": (
            "Restricted-regulatory data — recall records, FSMA 204 "
            "provenance, NERC CIP BES Cyber Systems, 21 CFR Part 11 records. "
            "Retention-locked; every access audit-rowed."
        ),
    },
    "cpni": {
        "type_name": "APEX.CPNI",
        "description": (
            "Customer Proprietary Network Information (FCC §222). "
            "Purpose-tagged access; TEL-specific governance."
        ),
    },
    "member_only": {
        "type_name": "APEX.MemberOnly",
        "description": (
            "Loyalty-member-scoped data — reward balances, tier-earned "
            "offers, member-exclusive pricing. Agent access scoped to "
            "loyalty-authorized roles; never exposed to non-member-scoped "
            "analytics."
        ),
    },
    "export_controlled": {
        "type_name": "APEX.ExportControlled",
        "description": (
            "ITAR / EAR export-controlled data. Nation-of-residence gating; "
            "restricted cross-border flow."
        ),
    },
}


# ---------------------------------------------------------------------------
# Data classes for emitted payloads
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ClassificationDef:
    """One Purview / Atlas classificationDef entry.

    Emitted as a member of ``{"classificationDefs": [...]}`` for the
    Atlas ``POST /api/atlas/v2/types/typedefs`` endpoint.
    """

    type_name: str
    description: str
    super_types: tuple[str, ...] = ()
    #: APEX-specific attributes attached to the classification. Used when
    #: classifications need propagation metadata (e.g. ``retention_years``).
    attributes: tuple[dict[str, Any], ...] = ()

    def to_atlas(self) -> dict[str, Any]:
        """Return the Atlas-v2 wire payload for this classification."""
        return {
            "category": "CLASSIFICATION",
            "name": self.type_name,
            "description": self.description,
            "typeVersion": "1.0",
            "superTypes": list(self.super_types),
            "entityTypes": [],
            "attributeDefs": list(self.attributes),
        }


@dataclass(frozen=True)
class ClassificationAttachment:
    """One classification attached to an entity or attribute.

    Emitted as a member of the array body for
    ``PUT /api/atlas/v2/entity/guid/{guid}/classifications``.
    """

    type_name: str
    #: APEX-qualified name for the target: e.g. ``apex.rc.scml.sku`` or
    #: ``apex.rc.scml.sku.unit_cost_token``. Callers resolve qualified names
    #: to Purview GUIDs via a separate resolver.
    qualified_name: str
    attributes: dict[str, Any] = field(default_factory=dict)
    propagate: bool = True
    remove_propagations_on_entity_delete: bool = True

    def to_atlas(self) -> dict[str, Any]:
        """Return the Atlas-v2 wire payload for this attachment."""
        return {
            "typeName": self.type_name,
            "attributes": dict(self.attributes),
            "propagate": self.propagate,
            "removePropagationsOnEntityDelete": self.remove_propagations_on_entity_delete,
            "entityQualifiedName": self.qualified_name,
        }


# ---------------------------------------------------------------------------
# Enumeration
# ---------------------------------------------------------------------------


def enumerate_classifications(schema: dict[str, Any]) -> set[str]:
    """Return the set of classification keys referenced in a schema document.

    Classifications appear at entity level and at attribute level. The
    return value is the **set of keys** (e.g., ``{"internal", "trade_secret"}``),
    not the full classification metadata. Use :func:`emit_classification_typedefs`
    to emit the corresponding Atlas definitions.
    """
    keys: set[str] = set()
    for entity in schema.get("entities", []) or []:
        if "classification" in entity:
            keys.add(_normalize_key(entity["classification"]))
        for attr in entity.get("attributes", []) or []:
            if "classification" in attr:
                keys.add(_normalize_key(attr["classification"]))
    return keys


def _normalize_key(raw: str) -> str:
    """Normalize a classification key: lowercase, replace ' ' and '-' with '_'.

    Accepts ``"Trade Secret"`` / ``"trade-secret"`` / ``"trade_secret"`` —
    all collapse to ``"trade_secret"``.
    """
    return raw.strip().lower().replace(" ", "_").replace("-", "_")


# ---------------------------------------------------------------------------
# Emit type-defs
# ---------------------------------------------------------------------------


def emit_classification_typedefs(
    schema: dict[str, Any],
    *,
    include_all: bool = False,
) -> dict[str, Any]:
    """Emit the Atlas v2 ``typedefs`` POST body for a schema.

    Args:
        schema: Parsed APEX schema YAML (as a dict).
        include_all: If True, emit every classification in
            :data:`APEX_CLASSIFICATIONS` (use for first-time Purview
            bootstrap). If False (default), emit only the classifications
            referenced in the supplied schema.

    Returns:
        A dict shaped like ``{"classificationDefs": [...], ...}`` ready to
        POST to ``/api/atlas/v2/types/typedefs``.

    Raises:
        ValueError: if the schema references an unknown classification key.
    """
    used = set(APEX_CLASSIFICATIONS.keys()) if include_all else enumerate_classifications(schema)

    unknown = used - set(APEX_CLASSIFICATIONS.keys())
    if unknown:
        sorted_unknown = ", ".join(sorted(unknown))
        raise ValueError(
            "Unknown APEX classification(s) referenced in schema: "
            f"{sorted_unknown}. Extend APEX_CLASSIFICATIONS in "
            "apex_purview.classifications or correct the schema."
        )

    defs: list[ClassificationDef] = []
    for key in sorted(used):
        spec = APEX_CLASSIFICATIONS[key]
        defs.append(
            ClassificationDef(
                type_name=spec["type_name"],
                description=spec["description"],
            )
        )

    return {
        "enumDefs": [],
        "structDefs": [],
        "classificationDefs": [d.to_atlas() for d in defs],
        "entityDefs": [],
        "relationshipDefs": [],
        "businessMetadataDefs": [],
    }


# ---------------------------------------------------------------------------
# Emit entity attachments
# ---------------------------------------------------------------------------


def emit_entity_classifications(
    schema: dict[str, Any],
) -> list[dict[str, Any]]:
    """Emit per-entity / per-attribute classification attachment payloads.

    For every entity with a ``classification`` key, emits one attachment
    to the entity's qualified name. For every attribute with a
    ``classification`` key, emits one attachment to the attribute's
    qualified name.

    Qualified-name pattern used:

    - Entity:    ``apex.{practice}.{family}.{entity_name}``
    - Attribute: ``apex.{practice}.{family}.{entity_name}.{attribute_name}``

    Args:
        schema: Parsed APEX schema YAML (as a dict).

    Returns:
        A list of dicts, each ready to include in the Atlas v2
        ``PUT /api/atlas/v2/entity/guid/{guid}/classifications`` body.
        (Callers resolve qualified name → GUID via a separate resolver.)

    Raises:
        ValueError: on missing required schema fields or unknown classifications.
    """
    practice = _require(schema, "practice")
    family = _require(schema, "family")

    unknown = enumerate_classifications(schema) - set(APEX_CLASSIFICATIONS.keys())
    if unknown:
        sorted_unknown = ", ".join(sorted(unknown))
        raise ValueError(
            "Unknown APEX classification(s) referenced in schema: "
            f"{sorted_unknown}."
        )

    attachments: list[ClassificationAttachment] = []

    for entity in schema.get("entities", []) or []:
        entity_name = _require(entity, "name")
        entity_qname = f"apex.{practice}.{family}.{entity_name}".lower()

        if "classification" in entity:
            key = _normalize_key(entity["classification"])
            type_name = APEX_CLASSIFICATIONS[key]["type_name"]
            attachments.append(
                ClassificationAttachment(
                    type_name=type_name,
                    qualified_name=entity_qname,
                )
            )

        for attr in entity.get("attributes", []) or []:
            if "classification" in attr:
                attr_name = _require(attr, "name")
                attr_qname = f"{entity_qname}.{attr_name}".lower()
                key = _normalize_key(attr["classification"])
                type_name = APEX_CLASSIFICATIONS[key]["type_name"]
                attachments.append(
                    ClassificationAttachment(
                        type_name=type_name,
                        qualified_name=attr_qname,
                    )
                )

    return [a.to_atlas() for a in attachments]


# ---------------------------------------------------------------------------
# Convenience loaders
# ---------------------------------------------------------------------------


def load_schema_yaml(path: str | Path) -> dict[str, Any]:
    """Parse a schema YAML from disk and return the dict representation."""
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"Schema YAML {path} must parse to a mapping; got {type(data).__name__}")
    if data.get("kind") != "schema":
        raise ValueError(
            f"Schema YAML {path} has kind={data.get('kind')!r}; expected 'schema'."
        )
    return data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _require(d: dict[str, Any], key: str) -> Any:
    """Return ``d[key]`` or raise ValueError with a readable message."""
    if key not in d:
        raise ValueError(f"Missing required field: {key!r}")
    return d[key]
