"""RC CRMML alias surface — CRMML.* → CXML.*.

Sprint 30 item 30.5. The RC build status YAML and Services Guide §18 refer
to customer-relationship entities by the practice-namespaced alias **CRMML**
(CRM Markup Language), but the canonical schemas live in the framework-wide
``apex-cxml`` package per Roadmap.md BL.P.10.

This module makes the alias explicit so:

- The RC silver-layer notebooks can read ``apex_rc.crmml.Customer`` while
  the framework keeps a single canonical definition in ``apex_cxml``.
- ``rc_bundle().entities['cxml']`` and ``rc_bundle().entities['proml']`` keep
  the canonical naming, while the wizard / Services Guide can resolve the
  CRMML alias unambiguously.
- Sensitivity classifications travel with the entity definitions (CRMML
  inherits CXML's PII / PCI markings).

There is intentionally no separate Pydantic class here — the canonical
entity is the same object. CRMML is a *naming convention*, not a schema fork.
"""

from __future__ import annotations

# Re-export the canonical CXML entities under the CRMML alias.
from apex_cxml import (
    Customer as Customer,
    Interaction as Interaction,
    Loyalty as Loyalty,
    Order as Order,
)

# Module-level mapping that the wizard / Services Guide can introspect.
CRMML_ALIASES: dict[str, type] = {
    "CRMML.Customer":    Customer,
    "CRMML.Loyalty":     Loyalty,
    "CRMML.Interaction": Interaction,
    "CRMML.Order":       Order,
}

# Per RC build-status sprint-30 item 30.5 — Customer / Loyalty / Interaction
# are the three the RC services consume; Order is included because RC-E2E-04
# Loyalty Churn joins it for spend signal.

__all__ = [
    "Customer",
    "Interaction",
    "Loyalty",
    "Order",
    "CRMML_ALIASES",
]
