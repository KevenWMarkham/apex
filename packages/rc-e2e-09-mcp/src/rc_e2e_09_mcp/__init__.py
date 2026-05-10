"""rc-e2e-09-mcp — RC-E2E-09 Product Tracking (FSMA 204) MCP tools.

Sprint 39. Three tools:

- get_recall_panel       — affected-lot CTE/KDE inventory for the Handoff chain
- get_lot_provenance     — cross-service read for RC-E2E-03 + RC-E2E-07
- commit_lot_event       — canonical SCML.Lot SCD2 write (RC-E2E-09 sole writer)

Per the SCML.Lot ownership boundary (Sprint 39.4), this package is the sole
writer of SCML.Lot. Other RC services consume `get_lot_provenance` only.
"""

from rc_e2e_09_mcp.tools import (
    CONTRACTS,
    commit_lot_event,
    get_lot_provenance,
    get_recall_panel,
)

__all__ = [
    "CONTRACTS",
    "commit_lot_event",
    "get_lot_provenance",
    "get_recall_panel",
]
