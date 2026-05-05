"""hlscml-mcp MCP server entry-point."""

from __future__ import annotations


def main() -> None:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

    from hlscml_mcp.tools import (
        get_patient_by_key,
        list_medications_for_patient,
        list_observations_for_patient,
    )

    mcp = FastMCP("hlscml-mcp")
    mcp.tool()(get_patient_by_key)
    mcp.tool()(list_observations_for_patient)
    mcp.tool()(list_medications_for_patient)
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
