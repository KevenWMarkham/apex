"""APEX SOR-adapter framework + 15 reference adapters — Sprint 15."""

from __future__ import annotations

from apex_adapters.catalog import (
    ADAPTER_REGISTRY,
    list_shipped_manifests,
    load_all_shipped_manifests,
    load_shipped_manifest,
    manifests_dir,
)
from apex_adapters.framework import (
    Adapter,
    AdapterSpec,
    ConnectionMethod,
    FailureMode,
    FieldMapping,
    Runbook,
    SchemaMapping,
    SmokeTestResult,
    get_adapter,
    list_adapters,
    load_adapter_spec,
    register_adapter,
)
from apex_adapters.implementations import EpicClarityAdapter, SapS4HanaAdapter

__all__ = [
    "ADAPTER_REGISTRY",
    "Adapter",
    "AdapterSpec",
    "ConnectionMethod",
    "EpicClarityAdapter",
    "FailureMode",
    "FieldMapping",
    "Runbook",
    "SapS4HanaAdapter",
    "SchemaMapping",
    "SmokeTestResult",
    "get_adapter",
    "list_adapters",
    "list_shipped_manifests",
    "load_adapter_spec",
    "load_all_shipped_manifests",
    "load_shipped_manifest",
    "manifests_dir",
    "register_adapter",
]

__version__ = "0.1.0"
