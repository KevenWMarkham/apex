"""Tests for apex_purview.retention — Sprint 13 Task 13.4."""

from __future__ import annotations

import json

import pytest
from typer.testing import CliRunner

from apex_purview._cli import purview_app
from apex_purview.retention import (
    DEFAULT_RETENTION_MATRIX,
    RETENTION_DURATIONS,
    LegalHoldConfig,
    RetentionPolicyBundle,
    RetentionRule,
    _longer_duration,
    build_default_retention_bundle,
    build_retention_with_overrides,
    emit_retention_payload,
    lookup_retention,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# Duration table coverage
# ---------------------------------------------------------------------------


def test_default_matrix_covers_every_classification() -> None:
    from apex_purview.classifications import APEX_CLASSIFICATIONS

    for c in APEX_CLASSIFICATIONS:
        assert c in DEFAULT_RETENTION_MATRIX, f"Missing retention duration for: {c}"


def test_phi_is_ten_years() -> None:
    assert DEFAULT_RETENTION_MATRIX["phi"] == "P10Y"


def test_pci_is_seven_years() -> None:
    assert DEFAULT_RETENTION_MATRIX["pci"] == "P7Y"


def test_restricted_is_permanent() -> None:
    assert DEFAULT_RETENTION_MATRIX["restricted"] == "PERMANENT"


def test_public_is_three_years() -> None:
    assert DEFAULT_RETENTION_MATRIX["public"] == "P3Y"


# ---------------------------------------------------------------------------
# RetentionRule
# ---------------------------------------------------------------------------


def test_rule_rejects_unknown_classification() -> None:
    with pytest.raises(ValueError, match="Unknown classification"):
        RetentionRule(classification="sparklepants", duration="P7Y")


def test_rule_rejects_unknown_duration() -> None:
    with pytest.raises(ValueError, match="Unknown duration"):
        RetentionRule(classification="pii", duration="P99Y")


def test_rule_to_atlas_shape() -> None:
    r = RetentionRule(classification="phi", duration="P10Y")
    payload = r.to_atlas()
    assert payload["classification"] == "APEX.PHI"
    assert payload["duration"] == "P10Y"
    assert payload["durationYears"] == 10
    assert payload["worm"] is True
    assert "HIPAA" in payload["regulatoryBasis"]


def test_rule_to_atlas_permanent_has_null_years() -> None:
    r = RetentionRule(classification="restricted", duration="PERMANENT")
    payload = r.to_atlas()
    assert payload["durationYears"] is None
    assert payload["label"].startswith("Permanent")


def test_rule_to_atlas_custom_regulatory_basis() -> None:
    r = RetentionRule(
        classification="pii",
        duration="P10Y",
        regulatory_basis="CUSTOM-CITATION",
    )
    payload = r.to_atlas()
    assert payload["regulatoryBasis"] == "CUSTOM-CITATION"


# ---------------------------------------------------------------------------
# Longer-duration helper
# ---------------------------------------------------------------------------


def test_longer_duration_year_quantified() -> None:
    assert _longer_duration("P3Y", "P7Y") == "P7Y"
    assert _longer_duration("P10Y", "P3Y") == "P10Y"
    assert _longer_duration("P7Y", "P7Y") == "P7Y"


def test_longer_duration_permanent_dominates() -> None:
    assert _longer_duration("PERMANENT", "P10Y") == "PERMANENT"
    assert _longer_duration("P3Y", "PERMANENT") == "PERMANENT"


# ---------------------------------------------------------------------------
# Bundle
# ---------------------------------------------------------------------------


def test_bundle_add_rule_replaces() -> None:
    b = RetentionPolicyBundle(name="t", description="d")
    b.add_rule("pii", "P3Y")
    b.add_rule("pii", "P10Y")
    assert len(b.rules) == 1
    assert b.rules[0].duration == "P10Y"


def test_build_default_bundle_covers_all() -> None:
    bundle = build_default_retention_bundle()
    payload = emit_retention_payload(bundle)
    assert len(payload["rules"]) == len(DEFAULT_RETENTION_MATRIX)


def test_overrides_never_shorten_below_default() -> None:
    overrides = {"phi": "P3Y"}  # default: P10Y
    bundle = build_retention_with_overrides(overrides)
    rule = next(r for r in bundle.rules if r.classification == "phi")
    assert rule.duration == "P10Y"


def test_overrides_apply_when_longer() -> None:
    overrides = {"internal": "P7Y"}  # default: P3Y
    bundle = build_retention_with_overrides(overrides)
    rule = next(r for r in bundle.rules if r.classification == "internal")
    assert rule.duration == "P7Y"


def test_overrides_permanent_locks_in() -> None:
    overrides = {"pii": "PERMANENT"}
    bundle = build_retention_with_overrides(overrides)
    rule = next(r for r in bundle.rules if r.classification == "pii")
    assert rule.duration == "PERMANENT"


# ---------------------------------------------------------------------------
# Legal hold
# ---------------------------------------------------------------------------


def test_legal_hold_to_atlas_shape() -> None:
    hold = LegalHoldConfig(
        matter_id="LIT-2026-042",
        classifications=("phi", "pii"),
        custodian="legal@deloitte.com",
        started_iso="2026-04-22T00:00:00Z",
        description="Class action discovery hold.",
    )
    payload = hold.to_atlas()
    assert payload["matterId"] == "LIT-2026-042"
    assert "APEX.PHI" in payload["classifications"]
    assert "APEX.PII" in payload["classifications"]
    assert payload["active"] is True


def test_legal_hold_rejects_unknown_classification() -> None:
    hold = LegalHoldConfig(
        matter_id="m",
        classifications=("sparklepants",),
        custodian="x",
        started_iso="2026-01-01T00:00:00Z",
    )
    with pytest.raises(ValueError, match="Unknown classification"):
        hold.to_atlas()


def test_bundle_with_legal_hold() -> None:
    bundle = build_default_retention_bundle()
    bundle.add_legal_hold(
        LegalHoldConfig(
            matter_id="LIT-001",
            classifications=("phi",),
            custodian="x",
            started_iso="2026-01-01T00:00:00Z",
        )
    )
    payload = emit_retention_payload(bundle)
    assert len(payload["legalHolds"]) == 1
    assert payload["legalHolds"][0]["matterId"] == "LIT-001"


# ---------------------------------------------------------------------------
# Lookup
# ---------------------------------------------------------------------------


def test_lookup_retention_normalizes() -> None:
    assert lookup_retention("Trade Secret") == "P7Y"
    assert lookup_retention("trade-secret") == "P7Y"


def test_lookup_retention_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown classification"):
        lookup_retention("sparklepants")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_emit_retention_stdout() -> None:
    result = runner.invoke(purview_app, ["emit-retention"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["rules"]


def test_cli_retention_lookup() -> None:
    result = runner.invoke(purview_app, ["retention-lookup", "phi"])
    assert result.exit_code == 0
    assert "P10Y" in result.stdout
