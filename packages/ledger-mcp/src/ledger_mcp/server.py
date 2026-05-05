"""ledger-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from ledger_mcp.tools import append_audit_row, fetch_row_by_trace, verify_row_signature

    mcp = FastMCP("ledger-mcp")
    mcp.tool()(append_audit_row)
    mcp.tool()(fetch_row_by_trace)
    mcp.tool()(verify_row_signature)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
