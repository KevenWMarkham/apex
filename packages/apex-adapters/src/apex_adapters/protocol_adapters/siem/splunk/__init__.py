"""APEX adapter: Splunk (AuditLedger, Observability).

Client-mandated parallel-write to Splunk SIEM.

Status: stub. Concrete implementation builds per-engagement when a
firm client's CAB has approved the integration. See README.md
and sec_independence.md.
"""

from .protocols import ADAPTER_NAME, PROVIDER_LABEL, SATISFIES

__all__ = ["ADAPTER_NAME", "PROVIDER_LABEL", "SATISFIES"]
