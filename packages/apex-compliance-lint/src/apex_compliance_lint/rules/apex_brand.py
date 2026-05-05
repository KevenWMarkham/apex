"""APEX brand-and-positioning rule pack — Sprint 29 Task 29.9.

Beyond Independence-language, APEX content has positional rules:

- The agent never claims to "deliver" client outcomes — Deloitte
  delivers outcomes; APEX is the framework.
- The agent never claims to be "AI-powered" or "AI-driven" — those
  are marketing-shorthand terms that gloss the HITL governance.
- "Black box" is forbidden — APEX is intentionally auditable.

Severity is mostly WARNING here; the linter surfaces these without
blocking by default. Tenants can promote to ERROR via custom rule packs.
"""

from __future__ import annotations

import re

from apex_compliance_lint.types import Rule, RulePack, Severity, make_pattern


APEX_BRAND = RulePack(
    pack_id="apex_brand",
    name="APEX Brand & Positioning",
    description=(
        "APEX positional rules — the agent never claims to deliver "
        "outcomes, never describes itself as a black box, never uses "
        "marketing-shorthand for HITL governance."
    ),
    rules=(
        Rule(
            rule_id="apex_brand.black_box",
            description="Forbidden: describing APEX as a 'black box'.",
            pattern=re.compile(r"\bblack[\s-]*box\b", re.IGNORECASE),
            severity=Severity.ERROR,
            guidance=(
                "APEX is auditable by design — every consequential decision "
                "emits an audit row per Sellers Guide §6.10."
            ),
            approved_substitutes=(
                "auditable",
                "transparent",
                "fully traceable",
            ),
        ),
        Rule(
            rule_id="apex_brand.ai_powered",
            description="Discouraged: marketing-shorthand 'AI-powered'.",
            pattern=re.compile(r"\b(AI[\s-]powered|AI[\s-]driven)\b", re.IGNORECASE),
            severity=Severity.WARNING,
            guidance=(
                "'AI-powered' / 'AI-driven' overstates the autonomy and "
                "understates the HITL governance. APEX uses 'agentic' or "
                "names the specific archetype family."
            ),
            approved_substitutes=("agentic", "agent-orchestrated"),
        ),
        Rule(
            rule_id="apex_brand.fully_autonomous",
            description="Forbidden: claiming APEX is 'fully autonomous'.",
            pattern=re.compile(r"\bfully\s+autonomous\b", re.IGNORECASE),
            severity=Severity.ERROR,
            guidance=(
                "APEX uses HITL / HOTL / HIC oversight per Sellers Guide §2.2C — "
                "'fully autonomous' contradicts the governance posture."
            ),
            approved_substitutes=(
                "HOTL (Human-on-the-Loop)",
                "agent-orchestrated with HITL gates",
            ),
        ),
        Rule(
            rule_id="apex_brand.silver_bullet",
            description="Discouraged: 'silver bullet' / 'magic' marketing language.",
            pattern=re.compile(
                r"\b(silver\s+bullet|magic\s+wand|cure[\s-]all|panacea)\b",
                re.IGNORECASE,
            ),
            severity=Severity.WARNING,
            guidance=(
                "APEX content describes specific outcomes per Sellers Guide §2.2 "
                "Wave commitments. Marketing-shorthand undermines the "
                "evidence-based posture."
            ),
            approved_substitutes=("integrated solution", "engagement framework"),
        ),
        Rule(
            rule_id="apex_brand.guarantees",
            description="Forbidden: outcome guarantees.",
            pattern=re.compile(
                r"\b(guarantees?|guaranteed)\s+(outcomes?|results?|savings|ROI|return)\b",
                re.IGNORECASE,
            ),
            severity=Severity.ERROR,
            guidance=(
                "APEX commercial language uses Wave-based commitments + KPI "
                "bands per Sellers Guide §2.2 — never outcome guarantees."
            ),
            approved_substitutes=(
                "targets",
                "Wave-2 commitments per Sellers Guide §2.2",
            ),
        ),
    ),
    version="0.1.0",
)
