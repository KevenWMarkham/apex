"""rc-e2e-04-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from rc_e2e_04_mcp.tools import (
        commit_winback_offer,
        get_loyalty_churn_cohort,
        get_winback_offer_basis,
    )

    mcp = FastMCP("rc-e2e-04-mcp")
    mcp.tool()(get_loyalty_churn_cohort)
    mcp.tool()(get_winback_offer_basis)
    mcp.tool()(commit_winback_offer)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
