"""APEX Fabric integration — Sprint 14.

Modules:

- ``workspaces`` (Task 14.2) — workspace REST wrapper + naming-convention enforcement
- ``shortcuts`` (Task 14.4) — OneLake shortcut provisioning for ADLS Gen2 / S3 / GCS / Dataverse / cross-workspace OneLake

Terraform deliverables (Tasks 14.1 + 14.3) live in ``infra/terraform/``.
"""

from __future__ import annotations

from apex_fabric.shortcuts import (
    AdlsGen2Target,
    DataverseTarget,
    GoogleCloudStorageTarget,
    OneLakeTarget,
    S3Target,
    ShortcutClient,
    ShortcutPlan,
    ShortcutSpec,
    practice_reference_shortcuts,
)
from apex_fabric.workspaces import (
    ENVIRONMENTS,
    FABRIC_API_BASE,
    PRACTICES,
    ROLES,
    TokenProvider,
    WorkspaceClient,
    WorkspaceSpec,
    canonical_workspace_name,
    parse_workspace_name,
    validate_workspace_name,
)

__all__ = [
    # workspaces
    "ENVIRONMENTS",
    "FABRIC_API_BASE",
    "PRACTICES",
    "ROLES",
    "TokenProvider",
    "WorkspaceClient",
    "WorkspaceSpec",
    "canonical_workspace_name",
    "parse_workspace_name",
    "validate_workspace_name",
    # shortcuts
    "AdlsGen2Target",
    "DataverseTarget",
    "GoogleCloudStorageTarget",
    "OneLakeTarget",
    "S3Target",
    "ShortcutClient",
    "ShortcutPlan",
    "ShortcutSpec",
    "practice_reference_shortcuts",
]

__version__ = "0.1.0"
