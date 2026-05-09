"""APEX adapter: Salesforce (DataLake).

Salesforce CRM as Silver source (RC-E2E-04 Loyalty, HLS Patient relationships).

Status: stub. Concrete implementation builds per-engagement when a
Deloitte client's CAB has approved the integration. See README.md
and sec_independence.md.
"""

from .protocols import SATISFIES, ADAPTER_NAME, PROVIDER_LABEL

__all__ = ["SATISFIES", "ADAPTER_NAME", "PROVIDER_LABEL"]
