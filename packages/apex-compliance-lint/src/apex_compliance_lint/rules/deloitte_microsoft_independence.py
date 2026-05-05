"""Deloitte-Microsoft Independence rule pack — Sprint 29 Task 29.9.1.

The most-flagged compliance class in APEX artifacts: language that
implies a commercial alliance / partnership / endorsement between
Deloitte and Microsoft (or any third-party SOR vendor). Per
Independence Office guidance, APEX agents and APEX artifacts must use
precise language: "the platform" / "the underlying technology" /
"vendor", not "partner" / "alliance partner" / "endorsed by".

Each rule documents the approved substitutes so the linter output
includes a ready-to-paste replacement.
"""

from __future__ import annotations

import re

from apex_compliance_lint.types import Rule, RulePack, Severity, make_pattern


# ---------------------------------------------------------------------------
# Allowed-context patterns (suppress matches inside these contexts)
# ---------------------------------------------------------------------------

# "Microsoft Partner Of The Year" / "Microsoft Partner Network" — formal
# award names OR product names; we don't flag inside those literal strings.
_AWARD_PARTNER = re.compile(
    r"Microsoft\s+Partner\s+(Of\s+The\s+Year|Network|Center)",
    re.IGNORECASE,
)

# "trading partner" / "channel partner" / "payment partner" — domain-of-art
# usage in retail / supply-chain / payments where "partner" is the term of
# art for a SOR-side counterpart, not a Deloitte-Microsoft commercial
# relationship.
_DOMAIN_PARTNER = re.compile(
    r"\b(trading|channel|payment|business|community|supply|EDI|fusion)\s+partner",
    re.IGNORECASE,
)

# Quoted / metalinguistic — prose where the rule itself is being
# explained tends to wrap the forbidden term in quotes or backticks.
# We allow when the match appears inside any pair of "...", '...',
# `...`, curly “...”, ‘...’, etc., within the context window.
_QUOTED_TERM = re.compile(
    r"""["'`“‘][^"'`”’\n]{0,120}\b(partner|partnership|alliance|partnered|allied|endorse)[^"'`”’\n]{0,120}["'`”’]""",
    re.IGNORECASE,
)

# Explicit negation — "not partnered with X" / "never call X 'partner'" /
# "no commercial alliance" / "does not claim partnership" / "is not in
# partnership with" — these negate the relationship rather than asserting
# it. We allow up to 8 intervening words between the negator and the term.
_NEGATED_TERM = re.compile(
    r"\b(not|never|no|without|neither|nor|isn'?t|aren'?t|wasn'?t|weren'?t|"
    r"don'?t|doesn'?t|didn'?t|hasn'?t|haven'?t|hadn'?t)"
    r"(\s+\S+){0,8}\s+"
    r"(partner(s|ed|ing|ship)?|allied|alliance|endorse(s|d|ment)?)\b",
    re.IGNORECASE,
)

