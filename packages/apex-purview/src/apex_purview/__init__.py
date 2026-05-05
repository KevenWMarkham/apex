"""APEX Purview integration.

Sprint 13 modules:

- ``classifications`` (Task 13.1) — classification type-defs + entity attachments
- ``lineage`` (Task 13.2) — seven-hop lineage Process emitters
- ``dlp`` (Task 13.3) — DLP policy bundle + violation alerting
- ``retention`` (Task 13.4) — WORM retention bands + legal-hold config
- ``catalog`` (Task 13.5) — business-glossary terms + cross-entity relationships
- ``propagation`` (Task 13.6) — most-restrictive-label propagation validator
"""

from __future__ import annotations

from apex_purview.classifications import (
    APEX_CLASSIFICATIONS,
    ClassificationAttachment,
    ClassificationDef,
    emit_classification_typedefs,
    emit_entity_classifications,
    enumerate_classifications,
)
from apex_purview.lineage import (
    PROCESS_TYPES,
    EntityRef,
    LineageProcess,
    emit_agent_to_orchestration,
    emit_bronze_to_silver,
    emit_from_spec,
    emit_gold_to_mcp,
    emit_lineage_batch,
    emit_mcp_to_agent,
    emit_orchestration_to_audit,
    emit_process_typedefs,
    emit_silver_to_gold,
    emit_sor_to_bronze,
    load_lineage_spec,
)
from apex_purview.dlp import (
    ACTIONS,
    DEFAULT_DLP_MATRIX,
    SURFACES,
    DLPPolicyBundle,
    DLPRule,
    DLPViolationAlert,
    action_severity,
    build_bundle_from_overrides,
    build_default_bundle,
    emit_dlp_payload,
    lookup_action,
    most_restrictive as most_restrictive_action,
)
from apex_purview.retention import (
    DEFAULT_RETENTION_MATRIX,
    RETENTION_DURATIONS,
    LegalHoldConfig,
    RetentionPolicyBundle,
    RetentionRule,
    build_default_retention_bundle,
    build_retention_with_overrides,
    emit_retention_payload,
    lookup_retention,
)
from apex_purview.catalog import (
    EntityRelationship,
    GlossaryDef,
    GlossaryTerm,
    emit_catalog_bundle,
    emit_glossary_def,
    emit_glossary_terms_from_schema,
    emit_relationship_typedefs,
    emit_relationships_from_schema,
)
from apex_purview.propagation import (
    CLASSIFICATION_SEVERITY,
    PropagationNode,
    PropagationReport,
    PropagationViolation,
    build_propagation_graph,
    most_restrictive as most_restrictive_classification,
    severity,
    validate_propagation,
)

__all__ = [
    # classifications
    "APEX_CLASSIFICATIONS",
    "ClassificationAttachment",
    "ClassificationDef",
    "emit_classification_typedefs",
    "emit_entity_classifications",
    "enumerate_classifications",
    # lineage
    "PROCESS_TYPES",
    "EntityRef",
    "LineageProcess",
    "emit_agent_to_orchestration",
    "emit_bronze_to_silver",
    "emit_from_spec",
    "emit_gold_to_mcp",
    "emit_lineage_batch",
    "emit_mcp_to_agent",
    "emit_orchestration_to_audit",
    "emit_process_typedefs",
    "emit_silver_to_gold",
    "emit_sor_to_bronze",
    "load_lineage_spec",
    # dlp
    "ACTIONS",
    "DEFAULT_DLP_MATRIX",
    "SURFACES",
    "DLPPolicyBundle",
    "DLPRule",
    "DLPViolationAlert",
    "action_severity",
    "build_bundle_from_overrides",
    "build_default_bundle",
    "emit_dlp_payload",
    "lookup_action",
    "most_restrictive_action",
    # retention
    "DEFAULT_RETENTION_MATRIX",
    "RETENTION_DURATIONS",
    "LegalHoldConfig",
    "RetentionPolicyBundle",
    "RetentionRule",
    "build_default_retention_bundle",
    "build_retention_with_overrides",
    "emit_retention_payload",
    "lookup_retention",
    # catalog
    "EntityRelationship",
    "GlossaryDef",
    "GlossaryTerm",
    "emit_catalog_bundle",
    "emit_glossary_def",
    "emit_glossary_terms_from_schema",
    "emit_relationship_typedefs",
    "emit_relationships_from_schema",
    # propagation
    "CLASSIFICATION_SEVERITY",
    "PropagationNode",
    "PropagationReport",
    "PropagationViolation",
    "build_propagation_graph",
    "most_restrictive_classification",
    "severity",
    "validate_propagation",
]

__version__ = "0.1.0"
