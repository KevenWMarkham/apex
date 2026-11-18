"""tokenizer-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    """Register the detokenize tool on a FastMCP server and run it."""
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from tokenizer_mcp.tools import detokenize_under_scope

    mcp = FastMCP("tokenizer-mcp")
    mcp.tool()(detokenize_under_scope)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
