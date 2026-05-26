---
name: constitution-author
description: Use when drafting hard/soft/Independence rules for a pack constitution from regulatory text. Triggers include "draft constitution", "add regulatory rule", "Independence check for X".
---

# Constitution authoring for APEX packs

Use the `apex-constitution-author` agent. Provide:
- Regulatory text (SOX · HIPAA · GDPR · OSHA · industry-specific)
- Industry context
- Client jurisdiction

The agent drafts hard + soft + Independence rules in `packs/<industry>/constitution.yaml`.

## Conventions
- Hard rules block + escalate (cannot be bypassed)
- Soft rules warn-only (annotate the Card)
- Independence rules cite Deloitte-as-auditor constraints (no ECIF · no forecasts for SEC clients · etc.)
- Always reference the pre-cleared funding paths in `.rapids/governance/independence-allowlist.yaml`
- Always include OGC review checkpoint before constitution merges to main

## Validation
The Constitution Engine validates every recommendation against these rules at runtime. Hard-rule violations route to escalation persona.
