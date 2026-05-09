"""APEX-M DataLake — Microsoft Fabric (OneLake / Lakehouse / Eventhouse / Mirroring).

Concrete implementation of `apex_core.protocols.DataLake` for APEX-M.
Honors the OneLake user-identity-mode contract — table reads are governed
by OneLake security roles, not SQL GRANT/REVOKE on tables.

Adopts the primary-workspace pattern (per Phase I.2 design): one primary
workspace per practice (e.g., rc-canonical) owns the canonical Silver
entities; per-service workspaces (rc-e2e-03, rc-e2e-04, …) consume via
OneLake shortcuts.

Reference: https://learn.microsoft.com/fabric/onelake/security/best-practices-secure-data-in-onelake
Reference: https://learn.microsoft.com/fabric/onelake/security/sql-analytics-endpoint-onelake-security
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from apex_core.protocols import DataLake, DataLakeQuery, DataLakeWrite


@dataclass(frozen=True)
class FabricDataLakeConfig:
    """Tenant configuration for Fabric DataLake operations."""
    capacity_id: str                # Microsoft.Fabric/capacities resource id
    primary_workspace: str          # e.g., "rc-canonical" (primary-workspace pattern)
    onelake_endpoint: str = "https://onelake.dfs.fabric.microsoft.com"
    sql_analytics_endpoint_mode: str = "user_identity"  # "user_identity" | "delegated_identity"


class DataLakeFabric:
    """Concrete `DataLake` against Microsoft Fabric.

    Reads honor OneLake user identity mode — RLS / CLS / object-level
    policies live in OneLake, not SQL GRANT/REVOKE. Writes hit Bronze
    (append-only) or Silver (CDC-driven only).
    """

    variant = "APEX-M"

    def __init__(self, config: FabricDataLakeConfig) -> None:
        self.config = config
        self.primary_workspace = config.primary_workspace

    def query(self, q: DataLakeQuery, *, operator_scope: str) -> Iterator[dict[str, Any]]:
        """Read with operator scope enforced via OneLake user identity mode.

        TBD — see `bicep_runner.py` companion. Implementation must:
        1. Open Fabric SQL analytics endpoint with operator's Entra token
           (NOT the Bicep-time delegated identity)
        2. Read tier+schema+entity per the request
        3. Stream rows; OneLake security policies filter inline
        4. Track classification_max — caller's scope must satisfy
        """
        raise NotImplementedError(
            "DataLakeFabric.query — see Phase I.2 follow-up sprint. "
            "Mock available via apex_m.data_lake_fabric.MockDataLakeFabric."
        )

    def write(self, w: DataLakeWrite) -> int:
        raise NotImplementedError(
            "DataLakeFabric.write — Bronze append-only and Silver CDC paths "
            "land in Phase I.2 follow-up sprint."
        )

    def get_security_policy(self, *, schema: str, entity: str) -> dict[str, Any]:
        """Returns the OneLake security policy for (schema, entity):
        RLS predicate, column masks, sensitivity-label classification."""
        raise NotImplementedError

    def list_entities(self, *, schema: str | None = None) -> list[str]:
        raise NotImplementedError


@dataclass
class _InMemoryEntity:
    schema: str
    entity: str
    rows: list[dict[str, Any]] = field(default_factory=list)
    classification: str = "T2"


class MockDataLakeFabric:
    """In-memory mock for unit tests + laptop-substrate development."""

    variant = "APEX-M"

    def __init__(self, *, primary_workspace: str = "rc-canonical") -> None:
        self.primary_workspace = primary_workspace
        self._entities: dict[tuple[str, str], _InMemoryEntity] = {}

    def query(self, q: DataLakeQuery, *, operator_scope: str) -> Iterator[dict[str, Any]]:
        key = (q.schema, q.entity)
        e = self._entities.get(key)
        if not e:
            return iter([])
        rows = e.rows
        # Apply filters
        for col, val in (q.filters or {}).items():
            rows = [r for r in rows if r.get(col) == val]
        if q.columns:
            rows = [{c: r.get(c) for c in q.columns} for r in rows]
        if q.limit:
            rows = rows[: q.limit]
        return iter(rows)

    def write(self, w: DataLakeWrite) -> int:
        key = (w.schema, w.entity)
        if key not in self._entities:
            self._entities[key] = _InMemoryEntity(
                schema=w.schema, entity=w.entity, classification=w.classification
            )
        self._entities[key].rows.extend(w.rows)
        return len(w.rows)

    def get_security_policy(self, *, schema: str, entity: str) -> dict[str, Any]:
        e = self._entities.get((schema, entity))
        return {
            "schema": schema,
            "entity": entity,
            "classification": e.classification if e else "T1",
            "rls_predicate": None,
            "column_masks": [],
        }

    def list_entities(self, *, schema: str | None = None) -> list[str]:
        return [
            f"{s}.{e}" for (s, e) in self._entities
            if schema is None or s == schema
        ]


__all__ = [
    "FabricDataLakeConfig", "DataLakeFabric", "MockDataLakeFabric",
]
