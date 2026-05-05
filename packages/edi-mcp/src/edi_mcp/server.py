"""edi-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from edi_mcp.tools import emit_810, parse_850, parse_856

    mcp = FastMCP("edi-mcp")
    mcp.tool()(parse_850)
    mcp.tool()(parse_856)
    mcp.tool()(emit_810)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
