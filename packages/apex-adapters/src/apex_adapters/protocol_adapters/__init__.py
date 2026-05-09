"""APEX protocol adapters — integrate non-primary services with APEX-Core protocols.

Each adapter under cloud/, saas/, siem/, identity/ declares which APEX-Core
protocols it satisfies and provides a stub implementation today. Concrete impls
build per-engagement.

See docs/apex-core/Adapter-Catalog.md for the full inventory.
"""

__all__: list[str] = []
