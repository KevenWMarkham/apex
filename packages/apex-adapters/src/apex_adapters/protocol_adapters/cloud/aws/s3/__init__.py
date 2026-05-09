"""APEX adapter: AWS S3 (DataLake).

Bronze ingestion from client S3 buckets into APEX-M Fabric (or APEX-G/A primaries).

Status: stub. Concrete implementation builds per-engagement when a
Deloitte client's CAB has approved the integration. See README.md
and sec_independence.md.
"""

from .protocols import SATISFIES, ADAPTER_NAME, PROVIDER_LABEL

__all__ = ["SATISFIES", "ADAPTER_NAME", "PROVIDER_LABEL"]
