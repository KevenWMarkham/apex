"""APEX-Core provider-neutral protocols.

These protocols are the contract every APEX variant (APEX-M / APEX-G /
APEX-A) and every adapter under `apex-adapters/` must satisfy. They are
deliberately runtime-checkable Python `Protocol` types so duck-typed
implementations (Microsoft, Google, AWS, SaaS adapters) can satisfy them
without inheritance.

The 10 protocols correspond 1:1 with the 10 APEX layers a client
deployment touches:

    AgentRuntime           — where agents execute
    AgentIdentityProvider  — who the agent is, how it authenticates
    SecretStore            — credentials and rotation
    AuditLedger            — append-only decision history
    DataLake               — Bronze/Silver/Gold storage abstraction
    EmbeddingService       — vector embeddings + similarity search
    MessageBus             — pub/sub + activator-style triggers
    SensitivityClassifier  — APEX T1–T4 ↔ provider sensitivity labels
    Observability          — traces, metrics, alerts
    ThreatProtection       — prompt-shield, jailbreak, DLP for AI

See `docs/apex-core/Protocols-Reference.md` for the canonical reference.
"""

from .agent_identity import AgentBlueprint, AgentIdentity, AgentIdentityProvider
from .agent_runtime import AgentInvocation, AgentResponse, AgentRuntime
from .audit_ledger import AuditLedger, AuditRow
from .data_lake import DataLake, DataLakeQuery, DataLakeWrite
from .embedding_service import Embedding, EmbeddingService, SimilarityResult
from .message_bus import Message, MessageBus, Subscription
from .observability import Metric, Observability, TraceContext
from .persona_binding import (
    BindingMode,
    PersonaPrincipalBinding,
    UseCasePersonaBindings,
)
from .secret_store import Secret, SecretReference, SecretStore
from .sensitivity_classifier import ProviderLabel, SensitivityClassifier, SensitivityTier
from .threat_protection import PromptShieldResult, ThreatProtection, ThreatVerdict

__all__ = [
    "AgentBlueprint",
    "AgentIdentity",
    "AgentIdentityProvider",
    "AgentInvocation",
    "AgentResponse",
    "AgentRuntime",
    "AuditLedger",
    "AuditRow",
    "BindingMode",
    "DataLake",
    "DataLakeQuery",
    "DataLakeWrite",
    "Embedding",
    "EmbeddingService",
    "Message",
    "MessageBus",
    "Metric",
    "Observability",
    "PersonaPrincipalBinding",
    "PromptShieldResult",
    "ProviderLabel",
    "Secret",
    "SecretReference",
    "SecretStore",
    "SensitivityClassifier",
    "SensitivityTier",
    "SimilarityResult",
    "Subscription",
    "ThreatProtection",
    "ThreatVerdict",
    "TraceContext",
    "UseCasePersonaBindings",
]
