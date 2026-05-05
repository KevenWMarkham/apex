"""policy-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from policy_mcp.tools import check_compliance, classify_bump, evaluate_policy

    mcp = FastMCP("policy-mcp")
    mcp.tool()(evaluate_policy)
    mcp.tool()(check_compliance)
    mcp.tool()(classify_bump)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
