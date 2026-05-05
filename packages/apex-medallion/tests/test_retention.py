"""Tests for ``apex_medallion.bronze.retention``."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from apex_core.types import Classification, Practice
from apex_medallion import (
    RetentionPolicy,
    build_purview_retention_payload,
)


class TestRetentionPolicy:
    def test_default_is_seven_years(self) -> None:
        p = RetentionPolicy()
        assert p.duration_days == 7 * 365
        assert p.legal_hold is False

    def test_hls_default_is_ten_years(self) -> None:
        p = RetentionPolicy.default_for_practice(Practice.HLS)
        assert p.duration_days == 10 * 365
        assert p.practice is Practice.HLS

    def test_non_hls_default_is_seven_years(self) -> None:
        assert RetentionPolicy.default_for_practice(Practice.RC).duration_days == 7 * 365
        assert RetentionPolicy.default_for_practice(Practice.ER).duration_days == 7 * 365

    def test_effective_duration_with_override(self) -> None:
        p = RetentionPolicy(
            duration_days=7 * 365,
            classification_overrides={Classification.PHI: 10 * 365},
        )
        assert p.effective_duration_days(Classification.INTERNAL) == 7 * 365
        assert p.effective_duration_days(Classification.PHI) == 10 * 365

    def test_legal_hold_expiry_requires_legal_hold(self) -> None:
        with pytest.raises(ValidationError):
            RetentionPolicy(
                legal_hold=False,
                legal_hold_expires=datetime(2030, 1, 1, tzinfo=UTC),
            )

    def test_legal_hold_with_expiry_ok(self) -> None:
        p = RetentionPolicy(
            legal_hold=True,
            legal_hold_expires=datetime(2030, 1, 1, tzinfo=UTC),
        )
        assert p.legal_hold is True


class TestPurviewPayload:
    def test_minimal(self) -> None:
        policy = RetentionPolicy()
        payload = build_purview_retention_payload(
            policy, asset_path="OneLake/bronze/scml/sku",
        )
        assert payload["asset_path"] == "OneLake/bronze/scml/sku"
        assert payload["retention"]["duration_days"] == 7 * 365
        assert payload["retention"]["legal_hold"] is False

    def test_with_overrides(self) -> None:
        policy = RetentionPolicy(
            practice=Practice.HLS,
            classification_overrides={Classification.PHI: 3650},
            notes="HIPAA-aligned",
        )
        payload = build_purview_retention_payload(policy, asset_path="OneLake/hls/patient")
        assert payload["practice"] == "hls"
        assert payload["retention"]["per_classification"]["phi"] == 3650
        assert payload["notes"] == "HIPAA-aligned"

    def test_legal_hold_expiry_serialised_when_present(self) -> None:
        policy = RetentionPolicy(
            legal_hold=True,
            legal_hold_expires=datetime(2030, 1, 1, tzinfo=UTC),
        )
        payload = build_purview_retention_payload(policy, asset_path="x")
        assert "legal_hold_expires" in payload["retention"]
        assert payload["retention"]["legal_hold_expires"].startswith("2030-01-01")
