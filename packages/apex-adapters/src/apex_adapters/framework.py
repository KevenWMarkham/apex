"""APEX SOR-adapter framework — Sprint 15.

Every Sprint-15 adapter implements the same shape:

1. **Adapter manifest (YAML)** — declares the SOR, its connection method,
   the source-to-Bronze field mapping, the schedule, and the runbook
   (failure modes + escalation + retry policy).
2. **Adapter implementation (Python class)** — subclasses :class:`Adapter`
   and supplies four operations: ``probe`` (connection test), ``discover``
   (source-schema inspection), ``ingest`` (read SOR → write Bronze), and
   ``validate`` (smoke-test against a golden dataset).
3. **Reference workspace (Terraform)** — provisions the Bronze lakehouse,
   ingest pipeline, and Purview registration. See
   ``infra/terraform/blueprints/adapter-workspace/``.
4. **Runbook (markdown)** — operations document covering failure modes,
   escalation paths, and retry policy.

This module ships the framework — manifest models, schema-mapping
primitives, runbook structure, smoke-test harness, and the abstract
adapter base class. Specific adapters live under
``apex_adapters.implementations``.

Cross-reference: Sellers Guide §5.2 (medallion Bronze landing) + §6.13
(file-first context). Sprint 4 Bronze landing patterns parameterise the
ingest workflow this framework targets.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Connection methods
# ---------------------------------------------------------------------------


class ConnectionMethod(str, Enum):
    """Bronze-landing connection patterns from Sellers Guide §5.2 / Sprint 4."""

    MIRRORED_DB = "mirrored_db"          # Fabric Mirroring (CDC) over a SQL source
    EVENTSTREAM = "eventstream"          # Eventhouse / Event Hub real-time
    DATA_PIPELINE = "data_pipeline"      # Fabric Data Pipeline (Copy + Notebook)
    DATAFLOW_GEN2 = "dataflow_gen2"      # Power Query (REST / SaaS)
    CUSTOM_ENDPOINT = "custom_endpoint"  # Azure Function HTTP webhook
    ODBC = "odbc"                        # ODBC / JDBC pull (legacy)
    FILE_DROP = "file_drop"              # Periodic file drop (SFTP, ADLS landing zone)


# ---------------------------------------------------------------------------
# Schema mapping primitives
# ---------------------------------------------------------------------------


class FieldMapping(BaseModel):
    """One source-field → Bronze-column mapping."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    source_field: str
    bronze_column: str
    bronze_type: Literal[
        "string", "int", "long", "double", "decimal", "boolean",
        "timestamp", "date", "binary", "struct", "array",
    ]
    nullable: bool = True
    description: str = ""
    classification: str | None = Field(
        default=None,
        description="APEX classification key for the Bronze column. None defaults to 'internal'.",
    )
    transform: str | None = Field(
        default=None,
        description="Optional Python expression for in-flight transform (e.g., 'value.lower()').",
    )


class SchemaMapping(BaseModel):
    """Source-table → Bronze-table mapping."""

    model_config = ConfigDict(populate_by_name=True)

    source_table: str
    bronze_table: str
    fields: list[FieldMapping]
    primary_key: list[str] = Field(default_factory=list)
    """Source-side primary-key field names (used for CDC + dedup)."""

    partition_by: list[str] = Field(default_factory=list)
    """Bronze partition columns. Default: ``ingest_date``."""

    def field_count(self) -> int:
        return len(self.fields)

    def classified_fields(self, classification: str) -> list[FieldMapping]:
        return [f for f in self.fields if f.classification == classification]


# ---------------------------------------------------------------------------
# Runbook
# ---------------------------------------------------------------------------


class FailureMode(BaseModel):
    """One declared failure mode + handling."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    code: str
    """Short machine-readable code (e.g., ``CONN_TIMEOUT``, ``SCHEMA_DRIFT``)."""

    description: str
    severity: Literal["info", "warning", "error", "critical"] = "error"
    retry: bool = False
    retry_max: int = 3
    backoff_seconds: int = 30
    escalation: str = "ops-on-call"
    """Named escalation channel (e.g., ``ops-on-call``, ``data-platform-team``)."""


class Runbook(BaseModel):
    """Adapter runbook — failure modes + escalation contact + retry policy."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    primary_contact: str
    """Owner UPN or team alias responsible for the adapter."""

    secondary_contact: str = ""
    failure_modes: list[FailureMode] = Field(default_factory=list)
    sla_recovery_minutes: int = 60
    """Target time-to-recovery for any failure mode marked 'critical'."""

    notes: str = ""


