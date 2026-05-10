"""rc-e2e-05-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from rc_e2e_05_mcp.tools import (
        commit_task_dispatch,
        get_oos_event,
        get_shelf_gap_assignment_basis,
    )

    mcp = FastMCP("rc-e2e-05-mcp")
    mcp.tool()(get_oos_event)
    mcp.tool()(get_shelf_gap_assignment_basis)
    mcp.tool()(commit_task_dispatch)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
