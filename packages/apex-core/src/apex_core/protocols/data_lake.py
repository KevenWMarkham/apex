"""DataLake protocol — Bronze/Silver/Gold storage abstraction.

APEX-M satisfies via Microsoft Fabric (OneLake + Lakehouse + Eventhouse +
Mirroring + Direct Lake), with OneLake Security in user identity mode.
APEX-G satisfies via Google BigQuery + Cloud Storage + Pub/Sub.
APEX-A satisfies via AWS Lake Formation + S3 + Glue.

Adapters that bring data from a client's existing data plane:
- cloud.aws.s3 (S3 Bronze ingestion)
- cloud.aws.rds (RDS Mirroring source)
- cloud.gcp.bigquery (BigQuery Silver source)
- saas.snowflake (Snowflake Gold consumer)
- saas.databricks (Unity Catalog interop)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator, Protocol, runtime_checkable


@dataclass(frozen=True)
class DataLakeQuery:
    """Read intent against a tier. Engine-neutral; concrete impl picks
    SQL / KQL / Spark / Bedrock SQL based on tier and provider."""
    tier: str           # "bronze" | "silver" | "gold"
    schema: str         # APEX-Core canonical schema family (SCML, MERML, etc.)
    entity: str         # e.g., "Inventory", "Markdown", "Lot"
    filters: dict[str, Any] = field(default_factory=dict)
    columns: list[str] | None = None
    limit: int | None = None
    classification_max: str | None = None  # T1..T4 — must satisfy operator scope


@dataclass(frozen=True)
class DataLakeWrite:
    """Write intent, only valid against Bronze landing or Silver-from-source."""
    tier: str
    schema: str
    entity: str
    rows: list[dict[str, Any]]
    classification: str
    source_system: str


@runtime_checkable
class DataLake(Protocol):
    """Read and write the canonical Bronze/Silver/Gold tiers."""

    variant: str
    primary_workspace: str   # e.g., "rc-canonical" — primary workspace pattern

    def query(self, q: DataLakeQuery, *, operator_scope: str) -> Iterator[dict[str, Any]]:
        """Read with operator scope enforced via the variant's identity model
        (OneLake user identity mode for APEX-M, etc.)."""
        ...

    def write(self, w: DataLakeWrite) -> int:
        """Append rows. Returns count written. Bronze accepts append-only
        with ingest metadata; Silver writes are CDC-driven."""
        ...

    def get_security_policy(self, *, schema: str, entity: str) -> dict[str, Any]:
        """Returns the OneLake/equivalent policy enforced on this entity:
        RLS predicates, column masks, classification."""
        ...

    def list_entities(self, *, schema: str | None = None) -> list[str]:
        """Inventory of entities visible to the caller."""
        ...
