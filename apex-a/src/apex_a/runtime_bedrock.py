"""APEX-A AgentRuntime stub — AWS Bedrock Agents + AgentCore."""
from __future__ import annotations

from . import _stub


class AgentRuntimeBedrock:
    """Stub implementation. Will satisfy AgentRuntime when APEX-A ships."""

    variant = "APEX-A"

    def __init__(self, *args, **kwargs):
        _stub("AgentRuntime (Bedrock Agents)")

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


__all__ = ["AgentRuntimeBedrock"]
