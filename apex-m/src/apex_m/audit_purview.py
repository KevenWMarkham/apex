"""APEX-M AuditLedger — Microsoft Purview Audit (system of record) + Fabric SQL overlay.

Purview Audit captures every AI interaction at the platform layer (per
Microsoft's `audit-copilot` + `ai-agent-365` reference architectures).
APEX-M's overlay row in Fabric SQL provides KPI-attribution joins that
Purview Audit doesn't natively model.

The split is critical:
- **Primary** = Microsoft Purview Audit (`is_primary=True`). Append-only,
  Microsoft-managed retention, immutable, system of record for
  compliance and audit. APEX does NOT replace this.
- **Secondary overlay** = Fabric SQL ledger table (`is_primary=False`).
  Indexed for `decision_ledger_id` ↔ KPI attribution joins, signed with
  HMAC for the WORM contract, but NOT the system of record.

Reference: https://learn.microsoft.com/purview/ai-agent-365
Reference: https://learn.microsoft.com/purview/audit-copilot
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from apex_core.protocols import AuditLedger, AuditRow


@dataclass(frozen=True)
class PurviewAuditConfig:
    tenant_id: str
    purview_account: str
    overlay_sql_connection_secret_uri: str  # Key Vault ref to Fabric SQL DSN


class AuditLedgerPurview:
    """Concrete primary AuditLedger against Microsoft Purview Audit."""

    variant = "APEX-M"
    is_primary = True

    def __init__(self, config: PurviewAuditConfig) -> None:
        self.config = config

    def append(self, row: AuditRow) -> str:
        raise NotImplementedError(
            "AuditLedgerPurview.append — emits to Microsoft Purview Audit "
            "via Microsoft.Compliance/audit Graph API. Phase I.3 follow-up."
        )

    def query(self, **kwargs) -> list[AuditRow]:
        raise NotImplementedError("Purview Audit query API — Phase I.3 follow-up")

    def verify(self, row_id: str) -> bool:
        raise NotImplementedError


class AuditLedgerFabricOverlay:
    """Concrete secondary overlay AuditLedger against Fabric SQL.

    NEVER the system of record. Use only for KPI-attribution joins
    (decision_ledger_id → realized margin in Gold marts).
    """

    variant = "APEX-M"
    is_primary = False

    def __init__(self, *, fabric_sql_dsn: str) -> None:
        self.fabric_sql_dsn = fabric_sql_dsn

    def append(self, row: AuditRow) -> str:
        raise NotImplementedError("AuditLedgerFabricOverlay.append — Phase I.3 follow-up")

    def query(self, **kwargs) -> list[AuditRow]:
        raise NotImplementedError

    def verify(self, row_id: str) -> bool:
        raise NotImplementedError


class MockAuditLedgerPurview:
    """In-memory mock — primary semantics."""

    variant = "APEX-M"
    is_primary = True

    def __init__(self) -> None:
        self._rows: dict[str, AuditRow] = {}

    def append(self, row: AuditRow) -> str:
        rid = f"purview-{row.trace_id}-{row.decision_ledger_id}"
        self._rows[rid] = row
        return rid

    def query(self, **kwargs) -> list[AuditRow]:
        rows = list(self._rows.values())
        if kwargs.get("trace_id"):
            rows = [r for r in rows if r.trace_id == kwargs["trace_id"]]
        if kwargs.get("agent_id"):
            rows = [r for r in rows if r.agent_id == kwargs["agent_id"]]
        if kwargs.get("service_code"):
            rows = [r for r in rows if r.service_code == kwargs["service_code"]]
        return rows

    def verify(self, row_id: str) -> bool:
        return row_id in self._rows


__all__ = [
    "PurviewAuditConfig",
    "AuditLedgerPurview",
    "AuditLedgerFabricOverlay",
    "MockAuditLedgerPurview",
]
