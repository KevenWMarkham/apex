"""WORM retention policy emitter — Sprint 13 Task 13.4.

Generates Purview-managed retention policy payloads (Microsoft 365
Compliance / Purview Retention API) for APEX-classified data.

Retention bands
---------------
- **3 years** — Public, Internal default
- **7 years** — Trade secret, PCI, FERC/NERC CIP, SOX, member-only
- **10 years** — PHI (HIPAA §164.530), Genetic, Behavioral Health (42 CFR Part 2)
- **Lifetime + post-market** — Restricted (21 CFR Part 11, recall, regulator-correspondence)
- **Legal hold** — Capability, never automatic; configured per matter

Subtask
-------
- **13.4.1** — Purview-managed retention (7y default, 10y HLS, legal-hold support)

Cross-reference: Sellers Guide §8.8.3 retention-lock matrix; HIPAA
§164.530(j)(2) 6-year minimum (APEX uses 10y for safety margin); 21 CFR
Part 11 §11.10 record retention; FERC Standard COM-002 retention.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apex_purview.classifications import APEX_CLASSIFICATIONS, _normalize_key


# ---------------------------------------------------------------------------
# Retention duration enum
# ---------------------------------------------------------------------------

#: ISO-8601-like duration codes APEX uses.
RETENTION_DURATIONS: dict[str, dict[str, Any]] = {
    "P3Y": {"label": "3 years", "years": 3, "regulatory_basis": "default"},
    "P7Y": {
        "label": "7 years",
        "years": 7,
        "regulatory_basis": "SOX §103(a), NERC CIP-009, PCI DSS §10.7",
    },
    "P10Y": {
        "label": "10 years",
        "years": 10,
        "regulatory_basis": "HIPAA §164.530(j)(2) (6y min, APEX uses 10y safety margin); GINA",
    },
    "PERMANENT": {
        "label": "Permanent (lifetime + post-market)",
        "years": None,
        "regulatory_basis": "21 CFR Part 11 §11.10; FDA recall recordkeeping; FSMA 204",
    },
}


#: Default retention-band assignment per APEX classification. Tenant
#: manifests may override per regulatory profile.
DEFAULT_RETENTION_MATRIX: dict[str, str] = {
    "public": "P3Y",
    "internal": "P3Y",
    "trade_secret": "P7Y",
    "pii": "P7Y",
    "phi": "P10Y",
    "pci": "P7Y",
    "genetic": "P10Y",
    "behavioral_health": "P10Y",
    "restricted": "PERMANENT",
    "cpni": "P7Y",
    "export_controlled": "P7Y",
    "member_only": "P7Y",
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RetentionRule:
    """One classification → duration retention rule."""

    classification: str
    duration: str
    """ISO-8601 duration key from :data:`RETENTION_DURATIONS`."""

    regulatory_basis: str | None = None
    worm: bool = True
    """If True, mark records write-once-read-many (WORM)."""

    def __post_init__(self) -> None:
        if self.classification not in APEX_CLASSIFICATIONS:
            raise ValueError(f"Unknown classification: {self.classification!r}.")
        if self.duration not in RETENTION_DURATIONS:
            raise ValueError(
                f"Unknown duration: {self.duration!r}. Allowed: {sorted(RETENTION_DURATIONS.keys())}"
            )

    def to_atlas(self) -> dict[str, Any]:
        spec = RETENTION_DURATIONS[self.duration]
        body: dict[str, Any] = {
            "classification": APEX_CLASSIFICATIONS[self.classification]["type_name"],
            "duration": self.duration,
            "durationYears": spec["years"],
            "label": spec["label"],
            "worm": self.worm,
        }
        body["regulatoryBasis"] = self.regulatory_basis or spec["regulatory_basis"]
        return body


@dataclass(frozen=True)
class LegalHoldConfig:
    """Configuration for legal-hold capability — Subtask 13.4.1."""

    matter_id: str
    """Matter or case identifier the hold is attached to."""

    classifications: tuple[str, ...]
    """Classifications under hold."""

    custodian: str
    """Custodian / legal contact for the hold."""

    started_iso: str
    """ISO-8601 timestamp the hold was applied."""

    description: str = ""

    def to_atlas(self) -> dict[str, Any]:
        for c in self.classifications:
            if c not in APEX_CLASSIFICATIONS:
                raise ValueError(f"Unknown classification in legal hold: {c!r}.")
        return {
            "matterId": self.matter_id,
            "classifications": [
                APEX_CLASSIFICATIONS[c]["type_name"] for c in self.classifications
            ],
            "custodian": self.custodian,
            "startedAt": self.started_iso,
            "description": self.description,
            "active": True,
        }


@dataclass
class RetentionPolicyBundle:
    """A retention bundle — rules + optional legal holds."""

    name: str
    description: str
    rules: list[RetentionRule] = field(default_factory=list)
    legal_holds: list[LegalHoldConfig] = field(default_factory=list)
    version: str = "1.0"

    def add_rule(
        self,
        classification: str,
        duration: str,
        *,
        regulatory_basis: str | None = None,
        worm: bool = True,
    ) -> None:
        self.rules = [r for r in self.rules if r.classification != classification]
        self.rules.append(
            RetentionRule(
                classification=classification,
                duration=duration,
                regulatory_basis=regulatory_basis,
                worm=worm,
            )
        )

    def add_legal_hold(self, hold: LegalHoldConfig) -> None:
        self.legal_holds.append(hold)

    def to_atlas(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "rules": [r.to_atlas() for r in self.rules],
            "legalHolds": [h.to_atlas() for h in self.legal_holds],
        }


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def build_default_retention_bundle(
    *,
    name: str = "APEX-Retention-Default",
    description: str = "APEX default retention bands per classification (HIPAA / SOX / FERC / 21 CFR Part 11 aligned).",
) -> RetentionPolicyBundle:
    """Build the default retention bundle from :data:`DEFAULT_RETENTION_MATRIX`."""
    bundle = RetentionPolicyBundle(name=name, description=description)
    for classification, duration in DEFAULT_RETENTION_MATRIX.items():
        bundle.add_rule(classification, duration)
    return bundle


def build_retention_with_overrides(
    overrides: dict[str, str],
    *,
    name: str = "APEX-Retention-Custom",
    description: str = "Tenant-customized APEX retention bundle.",
    base_matrix: dict[str, str] | None = None,
) -> RetentionPolicyBundle:
    """Build a retention bundle with overrides; never reduces below default.

    Same safety rule as DLP — the final duration is the longer of base
    and override, expressed in years (PERMANENT is treated as longer than
    any year-quantified band).
    """
    base = base_matrix if base_matrix is not None else DEFAULT_RETENTION_MATRIX
    bundle = RetentionPolicyBundle(name=name, description=description)

    for classification, default_duration in base.items():
        override = overrides.get(classification)
        if override is None:
            bundle.add_rule(classification, default_duration)
        else:
            bundle.add_rule(
                classification,
                _longer_duration(default_duration, override),
            )
    return bundle


def _longer_duration(a: str, b: str) -> str:
    """Return whichever of two duration codes is longer.

    PERMANENT > any P*Y. Among year-quantified durations, the larger
    ``years`` wins.
    """
    if a == "PERMANENT" or b == "PERMANENT":
        return "PERMANENT"
    years_a = RETENTION_DURATIONS[a]["years"]
    years_b = RETENTION_DURATIONS[b]["years"]
    return a if years_a >= years_b else b


def emit_retention_payload(bundle: RetentionPolicyBundle) -> dict[str, Any]:
    """Return wire-ready Purview retention policy body."""
    return bundle.to_atlas()


def lookup_retention(
    classification: str,
    matrix: dict[str, str] | None = None,
) -> str:
    """Look up the retention duration code for a classification."""
    matrix = matrix if matrix is not None else DEFAULT_RETENTION_MATRIX
    key = _normalize_key(classification)
    if key not in APEX_CLASSIFICATIONS:
        raise ValueError(f"Unknown classification: {classification!r} (normalized {key!r}).")
    if key not in matrix:
        raise ValueError(
            f"Classification {key!r} missing from retention matrix."
        )
    return matrix[key]
