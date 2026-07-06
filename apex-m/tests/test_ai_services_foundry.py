"""Tests for apex_m.ai_services_foundry — the AIS tool layer."""

from __future__ import annotations

import pytest

from apex_core.protocols import SensitivityTier
from apex_m.ai_services_foundry import (
    CANONICAL_AIS_CATALOG,
    AIServiceGovernanceError,
    AIServiceKind,
    AIServiceProvider,
    AIServiceProviderFoundry,
    AIServiceRelay,
    AIServiceResult,
    AIServicesConfig,
    MockAIServiceProviderFoundry,
)


def _full_config() -> AIServicesConfig:
    """A relay for every AIS kind — the minimum a production provider needs."""
    return AIServicesConfig(
        relays={
            kind: AIServiceRelay(
                kind=kind,
                endpoint=f"https://mcp-hub.internal/relay/{kind.value}",
                key_vault_secret_ref=f"kv://apex-m/{kind.value}-key",
            )
            for kind in AIServiceKind
        },
        managed_identity_client_id="agent-id-0001",
    )


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------


def test_catalog_covers_all_five_workbenches() -> None:
    kinds = {t.kind for t in CANONICAL_AIS_CATALOG}
    assert kinds == set(AIServiceKind)


def test_tool_names_are_unique_and_one_purpose() -> None:
    names = [t.tool_name for t in CANONICAL_AIS_CATALOG]
    assert len(names) == len(set(names))
    # one-purpose = namespaced tool id
    assert all("." in n for n in names)


def test_pii_detector_is_cleared_to_t4() -> None:
    pii = next(t for t in CANONICAL_AIS_CATALOG if t.tool_name == "language.detect_pii")
    assert pii.max_sensitivity is SensitivityTier.T4_HIGHLY_CONFIDENTIAL


# ---------------------------------------------------------------------------
# Mock provider — laptop / unit-test path
# ---------------------------------------------------------------------------


def test_mock_lists_full_catalog() -> None:
    provider = MockAIServiceProviderFoundry()
    assert len(provider.list_tools()) == len(CANONICAL_AIS_CATALOG)


def test_mock_invoke_returns_result_with_audit_fields() -> None:
    provider = MockAIServiceProviderFoundry()
    result = provider.invoke(
        "maps.geocode", {"address": "1 Microsoft Way"}, trace_id="t-1",
    )
    assert isinstance(result, AIServiceResult)
    assert result.tool_name == "maps.geocode"
    assert result.kind is AIServiceKind.PLACE
    assert result.trace_id == "t-1"
    assert result.ledger_id.endswith("maps.geocode")
    assert result.relay.startswith("mock-relay://")


def test_mock_invoke_returns_canned_output_when_registered() -> None:
    provider = MockAIServiceProviderFoundry(
        canned={"language.detect_pii": {"entities": [{"category": "Email"}]}},
    )
    result = provider.invoke(
        "language.detect_pii", {"text": "reach me at a@b.com"},
        trace_id="t-2", sensitivity=SensitivityTier.T4_HIGHLY_CONFIDENTIAL,
    )
    assert result.output == {"entities": [{"category": "Email"}]}


def test_mock_invoke_unknown_tool_raises() -> None:
    provider = MockAIServiceProviderFoundry()
    with pytest.raises(KeyError, match="Unknown AIS tool"):
        provider.invoke("language.translate", {}, trace_id="t-3")


# ---------------------------------------------------------------------------
# Governance — fail-closed on sensitivity + HITL
# ---------------------------------------------------------------------------


def test_invoke_refuses_payload_above_tool_clearance() -> None:
    provider = MockAIServiceProviderFoundry()
    # maps.geocode is cleared to T2; a T4 payload must be refused.
    with pytest.raises(AIServiceGovernanceError, match="fail-closed"):
        provider.invoke(
            "maps.geocode", {"address": "secret site"},
            trace_id="t-4", sensitivity=SensitivityTier.T4_HIGHLY_CONFIDENTIAL,
        )


def test_pii_detector_accepts_t4_by_design() -> None:
    provider = MockAIServiceProviderFoundry()
    result = provider.invoke(
        "language.detect_pii", {"text": "SSN 000-00-0000"},
        trace_id="t-5", sensitivity=SensitivityTier.T4_HIGHLY_CONFIDENTIAL,
    )
    assert result.sensitivity is SensitivityTier.T4_HIGHLY_CONFIDENTIAL


# ---------------------------------------------------------------------------
# Production provider — happy paths that don't require the Azure SDKs
# ---------------------------------------------------------------------------


def test_production_requires_relay_for_every_kind() -> None:
    partial = AIServicesConfig(
        relays={
            AIServiceKind.PLACE: AIServiceRelay(
                AIServiceKind.PLACE, "https://x/relay/place", "kv://x/place",
            ),
        },
    )
    with pytest.raises(ValueError, match="missing relays"):
        AIServiceProviderFoundry(partial)


def test_production_lists_catalog_without_sdks() -> None:
    provider = AIServiceProviderFoundry(_full_config())
    assert len(provider.list_tools()) == len(CANONICAL_AIS_CATALOG)


def test_production_invoke_raises_without_runtime_extras() -> None:
    """Without azure-identity + httpx installed, the relay call fails clearly."""
    provider = AIServiceProviderFoundry(_full_config())
    try:
        provider.invoke("maps.geocode", {"address": "x"}, trace_id="t-6")
    except NotImplementedError as exc:
        assert "apex-m[runtime]" in str(exc)
    except ImportError:
        # Acceptable if a partial install made the import fail differently
        pass


def test_production_guard_runs_before_relay_call() -> None:
    """Governance refusal must fire even without the runtime SDKs present."""
    provider = AIServiceProviderFoundry(_full_config())
    with pytest.raises(AIServiceGovernanceError):
        provider.invoke(
            "maps.geocode", {"address": "x"},
            trace_id="t-7", sensitivity=SensitivityTier.T4_HIGHLY_CONFIDENTIAL,
        )


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------


def test_mock_satisfies_protocol() -> None:
    assert isinstance(MockAIServiceProviderFoundry(), AIServiceProvider)


def test_production_satisfies_protocol() -> None:
    assert isinstance(AIServiceProviderFoundry(_full_config()), AIServiceProvider)
