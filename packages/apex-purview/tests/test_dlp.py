"""Tests for apex_purview.dlp — Sprint 13 Task 13.3."""

from __future__ import annotations

import json

import pytest
from typer.testing import CliRunner

from apex_purview._cli import purview_app
from apex_purview.dlp import (
    ACTIONS,
    DEFAULT_DLP_MATRIX,
    SURFACES,
    DLPPolicyBundle,
    DLPRule,
    DLPViolationAlert,
    action_severity,
    build_bundle_from_overrides,
    build_default_bundle,
    emit_dlp_payload,
    lookup_action,
    most_restrictive,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# Action severity
# ---------------------------------------------------------------------------


def test_action_severity_strict_ordering() -> None:
    ranks = [action_severity(a) for a in ACTIONS]
    assert ranks == sorted(ranks)
    assert action_severity("allow") < action_severity("escalate")


def test_action_severity_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown DLP action"):
        action_severity("nuke_from_orbit")


def test_most_restrictive() -> None:
    assert most_restrictive(["allow", "redact", "mask"]) == "redact"
    assert most_restrictive(["block", "escalate", "allow"]) == "escalate"


def test_most_restrictive_rejects_empty() -> None:
    with pytest.raises(ValueError, match="empty list"):
        most_restrictive([])


# ---------------------------------------------------------------------------
# DLPRule validation
# ---------------------------------------------------------------------------


def test_dlp_rule_rejects_unknown_classification() -> None:
    with pytest.raises(ValueError, match="Unknown classification"):
        DLPRule("sparklepants", "copilot_chat", "redact")


def test_dlp_rule_rejects_unknown_surface() -> None:
    with pytest.raises(ValueError, match="Unknown surface"):
        DLPRule("pii", "telegram", "redact")


def test_dlp_rule_rejects_unknown_action() -> None:
    with pytest.raises(ValueError, match="Unknown action"):
        DLPRule("pii", "copilot_chat", "obliterate")


# ---------------------------------------------------------------------------
# DLPPolicyBundle
# ---------------------------------------------------------------------------


def test_bundle_add_rule_replaces_existing_pair() -> None:
    b = DLPPolicyBundle(name="t", description="t")
    b.add_rule("pii", "copilot_chat", "mask")
    b.add_rule("pii", "copilot_chat", "redact")  # same pair, new action
    assert len(b.rules) == 1
    assert b.rules[0].action == "redact"


def test_bundle_to_atlas_shape() -> None:
    b = DLPPolicyBundle(name="t", description="d")
    b.add_rule("phi", "copilot_chat", "redact")
    payload = b.to_atlas()
    assert payload["name"] == "t"
    assert payload["description"] == "d"
    assert payload["version"] == "1.0"
    assert len(payload["rules"]) == 1
    rule = payload["rules"][0]
    assert rule["classification"] == "APEX.PHI"
    assert rule["surface"] == "copilot_chat"
    assert rule["action"] == "redact"


def test_bundle_with_alerting() -> None:
    alert = DLPViolationAlert(
        webhook_url="https://example.com/dlp",
        severity_threshold="block",
    )
    b = DLPPolicyBundle(name="t", description="d", alerting=alert)
    b.add_rule("pii", "email", "redact")
    payload = b.to_atlas()
    assert payload["alerting"]["webhookUrl"] == "https://example.com/dlp"
    assert payload["alerting"]["severityThreshold"] == "block"
    assert payload["alerting"]["auditStamp"] is True


# ---------------------------------------------------------------------------
# Default matrix coverage
# ---------------------------------------------------------------------------


def test_default_matrix_covers_every_classification_and_surface() -> None:
    from apex_purview.classifications import APEX_CLASSIFICATIONS

    for c in APEX_CLASSIFICATIONS:
        assert c in DEFAULT_DLP_MATRIX, f"Missing classification: {c}"
        for s in SURFACES:
            assert s in DEFAULT_DLP_MATRIX[c], f"Missing surface {s} for {c}"


def test_build_default_bundle_creates_full_grid() -> None:
    bundle = build_default_bundle()
    payload = emit_dlp_payload(bundle)
    expected = sum(len(s) for s in DEFAULT_DLP_MATRIX.values())
    assert len(payload["rules"]) == expected


def test_default_matrix_phi_blocks_email_and_public_web() -> None:
    assert DEFAULT_DLP_MATRIX["phi"]["email"] == "block"
    assert DEFAULT_DLP_MATRIX["phi"]["public_web"] == "block"


def test_default_matrix_restricted_escalates() -> None:
    assert DEFAULT_DLP_MATRIX["restricted"]["copilot_chat"] == "escalate"


def test_default_matrix_public_allows_everywhere() -> None:
    for s in SURFACES:
        assert DEFAULT_DLP_MATRIX["public"][s] == "allow"


# ---------------------------------------------------------------------------
# Override builder — never relax
# ---------------------------------------------------------------------------


def test_overrides_never_relax_below_default() -> None:
    """A weaker override is silently strengthened to default."""
    overrides = {"phi": {"copilot_chat": "allow"}}  # default: redact
    bundle = build_bundle_from_overrides(overrides)
    rule = next(
        r for r in bundle.rules if r.classification == "phi" and r.surface == "copilot_chat"
    )
    assert rule.action == "redact"  # default wins


def test_overrides_apply_when_more_restrictive() -> None:
    overrides = {"internal": {"copilot_chat": "block"}}  # default: allow
    bundle = build_bundle_from_overrides(overrides)
    rule = next(
        r for r in bundle.rules if r.classification == "internal" and r.surface == "copilot_chat"
    )
    assert rule.action == "block"


# ---------------------------------------------------------------------------
# lookup_action
# ---------------------------------------------------------------------------


def test_lookup_action_normalizes_keys() -> None:
    assert lookup_action("Trade Secret", "email") == "block"
    assert lookup_action("trade-secret", "email") == "block"


def test_lookup_action_rejects_unknown_classification() -> None:
    with pytest.raises(ValueError, match="Unknown classification"):
        lookup_action("sparklepants", "copilot_chat")


def test_lookup_action_rejects_unknown_surface() -> None:
    with pytest.raises(ValueError, match="Unknown surface"):
        lookup_action("pii", "telegram")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_emit_dlp_stdout() -> None:
    result = runner.invoke(purview_app, ["emit-dlp"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["rules"]


def test_cli_dlp_lookup() -> None:
    result = runner.invoke(purview_app, ["dlp-lookup", "phi", "email"])
    assert result.exit_code == 0
    assert "block" in result.stdout
