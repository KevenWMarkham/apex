"""APEX-M AI Services provider — the Azure AI Services (AIS) tool layer.

The AIS workbenches surface five Azure AI Services to an APEX agent as
**MCP tools behind key-holding relays**: the agent's toolbelt is Gold
virtual views (data tools) *plus* these AI-service tools. Every tool is
one-purpose (per the APEX MCP boundary), the owning relay authenticates
with the agent's Microsoft Entra Agent ID / managed identity, and the
service key **never leaves the relay** (it is resolved from Azure Key
Vault by the relay, not handed to the agent).

The five workbenches → Azure services:

    Realtime voice  — Azure AI Foundry Voice Live API (gpt-realtime / -mini)
                      + Azure AI Speech (ASR + neural TTS + real-time
                      text-to-speech talking avatar over WebRTC)
    Language        — Azure AI Language (sentiment · key phrases · NER ·
                      PII · entity linking · summarization)
    Vision          — Azure AI Vision, Image Analysis 4.0 (Florence)
    Documents       — Azure AI Document Intelligence (invoice · receipt ·
                      ID · contract · layout · custom)
    Place           — Azure Maps (geocode · route · isochrone · traffic ·
                      weather · time zone)

Provider-neutral by construction — the :class:`AIServiceProvider` protocol
is what APEX-G (Google: Speech · Cloud NL · Vision · Document AI · Maps)
and APEX-A (AWS: Transcribe+Polly · Comprehend · Rekognition · Textract ·
Location Service) implement in turn. Like ``persona_resolver``, the
protocol lives in the variant package rather than the 10-protocol core
contract: AIS is a capability layer a variant *may* ship, not one of the
10 infrastructure layers every deployment touches.

Governance is not bypassed by adding tools:

- ``language.detect_pii`` is the pre/post-processing guardrail — run it on
  text before it reaches the model or the ledger.
- Every ``invoke`` refuses payloads above the tool's ``max_sensitivity``
  (fail-closed) and emits an audit row for the hash-chained ledger.
- Content flowing through vision/voice/language is screened by Azure AI
  Content Safety + Prompt Shields (see ``threat_defender``).
- AIS tools are perception/analysis only — they never write back. Any
  write-back an agent performs *after* reasoning over an AIS result still
  passes the single HITL gate at step 16 in the runtime, not here.

Lazy import strategy
====================

This module imports cleanly without the Azure AI SDKs installed — real
service calls happen lazily inside :class:`AIServiceProviderFoundry`,
behind ``apex-m[runtime]``. :class:`MockAIServiceProviderFoundry` satisfies
the same contract for laptop substrate + unit tests.

Reference: https://learn.microsoft.com/azure/ai-services/speech-service/voice-live
Reference: https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar
Reference: https://learn.microsoft.com/azure/ai-services/language-service/overview
Reference: https://learn.microsoft.com/azure/ai-services/computer-vision/overview-image-analysis
Reference: https://learn.microsoft.com/azure/ai-services/document-intelligence/overview
Reference: https://learn.microsoft.com/azure/azure-maps/about-azure-maps
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Protocol, runtime_checkable

from apex_core.protocols import SensitivityTier


# ---------------------------------------------------------------------------
# Tool taxonomy
# ---------------------------------------------------------------------------


class AIServiceKind(str, Enum):
    """The five AIS workbenches, provider-neutral."""

    VOICE_REALTIME = "voice_realtime"   # Voice Live API + Azure AI Speech
    LANGUAGE = "language"               # Azure AI Language
    VISION = "vision"                   # Azure AI Vision (Image Analysis 4.0)
    DOCUMENT = "document"               # Azure AI Document Intelligence
    PLACE = "place"                     # Azure Maps


# Highest APEX tier a tool is cleared to process. `invoke` fails closed when
# a payload's sensitivity exceeds this — e.g. general captioning must not be
# handed T4 regulated imagery, while the PII detector is cleared to T4 by
# design because screening PII *is* its purpose.
_TIER_RANK = {
    SensitivityTier.T1_PUBLIC: 1,
    SensitivityTier.T2_INTERNAL: 2,
    SensitivityTier.T3_CONFIDENTIAL: 3,
    SensitivityTier.T4_HIGHLY_CONFIDENTIAL: 4,
}


@dataclass(frozen=True)
class AIServiceTool:
    """One-purpose MCP tool descriptor for an AIS capability.

    ``tool_name`` is the MCP tool id the agent calls; ``azure_operation`` is
    the concrete service operation the owning relay invokes with its
    Key-Vault-held key.
    """

    kind: AIServiceKind
    tool_name: str                 # MCP one-purpose tool id, e.g. "language.detect_pii"
    azure_operation: str           # concrete Azure op the relay calls
    description: str
    max_sensitivity: SensitivityTier  # highest APEX tier this tool may process
    requires_hitl: bool = False    # AIS tools perceive/analyse; write-backs gate in the runtime


@dataclass(frozen=True)
class AIServiceResult:
    """Result of one AIS tool call.

    Carries the audit fields the hash-chained ledger records for every
    AI-service tool call.
    """

    tool_name: str
    kind: AIServiceKind
    output: dict[str, Any]
    trace_id: str
    relay: str                     # which key-holding relay served the call
    invoked_at: datetime
    ledger_id: str
    sensitivity: SensitivityTier
    notes: str = ""


# ---------------------------------------------------------------------------
# Relay + provider configuration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AIServiceRelay:
    """A key-holding relay in front of one Azure AI Service.

    The agent calls the relay endpoint authenticated with its Entra Agent
    ID / managed identity; the relay resolves the service key from Key Vault
    (``key_vault_secret_ref``) and injects it. The key is never returned to,
    or visible to, the agent.
    """

    kind: AIServiceKind
    endpoint: str                  # relay URL (mcp-hub route), not the raw Azure endpoint
    key_vault_secret_ref: str      # Key Vault secret the relay reads; agent never sees it


@dataclass(frozen=True)
class AIServicesConfig:
    """Tenant configuration binding each AIS kind to its relay."""

    relays: dict[AIServiceKind, AIServiceRelay]
    voice_live_model: str = "gpt-realtime"   # or gpt-realtime-mini
    managed_identity_client_id: str | None = None  # Entra Agent ID the relays trust


# The canonical AIS tool catalog — one-purpose tools per the MCP boundary.
# max_sensitivity is conservative: the PII detector and Document Intelligence
# are cleared to T4 because screening regulated content is their job; general
# perception tops out at T3.
CANONICAL_AIS_CATALOG: tuple[AIServiceTool, ...] = (
    # Realtime voice — Voice Live API + Azure AI Speech
    AIServiceTool(
        AIServiceKind.VOICE_REALTIME, "voice.realtime_session",
        "foundry.voice_live.open_session",
        "Open a speech-to-speech Voice Live session; toolBridge lets the "
        "voice agent call sibling AIS tools mid-conversation.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    AIServiceTool(
        AIServiceKind.VOICE_REALTIME, "voice.transcribe", "speech.stt.recognize",
        "Speech-to-text (ASR) over an audio payload.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    AIServiceTool(
        AIServiceKind.VOICE_REALTIME, "voice.synthesize", "speech.tts.synthesize",
        "Neural text-to-speech.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    AIServiceTool(
        AIServiceKind.VOICE_REALTIME, "voice.avatar_session",
        "speech.tts.avatar.realtime",
        "Open a real-time text-to-speech talking-avatar session — an animated "
        "video face lip-synced to neural TTS, streamed over WebRTC. The relay "
        "fetches the ICE/relay token so the Speech key stays server-side.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    # Language — Azure AI Language
    AIServiceTool(
        AIServiceKind.LANGUAGE, "language.detect_pii", "language.analyze_text.pii",
        "Detect + redact PII. The pre/post-processing guardrail — run before "
        "text reaches the model or the ledger.",
        SensitivityTier.T4_HIGHLY_CONFIDENTIAL,
    ),
    AIServiceTool(
        AIServiceKind.LANGUAGE, "language.analyze_sentiment",
        "language.analyze_text.sentiment", "Sentiment + opinion mining.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    AIServiceTool(
        AIServiceKind.LANGUAGE, "language.extract_key_phrases",
        "language.analyze_text.keyPhrases", "Key-phrase extraction.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    AIServiceTool(
        AIServiceKind.LANGUAGE, "language.recognize_entities",
        "language.analyze_text.entityRecognition",
        "Named-entity recognition + entity linking.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    AIServiceTool(
        AIServiceKind.LANGUAGE, "language.summarize",
        "language.analyze_text.summarization",
        "Extractive + abstractive summarization.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    # Vision — Azure AI Vision, Image Analysis 4.0 (Florence)
    AIServiceTool(
        AIServiceKind.VISION, "vision.analyze_image", "vision.imageAnalysis.analyze",
        "Caption, tags, object + people detection, smart crops.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    AIServiceTool(
        AIServiceKind.VISION, "vision.read_ocr", "vision.imageAnalysis.read",
        "OCR — read printed + handwritten text from an image.",
        SensitivityTier.T3_CONFIDENTIAL,
    ),
    # Documents — Azure AI Document Intelligence
    AIServiceTool(
        AIServiceKind.DOCUMENT, "document.analyze", "documentIntelligence.analyze",
        "Extract structured fields from invoice / receipt / ID / contract / "
        "health-insurance-card / layout, or a custom-trained model.",
        SensitivityTier.T4_HIGHLY_CONFIDENTIAL,
    ),
    # Place — Azure Maps
    AIServiceTool(
        AIServiceKind.PLACE, "maps.geocode", "maps.search.geocode",
        "Address ↔ coordinate geocoding.",
        SensitivityTier.T2_INTERNAL,
    ),
    AIServiceTool(
        AIServiceKind.PLACE, "maps.route", "maps.route.directions",
        "Routing + traffic-aware directions.",
        SensitivityTier.T2_INTERNAL,
    ),
    AIServiceTool(
        AIServiceKind.PLACE, "maps.isochrone", "maps.route.range",
        "Reachable-range (isochrone) polygons.",
        SensitivityTier.T2_INTERNAL,
    ),
    AIServiceTool(
        AIServiceKind.PLACE, "maps.timezone", "maps.timezone.byCoordinates",
        "Time zone + weather + IP-geolocation lookups.",
        SensitivityTier.T2_INTERNAL,
    ),
)


class AIServiceGovernanceError(RuntimeError):
    """Raised when an ``invoke`` is refused for governance reasons.

    Either the payload sensitivity exceeds the tool's clearance, or an
    ungated write-back was attempted.
    """


def _guard(tool: AIServiceTool, sensitivity: SensitivityTier, hitl_approved: bool) -> None:
    """Fail-closed governance check shared by every provider impl."""
    if _TIER_RANK[sensitivity] > _TIER_RANK[tool.max_sensitivity]:
        raise AIServiceGovernanceError(
            f"Tool {tool.tool_name!r} is cleared to {tool.max_sensitivity.value}; "
            f"payload is {sensitivity.value}. Refused (fail-closed). Route "
            f"{sensitivity.value} content through a tool cleared for it, or "
            f"redact via language.detect_pii first."
        )
    if tool.requires_hitl and not hitl_approved:
        raise AIServiceGovernanceError(
            f"Tool {tool.tool_name!r} requires HITL approval (step-16 gate) "
            f"before it runs."
        )


# ---------------------------------------------------------------------------
# Protocol — the contract APEX-G + APEX-A also implement
# ---------------------------------------------------------------------------


@runtime_checkable
class AIServiceProvider(Protocol):
    """Enumerate + invoke AIS tools behind key-holding relays.

    Implementations:

    - :class:`AIServiceProviderFoundry` — APEX-M, Azure AI Services
    - APEX-G ``AIServiceProviderVertex`` (future) — Google Cloud AI
    - APEX-A ``AIServiceProviderBedrock`` (future) — AWS AI
    - :class:`MockAIServiceProviderFoundry` — laptop / unit-test substrate
    """

    variant: str

    def list_tools(self) -> list[AIServiceTool]:
        """The AIS tools this provider exposes to the agent's toolbelt."""
        ...

    def invoke(
        self,
        tool_name: str,
        payload: dict[str, Any],
        *,
        trace_id: str,
        sensitivity: SensitivityTier = SensitivityTier.T2_INTERNAL,
        hitl_approved: bool = False,
    ) -> AIServiceResult:
        """Call one AIS tool through its relay and return the result.

        Fail-closed on sensitivity / HITL via :func:`_guard`; the returned
        result carries the audit fields for the ledger.
        """
        ...


