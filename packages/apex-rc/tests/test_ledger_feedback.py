"""Tests for apex_rc.ledger_feedback (Sprint 40 item 40.2)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from apex_rc.ledger_feedback import (
    ALL_SERVICES,
    FusionBucket,
    LedgerRow,
    SimilarityQuery,
    all_redis_keys_for_row,
    attribute_realised_outcome,
    canonicalise_risk_class,
    compute_fusion_bucket,
    compute_similarity_score,
    fusion_bucket_redis_key,
    make_ledger_row_for_service,
    realisation_delta_pct,
    retrieve_similar,
    service_local_redis_keys,
)


# ---------------------------------------------------------------------------
# Risk-class canonicalisation
# ---------------------------------------------------------------------------


def test_canonicalise_risk_class_maps_all_5_services_high() -> None:
    """All 5 services have a 'high' canonical class for their top risk band."""
    assert canonicalise_risk_class("RC-E2E-03", "critical") == "high"
    assert canonicalise_risk_class("RC-E2E-04", "high") == "high"
    assert canonicalise_risk_class("RC-E2E-05", "P0_critical") == "high"
    assert canonicalise_risk_class("RC-E2E-07", "high") == "high"
    assert canonicalise_risk_class("RC-E2E-09", "I") == "high"


def test_canonicalise_risk_class_maps_low_band() -> None:
    assert canonicalise_risk_class("RC-E2E-03", "monitor_only") == "low"
    assert canonicalise_risk_class("RC-E2E-04", "low") == "low"
    assert canonicalise_risk_class("RC-E2E-05", "deferred") == "low"
    assert canonicalise_risk_class("RC-E2E-07", "low") == "low"
    assert canonicalise_risk_class("RC-E2E-09", "no_recall") == "low"


def test_canonicalise_risk_class_unknown_raises_keyerror() -> None:
    """Production fail-closed — unknown class raises clearly."""
    with pytest.raises(KeyError):
        canonicalise_risk_class("RC-E2E-03", "ultra-mega")


def test_canonicalise_risk_class_unknown_service_raises() -> None:
    with pytest.raises(KeyError):
        canonicalise_risk_class("RC-E2E-XYZ", "high")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Fusion bucket composite key
# ---------------------------------------------------------------------------


def test_fusion_bucket_composite_key_is_deterministic() -> None:
    bucket = FusionBucket(
        category="dairy", season_quarter="2026-Q2",
        loyalty_tier_distribution="platinum_dominant",
        risk_class_canonical="high",
    )
    expected = "fusion::dairy::2026-Q2::platinum_dominant::high"
    assert bucket.composite_key() == expected


def test_compute_fusion_bucket_q2() -> None:
    """Apr–Jun timestamps land in Q2."""
    ts = datetime(2026, 5, 10, 12, 0, 0, tzinfo=UTC)
    bucket = compute_fusion_bucket(
        "RC-E2E-03",
        category="dairy",
        decision_at=ts,
        loyalty_tier_distribution="platinum_dominant",
        service_local_risk_class="moderate",
    )
    assert bucket.season_quarter == "2026-Q2"
    assert bucket.risk_class_canonical == "medium"


def test_compute_fusion_bucket_q1_q3_q4() -> None:
    for month, q in [(1, 1), (3, 1), (4, 2), (7, 3), (10, 4), (12, 4)]:
        ts = datetime(2026, month, 15, tzinfo=UTC)
        bucket = compute_fusion_bucket(
            "RC-E2E-03", category="dairy", decision_at=ts,
            loyalty_tier_distribution="mixed",
            service_local_risk_class="severe",
        )
        assert bucket.season_quarter == f"2026-Q{q}", (
            f"month={month} should be Q{q}, got {bucket.season_quarter}"
        )


# ---------------------------------------------------------------------------
# LedgerRow construction + Redis key indexing
# ---------------------------------------------------------------------------


_DEFAULT_MEDIUM_RISK_CLASS_PER_SERVICE = {
    "RC-E2E-03": "moderate",
    "RC-E2E-04": "medium",
    "RC-E2E-05": "P2_medium",
    "RC-E2E-07": "medium",
    "RC-E2E-09": "II",
}


def _make_row(
    service_code: str = "RC-E2E-03",
    risk_class: str | None = None,
    category: str = "dairy",
) -> LedgerRow:
    # Default to the per-service "medium" canonical class so the fusion
    # bucket lands in the same risk_class_canonical regardless of service.
    if risk_class is None:
        risk_class = _DEFAULT_MEDIUM_RISK_CLASS_PER_SERVICE[service_code]
    return make_ledger_row_for_service(
        service_code=service_code,  # type: ignore[arg-type]
        decision_id=f"DEC-{service_code}-001",
        trace_id="trace-fusion-001",
        decision_kind="markdown_proposal",
        service_local_outcome_class="approved",
        service_local_risk_class=risk_class,
        category=category,
        loyalty_tier_distribution="platinum_dominant",
        decision_at=datetime(2026, 5, 10, tzinfo=UTC),
        expected_outcome_value_usd=142.0,
        audit_row_outputs_hash="hash-abc-001",
        operator_principal="marisol.reyes@labtenant.onmicrosoft.com",
        persona_id="marisol-reyes-store-ops",
    )


def test_make_ledger_row_for_service_populates_fusion_bucket() -> None:
    row = _make_row()
    assert row.service_code == "RC-E2E-03"
    assert row.fusion_bucket.category == "dairy"
    assert row.fusion_bucket.season_quarter == "2026-Q2"
    assert row.fusion_bucket.risk_class_canonical == "medium"


def test_all_redis_keys_for_row_includes_local_and_fusion() -> None:
    row = _make_row()
    keys = all_redis_keys_for_row(row)
    # At least the fusion key
    assert any(k.startswith("fusion::") for k in keys)
    # And the per-service local keys
    assert any(k.startswith("local::RC-E2E-03::") for k in keys)


def test_service_local_redis_keys_carry_service_code() -> None:
    row = _make_row(service_code="RC-E2E-04")
    keys = service_local_redis_keys(row)
    for k in keys:
        assert "RC-E2E-04" in k


# ---------------------------------------------------------------------------
# Cross-service similarity retrieval
# ---------------------------------------------------------------------------


def _query_for(bucket: FusionBucket) -> SimilarityQuery:
    return SimilarityQuery(
        fusion_bucket=bucket,
        requesting_service="RC-E2E-03",
        requesting_decision_kind="markdown_proposal",
        max_results=10,
    )


def test_similarity_score_exact_fusion_match() -> None:
    row = _make_row()
    query = _query_for(row.fusion_bucket)
    score = compute_similarity_score(query, row)
    # All 4 dimensions match + not realised → 0.40 + 0.20 + 0.20 + 0.10 = 0.90
    assert score == pytest.approx(0.90)


def test_similarity_score_realised_row_gets_extra_weight() -> None:
    row = attribute_realised_outcome(
        _make_row(),
        realised_value_usd=128.0,
        realised_at=datetime(2026, 8, 10, tzinfo=UTC),
    )
    query = _query_for(row.fusion_bucket)
    score = compute_similarity_score(query, row)
    assert score == pytest.approx(1.00)


def test_similarity_score_partial_match_lower() -> None:
    row = _make_row(risk_class="critical")
    different_bucket = FusionBucket(
        category="produce",                    # different
        season_quarter="2026-Q2",              # same
        loyalty_tier_distribution="mixed",     # different
        risk_class_canonical="high",           # same
    )
    query = _query_for(different_bucket)
    score = compute_similarity_score(query, row)
    # Same season + same canonical risk = 0.20 + 0.20 = 0.40
    assert score == pytest.approx(0.40)


def test_retrieve_similar_returns_sorted_top_n() -> None:
    """retrieve_similar sorts by score descending and respects max_results."""
    base_bucket = FusionBucket(
        category="dairy", season_quarter="2026-Q2",
        loyalty_tier_distribution="platinum_dominant",
        risk_class_canonical="medium",
    )
    candidates = [
        _make_row(service_code="RC-E2E-03"),                      # exact match
        _make_row(service_code="RC-E2E-04"),                      # exact match
        _make_row(service_code="RC-E2E-09", category="produce"),  # partial
    ]
    results = retrieve_similar(_query_for(base_bucket), candidates)
    assert len(results) == 3
    # Sorted descending
    scores = [r.similarity_score for r in results]
    assert scores == sorted(scores, reverse=True)
    # Top result is one of the exact matches
    assert results[0].similarity_score >= 0.90


def test_retrieve_similar_only_realised_filter() -> None:
    realised = attribute_realised_outcome(
        _make_row(service_code="RC-E2E-03"),
        realised_value_usd=128.0,
        realised_at=datetime(2026, 8, 10, tzinfo=UTC),
    )
    not_realised = _make_row(service_code="RC-E2E-04")
    query = SimilarityQuery(
        fusion_bucket=realised.fusion_bucket,
        requesting_service="RC-E2E-03",
        requesting_decision_kind="markdown_proposal",
        max_results=10,
        only_realised=True,
    )
    results = retrieve_similar(query, [realised, not_realised])
    assert len(results) == 1
    assert results[0].row.realised_outcome_value_usd is not None


def test_similarity_rationale_includes_source_service() -> None:
    row = _make_row(service_code="RC-E2E-09")
    query = _query_for(row.fusion_bucket)
    results = retrieve_similar(query, [row])
    assert "src=RC-E2E-09" in results[0].similarity_rationale


# ---------------------------------------------------------------------------
# Realised-outcome attribution
# ---------------------------------------------------------------------------


def test_attribute_realised_outcome_returns_new_immutable_row() -> None:
    row = _make_row()
    assert row.realised_outcome_value_usd is None
    updated = attribute_realised_outcome(
        row, realised_value_usd=128.0,
        realised_at=datetime(2026, 8, 10, tzinfo=UTC),
    )
    assert updated.realised_outcome_value_usd == 128.0
    assert updated.realised_at == datetime(2026, 8, 10, tzinfo=UTC)
    # Original row unchanged (frozen dataclass replace semantics)
    assert row.realised_outcome_value_usd is None


def test_realisation_delta_pct_positive_drift() -> None:
    row = attribute_realised_outcome(
        _make_row(),  # expected = 142.0
        realised_value_usd=156.2,  # +10%
        realised_at=datetime(2026, 8, 10, tzinfo=UTC),
    )
    assert realisation_delta_pct(row) == pytest.approx(10.0)


def test_realisation_delta_pct_negative_drift() -> None:
    row = attribute_realised_outcome(
        _make_row(),  # expected = 142.0
        realised_value_usd=113.6,  # -20%
        realised_at=datetime(2026, 8, 10, tzinfo=UTC),
    )
    assert realisation_delta_pct(row) == pytest.approx(-20.0)


def test_realisation_delta_pct_returns_none_when_unrealised() -> None:
    row = _make_row()
    assert realisation_delta_pct(row) is None


def test_realisation_delta_pct_returns_none_on_zero_expected() -> None:
    row = make_ledger_row_for_service(
        service_code="RC-E2E-03",
        decision_id="DEC-X",
        trace_id="t",
        decision_kind="markdown_proposal",
        service_local_outcome_class="approved",
        service_local_risk_class="moderate",
        category="dairy",
        loyalty_tier_distribution="mixed",
        expected_outcome_value_usd=0.0,
    )
    realised = attribute_realised_outcome(
        row, realised_value_usd=10.0,
        realised_at=datetime(2026, 8, 10, tzinfo=UTC),
    )
    assert realisation_delta_pct(realised) is None


# ---------------------------------------------------------------------------
# Coverage — every service contributes
# ---------------------------------------------------------------------------


def test_all_services_can_create_ledger_rows() -> None:
    """Every RC service can produce a fusion-bucket-bearing LEDGER row."""
    rows = [
        make_ledger_row_for_service(
            service_code=svc,
            decision_id=f"DEC-{svc}-COV",
            trace_id=f"trace-cov-{svc}",
            decision_kind="generic",
            service_local_outcome_class="approved",
            service_local_risk_class={
                "RC-E2E-03": "moderate",
                "RC-E2E-04": "medium",
                "RC-E2E-05": "P2_medium",
                "RC-E2E-07": "medium",
                "RC-E2E-09": "II",
            }[svc],
            category="dairy",
            loyalty_tier_distribution="mixed",
        )
        for svc in ALL_SERVICES
    ]
    assert len(rows) == 5
    # Fusion bucket should be the same for all (all map "medium" canonical)
    buckets = {r.fusion_bucket.composite_key() for r in rows}
    assert len(buckets) == 1, (
        "All 5 services should produce the same fusion bucket for "
        f"category=dairy/season=Q2/tier=mixed/canonical=medium; got {buckets}"
    )


def test_fusion_bucket_redis_key_helper() -> None:
    """fusion_bucket_redis_key matches FusionBucket.composite_key."""
    bucket = FusionBucket(
        category="produce", season_quarter="2026-Q3",
        loyalty_tier_distribution="non_loyalty",
        risk_class_canonical="low",
    )
    assert fusion_bucket_redis_key(bucket) == bucket.composite_key()
