"""DLP policy emitter — Sprint 13 Task 13.3.

Generates label-based redaction policies for the surfaces APEX agents
emit to: Microsoft 365 Copilot, agent output channels, Power BI exports,
Teams messages, email, and public web. Policies are keyed by APEX
classification and produce a payload compatible with the Microsoft 365
Compliance / Purview DLP policy API
(``/api/dlp/policies`` and the equivalent Atlas-side governance hooks).

Subtasks
--------
- **13.3.1** — label-based redaction policies for Copilot, agent output, Power BI
- **13.3.2** — policy-violation alerting (webhook + audit-row stamp)

Action vocabulary
-----------------
- ``allow``                — no DLP action; pass through
- ``allow_with_warning``   — pass through but stamp the audit row
- ``mask``                 — partial redaction (e.g., last-four for PCI)
- ``redact``               — full removal of the classified token
- ``block``                — refuse to render the surface
- ``escalate``             — block + page Compliance Office (Restricted only)

Cross-reference: Sellers Guide §8.8.3 retention matrix, §9.11.7 RC DLP
table, §10.10.7 HLS DLP table, §11.10.7 ER DLP table.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apex_purview.classifications import APEX_CLASSIFICATIONS, _normalize_key


# ---------------------------------------------------------------------------
# Surface and action taxonomy
# ---------------------------------------------------------------------------

#: The six surfaces APEX agent output flows into. New surfaces are added
#: with Independence-Office review.
SURFACES: tuple[str, ...] = (
    "copilot_chat",
    "agent_output",
    "power_bi_export",
    "teams_message",
    "email",
    "public_web",
)

#: DLP actions, ordered from least to most restrictive. The propagation
#: validator (Task 13.6) uses this ordering to compute most-restrictive
#: inheritance.
ACTIONS: tuple[str, ...] = (
    "allow",
    "allow_with_warning",
    "mask",
    "redact",
    "block",
    "escalate",
)

_ACTION_RANK = {a: i for i, a in enumerate(ACTIONS)}


def action_severity(action: str) -> int:
    """Return the integer severity of a DLP action (higher = more restrictive)."""
    if action not in _ACTION_RANK:
        raise ValueError(f"Unknown DLP action: {action!r}. Allowed: {ACTIONS}")
    return _ACTION_RANK[action]


def most_restrictive(actions: list[str]) -> str:
    """Return the most-restrictive action from a list."""
    if not actions:
        raise ValueError("Cannot compute most-restrictive of empty list.")
    return max(actions, key=action_severity)


# ---------------------------------------------------------------------------
# Default APEX DLP policy matrix
# ---------------------------------------------------------------------------

#: Default DLP-action matrix per APEX classification × surface. This is the
#: starting policy bundle. Tenant manifests can override per their Practice
#: regulatory profile.
DEFAULT_DLP_MATRIX: dict[str, dict[str, str]] = {
    "public": {
        "copilot_chat": "allow",
        "agent_output": "allow",
        "power_bi_export": "allow",
        "teams_message": "allow",
        "email": "allow",
        "public_web": "allow",
    },
    "internal": {
        "copilot_chat": "allow",
        "agent_output": "allow",
        "power_bi_export": "allow",
        "teams_message": "allow",
        "email": "allow_with_warning",
        "public_web": "block",
    },
    "trade_secret": {
        "copilot_chat": "allow_with_warning",
        "agent_output": "allow_with_warning",
        "power_bi_export": "allow_with_warning",
        "teams_message": "allow_with_warning",
        "email": "block",
        "public_web": "block",
    },
    "pii": {
        "copilot_chat": "mask",
        "agent_output": "mask",
        "power_bi_export": "redact",
        "teams_message": "mask",
        "email": "redact",
        "public_web": "block",
    },
    "phi": {
        "copilot_chat": "redact",
        "agent_output": "redact",
        "power_bi_export": "redact",
        "teams_message": "redact",
        "email": "block",
        "public_web": "block",
    },
    "pci": {
        "copilot_chat": "redact",
        "agent_output": "redact",
        "power_bi_export": "block",
        "teams_message": "redact",
        "email": "block",
        "public_web": "block",
    },
    "genetic": {
        "copilot_chat": "block",
        "agent_output": "redact",
        "power_bi_export": "block",
        "teams_message": "block",
        "email": "block",
        "public_web": "block",
    },
    "behavioral_health": {
        "copilot_chat": "block",
        "agent_output": "redact",
        "power_bi_export": "block",
        "teams_message": "block",
        "email": "block",
        "public_web": "block",
    },
    "restricted": {
        "copilot_chat": "escalate",
        "agent_output": "escalate",
        "power_bi_export": "block",
        "teams_message": "escalate",
        "email": "escalate",
        "public_web": "block",
    },
    "cpni": {
        "copilot_chat": "redact",
        "agent_output": "redact",
        "power_bi_export": "block",
        "teams_message": "redact",
        "email": "block",
        "public_web": "block",
    },
    "export_controlled": {
        "copilot_chat": "escalate",
        "agent_output": "escalate",
        "power_bi_export": "block",
        "teams_message": "escalate",
        "email": "block",
        "public_web": "block",
    },
    "member_only": {
        "copilot_chat": "allow_with_warning",
        "agent_output": "allow_with_warning",
        "power_bi_export": "allow_with_warning",
        "teams_message": "allow_with_warning",
        "email": "block",
        "public_web": "block",
    },
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DLPRule:
    """A single classification × surface DLP rule."""

    classification: str
    surface: str
    action: str

    def __post_init__(self) -> None:
        if self.classification not in APEX_CLASSIFICATIONS:
            raise ValueError(
                f"Unknown classification: {self.classification!r}. "
                f"See APEX_CLASSIFICATIONS in apex_purview.classifications."
            )
        if self.surface not in SURFACES:
            raise ValueError(
                f"Unknown surface: {self.surface!r}. Allowed: {SURFACES}"
            )
        if self.action not in ACTIONS:
            raise ValueError(
                f"Unknown action: {self.action!r}. Allowed: {ACTIONS}"
            )


@dataclass(frozen=True)
class DLPViolationAlert:
    """Webhook configuration for policy-violation alerting (Subtask 13.3.2)."""

    webhook_url: str
    """HTTPS endpoint receiving violation events."""

    severity_threshold: str = "block"
    """Minimum severity that triggers the webhook. Default: ``block``."""

    audit_stamp: bool = True
    """Whether to stamp the violation on the originating decision's audit row."""

    def to_atlas(self) -> dict[str, Any]:
        return {
            "webhookUrl": self.webhook_url,
            "severityThreshold": self.severity_threshold,
            "auditStamp": self.audit_stamp,
        }


