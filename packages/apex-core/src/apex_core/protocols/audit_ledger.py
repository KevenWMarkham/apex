"""AuditLedger protocol — append-only decision history.

APEX-M satisfies via Microsoft Purview Audit (system of record) +
overlay row in Fabric SQL ledger table for KPI attribution.
APEX-G satisfies via Cloud Audit Logs + BigQuery overlay.
APEX-A satisfies via AWS CloudTrail + DynamoDB overlay.

Adapters for client SIEM (Splunk, Sumo Logic, Datadog, QRadar) implement
this for the `siem_audit.secondary` slot — parallel write only, never
primary.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class AuditRow:
    """The 14-field APEX audit row, generalized across providers.

    Field set is normative across variants — concrete impl maps to provider
    schema (Purview Audit, CloudTrail, etc.) and the local overlay table.
    """
    trace_id: str
    decision_ledger_id: str
    tenant_id: str
    service_code: str           # e.g., RC-E2E-03
    scenario_id: str            # e.g., rc-cold-chain-excursion-mid-shift
    agent_id: str
    operator_principal: str | None
    decision_kind: str          # zero-touch | ack-only | hitl | escalation
    inputs_hash: str            # content-addressed
    outputs_hash: str           # content-addressed
    manifest_version: str       # three-version rule
    policy_version: str
    prompt_version: str
    timestamp: datetime
    classification: str         # T1 | T2 | T3 | T4 (mapped to provider label)
    extras: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class AuditLedger(Protocol):
    """Append, query, sign, verify."""

    variant: str
    is_primary: bool   # True = system of record; False = parallel-write overlay

    def append(self, row: AuditRow) -> str:
        """Append-only. Returns the persisted row's signed id."""
        ...

    def query(
        self,
        *,
        trace_id: str | None = None,
        agent_id: str | None = None,
        service_code: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
    ) -> list[AuditRow]:
        """Filter the ledger. Indexed by trace_id and decision_ledger_id."""
        ...

    def verify(self, row_id: str) -> bool:
        """Verify a row's signature against the WORM store. Returns False
        on tamper or missing."""
        ...
