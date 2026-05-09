"""APEX adapter: Google Pub/Sub (MessageBus).

Cross-cloud event routing GCP -> APEX-M Eventstream.

Status: stub. Concrete implementation builds per-engagement when a
Deloitte client's CAB has approved the integration. See README.md
and sec_independence.md.
"""

from .protocols import SATISFIES, ADAPTER_NAME, PROVIDER_LABEL

__all__ = ["SATISFIES", "ADAPTER_NAME", "PROVIDER_LABEL"]
