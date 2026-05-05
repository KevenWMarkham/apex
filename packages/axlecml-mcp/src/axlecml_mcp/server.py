"""axlecml-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from axlecml_mcp.tools import (
        get_equipment_by_key, list_production_events, list_recent_quality_results,
    )

    mcp = FastMCP("axlecml-mcp")
    mcp.tool()(get_equipment_by_key)
    mcp.tool()(list_production_events)
    mcp.tool()(list_recent_quality_results)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
