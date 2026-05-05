"""scml-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from scml_mcp.tools import (
        get_sku_by_key,
        list_shipments_by_destination,
        list_skus_by_supplier,
    )

    mcp = FastMCP("scml-mcp")
    mcp.tool()(get_sku_by_key)
    mcp.tool()(list_skus_by_supplier)
    mcp.tool()(list_shipments_by_destination)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
