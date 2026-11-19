"""APEX adapter: Google Pub/Sub (MessageBus).

Cross-cloud event routing GCP -> APEX-M Eventstream.

Status: stub. Concrete implementation builds per-engagement when a
firm client's CAB has approved the integration. See README.md
and sec_independence.md.
"""

from .protocols import ADAPTER_NAME, PROVIDER_LABEL, SATISFIES

__all__ = ["ADAPTER_NAME", "PROVIDER_LABEL", "SATISFIES"]
