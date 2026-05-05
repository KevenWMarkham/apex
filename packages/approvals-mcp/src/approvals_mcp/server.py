"""approvals-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from approvals_mcp.tools import get_approval_status, record_decision, request_approval

    mcp = FastMCP("approvals-mcp")
    mcp.tool()(request_approval)
    mcp.tool()(get_approval_status)
    mcp.tool()(record_decision)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
