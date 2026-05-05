"""fda-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from fda_mcp.tools import get_recall_detail, list_recalls_by_date, search_adverse_events

    mcp = FastMCP("fda-mcp")
    mcp.tool()(list_recalls_by_date)
    mcp.tool()(get_recall_detail)
    mcp.tool()(search_adverse_events)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