# ---------------------------------------------------------------------------
# APEX-M production provider (Azure AI Services)
# ---------------------------------------------------------------------------


class AIServiceProviderFoundry:
    """Concrete :class:`AIServiceProvider` for APEX-M.

    Ships the tool catalog + governance dispatch. The Azure AI SDK calls are
    lazy-imported behind ``apex-m[runtime]``; until they are wired the
    dispatch raises :class:`NotImplementedError` with a clear hint. The mock
    provider covers the test + laptop path.
    """

    variant = "APEX-M"

    def __init__(
        self,
        config: AIServicesConfig,
        *,
        catalog: tuple[AIServiceTool, ...] = CANONICAL_AIS_CATALOG,
    ) -> None:
        self.config = config
        self._catalog = catalog
        self._by_name = {t.tool_name: t for t in catalog}
        missing = {t.kind for t in catalog} - set(config.relays)
        if missing:
            raise ValueError(
                "AIServicesConfig is missing relays for kinds "
                f"{sorted(k.value for k in missing)}. Every tool kind needs a "
                "key-holding relay."
            )

    def list_tools(self) -> list[AIServiceTool]:
        return list(self._catalog)

    def invoke(
        self,
        tool_name: str,
        payload: dict[str, Any],
        *,
        trace_id: str,
        sensitivity: SensitivityTier = SensitivityTier.T2_INTERNAL,
        hitl_approved: bool = False,
    ) -> AIServiceResult:
        tool = self._by_name.get(tool_name)
        if tool is None:
            raise KeyError(
                f"Unknown AIS tool {tool_name!r}. Known: "
                f"{sorted(self._by_name)}"
            )
        _guard(tool, sensitivity, hitl_approved)
        relay = self.config.relays[tool.kind]
        return self._call_relay(tool, relay, payload, trace_id, sensitivity)

    def _call_relay(
        self,
        tool: AIServiceTool,
        relay: AIServiceRelay,
        payload: dict[str, Any],
        trace_id: str,
        sensitivity: SensitivityTier,
    ) -> AIServiceResult:
        try:
            import httpx                       # type: ignore[import-not-found]
            from azure.identity import DefaultAzureCredential  # type: ignore[import-not-found]
        except ImportError:                     # pragma: no cover — unit-test path
            raise NotImplementedError(
                "AIServiceProviderFoundry._call_relay requires apex-m[runtime] "
                "extras (azure-identity + httpx). Use "
                "MockAIServiceProviderFoundry in non-Lab environments."
            )

        # The relay — not the agent — holds the service key. We authenticate
        # to the relay with the agent's managed identity / Entra Agent ID and
        # send only the operation + payload; the relay injects the Key-Vault
        # key (relay.key_vault_secret_ref) before it calls Azure.
        cred = DefaultAzureCredential(
            managed_identity_client_id=self.config.managed_identity_client_id,
        )
        token = cred.get_token("https://cognitiveservices.azure.com/.default").token
        headers = {"Authorization": f"Bearer {token}", "x-apex-trace-id": trace_id}
        body = {"operation": tool.azure_operation, "payload": payload}
        with httpx.Client(timeout=60.0) as client:  # pragma: no cover
            resp = client.post(relay.endpoint, json=body, headers=headers)
            resp.raise_for_status()
            output = resp.json()
        return AIServiceResult(
            tool_name=tool.tool_name,
            kind=tool.kind,
            output=output,
            trace_id=trace_id,
            relay=relay.endpoint,
            invoked_at=datetime.now(UTC),
            ledger_id=f"aisvc-{trace_id}-{tool.tool_name}",
            sensitivity=sensitivity,
        )


