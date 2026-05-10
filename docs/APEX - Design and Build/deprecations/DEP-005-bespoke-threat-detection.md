# DEP-005 · Bespoke agent threat detection → Defender for AI services

**Status:** Deprecated
**Date:** 2026-05-09
**Supersedes:** Roadmap.md §2.10 Purview Trust Architecture custom threat-detection scope (subset)

## What APEX was building

Custom in-agent prompt-injection and jailbreak detection — a regex pre-processor in front of the LLM call, plus heuristic post-processing to detect data exfiltration patterns in agent outputs. Enough to satisfy a "we have *something*" gate, never strong enough for production.

## What Microsoft shipped

**Microsoft Defender for AI services** is GA, Microsoft Defender for Cloud's CSPM AI security posture is GA:

- [AI threat protection](https://learn.microsoft.com/azure/defender-for-cloud/ai-threat-protection) (GA)
- [AI security posture management (DSPM for AI)](https://learn.microsoft.com/azure/defender-for-cloud/ai-security-posture) (GA)
- [Azure AI Content Safety Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) (GA)
- [AI model security](https://learn.microsoft.com/azure/defender-for-cloud/ai-model-security) (Preview)

Capabilities Defender provides that bespoke detection cannot:
- Microsoft threat-intelligence signal feed
- Real-time prompt-shield + jailbreak detection (Content Safety)
- Cross-customer attack-pattern correlation
- Defender XDR integration for SOC workflows
- AI BOM discovery + attack-path analysis at the workload level

## Migration path

1. Stop investing in bespoke prompt-injection regex. Replace with Azure AI Content Safety Prompt Shields call before every LLM invocation — handled by `apex-m.threat_defender.ThreatProtectionDefender`.
2. Defender for AI services and Defender for Cloud CSPM (with AI security posture) become Pre-deployment Security Gate items #1 and #2 (per [`Pre-deployment-Security-Gate.md`](../Pre-deployment-Security-Gate.md)).
3. Roadmap.md §2.10 entries narrow scope: classification + DLP + audit (which Microsoft Purview covers per ADR-003) and lineage + retention stay in the APEX scope; threat-detection moves to Defender.

## Independence implications

None. Defender plans are part of the client's existing Microsoft Defender posture.

## Cost note

Defender for AI services has a documented free trial (30 days, capped at 75B tokens scanned). After that, billing is per-token. Engagements should validate cost in the commercial envelope; for the RC-E2E-03 Lab pilot the volume is well within the trial cap.

## What stays

APEX's agent-output post-processing for **business-rule** checks (e.g., "is the proposed markdown within the commercial envelope") stays in agent code — Defender doesn't model business rules. Defender catches *security threats*; APEX catches *policy violations*. Different layers, both required.
