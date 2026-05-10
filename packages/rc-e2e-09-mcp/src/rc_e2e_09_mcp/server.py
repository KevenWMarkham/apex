"""rc-e2e-09-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from rc_e2e_09_mcp.tools import (
        commit_lot_event,
        get_lot_provenance,
        get_recall_panel,
    )

    mcp = FastMCP("rc-e2e-09-mcp")
    mcp.tool()(get_recall_panel)
    mcp.tool()(get_lot_provenance)
    mcp.tool()(commit_lot_event)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
