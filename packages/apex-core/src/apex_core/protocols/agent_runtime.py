"""AgentRuntime protocol — where APEX agents execute.

APEX-M satisfies via Microsoft Foundry Agent Service (Foundry Hosted Agents).
APEX-G satisfies via Google Vertex AI Agent Builder.
APEX-A satisfies via AWS Bedrock Agents.

Adapters do NOT satisfy this protocol — agents always run on a primary
variant's runtime. Adapters provide other protocols (DataLake, SIEM, etc.)
that the agent calls into.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class AgentInvocation:
    agent_id: str           # variant-scoped (e.g., "apex-m:rc-e2e-03:pricing")
    scenario_id: str
    inputs: dict[str, Any]
    trace_id: str
    operator_principal: str | None = None  # for OBO flows


@dataclass(frozen=True)
class AgentResponse:
    output: dict[str, Any]
    trace_id: str
    decision_ledger_id: str | None
    tokens_used: int
    duration_ms: int
    hitl_gate_triggered: bool = False


@runtime_checkable
class AgentRuntime(Protocol):
    """Deploy, invoke, drain, and query agents on a primary variant runtime."""

    variant: str  # "APEX-M" | "APEX-G" | "APEX-A"

    def deploy_agent(
        self,
        *,
        blueprint_id: str,
        agent_definition: dict[str, Any],
        image_ref: str | None = None,
    ) -> str:
        """Deploy or update an agent. Returns the variant-scoped agent_id."""
        ...

    def invoke(self, invocation: AgentInvocation) -> AgentResponse:
        """Synchronously invoke an agent and return its response."""
        ...

    async def invoke_async(self, invocation: AgentInvocation) -> AgentResponse:
        """Async variant for streaming or long-running invocations."""
        ...

    def drain(self, agent_id: str, *, timeout_seconds: int = 60) -> None:
        """Stop accepting new invocations; let in-flight complete."""
        ...

    def list_agents(self, *, blueprint_id: str | None = None) -> list[dict[str, Any]]:
        """Inventory of deployed agents under this runtime."""
        ...
