"""ercml-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from ercml_mcp.tools import (
        get_meter_by_key, list_grid_events_by_type, list_recent_readings,
    )

    mcp = FastMCP("ercml-mcp")
    mcp.tool()(get_meter_by_key)
    mcp.tool()(list_recent_readings)
    mcp.tool()(list_grid_events_by_type)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
