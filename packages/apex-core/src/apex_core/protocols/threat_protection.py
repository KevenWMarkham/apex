"""ThreatProtection protocol — prompt-shield, jailbreak, DLP for AI.

APEX-M satisfies via Microsoft Defender for AI services + Azure AI Content
Safety Prompt Shields + Defender for Cloud CSPM (DSPM for AI).
APEX-G satisfies via Vertex AI safety filters + Cloud DLP for AI.
APEX-A satisfies via Bedrock Guardrails + Macie.

Adapters: cross-cloud SIEM forwarders (Splunk, Sentinel-via-Splunk-add-on,
etc.) for client-mandated parallel detection.

This protocol is mandatory pre-prod per MCSB v2 Artificial Intelligence
Security baseline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class PromptShieldResult:
    """Outcome of a pre-invocation prompt shield check."""

    is_safe: bool
    detected_attacks: list[str] = field(
        default_factory=list
    )  # e.g., ["jailbreak", "prompt-injection"]
    severity: str = "info"  # "info" | "low" | "medium" | "high" | "critical"
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ThreatVerdict:
    """Threat assessment of a response or model, with the recommended action."""

    safe: bool
    threats_detected: list[str]
    severity: str
    recommended_action: str  # "block" | "audit" | "warn" | "pass"
    evidence_ref: str | None = None


@runtime_checkable
class ThreatProtection(Protocol):
    """Pre-invocation prompt shielding and post-invocation threat detection."""

    variant: str

    def shield_prompt(self, *, prompt: str, context: dict[str, Any]) -> PromptShieldResult:
        """Pre-invocation check on a user-controlled prompt.

        Returns whether the prompt is safe to forward to the agent runtime.
        Defender for AI Prompt Shields on APEX-M.
        """
        ...

    def evaluate_response(
        self, *, prompt: str, response: str, context: dict[str, Any]
    ) -> ThreatVerdict:
        """Evaluate an agent response after invocation.

        Covers data leak detection, credential theft signals, and off-policy
        completion.
        """
        ...

    def get_posture(self, *, agent_id: str) -> dict[str, Any]:
        """Return a DSPM-for-AI style posture report for the agent.

        The report covers known vulnerabilities, attack-path findings, and
        classification gaps.
        """
        ...

    def scan_model(self, *, image_ref: str) -> ThreatVerdict:
        """Run an AI Model Security scan (preview on APEX-M).

        Acts as a pre-deploy gate for embedded malware, unsafe operators, and
        exposed secrets.
        """
        ...
