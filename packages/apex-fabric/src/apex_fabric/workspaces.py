"""Microsoft Fabric workspace API wrapper — Sprint 14 Task 14.2 (BL.P.92).

Provisions Fabric workspaces against the public REST API
(`POST /v1/workspaces`) with APEX-canonical naming-convention
enforcement.

Naming convention
-----------------
Every APEX workspace name follows:

    apex-{practice}-{environment}-{role}[-{suffix}]

Where:

- ``practice``    — rc / hls / er / axle / tmt / th / ice / core
- ``environment`` — dev / test / stage / prod
- ``role``        — bronze / silver / gold / governance / runtime / sandbox
- ``suffix``      — optional region or tenant-scoped marker

The wrapper rejects any non-conforming name. Engagement-specific overrides
must use ``WorkspaceSpec(name_override=...)`` with explicit Independence
sign-off captured in the PR description.

API reference
-------------
Workspace REST API:
``POST https://api.fabric.microsoft.com/v1/workspaces``
``GET  https://api.fabric.microsoft.com/v1/workspaces``
``DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}``
``POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/assignToCapacity``

Authentication is Entra-issued bearer token. The wrapper never accepts
connection-string auth.

Cross-reference: Sellers Guide §5.4 (workspace pattern), Sprint 14
Orchestrator goal (zero → workspace in <30 minutes).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PRACTICES: tuple[str, ...] = (
    "rc", "hls", "er", "axle", "tmt", "th", "ice", "core"
)

ENVIRONMENTS: tuple[str, ...] = ("dev", "test", "stage", "prod")

#: Workspace roles in the APEX medallion stack.
ROLES: tuple[str, ...] = (
    "bronze",       # raw SOR-fidelity ingest
    "silver",       # canonical / tokenized
    "gold",         # agent-safe views
    "governance",   # Purview tooling, classification, lineage
    "runtime",      # Foundry agents, MCP tooling
    "sandbox",      # exploratory / R&D
)

#: Regex for the canonical workspace naming convention.
_NAME_RE = re.compile(
    r"^apex-(?P<practice>[a-z]+)-(?P<environment>[a-z]+)-(?P<role>[a-z]+)(?:-(?P<suffix>[a-z0-9]+))?$"
)

#: Fabric public REST API base URL.
FABRIC_API_BASE: str = "https://api.fabric.microsoft.com/v1"


# ---------------------------------------------------------------------------
# Naming convention enforcement
# ---------------------------------------------------------------------------


def canonical_workspace_name(
    practice: str,
    environment: str,
    role: str,
    suffix: str | None = None,
) -> str:
    """Return the canonical workspace name for the given attributes.

    Raises:
        ValueError: if any input is not in the canonical vocabulary.
    """
    if practice not in PRACTICES:
        raise ValueError(
            f"Unknown practice {practice!r}. Allowed: {PRACTICES}"
        )
    if environment not in ENVIRONMENTS:
        raise ValueError(
            f"Unknown environment {environment!r}. Allowed: {ENVIRONMENTS}"
        )
    if role not in ROLES:
        raise ValueError(
            f"Unknown role {role!r}. Allowed: {ROLES}"
        )

    base = f"apex-{practice}-{environment}-{role}"
    if suffix is None:
        return base

    if not re.fullmatch(r"[a-z0-9]+", suffix):
        raise ValueError(
            f"suffix {suffix!r} must match [a-z0-9]+ (lowercase alphanumeric)."
        )
    return f"{base}-{suffix}"


def parse_workspace_name(name: str) -> dict[str, str]:
    """Parse a canonical workspace name into its component parts.

    Returns a dict with keys: ``practice``, ``environment``, ``role``,
    and ``suffix`` (None if absent).

    Raises:
        ValueError: if the name does not match the canonical regex or
            if its parts are not in the canonical vocabularies.
    """
    m = _NAME_RE.match(name)
    if m is None:
        raise ValueError(
            f"Workspace name {name!r} does not match canonical pattern "
            "'apex-{practice}-{environment}-{role}[-{suffix}]'."
        )
    parsed = m.groupdict()
    if parsed["practice"] not in PRACTICES:
        raise ValueError(f"Unknown practice in {name!r}: {parsed['practice']!r}")
    if parsed["environment"] not in ENVIRONMENTS:
        raise ValueError(f"Unknown environment in {name!r}: {parsed['environment']!r}")
    if parsed["role"] not in ROLES:
        raise ValueError(f"Unknown role in {name!r}: {parsed['role']!r}")
    return parsed


def validate_workspace_name(name: str) -> bool:
    """Return True if the name parses cleanly; False otherwise.

    Does not raise; intended for filter / lint use.
    """
    try:
        parse_workspace_name(name)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Workspace specification
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkspaceSpec:
    """Declarative spec for a Fabric workspace to provision."""

    practice: str
    environment: str
    role: str
    capacity_id: str
    """Resource ID of the capacity the workspace will be assigned to."""

    suffix: str | None = None
    description: str = ""
    name_override: str | None = None
    """Bypass canonical naming. Discouraged — requires PR review."""

    tags: dict[str, str] = field(default_factory=dict)

    def name(self) -> str:
        """Return the canonical name (or override if supplied)."""
        if self.name_override is not None:
            if not validate_workspace_name(self.name_override):
                raise ValueError(
                    f"name_override {self.name_override!r} does not match "
                    "canonical pattern. Override anyway requires explicit Independence sign-off."
                )
            return self.name_override
        return canonical_workspace_name(
            self.practice, self.environment, self.role, self.suffix
        )

    def to_create_body(self) -> dict[str, Any]:
        """Return the body for ``POST /v1/workspaces``."""
        return {
            "displayName": self.name(),
            "description": self.description,
            "capacityId": self.capacity_id,
        }


# ---------------------------------------------------------------------------
# Token provider protocol
# ---------------------------------------------------------------------------


class TokenProvider(Protocol):
    """Provide an Entra-issued bearer token for the Fabric API.

    Production implementations use ``azure.identity.DefaultAzureCredential``
    or a managed-identity-backed credential. Tests inject a stub.
    """

    def __call__(self) -> str: ...


# ---------------------------------------------------------------------------
# REST client
# ---------------------------------------------------------------------------


@dataclass
class WorkspaceClient:
    """Thin Fabric workspace REST client — Entra-auth only.

    Args:
        token_provider: Callable returning a current Entra access token.
        base_url: Override the Fabric API base URL (used in tests).
        http_client: Optional injected ``httpx.Client`` (used in tests).
    """

    token_provider: TokenProvider
    base_url: str = FABRIC_API_BASE
    http_client: Any = None

    def _client(self) -> Any:
        """Return the injected http client or a fresh httpx.Client."""
        if self.http_client is not None:
            return self.http_client
        import httpx
        return httpx.Client(timeout=30.0)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token_provider()}",
            "Content-Type": "application/json",
            "User-Agent": "apex-fabric/0.1.0",
        }

    def list_workspaces(self) -> list[dict[str, Any]]:
        """``GET /v1/workspaces`` — return the value array."""
        client = self._client()
        resp = client.get(f"{self.base_url}/workspaces", headers=self._headers())
        resp.raise_for_status()
        body = resp.json()
        return body.get("value", [])

    def get_workspace_by_name(self, name: str) -> dict[str, Any] | None:
        """Return the workspace dict matching ``name``, or None."""
        for ws in self.list_workspaces():
            if ws.get("displayName") == name:
                return ws
        return None

    def create_workspace(self, spec: WorkspaceSpec) -> dict[str, Any]:
        """``POST /v1/workspaces`` — create the workspace per spec.

        Returns the created workspace dict.

        Raises:
            ValueError: if the spec name doesn't match the canonical pattern.
            httpx.HTTPStatusError: on non-2xx responses.
        """
        # Trip the validation up-front (prevents API call on bad input)
        spec.name()  # raises if not canonical

        client = self._client()
        resp = client.post(
            f"{self.base_url}/workspaces",
            json=spec.to_create_body(),
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()

    def delete_workspace(self, workspace_id: str) -> None:
        """``DELETE /v1/workspaces/{workspaceId}``."""
        client = self._client()
        resp = client.delete(
            f"{self.base_url}/workspaces/{workspace_id}",
            headers=self._headers(),
        )
        resp.raise_for_status()

    def assign_to_capacity(self, workspace_id: str, capacity_id: str) -> None:
        """``POST /v1/workspaces/{workspaceId}/assignToCapacity``."""
        client = self._client()
        resp = client.post(
            f"{self.base_url}/workspaces/{workspace_id}/assignToCapacity",
            json={"capacityId": capacity_id},
            headers=self._headers(),
        )
        resp.raise_for_status()

    def ensure_workspace(self, spec: WorkspaceSpec) -> dict[str, Any]:
        """Idempotent create — returns existing workspace if name matches.

        Useful for declarative-pipeline workflows where the same spec runs
        on every CI invocation.
        """
        existing = self.get_workspace_by_name(spec.name())
        if existing is not None:
            return existing
        return self.create_workspace(spec)
