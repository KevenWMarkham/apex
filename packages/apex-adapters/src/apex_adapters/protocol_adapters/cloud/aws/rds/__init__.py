"""APEX adapter: AWS RDS (DataLake).

Mirror RDS POS/ERP/CRM into the primary variant's data tier.

Status: stub. Concrete implementation builds per-engagement when a
firm client's CAB has approved the integration. See README.md
and sec_independence.md.
"""

from .protocols import ADAPTER_NAME, PROVIDER_LABEL, SATISFIES

__all__ = ["ADAPTER_NAME", "PROVIDER_LABEL", "SATISFIES"]
