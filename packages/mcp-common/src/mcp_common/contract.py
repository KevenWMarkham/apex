"""``ToolContract`` — every MCP tool declares one of these.

Mirrors the contract fields defined in ``APEX_Design.md`` §7.3. The contract
is the seam between the MCP transport (JSON-RPC) and the APEX governance
plane: classification propagation, SLO tracking, per-tool version pinning.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from apex_core.types import Classification


class SloSpec(BaseModel):
    """Service-level-objective for one tool."""

    model_config = ConfigDict(extra="forbid")

    latency_ms_p95: int | None = Field(None, gt=0)
    freshness_seconds: int | None = Field(None, gt=0)
    availability_pct: float | None = Field(None, ge=0.0, le=100.0)


class ToolContract(BaseModel):
    """Declarative per-tool contract.

    MCP server packages instantiate one ``ToolContract`` per tool and register
    it at start-up. The contract is introspectable by ``policy-mcp`` for
    compliance checks and by audit rows for classification propagation.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., min_length=1, description="Fully qualified tool name, e.g. 'fabric-mcp.get_entity_by_key'.")
    version: str = Field("1.0.0", description="Tool SemVer; new behaviour = new version.")
    description: str
    input_schema: dict = Field(
        default_factory=dict,
        description="JSON schema of tool input. Pydantic model_json_schema() output.",
    )
    output_schema: dict = Field(
        default_factory=dict,
        description="JSON schema of tool output.",
    )
    classification_propagation: list[Classification] = Field(
        default_factory=list,
        description=(
            "Classifications this tool's output may carry. Consumers apply the "
            "most-restrictive across this list for DLP."
        ),
    )
    slo: SloSpec | None = None
    required_scopes: list[str] = Field(
        default_factory=list,
        description="Scope dimensions the caller must satisfy (e.g. 'practice:rc').",
    )
