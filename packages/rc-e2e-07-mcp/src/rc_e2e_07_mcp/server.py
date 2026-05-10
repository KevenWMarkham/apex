"""rc-e2e-07-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from rc_e2e_07_mcp.tools import (
        commit_hold_decision,
        get_fraud_score_basis,
        get_return_event,
    )

    mcp = FastMCP("rc-e2e-07-mcp")
    mcp.tool()(get_return_event)
    mcp.tool()(get_fraud_score_basis)
    mcp.tool()(commit_hold_decision)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
