"""Concrete APEX SOR adapter implementations.

Importing this module triggers registration of all adapters via the
``@register_adapter`` decorator. Each concrete adapter lives in its own
module so engagement-specific extensions can override or substitute one
without touching the framework.
"""

from __future__ import annotations

from apex_adapters.implementations.epic_clarity import EpicClarityAdapter
from apex_adapters.implementations.sap_s4hana import SapS4HanaAdapter

__all__ = [
    "EpicClarityAdapter",
    "SapS4HanaAdapter",
]
