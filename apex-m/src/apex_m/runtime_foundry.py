"""APEX-M AgentRuntime — Microsoft Foundry Agent Service (Hosted Agents).

Concrete implementation of `apex_core.protocols.AgentRuntime` for APEX-M.
Wraps Microsoft Foundry Agent Service's Hosted Agents API — agents
deploy as containerized workloads to Foundry-managed infrastructure;
Foundry handles threading, tool calls, observability, content safety.

Reference: https://learn.microsoft.com/azure/foundry/agents/overview
Reference: https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent
Reference: https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apex_core.protocols import (
    AgentInvocation,
    AgentResponse,
    AgentRuntime,
)


@dataclass(frozen=True)
class FoundryRuntimeConfig:
    """Tenant configuration for Foundry Agent Service calls."""
    foundry_project_endpoint: str  # https://<project>.services.ai.azure.com/api/projects/<id>
    foundry_account_id: str
    model_default: str = "gpt-4o-2024-11-20"
    private_networking: bool = True   # Standard Setup with Private Networking required for prod
    byo_storage_account_id: str | None = None
    byo_search_service_id: str | None = None
    byo_cosmos_account_id: str | None = None


class AgentRuntimeFoundry:
    """Concrete `AgentRuntime` against Microsoft Foundry Agent Service."""

    variant = "APEX-M"

    def __init__(self, config: FoundryRuntimeConfig) -> None:
        self.config = config
        if config.private_networking and not all([
            config.byo_storage_account_id,
            config.byo_search_service_id,
            config.byo_cosmos_account_id,
        ]):
            raise ValueError(
                "Standard Setup with Private Networking requires BYO Storage + "
                "AI Search + Cosmos DB. See Deployment Guide §7 (revised for "
                "Phase I.4) for the canonical config."
            )

    def deploy_agent(
        self,
        *,
        blueprint_id: str,
        agent_definition: dict[str, Any],
        image_ref: str | None = None,
    ) -> str:
        raise NotImplementedError(
            "AgentRuntimeFoundry.deploy_agent — calls Foundry Agent Service "
            "REST API with hosted-agent payload. Phase I.4 follow-up sprint "
            "wires the SDK call (azure.ai.projects + agent-framework SDKs)."
        )

    def invoke(self, invocation: AgentInvocation) -> AgentResponse:
        raise NotImplementedError("AgentRuntimeFoundry.invoke — Phase I.4 follow-up")

    async def invoke_async(self, invocation: AgentInvocation) -> AgentResponse:
        raise NotImplementedError("AgentRuntimeFoundry.invoke_async — Phase I.4 follow-up")

    def drain(self, agent_id: str, *, timeout_seconds: int = 60) -> None:
        raise NotImplementedError

    def list_agents(self, *, blueprint_id: str | None = None) -> list[dict[str, Any]]:
        raise NotImplementedError


@dataclass
class _MockAgentRecord:
    agent_id: str
    blueprint_id: str
    definition: dict
    image_ref: str | None
    state: str = "running"


class MockAgentRuntimeFoundry:
    """In-memory mock for unit tests + laptop substrate."""

    variant = "APEX-M"

    def __init__(self) -> None:
        self._agents: dict[str, _MockAgentRecord] = {}

    def deploy_agent(
        self,
        *,
        blueprint_id: str,
        agent_definition: dict[str, Any],
        image_ref: str | None = None,
    ) -> str:
        agent_id = agent_definition.get("agent_id") or f"agent-{len(self._agents) + 1}"
        self._agents[agent_id] = _MockAgentRecord(
            agent_id=agent_id, blueprint_id=blueprint_id,
            definition=agent_definition, image_ref=image_ref,
        )
        return agent_id

    def invoke(self, invocation: AgentInvocation) -> AgentResponse:
        rec = self._agents.get(invocation.agent_id)
        if not rec or rec.state != "running":
            raise RuntimeError(f"Agent not running: {invocation.agent_id}")
        return AgentResponse(
            output={"echo": invocation.inputs, "mock": True},
            trace_id=invocation.trace_id,
            decision_ledger_id=f"mock-{invocation.trace_id}",
            tokens_used=0,
            duration_ms=1,
            hitl_gate_triggered=False,
        )

    async def invoke_async(self, invocation: AgentInvocation) -> AgentResponse:
        return self.invoke(invocation)

    def drain(self, agent_id: str, *, timeout_seconds: int = 60) -> None:
        if agent_id in self._agents:
            self._agents[agent_id].state = "drained"

    def list_agents(self, *, blueprint_id: str | None = None) -> list[dict[str, Any]]:
        return [
            {"agent_id": rec.agent_id, "blueprint_id": rec.blueprint_id, "state": rec.state}
            for rec in self._agents.values()
            if blueprint_id is None or rec.blueprint_id == blueprint_id
        ]


__all__ = [
    "FoundryRuntimeConfig",
    "AgentRuntimeFoundry",
    "MockAgentRuntimeFoundry",
]
