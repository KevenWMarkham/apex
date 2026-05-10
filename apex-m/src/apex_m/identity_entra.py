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
        operator_assertion: str | None = None,
    ) -> str:
        """OAuth 2.0 On-Behalf-Of flow per Microsoft identity platform docs.

        Reference: https://learn.microsoft.com/entra/identity-platform/v2-oauth2-on-behalf-of-flow

        The operator's first-party token (`operator_assertion`) is exchanged
        for a token that lets the agent identity call the target resource
        on behalf of the operator. The audit row records both principals.

        Sprint 41 implementation — wires Microsoft Authentication Library
        (MSAL) for the OBO grant. The deployment-time managed identity for
        this agent is the OBO client; the operator's token is the upstream
        assertion.

        Args:
            agent_id: APEX-scoped agent id (e.g., apex-m:RC-E2E-03:rc-cold-chain-...:decide)
            operator_principal: UPN or OID of the human operator
            target_resource: Microsoft Graph / Azure resource scope being called
                            (e.g., "https://graph.microsoft.com/.default")
            operator_assertion: The operator's existing access token (JWT). When
                                None and `MockAgentIdentityProviderEntra` is used
                                for tests, a mock token is returned.

        Returns:
            An access token (string) the agent can use to call `target_resource`
            on behalf of the operator. Token expiry is per Microsoft Entra defaults
            (1 hour for autonomous; 8 hours for HITL session).

        Raises:
            ValueError: when operator_assertion is None on the production impl.
            RuntimeError: when MSAL token acquisition fails — exception chain
                          carries the Microsoft Entra error code.
        """
        if operator_assertion is None:
            raise ValueError(
                "OBO flow requires the operator's existing access token as "
                "`operator_assertion`. The HITL approver's session token from "
                "Microsoft Teams (per use-case hitl_channel) is the typical "
                "source. See agent-identity-blueprints.md §9."
            )

        try:
            import msal  # noqa: F401 — verify availability
        except ImportError as e:
            raise RuntimeError(
                "msal SDK required for OBO. Install via `pip install apex-m[runtime]`."
            ) from e

        from msal import ConfidentialClientApplication

        identity = self.get_identity(agent_id)
        if identity is None:
            raise ValueError(
                f"Agent identity {agent_id} not provisioned. "
                f"Call provision_identity first."
            )

        # OBO requires a confidential client (the agent's app registration).
        # Authority follows the Microsoft Entra tenant convention.
        authority = f"https://login.microsoftonline.com/{self.config.tenant_id}"
        # The agent's client_id from the config — set by the platform/identity.bicep
        # deployment script when the agent identity blueprint was provisioned.
        app = ConfidentialClientApplication(
            client_id=self.config.client_id,
            authority=authority,
            client_credential=self._get_agent_client_secret(),
        )
        result = app.acquire_token_on_behalf_of(
            user_assertion=operator_assertion,
            scopes=[target_resource],
        )
        if "access_token" not in result:
            err_code = result.get("error", "unknown_error")
            err_desc = result.get("error_description", "")
            raise RuntimeError(
                f"OBO token acquisition failed: {err_code} — {err_desc}. "
                f"agent_id={agent_id} target={target_resource}"
            )
        # Record OBO event in audit trail per agent-identity-blueprints.md §9
        self._emit_obo_audit(
            agent_id=agent_id,
            operator_principal=operator_principal,
            target_resource=target_resource,
            token_correlation=result.get("id_token_claims", {}).get("aio", "n/a"),
        )
        return result["access_token"]

    def _get_agent_client_secret(self) -> str | None:
        """Retrieve the agent's client secret. Production deployments use
        federated credentials (Workload Identity Federation per Sprint 41
        item 41.2.3) instead of long-lived secrets — this returns None and
        MSAL falls through to the federated credential path."""
        # WIF path — the federated assertion file injected by the substrate
        # (Foundry hosted agent runtime / Container Apps env / laptop docker)
        # is read by msal automatically when client_credential is None.
        return None

    def _emit_obo_audit(
        self,
        *,
        agent_id: str,
        operator_principal: str,
        target_resource: str,
        token_correlation: str,
    ) -> None:
        """Audit OBO events per agent-identity-blueprints.md §9 fields 3+4
        (operator principal + Conditional Access result). The actual write
        goes through `apex_m.audit_purview.AuditLedgerPurview` at the
        wizard / agent-runtime level; here we just emit a structured log
        line that the ambient observability picks up.
        """
        import json
        import logging
        log = logging.getLogger("apex_m.identity_entra.obo")
        log.info(
            json.dumps({
                "event": "obo_token_acquired",
                "agent_id": agent_id,
                "operator_principal": operator_principal,
                "target_resource": target_resource,
                "token_correlation": token_correlation,
                "tenant_id": self.config.tenant_id,
            })
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
        operator_assertion: str | None = None,
    ) -> str:
        if agent_id in self._revoked:
            raise PermissionError(f"Agent identity {agent_id} is revoked")
        # Mock accepts operator_assertion=None for unit-test convenience;
        # production raises ValueError without it (see AgentIdentityProviderEntra).
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
