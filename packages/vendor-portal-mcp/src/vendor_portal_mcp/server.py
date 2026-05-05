"""vendor-portal-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from vendor_portal_mcp.tools import (
        get_vendor_compliance_score,
        get_vendor_status,
        list_vendor_orders,
    )

    mcp = FastMCP("vendor-portal-mcp")
    mcp.tool()(get_vendor_status)
    mcp.tool()(list_vendor_orders)
    mcp.tool()(get_vendor_compliance_score)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
