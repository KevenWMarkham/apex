"""Retention-policy model + Purview payload emitter.

Implements the retention contract from ``APEX_Design.md`` §6.3:

- 7 years default.
- 10 years for HLS-practice data.
- Permanent under legal hold.
- Per-classification overrides (e.g. longer for recall-traceable lots).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from apex_core.types import Classification, Practice

DAYS_PER_YEAR = 365
DEFAULT_RETENTION_DAYS = 7 * DAYS_PER_YEAR
HLS_RETENTION_DAYS = 10 * DAYS_PER_YEAR


class RetentionPolicy(BaseModel):
    """Declarative retention policy for a Bronze (or Silver/Gold) table."""

    model_config = ConfigDict(extra="forbid")

    duration_days: int = Field(
        DEFAULT_RETENTION_DAYS, ge=1,
        description="How long to retain rows (days). Default: 7 years.",
    )
    legal_hold: bool = Field(
        False, description="When True, retention is suspended indefinitely."
    )
    legal_hold_expires: datetime | None = Field(
        None, description="When the legal hold lapses (null = indefinite)."
    )
    classification_overrides: dict[Classification, int] = Field(
        default_factory=dict,
        description=(
            "Override duration_days for specific classifications. "
            "Example: {Classification.PHI: 3650} — 10y for PHI rows."
        ),
    )
    practice: Practice | None = None
    notes: str = ""

    @model_validator(mode="after")
    def _validate_legal_hold_expiry(self) -> "RetentionPolicy":
        if self.legal_hold_expires is not None and not self.legal_hold:
            raise ValueError(
                "legal_hold_expires is only valid when legal_hold=True."
            )
        return self

    def effective_duration_days(self, classification: Classification) -> int:
        """Resolve the effective retention for a specific classification."""
        return self.classification_overrides.get(classification, self.duration_days)

    @classmethod
    def default_for_practice(cls, practice: Practice) -> "RetentionPolicy":
        """Return the APEX-default retention for a given Practice."""
        if practice is Practice.HLS:
            return cls(practice=practice, duration_days=HLS_RETENTION_DAYS)
        return cls(practice=practice)


def build_purview_retention_payload(
    policy: RetentionPolicy,
    *,
    asset_path: str,
) -> dict[str, Any]:
    """Emit a Purview REST payload for a retention-policy registration.

    Note: the real Purview REST API requires tenant-scoped auth headers
    applied by the caller. This function produces the payload body only.

    Args:
        policy: Policy to register.
        asset_path: Fully-qualified OneLake path of the asset the policy applies to.

    Returns:
        JSON-serialisable dict suitable as a Purview policy-create request body.
    """
    body: dict[str, Any] = {
        "asset_path": asset_path,
        "retention": {
            "duration_days": policy.duration_days,
            "legal_hold": policy.legal_hold,
        },
    }
    if policy.legal_hold and policy.legal_hold_expires is not None:
        body["retention"]["legal_hold_expires"] = policy.legal_hold_expires.isoformat()
    if policy.classification_overrides:
        body["retention"]["per_classification"] = {
            c.value: days for c, days in policy.classification_overrides.items()
        }
    if policy.practice is not None:
        body["practice"] = policy.practice.value
    if policy.notes:
        body["notes"] = policy.notes
    return body
