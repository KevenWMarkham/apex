"""rc-e2e-03-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from rc_e2e_03_mcp.tools import (
        commit_markdown_decision,
        get_excursion_decision_panel,
        get_pricing_recommendation_basis,
    )

    mcp = FastMCP("rc-e2e-03-mcp")
    mcp.tool()(get_excursion_decision_panel)
    mcp.tool()(get_pricing_recommendation_basis)
    mcp.tool()(commit_markdown_decision)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