# ---------------------------------------------------------------------------
# Mock — laptop / unit-test provider
# ---------------------------------------------------------------------------


@dataclass
class MockAIServiceProviderFoundry:
    """Test / laptop provider for the AIS tool layer.

    Returns deterministic canned results per tool while still enforcing the
    same governance guard as production.
    """

    variant: str = "APEX-M-mock"
    catalog: tuple[AIServiceTool, ...] = CANONICAL_AIS_CATALOG
    canned: dict[str, dict[str, Any]] = field(default_factory=dict)

    def list_tools(self) -> list[AIServiceTool]:
        return list(self.catalog)

    def invoke(
        self,
        tool_name: str,
        payload: dict[str, Any],
        *,
        trace_id: str,
        sensitivity: SensitivityTier = SensitivityTier.T2_INTERNAL,
        hitl_approved: bool = False,
    ) -> AIServiceResult:
        by_name = {t.tool_name: t for t in self.catalog}
        tool = by_name.get(tool_name)
        if tool is None:
            raise KeyError(f"Unknown AIS tool {tool_name!r}. Known: {sorted(by_name)}")
        _guard(tool, sensitivity, hitl_approved)
        output = self.canned.get(
            tool_name, {"mock": True, "tool": tool_name, "echo": payload}
        )
        return AIServiceResult(
            tool_name=tool.tool_name,
            kind=tool.kind,
            output=output,
            trace_id=trace_id,
            relay=f"mock-relay://{tool.kind.value}",
            invoked_at=datetime.now(UTC),
            ledger_id=f"mock-aisvc-{trace_id}-{tool.tool_name}",
            sensitivity=sensitivity,
            notes="MOCK — no Azure call made",
        )


__all__ = [
    "AIServiceKind",
    "AIServiceTool",
    "AIServiceResult",
    "AIServiceRelay",
    "AIServicesConfig",
    "CANONICAL_AIS_CATALOG",
    "AIServiceGovernanceError",
    "AIServiceProvider",
    "AIServiceProviderFoundry",
    "MockAIServiceProviderFoundry",
]