@dataclass
class DLPPolicyBundle:
    """A composable DLP policy — rules + optional violation alerting."""

    name: str
    description: str
    rules: list[DLPRule] = field(default_factory=list)
    alerting: DLPViolationAlert | None = None
    version: str = "1.0"

    def add_rule(self, classification: str, surface: str, action: str) -> None:
        """Add or replace the rule for this classification × surface pair."""
        self.rules = [
            r
            for r in self.rules
            if not (r.classification == classification and r.surface == surface)
        ]
        self.rules.append(DLPRule(classification, surface, action))

    def to_atlas(self) -> dict[str, Any]:
        rules_payload = [
            {
                "classification": APEX_CLASSIFICATIONS[r.classification]["type_name"],
                "surface": r.surface,
                "action": r.action,
            }
            for r in self.rules
        ]
        body: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "rules": rules_payload,
        }
        if self.alerting is not None:
            body["alerting"] = self.alerting.to_atlas()
        return body


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def build_default_bundle(
    *,
    name: str = "APEX-DLP-Default",
    description: str = "Default APEX DLP matrix derived from the canonical classification × surface table.",
    alerting: DLPViolationAlert | None = None,
) -> DLPPolicyBundle:
    """Build the default DLP bundle from :data:`DEFAULT_DLP_MATRIX`.

    Every (classification, surface) pair is materialized as a DLPRule.
    """
    bundle = DLPPolicyBundle(name=name, description=description, alerting=alerting)
    for classification, surfaces in DEFAULT_DLP_MATRIX.items():
        for surface, action in surfaces.items():
            bundle.add_rule(classification, surface, action)
    return bundle


def build_bundle_from_overrides(
    overrides: dict[str, dict[str, str]],
    *,
    name: str = "APEX-DLP-Custom",
    description: str = "Tenant-customized APEX DLP bundle.",
    alerting: DLPViolationAlert | None = None,
    base_matrix: dict[str, dict[str, str]] | None = None,
) -> DLPPolicyBundle:
    """Build a DLP bundle from the default matrix overlaid with overrides.

    Args:
        overrides: Mapping of ``{classification: {surface: action}}`` —
            partial; only listed pairs are changed from the base.
        name: Bundle name.
        description: Bundle description.
        alerting: Optional violation-alert webhook configuration.
        base_matrix: Base matrix to overlay onto. Defaults to
            :data:`DEFAULT_DLP_MATRIX`.

    Raises:
        ValueError: if any classification, surface, or action is unknown.

    The final bundle never relaxes the base matrix below the overridden
    severity — it always picks the *more restrictive* of base and override
    so a misconfigured override cannot accidentally reduce protection.
    """
    base = base_matrix if base_matrix is not None else DEFAULT_DLP_MATRIX

    bundle = DLPPolicyBundle(name=name, description=description, alerting=alerting)
    for classification, surfaces in base.items():
        for surface, default_action in surfaces.items():
            override = overrides.get(classification, {}).get(surface)
            if override is None:
                bundle.add_rule(classification, surface, default_action)
            else:
                # never relax — pick more-restrictive of base and override
                bundle.add_rule(
                    classification,
                    surface,
                    most_restrictive([default_action, override]),
                )
    return bundle


def emit_dlp_payload(bundle: DLPPolicyBundle) -> dict[str, Any]:
    """Return the wire-ready DLP policy POST body for the given bundle."""
    return bundle.to_atlas()


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------


def lookup_action(
    classification: str,
    surface: str,
    matrix: dict[str, dict[str, str]] | None = None,
) -> str:
    """Look up the DLP action for a (classification, surface) pair.

    Args:
        classification: APEX classification key (will be normalized).
        surface: One of :data:`SURFACES`.
        matrix: Matrix to query; defaults to :data:`DEFAULT_DLP_MATRIX`.

    Returns:
        The DLP action.

    Raises:
        ValueError: on unknown classification or surface.
    """
    matrix = matrix if matrix is not None else DEFAULT_DLP_MATRIX
    key = _normalize_key(classification)

    if key not in APEX_CLASSIFICATIONS:
        raise ValueError(f"Unknown classification: {classification!r} (normalized {key!r}).")
    if surface not in SURFACES:
        raise ValueError(f"Unknown surface: {surface!r}. Allowed: {SURFACES}")

    if key not in matrix:
        raise ValueError(
            f"Classification {key!r} is in APEX_CLASSIFICATIONS but missing from the DLP matrix."
        )
    if surface not in matrix[key]:
        raise ValueError(
            f"Surface {surface!r} is missing for classification {key!r} in the DLP matrix."
        )

    return matrix[key][surface]
