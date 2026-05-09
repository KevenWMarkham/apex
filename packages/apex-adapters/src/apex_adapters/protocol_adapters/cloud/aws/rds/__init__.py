"""APEX adapter: AWS RDS (DataLake).

Mirror RDS POS/ERP/CRM into the primary variant's data tier.

Status: stub. Concrete implementation builds per-engagement when a
Deloitte client's CAB has approved the integration. See README.md
and sec_independence.md.
"""

from .protocols import SATISFIES, ADAPTER_NAME, PROVIDER_LABEL

__all__ = ["SATISFIES", "ADAPTER_NAME", "PROVIDER_LABEL"]
