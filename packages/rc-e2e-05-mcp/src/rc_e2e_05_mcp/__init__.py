"""rc-e2e-05-mcp — RC-E2E-05 Store Operations / On-Shelf Availability MCP tools.

Sprint 35. Three tools:

- get_oos_event                     — situation read for The Analyst + Demand Checker
- get_shelf_gap_assignment_basis    — roster + bay layout for Workforce Capacity Sizer
- commit_task_dispatch              — fan-out + completion ingest from Act
"""

from rc_e2e_05_mcp.tools import (
    CONTRACTS,
    commit_task_dispatch,
    get_oos_event,
    get_shelf_gap_assignment_basis,
)

__all__ = [
    "CONTRACTS",
    "commit_task_dispatch",
    "get_oos_event",
    "get_shelf_gap_assignment_basis",
]
