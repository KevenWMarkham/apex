"""LEDGER feedback loop — unified episodic memory across all 5 RC services.

Sprint 40 item 40.2 — Wave 3 Fusion. Per Roadmap.md BL.C.30d (LEDGER feedback
visualization) + Services Guide §25.8.

Each RC service's `learn` agent (The Briefer) emits a LEDGER row to Redis
under service-local similarity-bucket keys. Sprint 40 unifies those into a
**cross-service similarity surface** so the Pricing Agent (RC-E2E-03's
pricing role) can find precedent across cold-chain × loyalty × OSA × fraud
× lot-provenance — not just within RC-E2E-03's own history.

Why unification matters:

- A markdown decision today might benefit from knowing the customer is also
  in a winback cohort (RC-E2E-04 LEDGER) so the markdown's expected
  recovery is higher than the per-service model predicts.
- A returns-fraud hold might benefit from knowing the lot is recall-flagged
  (RC-E2E-09 LEDGER) so the hold is justified beyond the per-event score.
- The OSA shift digest (RC-E2E-05) might benefit from knowing the lot was
  destroyed today (RC-E2E-03 cold-chain) so the dispatch ignores it.

Cross-service similarity uses **content-addressed** bucket keys — each
service contributes its own primary key (e.g., sku_key + decision_class)
plus a shared **fusion bucket** (e.g., `category × season_quarter ×
loyalty_tier_distribution`) that all services compute identically.

References
----------
- Roadmap.md BL.C.30d (LEDGER feedback visualization)
- Services Guide §25.8 (Pricer learning loop)
- Sprint-Backlog-Retirement-Map.md §3 Sprint 40 (W3 Fusion)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal


# ---------------------------------------------------------------------------
# Service identity
# ---------------------------------------------------------------------------

ServiceCode = Literal[
    "RC-E2E-03",   # Pricing & Revenue Decision (cold-chain + dynamic markdown)
    "RC-E2E-04",   # Loyalty Churn Prediction & Winback
    "RC-E2E-05",   # On-Shelf Availability
    "RC-E2E-07",   # Returns & Refund Integrity
    "RC-E2E-09",   # Product Tracking (FSMA 204)
]

ALL_SERVICES: tuple[ServiceCode, ...] = (
    "RC-E2E-03", "RC-E2E-04", "RC-E2E-05", "RC-E2E-07", "RC-E2E-09",
)


# ---------------------------------------------------------------------------
# Cross-service fusion bucket
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FusionBucket:
    """Composite key shared across services for similarity-based retrieval.

    Every service's :class:`LedgerRow` carries a ``fusion_bucket`` field
    populated by :func:`compute_fusion_bucket`. Two LEDGER rows with the
    same fusion bucket are *similarity-comparable* across services — even
    when their service-local primary keys differ.

    Bucket dimensions are deliberately coarse so the cardinality stays
    small enough that the Pricer's similarity-search-on-Redis returns
    relevant precedents without memory blowup.
    """

    category: str          # e.g., "dairy", "produce", "grocery", "apparel"
    season_quarter: str    # "2026-Q2"
    loyalty_tier_distribution: str   # "platinum_dominant" | "mixed" | "non_loyalty"
    risk_class_canonical: str        # "low" | "medium" | "high" — service-mapped

    def composite_key(self) -> str:
        """Return the canonical Redis key for this bucket (deterministic)."""
        return (
            f"fusion::{self.category}::{self.season_quarter}::"
            f"{self.loyalty_tier_distribution}::{self.risk_class_canonical}"
        )


# Per-service mapping from service-local risk-class field to the canonical
# 3-tier scale. Used by compute_fusion_bucket so a "P0_critical" task in
# RC-E2E-05 + a "Class I recall" in RC-E2E-09 + a "fraud_score >= 0.7" in
# RC-E2E-07 all land in the same `risk_class_canonical: high` bucket.
_RISK_CLASS_CANONICAL_MAP: dict[ServiceCode, dict[str, str]] = {
    "RC-E2E-03": {
        "critical":      "high",
        "severe":        "medium",
        "moderate":      "medium",
        "monitor_only":  "low",
    },
    "RC-E2E-04": {
        "high":   "high",
        "medium": "medium",
        "low":    "low",
    },
    "RC-E2E-05": {
        "P0_critical": "high",
        "P1_high":     "high",
        "P2_medium":   "medium",
        "P3_low":      "low",
        "deferred":    "low",
    },
    "RC-E2E-07": {
        "high":   "high",     # fraud_score >= 0.7
        "medium": "medium",   # 0.4 <= fraud_score < 0.7
        "low":    "low",      # fraud_score < 0.4
    },
    "RC-E2E-09": {
        "I":          "high",
        "II":         "medium",
        "III":        "low",
        "no_recall":  "low",
    },
}


def canonicalise_risk_class(service_code: ServiceCode, service_local_class: str) -> str:
    """Map a service-local risk class to the canonical 3-tier scale.

    Raises:
        KeyError: if the service or class is not registered. Production wiring
            fails closed — registering a new class requires a Sprint 40+ doc
            update so cross-service consumers know what to expect.
    """
    return _RISK_CLASS_CANONICAL_MAP[service_code][service_local_class]


def compute_fusion_bucket(
    service_code: ServiceCode,
    *,
    category: str,
    decision_at: datetime,
    loyalty_tier_distribution: str,
    service_local_risk_class: str,
) -> FusionBucket:
    """Compute the canonical fusion bucket for a LEDGER row.

    Each service's Briefer (learn agent) calls this with its local
    decision context; the resulting bucket is stored on the LEDGER row's
    ``fusion_bucket`` field so cross-service similarity search works.
    """
    # Quarter computation — Q1 = Jan-Mar, Q2 = Apr-Jun, Q3 = Jul-Sep, Q4 = Oct-Dec
    q = ((decision_at.month - 1) // 3) + 1
    return FusionBucket(
        category=category,
        season_quarter=f"{decision_at.year}-Q{q}",
        loyalty_tier_distribution=loyalty_tier_distribution,
        risk_class_canonical=canonicalise_risk_class(
            service_code, service_local_risk_class,
        ),
    )


# ---------------------------------------------------------------------------
# Unified LEDGER row
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LedgerRow:
    """One unified cross-service LEDGER row.

    Per-service Briefers emit this shape into Redis under both:

    1. The service-local similarity bucket (per-service legacy keys).
    2. The cross-service fusion bucket (Sprint 40 unified key).

    The Pricing Agent (RC-E2E-03 pricing role) reads via the fusion bucket
    when computing markdown depth — finds precedent across all 5 services'
    realised outcomes for similar context.
    """

    # Identity
    decision_id: str
    trace_id: str
    service_code: ServiceCode
    decision_kind: str           # service-local: markdown_proposal / winback_offer / task_dispatch / hold_decision / lot_event
    decision_at: datetime

    # Service-local outcome (for legacy per-service search)
    service_local_outcome_class: str
    service_local_risk_class: str

    # Cross-service fusion bucket (Sprint 40 — for unified search)
    fusion_bucket: FusionBucket

    # Realised vs expected — populated by the 30/60/90-day attribution batch
    # job; null when the LEDGER row is first emitted.
    expected_outcome_value_usd: float | None = None
    realised_outcome_value_usd: float | None = None
    realised_at: datetime | None = None

    # Audit chain references
    audit_row_outputs_hash: str = ""
    operator_principal: str | None = None
    persona_id: str | None = None

    # Per-service extras — opaque to cross-service consumers; only the
    # service that emitted this row interprets them.
    service_local_payload: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Redis bucket-key helpers
# ---------------------------------------------------------------------------


def fusion_bucket_redis_key(bucket: FusionBucket) -> str:
    """Canonical Redis key for cross-service similarity retrieval."""
    return bucket.composite_key()


def service_local_redis_keys(row: LedgerRow) -> list[str]:
    """Return the service-local bucket keys this row should also be indexed under.

    Each service's existing Sprint 32–39 LEDGER bucketing stays — we add
    the fusion bucket *alongside*, not replacing.
    """
    return [
        # Per-service primary bucket — service-specific shape.
        f"local::{row.service_code}::{row.service_local_risk_class}::{row.decision_kind}",
        # Per-service category bucket — drives the digest agent's
        # category-rollup queries.
        f"local::{row.service_code}::category::{row.fusion_bucket.category}",
    ]


def all_redis_keys_for_row(row: LedgerRow) -> list[str]:
    """All Redis keys this row should be indexed under (legacy + fusion)."""
    keys = list(service_local_redis_keys(row))
    keys.append(fusion_bucket_redis_key(row.fusion_bucket))
    return keys


# ---------------------------------------------------------------------------
# Cross-service similarity retrieval (Sprint 40 — used by The Pricer)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SimilarityQuery:
    """A request for similar precedents from the unified LEDGER."""

    fusion_bucket: FusionBucket
    requesting_service: ServiceCode
    requesting_decision_kind: str
    max_results: int = 30
    only_realised: bool = False    # True = only rows with realised outcomes


@dataclass(frozen=True)
class SimilarityResult:
    """One precedent returned to the requester."""

    row: LedgerRow
    similarity_score: float       # 0..1; higher = more similar
    similarity_rationale: str     # Short human-readable explanation


def compute_similarity_score(query: SimilarityQuery, row: LedgerRow) -> float:
    """Score how similar a candidate row is to the query (heuristic).

    Production replaces this with a proper vector-similarity call against
    the Eventhouse `ai_embeddings` SLM (per DEP-002). The heuristic here
    is the deterministic baseline that lets us test the wiring without
    a real LLM in the loop.

    Weights (sum to 1.0):
      - 0.40 — same fusion bucket (composite key match)
      - 0.20 — same season_quarter (recent precedents weight more)
      - 0.20 — same risk_class_canonical
      - 0.10 — same loyalty_tier_distribution
      - 0.10 — outcome already realised (signal not just forecast)
    """
    score = 0.0
    if row.fusion_bucket.composite_key() == query.fusion_bucket.composite_key():
        score += 0.40
    if row.fusion_bucket.season_quarter == query.fusion_bucket.season_quarter:
        score += 0.20
    if row.fusion_bucket.risk_class_canonical == query.fusion_bucket.risk_class_canonical:
        score += 0.20
    if row.fusion_bucket.loyalty_tier_distribution == query.fusion_bucket.loyalty_tier_distribution:
        score += 0.10
    if row.realised_outcome_value_usd is not None:
        score += 0.10
    return min(score, 1.0)


def retrieve_similar(
    query: SimilarityQuery,
    candidates: list[LedgerRow],
) -> list[SimilarityResult]:
    """Score candidates against the query and return the top N.

    Sprint 42 production wiring swaps `candidates` for the Eventhouse
    `ai_embeddings` neighbourhood query result. The signature stays
    stable so the callers (The Pricer, mostly) don't change.
    """
    if query.only_realised:
        candidates = [c for c in candidates if c.realised_outcome_value_usd is not None]
    scored: list[SimilarityResult] = []
    for c in candidates:
        score = compute_similarity_score(query, c)
        if score > 0.0:
            scored.append(SimilarityResult(
                row=c,
                similarity_score=score,
                similarity_rationale=_explain_similarity(query, c, score),
            ))
    scored.sort(key=lambda r: r.similarity_score, reverse=True)
    return scored[: query.max_results]


def _explain_similarity(
    query: SimilarityQuery, row: LedgerRow, score: float,
) -> str:
    """Short human-readable explanation of why a row scored as it did.

    Surfaced to the Pricer's decision rationale + the audit row.
    """
    parts: list[str] = []
    if row.fusion_bucket.composite_key() == query.fusion_bucket.composite_key():
        parts.append("exact fusion match")
    elif row.fusion_bucket.risk_class_canonical == query.fusion_bucket.risk_class_canonical:
        parts.append(f"same risk_class={row.fusion_bucket.risk_class_canonical}")
    if row.fusion_bucket.season_quarter == query.fusion_bucket.season_quarter:
        parts.append(f"same season={row.fusion_bucket.season_quarter}")
    parts.append(f"src={row.service_code}")
    if row.realised_outcome_value_usd is not None:
        parts.append("realised")
    return f"score={score:.2f}: " + " · ".join(parts)


# ---------------------------------------------------------------------------
# Realised-outcome attribution (30/60/90-day batch)
# ---------------------------------------------------------------------------


def attribute_realised_outcome(
    row: LedgerRow,
    realised_value_usd: float,
    realised_at: datetime,
) -> LedgerRow:
    """Update a LEDGER row with realised outcome.

    Called by the per-service attribution batch (30/60/90-day windows).
    Returns a new frozen row — the original immutable per audit-row
    discipline.

    Per Sprint 48's commercial milestone (3-month margin-attribution
    shadow window), the realised value drives the W3 commercial review.
    """
    # Frozen dataclass — replace via dataclasses.replace
    from dataclasses import replace
    return replace(
        row,
        realised_outcome_value_usd=realised_value_usd,
        realised_at=realised_at,
    )


def realisation_delta_pct(row: LedgerRow) -> float | None:
    """Return realised vs expected as a signed percent delta, or None."""
    if row.expected_outcome_value_usd is None or row.realised_outcome_value_usd is None:
        return None
    if row.expected_outcome_value_usd == 0:
        return None
    return (
        (row.realised_outcome_value_usd - row.expected_outcome_value_usd)
        / row.expected_outcome_value_usd
    ) * 100.0


# ---------------------------------------------------------------------------
# Construction helpers — used by per-service Briefers
# ---------------------------------------------------------------------------


def make_ledger_row_for_service(
    *,
    service_code: ServiceCode,
    decision_id: str,
    trace_id: str,
    decision_kind: str,
    service_local_outcome_class: str,
    service_local_risk_class: str,
    category: str,
    loyalty_tier_distribution: str,
    decision_at: datetime | None = None,
    expected_outcome_value_usd: float | None = None,
    audit_row_outputs_hash: str = "",
    operator_principal: str | None = None,
    persona_id: str | None = None,
    service_local_payload: dict[str, str] | None = None,
) -> LedgerRow:
    """Construct a unified LEDGER row from per-service Briefer inputs.

    The Briefer agent in each service builds its row through this helper
    so the fusion bucket is always computed consistently. Sprint 40
    contract — every Briefer must call this rather than constructing
    LedgerRow directly.
    """
    ts = decision_at or datetime.now(UTC)
    return LedgerRow(
        decision_id=decision_id,
        trace_id=trace_id,
        service_code=service_code,
        decision_kind=decision_kind,
        decision_at=ts,
        service_local_outcome_class=service_local_outcome_class,
        service_local_risk_class=service_local_risk_class,
        fusion_bucket=compute_fusion_bucket(
            service_code,
            category=category,
            decision_at=ts,
            loyalty_tier_distribution=loyalty_tier_distribution,
            service_local_risk_class=service_local_risk_class,
        ),
        expected_outcome_value_usd=expected_outcome_value_usd,
        audit_row_outputs_hash=audit_row_outputs_hash,
        operator_principal=operator_principal,
        persona_id=persona_id,
        service_local_payload=service_local_payload or {},
    )
