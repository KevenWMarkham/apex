"""APEX typography rule pack — Sprint 29 Task 29.10.3.

These rules enforce the design-system typography baseline at the text
level: APEX content uses Fraunces (display), IBM Plex Sans (body),
JetBrains Mono (code). Inline references to other fonts are flagged
so the design-token registry stays the single source of truth.

Note: full typography enforcement also lives at the CSS level
(Sprint 29 Task 29.10.3 typography-correctness lane). This rule pack
catches *prose* drift (e.g., "use Helvetica for body" in a doc) — the
CSS lane catches *implementation* drift.
"""

from __future__ import annotations

import re

from apex_compliance_lint.types import Rule, RulePack, Severity


APEX_TYPOGRAPHY = RulePack(
    pack_id="apex_typography",
    name="APEX Typography",
    description=(
        "APEX design-system typography baseline — Fraunces (display), "
        "IBM Plex Sans (body), JetBrains Mono (code). Flags prose "
        "references to other fonts that would drift from the registry."
    ),
    rules=(
        Rule(
            rule_id="apex_typography.unapproved_font",
            description="Prose mentions a font outside the APEX design-token registry.",
            pattern=re.compile(
                r"\b(Helvetica|Arial|Times\s+New\s+Roman|Calibri|Comic\s+Sans|"
                r"Courier|Verdana|Tahoma|Georgia|Cambria|Segoe\s+UI)\b",
                re.IGNORECASE,
            ),
            severity=Severity.WARNING,
            guidance=(
                "APEX uses Fraunces / IBM Plex Sans / JetBrains Mono per "
                "Appendix N (design-system reference). Prose suggesting an "
                "alternate font drifts from the design-token registry."
            ),
            approved_substitutes=(
                "Fraunces (display)",
                "IBM Plex Sans (body)",
                "JetBrains Mono (code)",
            ),
        ),
    ),
    version="0.1.0",
)
