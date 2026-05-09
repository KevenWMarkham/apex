"""APEX adapter: Snowflake (DataLake).

Snowflake-on-AWS Gold consumer for analytics-on-Snowflake clients.

Status: stub. Concrete implementation builds per-engagement when a
Deloitte client's CAB has approved the integration. See README.md
and sec_independence.md.
"""

from .protocols import SATISFIES, ADAPTER_NAME, PROVIDER_LABEL

__all__ = ["SATISFIES", "ADAPTER_NAME", "PROVIDER_LABEL"]
