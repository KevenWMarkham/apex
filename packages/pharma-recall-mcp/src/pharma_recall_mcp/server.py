"""pharma-recall-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from pharma_recall_mcp.tools import (
        get_recall_detail, list_pharma_recalls, search_recalls_by_ndc,
    )

    mcp = FastMCP("pharma-recall-mcp")
    mcp.tool()(list_pharma_recalls)
    mcp.tool()(search_recalls_by_ndc)
    mcp.tool()(get_recall_detail)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
