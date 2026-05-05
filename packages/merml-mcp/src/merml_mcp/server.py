"""merml-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from merml_mcp.tools import (
        get_current_price, list_active_promotions, list_recent_markdowns,
    )

    mcp = FastMCP("merml-mcp")
    mcp.tool()(get_current_price)
    mcp.tool()(list_active_promotions)
    mcp.tool()(list_recent_markdowns)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