# "the OpenClaw community pattern" / "is a community pattern Deloitte adopted"
# — APEX-CORE Appendix A discusses the OpenClaw lineage and explicitly
# disclaims the relationship. We allow the surrounding pattern.
_COMMUNITY_PATTERN = re.compile(
    r"\bcommunity\s+pattern\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

DELOITTE_MICROSOFT_INDEPENDENCE = RulePack(
    pack_id="deloitte_microsoft_independence",
    name="Deloitte-Microsoft Independence",
    description=(
        "Independence-language rules — APEX never describes Microsoft "
        "(or any third-party SOR vendor) as a partner / alliance partner / "
        "endorsing party. Per Deloitte Independence Office guidance."
    ),
    rules=(
        Rule(
            rule_id="deloitte_microsoft_independence.partner",
            description="Forbidden: describing a third-party vendor as a 'partner'.",
            pattern=make_pattern("partner"),
            severity=Severity.ERROR,
            guidance=(
                "Per Independence Office guidance, APEX must not describe "
                "Microsoft (or any SOR vendor) as a 'partner'. "
                "Domain-of-art usage like 'trading partner' / 'channel partner' "
                "is allowed and auto-suppressed."
            ),
            approved_substitutes=(
                "the platform",
                "the underlying technology",
                "the vendor",
                "the provider",
            ),
            allowed_contexts=(
                _AWARD_PARTNER, _DOMAIN_PARTNER, _QUOTED_TERM, _NEGATED_TERM,
            ),
        ),
        Rule(
            rule_id="deloitte_microsoft_independence.alliance",
            description="Forbidden: describing a third-party vendor as an 'alliance partner' or 'in alliance with'.",
            pattern=make_pattern("alliance"),
            severity=Severity.ERROR,
            guidance=(
                "Independence-language: 'alliance' implies a commercial "
                "relationship that does not exist. Use 'platform' / 'technology stack'."
            ),
            approved_substitutes=("platform", "technology stack", "the platform"),
            allowed_contexts=(_QUOTED_TERM, _NEGATED_TERM),
        ),
        Rule(
            rule_id="deloitte_microsoft_independence.partnership",
            description="Forbidden: 'partnership' between Deloitte and Microsoft (or any SOR vendor).",
            pattern=make_pattern("partnership"),
            severity=Severity.ERROR,
            guidance=(
                "'Partnership' implies a commercial relationship that is "
                "Independence-restricted. Reword as a community pattern, "
                "an integration, or a deployment posture."
            ),
            approved_substitutes=(
                "integration",
                "deployment",
                "community pattern",
                "adoption",
            ),
            allowed_contexts=(_QUOTED_TERM, _NEGATED_TERM, _COMMUNITY_PATTERN),
        ),
        Rule(
            rule_id="deloitte_microsoft_independence.endorse",
            description="Forbidden: claiming a third-party vendor 'endorses' Deloitte or APEX.",
            pattern=re.compile(r"\bendors(e|ed|es|ing|ement)\b", re.IGNORECASE),
            severity=Severity.ERROR,
            guidance=(
                "APEX never claims vendor endorsement. Reword as 'aligned with', "
                "'consistent with', or 'built on'."
            ),
            approved_substitutes=("aligned with", "consistent with", "built on"),
            allowed_contexts=(_QUOTED_TERM, _NEGATED_TERM),
        ),
        Rule(
            rule_id="deloitte_microsoft_independence.recommended_by",
            description="Forbidden: 'recommended by Microsoft' / 'recommended by SAP' etc.",
            pattern=re.compile(r"\brecommended\s+by\s+(microsoft|sap|oracle|salesforce|epic|workday|ibm|amazon|google|aws)\b", re.IGNORECASE),
            severity=Severity.ERROR,
            guidance=(
                "Vendor-recommendation language implies a commercial relationship "
                "Deloitte does not assert. Reword to describe the technical posture "
                "without invoking vendor authority."
            ),
            approved_substitutes=("aligned with the vendor's reference architecture",),
        ),
        Rule(
            rule_id="deloitte_microsoft_independence.deloitte_microsoft_jointly",
            description="Forbidden: 'Deloitte and Microsoft jointly' or 'co-developed'.",
            pattern=re.compile(
                r"\b(Deloitte\s+and\s+Microsoft\s+(jointly|together|co-?developed|co-?delivered))\b",
                re.IGNORECASE,
            ),
            severity=Severity.ERROR,
            guidance=(
                "'Jointly' / 'co-developed' / 'co-delivered' between Deloitte "
                "and Microsoft is Independence-restricted. APEX is Deloitte-built "
                "on top of Microsoft technology; reword to that posture."
            ),
            approved_substitutes=("APEX is built on Microsoft Fabric and Foundry",),
        ),
        Rule(
            rule_id="deloitte_microsoft_independence.gold_partner",
            description="Forbidden: 'Gold Partner' / 'Platinum Partner' tier badges.",
            pattern=re.compile(r"\b(Gold|Platinum|Premier)\s+Partner\b", re.IGNORECASE),
            severity=Severity.ERROR,
            guidance=(
                "Tier-badge language is partner-program terminology. APEX content "
                "should describe the underlying capability, not the tier."
            ),
            approved_substitutes=("certified on the platform", "deployed on the platform"),
        ),
    ),
    version="0.1.0",
)
