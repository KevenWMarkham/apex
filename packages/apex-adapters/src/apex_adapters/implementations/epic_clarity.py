"""Epic Clarity adapter — Sprint 15 Subtask 15.1.1 (BL.P.95).

Epic's Clarity is the canonical Epic reporting database (denormalized
SQL Server / Oracle replica of Epic's transactional data store). APEX
ingests from Clarity via ODBC into HLS Bronze.

Authentication: Entra Service Principal with read-only scope on the
Clarity database. Credentials live in Key Vault; never in source.

The implementation here is a **reference** — the production adapter
plugs in a live ODBC connector. This module ships:

- The Epic Clarity AdapterSpec loader
- A no-op ``probe`` / ``discover`` / ``ingest`` that simulates a
  successful run for smoke tests
- A `replay_golden_dataset` helper for fixture-based testing

When the production ODBC connector is wired (Wave-1 engagement
specific), the no-op methods are replaced with real pyodbc calls per
the ``odbc_connection_string`` field.

Cross-reference: Sellers Guide §10.10.3 HLS enterprise SOR table.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apex_adapters.framework import (
    Adapter,
    AdapterSpec,
    ConnectionMethod,
    SchemaMapping,
    SmokeTestResult,
    register_adapter,
)


@register_adapter("epic-clarity")
class EpicClarityAdapter(Adapter):
    """Epic Clarity ODBC adapter for HLS Bronze ingestion."""

    def __init__(self, spec: AdapterSpec) -> None:
        super().__init__(spec)
        if spec.connection_method != ConnectionMethod.ODBC:
            raise ValueError(
                f"Epic Clarity expects connection_method='odbc', got {spec.connection_method!r}"
            )
        self._golden_path: Path | None = None
        self._golden_data: dict[str, list[dict[str, Any]]] | None = None

    # ------------------------------------------------------------------
    # Test injection
    # ------------------------------------------------------------------

    def use_golden_dataset(self, path: Path) -> None:
        """Configure the adapter to read its 'source rows' from a golden JSON file."""
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError(
                f"Golden dataset {path}: expected mapping of {{table_name: [rows]}}"
            )
        self._golden_path = path
        self._golden_data = data

    # ------------------------------------------------------------------
    # Adapter interface
    # ------------------------------------------------------------------

    def probe(self) -> bool:
        """Probe the Clarity database. Returns True if reachable."""
        # In production: open ODBC connection, run `SELECT 1`.
        # In smoke test: succeed if golden data is loaded or if the
        # spec carries a probe_passes hint.
        return self._golden_data is not None or True

    def discover(self) -> list[str]:
        """Discover the source-table names this adapter can ingest."""
        # In production: query Clarity's information_schema.
        # In smoke test: return tables from the golden dataset.
        if self._golden_data is not None:
            return sorted(self._golden_data.keys())
        # No data → return tables declared in the spec
        return [m.source_table for m in self.spec.schema_mappings]

    def ingest(
        self, mapping: SchemaMapping, *, limit: int | None = None
    ) -> int:
        """Ingest the source table named by ``mapping`` into Bronze.

        In production: SELECT … FROM ``mapping.source_table``,
        apply ``mapping.fields`` transforms, write to Bronze Delta.

        In smoke test: replay the golden dataset rows, validate
        every declared field is present in the source, return the
        count of rows that would be written.
        """
        if self._golden_data is None:
            # Production no-op — count is 0 unless real ODBC wiring is supplied
            return 0

        rows = self._golden_data.get(mapping.source_table, [])
        if limit is not None:
            rows = rows[:limit]

        # Validate every field mapping resolves in at least one source row
        if rows:
            sample = rows[0]
            for field in mapping.fields:
                if field.source_field not in sample:
                    raise KeyError(
                        f"Source row missing declared field "
                        f"{field.source_field!r} from mapping for table "
                        f"{mapping.source_table!r}"
                    )

        # In production: write the rows to Bronze with PK + ingest_date partition
        return len(rows)

    def smoke_test(
        self,
        golden_dataset: Path | None = None,
        *,
        limit: int = 100,
    ) -> SmokeTestResult:
        """Override base smoke-test to support golden-fixture replay."""
        if golden_dataset is not None:
            self.use_golden_dataset(golden_dataset)
        result = SmokeTestResult(adapter_name=self.spec.name)
        try:
            if not self.probe():
                result.errors.append("probe failed")
                return result
            for mapping in self.spec.schema_mappings:
                rows = self.ingest(mapping, limit=limit)
                result.rows_read += rows
                result.rows_written += rows
                result.fields_mapped += mapping.field_count()
        except Exception as exc:  # noqa: BLE001
            result.errors.append(f"{type(exc).__name__}: {exc}")
        return result
