"""ferc-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from ferc_mcp.tools import (
        get_interconnection_queue_status,
        list_compliance_filings,
        list_enforcement_actions,
    )

    mcp = FastMCP("ferc-mcp")
    mcp.tool()(list_enforcement_actions)
    mcp.tool()(get_interconnection_queue_status)
    mcp.tool()(list_compliance_filings)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
