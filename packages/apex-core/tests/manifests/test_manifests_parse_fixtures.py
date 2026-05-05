"""Round-trip tests: every fixture YAML parses via its Pydantic model."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from apex_core.manifests import (
    AgentManifest,
    BaseManifest,
    EventManifest,
    OrchestrationManifest,
    PolicyManifest,
    SchemaManifest,
    ServiceManifest,
    TenantManifest,
)

FIXTURES = Path(__file__).parent.parent / "fixtures"

_CASES: list[tuple[str, type[BaseManifest]]] = [
    ("schema_scml.yaml", SchemaManifest),
    ("event_cold_chain.yaml", EventManifest),
    ("agent_cold_chain_disposition.yaml", AgentManifest),
    ("orchestration_cold_chain_response.yaml", OrchestrationManifest),
    ("tenant_acme_grocery.yaml", TenantManifest),
    ("policy_rc_default.yaml", PolicyManifest),
    ("service_cold_chain.yaml", ServiceManifest),
]


@pytest.mark.parametrize("filename,model_cls", _CASES)
def test_fixture_parses(filename: str, model_cls: type[BaseManifest]) -> None:
    path = FIXTURES / filename
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    instance = model_cls.model_validate(raw)
    assert instance.name  # non-empty identifier
    assert instance.semver().major >= 0


def test_agent_scope_defaults() -> None:
    raw = yaml.safe_load((FIXTURES / "agent_cold_chain_disposition.yaml").read_text())
    agent = AgentManifest.model_validate(raw)
    assert agent.scope.practice is not None
    assert "internal" in agent.scope.classification_visibility


def test_orchestration_stamps_required() -> None:
    raw = yaml.safe_load(
        (FIXTURES / "orchestration_cold_chain_response.yaml").read_text()
    )
    orch = OrchestrationManifest.model_validate(raw)
    assert orch.stamps.manifest_version
    assert orch.stamps.policy_version
    assert orch.stamps.prompt_version
