"""APEX-M ThreatProtection — Microsoft Defender for Cloud (CSPM, AI security
posture) + Defender for AI services + Azure AI Content Safety Prompt Shields.

Mandatory pre-prod per Microsoft Cloud Security Benchmark v2 AI Security
baseline.

Reference: https://learn.microsoft.com/azure/defender-for-cloud/ai-threat-protection
Reference: https://learn.microsoft.com/azure/defender-for-cloud/ai-security-posture
Reference: https://learn.microsoft.com/azure/defender-for-cloud/ai-model-security
Reference: https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection
"""
from __future__ import annotations

from typing import Any

from apex_core.protocols import (
    PromptShieldResult,
    ThreatProtection,
    ThreatVerdict,
)


class ThreatProtectionDefender:
    """Concrete ThreatProtection against Defender for AI + Content Safety."""

    variant = "APEX-M"

    def __init__(self, *, content_safety_endpoint: str, defender_workspace_id: str) -> None:
        self.content_safety_endpoint = content_safety_endpoint
        self.defender_workspace_id = defender_workspace_id

    def shield_prompt(self, *, prompt: str, context: dict[str, Any]) -> PromptShieldResult:
        raise NotImplementedError(
            "shield_prompt — calls Azure AI Content Safety Prompt Shields. "
            "Phase I.3 follow-up sprint wires the SDK call."
        )

    def evaluate_response(
        self, *, prompt: str, response: str, context: dict[str, Any]
    ) -> ThreatVerdict:
        raise NotImplementedError("Defender for AI post-invocation eval — Phase I.3 follow-up")

    def get_posture(self, *, agent_id: str) -> dict[str, Any]:
        raise NotImplementedError("DSPM-for-AI posture API — Phase I.3 follow-up")

    def scan_model(self, *, image_ref: str) -> ThreatVerdict:
        raise NotImplementedError(
            "Defender AI Model Security scan — preview API; Phase I.3 follow-up"
        )


class MockThreatProtectionDefender:
    """In-memory mock — uses regex heuristics for jailbreak detection."""

    variant = "APEX-M"

    _JAILBREAK_TOKENS = (
        "ignore previous instructions", "ignore all previous", "system prompt",
        "you are now", "developer mode", "DAN mode",
    )
    _DATA_EXFIL_TOKENS = (
        "list all customers", "dump", "select * from", "<script>",
    )

    def shield_prompt(self, *, prompt: str, context: dict[str, Any]) -> PromptShieldResult:
        lower = prompt.lower()
        attacks: list[str] = []
        if any(t in lower for t in self._JAILBREAK_TOKENS):
            attacks.append("jailbreak")
        if any(t in lower for t in self._DATA_EXFIL_TOKENS):
            attacks.append("data-exfiltration-attempt")
        return PromptShieldResult(
            is_safe=not attacks,
            detected_attacks=attacks,
            severity="critical" if "jailbreak" in attacks else ("high" if attacks else "info"),
        )

    def evaluate_response(
        self, *, prompt: str, response: str, context: dict[str, Any]
    ) -> ThreatVerdict:
        # Simple heuristic — production checks for credential leakage, PII spillover, etc.
        unsafe = "ssn:" in response.lower() or "password:" in response.lower()
        return ThreatVerdict(
            safe=not unsafe,
            threats_detected=["pii-leak"] if unsafe else [],
            severity="critical" if unsafe else "info",
            recommended_action="block" if unsafe else "pass",
        )

    def get_posture(self, *, agent_id: str) -> dict[str, Any]:
        return {
            "agent_id": agent_id,
            "vulnerabilities": [],
            "attack_paths": [],
            "classification_gaps": [],
            "posture_score": 1.0,
        }

    def scan_model(self, *, image_ref: str) -> ThreatVerdict:
        return ThreatVerdict(
            safe=True,
            threats_detected=[],
            severity="info",
            recommended_action="pass",
        )


__all__ = [
    "ThreatProtectionDefender",
    "MockThreatProtectionDefender",
]
