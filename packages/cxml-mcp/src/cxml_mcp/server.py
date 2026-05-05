"""cxml-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from cxml_mcp.tools import (
        get_customer_by_key, list_interactions_by_customer, list_orders_by_customer,
    )

    mcp = FastMCP("cxml-mcp")
    mcp.tool()(get_customer_by_key)
    mcp.tool()(list_orders_by_customer)
    mcp.tool()(list_interactions_by_customer)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
