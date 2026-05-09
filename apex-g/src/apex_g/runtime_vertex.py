"""APEX-G AgentRuntime stub — Vertex AI Agent Builder + Agent Engine."""
from __future__ import annotations

from apex_core.protocols import AgentRuntime
from . import _stub


class AgentRuntimeVertex:
    """Stub implementation. Will satisfy AgentRuntime when APEX-G ships."""

    variant = "APEX-G"

    def __init__(self, *args, **kwargs):
        _stub("AgentRuntime (Vertex AI Agent Builder)")

    def deploy_agent(self, **kwargs):
        _stub("AgentRuntime.deploy_agent")

    def invoke(self, invocation):
        _stub("AgentRuntime.invoke")

    async def invoke_async(self, invocation):
        _stub("AgentRuntime.invoke_async")

    def drain(self, agent_id, **kwargs):
        _stub("AgentRuntime.drain")

    def list_agents(self, **kwargs):
        _stub("AgentRuntime.list_agents")


__all__ = ["AgentRuntimeVertex"]
