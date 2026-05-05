"""APEX L1 manifest schemas.

Each module defines one manifest kind as a Pydantic v2 model. The :class:`BaseManifest`
carries the fields common to every kind; specific kinds add their own fields.

Kinds:

- :class:`SchemaManifest` — canonical schema declaration (§5)
- :class:`EventManifest` — event trigger + payload shape (§4.2, §10.1)
- :class:`OrchestrationManifest` — multi-agent composition (§10.4)
- :class:`AgentManifest` — single agent definition (§8)
- :class:`TenantManifest` — L4 client instance (§3.4)
- :class:`PolicyManifest` — HITL / DLP / classification rules (§9, §14)
- :class:`ServiceManifest` — named productised service (§15, §16)
"""

from apex_core.manifests.agent import AgentManifest, ScopeSpec
from apex_core.manifests.base import BaseManifest, ManifestKind
from apex_core.manifests.event import EventManifest, TriggerSpec
from apex_core.manifests.orchestration import (
    AgentRef,
    GatePlacement,
    OrchestrationManifest,
    VersionStamps,
)
from apex_core.manifests.policy import (
    ClassificationMapping,
    DlpRule,
    HitlRule,
    PolicyManifest,
)
from apex_core.manifests.schema import EntitySpec, SchemaManifest
from apex_core.manifests.service import CommercialSpec, ServiceManifest, SloSpec
from apex_core.manifests.tenant import (
    ExtensionRef,
    PolicyOverride,
    PracticePin,
    TenantManifest,
)

__all__ = [
    "AgentManifest",
    "AgentRef",
    "BaseManifest",
    "ClassificationMapping",
    "CommercialSpec",
    "DlpRule",
    "EntitySpec",
    "EventManifest",
    "ExtensionRef",
    "GatePlacement",
    "HitlRule",
    "ManifestKind",
    "OrchestrationManifest",
    "PolicyManifest",
    "PolicyOverride",
    "PracticePin",
    "SchemaManifest",
    "ScopeSpec",
    "ServiceManifest",
    "SloSpec",
    "TenantManifest",
    "TriggerSpec",
    "VersionStamps",
]
