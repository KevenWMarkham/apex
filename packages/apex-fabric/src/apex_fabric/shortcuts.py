"""OneLake shortcut provisioning — Sprint 14 Task 14.4 (BL.P.94).

Wraps the Fabric OneLake Shortcuts API
(``POST /v1/workspaces/{workspaceId}/items/{itemId}/shortcuts``) to
create shortcuts to:

- **ADLS Gen2** (``adlsGen2`` target) — Azure Data Lake Storage
- **Amazon S3** (``s3`` target)
- **Google Cloud Storage** (``googleCloudStorage`` target)
- **Dataverse** (``dataverse`` target)
- **Cross-workspace OneLake** (``oneLake`` target) — Practice-reference → Tenant pattern

Cross-workspace shortcuts unlock the APEX Practice-reference pattern: a
single canonical Practice workspace (e.g., ``apex-rc-prod-silver``)
holds the Silver canonical schemas, and tenant workspaces shortcut to
those Silver tables rather than copying. This is the "Bronze data
stays where it is, Silver canonical lives in one place" pattern from
Sellers Guide §1.6 and §6.13.

Cross-reference: Sellers Guide §1.6.6 / §6.13 / §9.11.4 Bronze→Silver→Gold→MCP→Agent path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from apex_fabric.workspaces import TokenProvider, FABRIC_API_BASE

#: Supported shortcut target kinds. Maps to the Fabric API's
#: ``target.{kind}`` envelope keys.
ShortcutKind = Literal[
    "adls_gen2",
    "s3",
    "google_cloud_storage",
    "dataverse",
    "onelake",
]


# ---------------------------------------------------------------------------
# Shortcut specifications
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AdlsGen2Target:
    """ADLS Gen2 shortcut target."""

    location: str
    """``https://{account}.dfs.core.windows.net``"""

    subpath: str
    """``/{filesystem}/{path}``"""

    connection_id: str
    """Pre-registered Fabric connection ID for the storage account."""

    def to_atlas(self) -> dict[str, Any]:
        return {
            "adlsGen2": {
                "location": self.location,
                "subpath": self.subpath,
                "connectionId": self.connection_id,
            }
        }


@dataclass(frozen=True)
class S3Target:
    """Amazon S3 shortcut target."""

    location: str
    """``https://{bucket}.s3.{region}.amazonaws.com``"""

    subpath: str
    connection_id: str

    def to_atlas(self) -> dict[str, Any]:
        return {
            "s3": {
                "location": self.location,
                "subpath": self.subpath,
                "connectionId": self.connection_id,
            }
        }


@dataclass(frozen=True)
class GoogleCloudStorageTarget:
    """GCS shortcut target."""

    location: str
    """``https://storage.googleapis.com/{bucket}``"""

    subpath: str
    connection_id: str

    def to_atlas(self) -> dict[str, Any]:
        return {
            "googleCloudStorage": {
                "location": self.location,
                "subpath": self.subpath,
                "connectionId": self.connection_id,
            }
        }


@dataclass(frozen=True)
class DataverseTarget:
    """Dataverse shortcut target."""

    environment_url: str
    """Dataverse env URL, e.g. ``https://contoso.crm.dynamics.com``"""

    delta_lake_folder: str
    """Delta Lake folder under Dataverse storage."""

    connection_id: str

    def to_atlas(self) -> dict[str, Any]:
        return {
            "dataverse": {
                "environmentUrl": self.environment_url,
                "deltaLakeFolder": self.delta_lake_folder,
                "connectionId": self.connection_id,
            }
        }


@dataclass(frozen=True)
class OneLakeTarget:
    """Cross-workspace OneLake shortcut target.

    Powers the APEX Practice-reference pattern: tenant workspaces
    shortcut to canonical Silver tables in a Practice-reference workspace
    rather than duplicating them.
    """

    workspace_id: str
    """Source workspace ID."""

    item_id: str
    """Source lakehouse / warehouse ID."""

    path: str
    """Path within the source item (e.g., ``Tables/scml_sku``)."""

    def to_atlas(self) -> dict[str, Any]:
        return {
            "oneLake": {
                "workspaceId": self.workspace_id,
                "itemId": self.item_id,
                "path": self.path,
            }
        }


@dataclass(frozen=True)
class ShortcutSpec:
    """Declarative spec for a OneLake shortcut.

    Args:
        workspace_id: Workspace that hosts the shortcut.
        item_id: Lakehouse or warehouse ID inside the workspace.
        name: Shortcut name (e.g., ``"shortcut_scml_sku"``).
        path: Folder path inside the lakehouse where the shortcut lives
            (typically ``"Tables"`` or ``"Files"``).
        target: One of the *Target dataclasses above.
        description: Optional description.
    """

    workspace_id: str
    item_id: str
    name: str
    path: str
    target: AdlsGen2Target | S3Target | GoogleCloudStorageTarget | DataverseTarget | OneLakeTarget
    description: str = ""

    def to_create_body(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "name": self.name,
            "path": self.path,
            "target": self.target.to_atlas(),
        }
        if self.description:
            body["description"] = self.description
        return body


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


