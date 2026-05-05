"""fabric-mcp MCP server entry-point.

Wires the tool functions in ``tools.py`` to Anthropic's MCP SDK. The SDK
import is deferred to ``main()`` so importing ``fabric_mcp`` doesn't require
``mcp`` installed (tests import only ``fabric_mcp.tools``).
"""

from __future__ import annotations


def main() -> None:  # pragma: no cover — manual / CI entry-point only
    """Run the fabric-mcp server over MCP's default transport."""
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from fabric_mcp.tools import (
        get_entity_by_key,
        list_classifications,
        query_gold_view,
    )

    mcp = FastMCP("fabric-mcp")
    mcp.tool()(get_entity_by_key)
    mcp.tool()(query_gold_view)
    mcp.tool()(list_classifications)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
