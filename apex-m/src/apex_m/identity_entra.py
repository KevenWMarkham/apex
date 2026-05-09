"""APEX-M AgentIdentityProvider — Microsoft Entra Agent ID.

Concrete implementation of `apex_core.protocols.AgentIdentityProvider`
for APEX-M (Microsoft variant). Wraps Microsoft Graph + Entra Agent ID
endpoints (GA April 2026).

Design: docs/APEX - Design and Build/agent-identity-blueprints.md
Reference: https://learn.microsoft.com/entra/agent-id/what-is-microsoft-entra-agent-id

This module exposes both the protocol-conformant class (`AgentIdentityProviderEntra`)
and a `MockAgentIdentityProviderEntra` for unit tests + offline development on
the laptop substrate. The mock satisfies the same protocol; the real impl
calls Microsoft Graph and requires Entra tenant configuration.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from apex_core.protocols import (
    AgentBlueprint,
    AgentIdentity,
    AgentIdentityProvider,
)


_GRAPH_BASE = "https://graph.microsoft.com/v1.0"
_BLUEPRINTS_PATH = "/agentIdentities/blueprints"
_INSTANCES_PATH_TEMPLATE = "/agentIdentities/blueprints/{blueprint_id}/instances"


def apex_m_blueprint_id(service_code: str | None) -> str:
    """Return the canonical blueprint id for a service code, per
    `agent-identity-blueprints.md` §3."""
    if service_code is None:
        return "apex-m-tenant-root"
    return f"apex-m-{service_code.lower()}-blueprint"


def apex_m_agent_id(*, service_code: str, scenario_id: str, role: str) -> str:
    """Return the canonical APEX-M agent id, e.g.
    `apex-m:rc-e2e-03:rc-cold-chain-excursion-mid-shift:pricing`."""
    return f"apex-m:{service_code}:{scenario_id}:{role}"


@dataclass(frozen=True)
class EntraAgentIdConfig:
    """Tenant configuration for Entra Agent ID calls."""
    tenant_id: str
    client_id: str
    # Authentication: prefer DefaultAzureCredential; allow override for testing.
    credential: Any | None = None
    graph_base: str = _GRAPH_BASE


class AgentIdentityProviderEntra:
    """Concrete `AgentIdentityProvider` against Microsoft Entra Agent ID.

    Authentication uses `azure.identity.DefaultAzureCredential` by default,
    which honors the substrate hierarchy:
    - Laptop: `AZURE_FEDERATED_TOKEN_FILE` (Workload Identity Federation)
    - Foundry / Container Apps: managed identity attached to the agent host
    """

    variant = "APEX-M"

    def __init__(self, config: EntraAgentIdConfig) -> None:
        self.config = config
        self._client = self._build_graph_client()

    def _build_graph_client(self):
        """Lazily import azure-identity + httpx to keep apex-m importable
        without those SDKs installed (matters for protocol tests)."""
        try:
            import httpx
            from azure.identity import DefaultAzureCredential
        except ImportError as e:  # pragma: no cover
            raise RuntimeError(
                "AgentIdentityProviderEntra requires azure-identity + httpx. "
                "Install via `pip install apex-m[runtime]`."
            ) from e

        credential = self.config.credential or DefaultAzureCredential()

        def _get_token() -> str:
            tok = credential.get_token("https://graph.microsoft.com/.default")
            return tok.token

        client = httpx.Client(base_url=self.config.graph_base, timeout=30.0)
        client._apex_get_token = _get_token  # type: ignore[attr-defined]
        return client

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._client._apex_get_token()}",  # type: ignore[attr-defined]
            "Content-Type": "application/json",
        }

    # -- AgentIdentityProvider protocol methods --

    def create_blueprint(self, blueprint: AgentBlueprint) -> AgentBlueprint:
        body = {
            "id": blueprint.blueprint_id,
            "displayName": blueprint.label,
            "parentBlueprintId": blueprint.parent_id,
            "conditionalAccessPolicyIds": list(blueprint.conditional_access_policy_ids),
            "roleAssignments": list(blueprint.role_assignments),
            "lifecyclePolicy": dict(blueprint.lifecycle_policy),
            "notes": blueprint.notes,
        }
        # Idempotent: PATCH if exists, POST if not.
        existing = self._client.get(
            f"{_BLUEPRINTS_PATH}/{blueprint.blueprint_id}",
            headers=self._headers(),
        )
        if existing.status_code == 404:
            res = self._client.post(_BLUEPRINTS_PATH, headers=self._headers(), json=body)
        else:
            res = self._client.patch(
                f"{_BLUEPRINTS_PATH}/{blueprint.blueprint_id}",
                headers=self._headers(),
                json=body,
            )
        res.raise_for_status()
        return blueprint

    def provision_identity(self, *, blueprint_id: str, agent_id: str) -> AgentIdentity:
        path = _INSTANCES_PATH_TEMPLATE.format(blueprint_id=blueprint_id)
        body = {"agentId": agent_id}
        res = self._client.post(path, headers=self._headers(), json=body)
        res.raise_for_status()
        data = res.json()
        return AgentIdentity(
            identity_id=data["id"],
            blueprint_id=blueprint_id,
            agent_id=agent_id,
            principal_id=data["principalId"],
            tenant_id=self.config.tenant_id,
            federated=False,
        )

    def get_identity(self, agent_id: str) -> AgentIdentity | None:
        res = self._client.get(
            f"/agentIdentities?$filter=agentId eq '{agent_id}'",
            headers=self._headers(),
        )
        if res.status_code == 404:
            return None
        res.raise_for_status()
        items = res.json().get("value", [])
        if not items:
            return None
        item = items[0]
        return AgentIdentity(
            identity_id=item["id"],
            blueprint_id=item["blueprintId"],
            agent_id=agent_id,
            principal_id=item["principalId"],
            tenant_id=self.config.tenant_id,
            federated=bool(item.get("isFederated")),
        )

    def revoke_identity(self, agent_id: str, *, reason: str) -> None:
        identity = self.get_identity(agent_id)
        if identity is None:
            return
        res = self._client.delete(
            f"/agentIdentities/{identity.identity_id}?reason={reason}",
            headers=self._headers(),
        )
        res.raise_for_status()

    def acquire_obo_token(
        self,
        *,
        agent_id: str,
        operator_principal: str,
        target_resource: str,
    ) -> str:
        # OAuth 2.0 OBO flow per
        # https://learn.microsoft.com/entra/identity-platform/v2-oauth2-on-behalf-of-flow
        # Implementation requires the operator's existing token + the agent's
        # client_id. This stub raises until the operator-token plumbing lands.
        raise NotImplementedError(
            "OBO flow requires operator-principal token + agent client_id. "
            "Wired in Phase I.1 follow-up sprint per agent-identity-blueprints §10."
        )

    def list_blueprints(self) -> list[AgentBlueprint]:
        res = self._client.get(
            f"{_BLUEPRINTS_PATH}?$filter=startswith(id,'apex-m-')",
            headers=self._headers(),
        )
        res.raise_for_status()
        return [
            AgentBlueprint(
                blueprint_id=item["id"],
                parent_id=item.get("parentBlueprintId"),
                label=item["displayName"],
                conditional_access_policy_ids=list(item.get("conditionalAccessPolicyIds") or []),
                role_assignments=list(item.get("roleAssignments") or []),
                lifecycle_policy=dict(item.get("lifecyclePolicy") or {}),
                notes=item.get("notes", ""),
            )
            for item in res.json().get("value", [])
        ]


class MockAgentIdentityProviderEntra:
    """In-memory mock for unit tests + laptop substrate development.

    Satisfies the same `AgentIdentityProvider` protocol; persists state
    in-memory only. Used by test suites and the wizard's local dev mode.
    """

    variant = "APEX-M"

    def __init__(self, *, tenant_id: str = "mock-tenant") -> None:
        self.tenant_id = tenant_id
        self._blueprints: dict[str, AgentBlueprint] = {}
        self._identities: dict[str, AgentIdentity] = {}
        self._revoked: set[str] = set()

    def create_blueprint(self, blueprint: AgentBlueprint) -> AgentBlueprint:
        self._blueprints[blueprint.blueprint_id] = blueprint
        return blueprint

    def provision_identity(self, *, blueprint_id: str, agent_id: str) -> AgentIdentity:
        if blueprint_id not in self._blueprints:
            raise KeyError(f"Unknown blueprint: {blueprint_id}")
        identity = AgentIdentity(
            identity_id=f"oid-{agent_id}",
            blueprint_id=blueprint_id,
            agent_id=agent_id,
            principal_id=f"sp-{agent_id}",
            tenant_id=self.tenant_id,
            federated=False,
        )
        self._identities[agent_id] = identity
        return identity

    def get_identity(self, agent_id: str) -> AgentIdentity | None:
        if agent_id in self._revoked:
            return None
        return self._identities.get(agent_id)

    def revoke_identity(self, agent_id: str, *, reason: str) -> None:
        self._revoked.add(agent_id)

    def acquire_obo_token(
        self,
        *,
        agent_id: str,
        operator_principal: str,
        target_resource: str,
    ) -> str:
        if agent_id in self._revoked:
            raise PermissionError(f"Agent identity {agent_id} is revoked")
        return f"mock-obo-token::{agent_id}::{operator_principal}::{target_resource}"

    def list_blueprints(self) -> list[AgentBlueprint]:
        return list(self._blueprints.values())


__all__ = [
    "EntraAgentIdConfig",
    "AgentIdentityProviderEntra",
    "MockAgentIdentityProviderEntra",
    "apex_m_blueprint_id",
    "apex_m_agent_id",
]