@dataclass
class ShortcutClient:
    """Fabric OneLake Shortcuts API client.

    Args:
        token_provider: Callable returning a current Entra access token.
        base_url: Override the API base URL (test injection).
        http_client: Optional injected httpx.Client.
    """

    token_provider: TokenProvider
    base_url: str = FABRIC_API_BASE
    http_client: Any = None

    def _client(self) -> Any:
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

    def create_shortcut(self, spec: ShortcutSpec) -> dict[str, Any]:
        """``POST /v1/workspaces/{ws}/items/{item}/shortcuts``."""
        client = self._client()
        url = (
            f"{self.base_url}/workspaces/{spec.workspace_id}"
            f"/items/{spec.item_id}/shortcuts"
        )
        resp = client.post(url, json=spec.to_create_body(), headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def list_shortcuts(self, workspace_id: str, item_id: str) -> list[dict[str, Any]]:
        """``GET /v1/workspaces/{ws}/items/{item}/shortcuts``."""
        client = self._client()
        url = (
            f"{self.base_url}/workspaces/{workspace_id}"
            f"/items/{item_id}/shortcuts"
        )
        resp = client.get(url, headers=self._headers())
        resp.raise_for_status()
        body = resp.json()
        return body.get("value", [])

    def delete_shortcut(
        self, workspace_id: str, item_id: str, name: str, path: str
    ) -> None:
        """``DELETE /v1/workspaces/{ws}/items/{item}/shortcuts/{path}/{name}``."""
        client = self._client()
        url = (
            f"{self.base_url}/workspaces/{workspace_id}"
            f"/items/{item_id}/shortcuts/{path}/{name}"
        )
        resp = client.delete(url, headers=self._headers())
        resp.raise_for_status()

    def ensure_shortcut(self, spec: ShortcutSpec) -> dict[str, Any]:
        """Idempotent create — returns existing shortcut if name matches."""
        existing = self.list_shortcuts(spec.workspace_id, spec.item_id)
        for s in existing:
            if s.get("name") == spec.name and s.get("path") == spec.path:
                return s
        return self.create_shortcut(spec)


# ---------------------------------------------------------------------------
# Bulk emission helpers
# ---------------------------------------------------------------------------


@dataclass
class ShortcutPlan:
    """A list of shortcut specs that will be applied as a batch."""

    specs: list[ShortcutSpec] = field(default_factory=list)

    def add(self, spec: ShortcutSpec) -> None:
        self.specs.append(spec)

    def apply(self, client: ShortcutClient) -> list[dict[str, Any]]:
        """Apply every spec idempotently, return the resulting shortcut records."""
        return [client.ensure_shortcut(s) for s in self.specs]

    def to_payload(self) -> list[dict[str, Any]]:
        """Return a JSON-serializable list of create-bodies (for review / CI)."""
        return [s.to_create_body() for s in self.specs]


def practice_reference_shortcuts(
    *,
    tenant_workspace_id: str,
    tenant_lakehouse_id: str,
    practice_reference_workspace_id: str,
    practice_reference_lakehouse_id: str,
    silver_table_names: list[str],
) -> ShortcutPlan:
    """Build a ShortcutPlan for the Practice-reference → Tenant pattern.

    For each canonical Silver table in the Practice-reference workspace,
    creates a OneLake shortcut into the tenant's Silver lakehouse. The
    tenant queries the canonical Silver schema without duplicating data.

    This is the "Bronze stays where it is, canonical Silver lives once"
    materialization that powers APEX scaling — see Sellers Guide §1.6
    canonical kernel and §6.13 file-first / control-plane chapter.

    Args:
        tenant_workspace_id: Tenant workspace ID (the consumer).
        tenant_lakehouse_id: Tenant lakehouse where shortcuts land.
        practice_reference_workspace_id: Source Practice-reference workspace.
        practice_reference_lakehouse_id: Source Practice-reference lakehouse.
        silver_table_names: Canonical table names to shortcut (e.g.,
            ``["scml_sku", "scml_lot", "merml_price", ...]``).

    Returns:
        :class:`ShortcutPlan` ready to apply.
    """
    plan = ShortcutPlan()
    for table_name in silver_table_names:
        plan.add(
            ShortcutSpec(
                workspace_id=tenant_workspace_id,
                item_id=tenant_lakehouse_id,
                name=table_name,
                path="Tables",
                target=OneLakeTarget(
                    workspace_id=practice_reference_workspace_id,
                    item_id=practice_reference_lakehouse_id,
                    path=f"Tables/{table_name}",
                ),
                description=f"APEX Practice-reference shortcut to canonical Silver table {table_name}.",
            )
        )
    return plan