# ---------------------------------------------------------------------------
# Adapter spec (the YAML manifest)
# ---------------------------------------------------------------------------


class AdapterSpec(BaseModel):
    """Top-level adapter manifest — the YAML on disk."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    kind: Literal["adapter"] = "adapter"
    name: str
    """Adapter id, e.g., ``epic-clarity``, ``sap-s4hana``, ``salesforce``."""

    version: str = "0.1.0"
    sor_name: str
    """Human-readable SOR display name."""

    sor_vendor: str
    """Vendor or upstream system (e.g., ``Epic``, ``SAP``)."""

    practice: str
    """Primary APEX Practice this adapter serves."""

    connection_method: ConnectionMethod
    schedule: str
    """Cron-style schedule string or named window (e.g., ``every 15 minutes``)."""

    bronze_workspace: str
    """Canonical workspace name where Bronze tables land. Should match
    ``apex-{practice}-{environment}-bronze`` per Sprint 14 naming."""

    schema_mappings: list[SchemaMapping]
    runbook: Runbook
    description: str = ""

    standards: list[str] = Field(default_factory=list)
    """Industry standards referenced (e.g., HL7 FHIR R4, EDI X12, ISA-95)."""

    def total_fields(self) -> int:
        return sum(m.field_count() for m in self.schema_mappings)


def load_adapter_spec(path: str | Path) -> AdapterSpec:
    """Parse an adapter manifest YAML from disk."""
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(
            f"Adapter spec {path} must parse to a mapping; got {type(data).__name__}"
        )
    return AdapterSpec.model_validate(data)


# ---------------------------------------------------------------------------
# Smoke-test harness
# ---------------------------------------------------------------------------


@dataclass
class SmokeTestResult:
    """Outcome of one adapter smoke-test invocation."""

    adapter_name: str
    rows_read: int = 0
    rows_written: int = 0
    fields_mapped: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1


# ---------------------------------------------------------------------------
# Adapter base class (abstract)
# ---------------------------------------------------------------------------


class Adapter(ABC):
    """Abstract base for all APEX SOR adapters.

    Concrete adapters subclass and implement ``probe``, ``discover``,
    ``ingest``, and ``smoke_test``. The base class provides the
    spec-loading and validation flow.
    """

    def __init__(self, spec: AdapterSpec) -> None:
        self.spec = spec

    @abstractmethod
    def probe(self) -> bool:
        """Verify the source SOR is reachable and credentials work."""

    @abstractmethod
    def discover(self) -> list[str]:
        """Return source-table names visible to the adapter's credentials."""

    @abstractmethod
    def ingest(
        self, mapping: SchemaMapping, *, limit: int | None = None
    ) -> int:
        """Read source rows per ``mapping`` and write to Bronze. Return rows written."""

    def smoke_test(
        self,
        golden_dataset: Path | None = None,
        *,
        limit: int = 100,
    ) -> SmokeTestResult:
        """Run the adapter's smoke test against optional golden data.

        Default implementation: probe + ingest the first declared mapping
        with the supplied limit. Subclasses may override for more
        sophisticated golden-fixture replay.
        """
        result = SmokeTestResult(adapter_name=self.spec.name)
        try:
            ok = self.probe()
            if not ok:
                result.errors.append("probe failed")
                return result
            if not self.spec.schema_mappings:
                result.errors.append("no schema mappings declared")
                return result
            mapping = self.spec.schema_mappings[0]
            result.rows_written = self.ingest(mapping, limit=limit)
            result.rows_read = result.rows_written
            result.fields_mapped = mapping.field_count()
        except Exception as exc:  # noqa: BLE001
            result.errors.append(f"{type(exc).__name__}: {exc}")
        return result


# ---------------------------------------------------------------------------
# Registry — keyed by adapter name
# ---------------------------------------------------------------------------


_ADAPTERS: dict[str, type[Adapter]] = {}


def register_adapter(name: str):
    """Decorator that registers a concrete adapter class by name."""

    def _wrap(cls: type[Adapter]) -> type[Adapter]:
        if name in _ADAPTERS:
            raise ValueError(f"Adapter {name!r} already registered")
        _ADAPTERS[name] = cls
        return cls

    return _wrap


def get_adapter(name: str) -> type[Adapter]:
    """Return the registered adapter class for ``name``."""
    if name not in _ADAPTERS:
        raise KeyError(
            f"Unknown adapter {name!r}. Registered: {sorted(_ADAPTERS.keys())}"
        )
    return _ADAPTERS[name]


def list_adapters() -> list[str]:
    """Return all registered adapter names."""
    return sorted(_ADAPTERS.keys())
