"""telemetry-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from telemetry_mcp.tools import emit_trace, log_event, query_latency_percentile

    mcp = FastMCP("telemetry-mcp")
    mcp.tool()(emit_trace)
    mcp.tool()(log_event)
    mcp.tool()(query_latency_percentile)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
