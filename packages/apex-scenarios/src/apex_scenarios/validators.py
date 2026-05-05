"""Scenario governance validators — Sprint 28 Tasks 28.1.6 + 28.7.2-5.

Five validators ship in this module:

1. **Wave-data presence** (Task 28.1.6) — every library row has non-empty
   ``w1`` / ``w2`` / ``w3``.
2. **Service-catalog resolution** (Task 28.7.2) — every ``service_code``
   resolves to a registered Service Catalog entry.
3. **Agent-catalog resolution** (Task 28.7.3) — every featured-scenario
   ``Solution`` references an agent registered in the Agent Catalog.
4. **KPI-registry resolution** (Task 28.7.4) — every featured-scenario
   ``KPI`` resolves to an Appendix-C entry.
5. **Versioning classification** (Task 28.7.5) — given two scenario
   library versions, classify the diff as PATCH / MINOR / MAJOR.

Each validator returns a structured :class:`ValidationReport` with an
``exit_code`` property suitable for CI gating.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

from apex_scenarios.models import FeaturedChain, Scenario


# ---------------------------------------------------------------------------
# Common report dataclasses
# ---------------------------------------------------------------------------


@dataclass
class ValidationIssue:
    """One validation failure."""

    code: str
    """Short machine-readable issue code (e.g., 'WAVE_MISSING')."""

    severity: str = "error"
    """One of 'info', 'warning', 'error'."""

    scope: str = ""
    """Identifier of the offending object (e.g., 'RC#42')."""

    message: str = ""
    """Human-readable detail."""


@dataclass
class ValidationReport:
    """Aggregate report from one validator pass."""

    name: str
    issues: list[ValidationIssue] = field(default_factory=list)
    nodes_checked: int = 0

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1

    def summary(self) -> str:
        return (
            f"[{self.name}] {self.nodes_checked} checked, "
            f"{len(self.errors)} error(s), {len(self.warnings)} warning(s)."
        )


# ---------------------------------------------------------------------------
# Task 28.1.6 — Wave-data presence
# ---------------------------------------------------------------------------


def validate_wave_data_presence(scenarios: Iterable[Scenario]) -> ValidationReport:
    """Every library row must have non-empty w1, w2, w3 fields.

    Sprint 28 Task 28.1.6 exit criterion. Pre-Sprint-28 rows lack these
    fields entirely; this validator is the gate that flips the library
    from "wave-incomplete" to "wave-complete".
    """
    report = ValidationReport(name="wave_data_presence")
    for s in scenarios:
        report.nodes_checked += 1
        missing: list[str] = []
        if not s.w1.strip():
            missing.append("w1")
        if not s.w2.strip():
            missing.append("w2")
        if not s.w3.strip():
            missing.append("w3")
        if missing:
            report.issues.append(
                ValidationIssue(
                    code="WAVE_MISSING",
                    scope=f"{s.practice or '?'}::{s.service_code} '{s.title}'",
                    message=f"Missing wave content: {', '.join(missing)}",
                )
            )
    return report


# ---------------------------------------------------------------------------
# Task 28.7.2 — Scenario → Service Catalog resolution
# ---------------------------------------------------------------------------


def validate_service_codes(
    scenarios: Iterable[Scenario],
    *,
    service_catalog_codes: set[str] | None = None,
) -> ValidationReport:
    """Every scenario's ``service_code`` must resolve to a Service Catalog entry.

    Args:
        scenarios: Library rows to check.
        service_catalog_codes: Set of registered service codes from
            BL.P.110–116 Service Catalogs. If None, the validator falls
            back to a structural check (the code must match the
            ``{PRACTICE}-{TRACK}-{NN}`` pattern).
    """
    report = ValidationReport(name="service_codes")
    # Structural pattern: {PRACTICE}-{Track}-{NN}
    #
    # Practice is one of the seven canonical APEX practices.
    # Track is alphanumeric (case-insensitive), 2–15 chars. Real-world
    # vocabulary observed across the 723-row live library:
    #   E2E TTP FUSION FOUNDATION QMS Supply Connected Ops Aftermarket EaaS
    #   AIR HOT OG PU MN LS TEC MED   (Practice sub-segments)
    # NN is 2–3 digits.
    #
    # The structural check keeps the validator deterministic without
    # hardcoding a closed enumeration that would drift as the Service
    # Catalog evolves. Closed-enum resolution is the second mode and
    # fires when ``service_catalog_codes`` is supplied (BL.P.110–116).
    # Track may be hyphenated (e.g., "Connected-Factory") — allow up to
    # 3 segments before the trailing numeric code.
    pattern = re.compile(
        r"^(RC|HLS|ER|AXLE|TMT|TH|ICE)-"
        r"([A-Za-z][A-Za-z0-9]{1,14}(?:-[A-Za-z][A-Za-z0-9]{1,14}){0,2})"
        r"-\d{2,3}$"
    )

    for s in scenarios:
        report.nodes_checked += 1
        code = (s.service_code or "").strip()

        if not code:
            report.issues.append(
                ValidationIssue(
                    code="SERVICE_CODE_EMPTY",
                    scope=f"{s.practice or '?'}::'{s.title}'",
                    message="Empty service_code",
                )
            )
            continue

        if service_catalog_codes is not None:
            if code not in service_catalog_codes:
                report.issues.append(
                    ValidationIssue(
                        code="SERVICE_CODE_UNRESOLVED",
                        scope=f"{s.practice or '?'}::{code} '{s.title}'",
                        message=(
                            f"Service code {code!r} is not registered in the "
                            f"Service Catalog (BL.P.110–116)."
                        ),
                    )
                )
        else:
            if not pattern.match(code):
                report.issues.append(
                    ValidationIssue(
                        code="SERVICE_CODE_MALFORMED",
                        scope=f"{s.practice or '?'}::'{s.title}'",
                        message=(
                            f"Service code {code!r} does not match "
                            "{PRACTICE}-{TRACK}-{NN} pattern."
                        ),
                    )
                )
    return report


# ---------------------------------------------------------------------------
# Task 28.7.3 — Scenario → Agent Catalog resolution
# ---------------------------------------------------------------------------


# Regex matches "<X> agent" where X is a noun phrase. Captures X.
_AGENT_NAME_RE = re.compile(
    r"\b([a-z][a-z0-9 \-]{2,40}?)\s+agent\b",
    re.IGNORECASE,
)

#: Common English determiners / conjunctions / prepositions that should be
#: stripped from the leading edge of a captured agent-name phrase.
#: A real agent name does not start with any of these.
_LEADING_NONNAME = {
    "the", "a", "an", "this", "that", "these", "those",
    "and", "or", "but", "for", "with", "by", "of", "from", "to", "into",
    "on", "at", "as", "via", "through", "across",
}

#: Maximum noun-phrase length (in words) to retain. Empirically a
#: well-named APEX agent fits in 3 tokens
#: (e.g., "perishables-integrity", "recall response", "cold chain response").
_MAX_PHRASE_WORDS = 3


def extract_agent_references(text: str) -> list[str]:
    """Return all agent-name references in a Solution string.

    Recognizes patterns like ``"perishables-integrity agent"``,
    ``"recall response agent"``. The greedy regex may capture material
    leading up to the agent phrase across clause boundaries; this
    function post-processes by:

    1. Stripping leading determiners / conjunctions / prepositions.
    2. Capping to the last :data:`_MAX_PHRASE_WORDS` tokens (the
       rightmost tokens are the most-specific noun phrase).
    3. Stripping again in case the cap left a leading non-name word.

    Returns lowercased, whitespace-collapsed phrases.
    """
    refs: list[str] = []
    for m in _AGENT_NAME_RE.finditer(text):
        ref = re.sub(r"\s+", " ", m.group(1)).strip().lower()
        words = ref.split(" ")

        # Phase 1: strip leading non-name tokens
        while words and words[0] in _LEADING_NONNAME:
            words = words[1:]
        # Phase 2: cap to most-specific tail
        if len(words) > _MAX_PHRASE_WORDS:
            words = words[-_MAX_PHRASE_WORDS:]
        # Phase 3: strip again in case the cap left a determiner up front
        while words and words[0] in _LEADING_NONNAME:
            words = words[1:]

        ref = " ".join(words)
        if ref:
            refs.append(ref)
    return refs


def _agent_resolves(ref: str, catalog: set[str]) -> bool:
    """Return True if ``ref`` (or any trailing substring of it) is in catalog.

    A capture like "real-time perishables-integrity" should resolve when
    "perishables-integrity" is registered, even if the full phrase is
    not. Walks the words right-to-left.
    """
    words = ref.split(" ")
    for i in range(len(words)):
        candidate = " ".join(words[i:])
        if candidate in catalog:
            return True
    return False


def validate_agent_references(
    chains: Iterable[FeaturedChain],
    *,
    agent_catalog_names: set[str] | None = None,
) -> ValidationReport:
    """Featured-scenario Solution strings must name agents in the Agent Catalog.

    Args:
        chains: Featured-chain rows.
        agent_catalog_names: Set of normalized agent names from
            BL.P.58–64 Agent Catalogs (lowercased, single-spaced). If
            None, agent-existence checking is downgraded to a warning
            (the Solution must mention at least one ``... agent`` phrase).
    """
    report = ValidationReport(name="agent_references")
    for c in chains:
        report.nodes_checked += 1
        refs = extract_agent_references(c.Solution)

        if not refs:
            report.issues.append(
                ValidationIssue(
                    code="AGENT_REF_MISSING",
                    severity="warning",
                    scope=c.title,
                    message=(
                        "Solution does not mention any '... agent'. "
                        "Featured chains should name the agents that realize them."
                    ),
                )
            )
            continue

        if agent_catalog_names is not None:
            unresolved = [
                r for r in refs if not _agent_resolves(r, agent_catalog_names)
            ]
            for u in unresolved:
                report.issues.append(
                    ValidationIssue(
                        code="AGENT_REF_UNRESOLVED",
                        scope=c.title,
                        message=f"Agent reference {u!r} not in Agent Catalog (BL.P.58–64).",
                    )
                )
    return report


# ---------------------------------------------------------------------------
# Task 28.7.4 — Scenario → KPI Registry resolution
# ---------------------------------------------------------------------------


# Two delta-token shapes supported:
#
# 1. Percentage / point-style:  "+2.4pp GM", "+18% margin", "-15% MAPE",
#    "8 pts FCR".  Captures trailing word(s) as the KPI name.
# 2. Money-style:               "+$2.8M/yr recovery",
#    "−$18M inventory" (note minus is U+2212 from upstream data).
#    Captures trailing word(s) as the KPI name.
# A "value" is one number, optionally with a decimal, optionally with a
# range partner like "6-9" (inclusive range), and an optional unit suffix.
_VALUE_PCT = r"\d+(?:\.\d+)?(?:[\-\u2013]\d+(?:\.\d+)?)?"
_UNIT_PCT = r"(?:%|pp|pts?|bps|x)?"
_KPI_NAME = r"[A-Za-z][A-Za-z0-9 \-/&]*?"

_KPI_DELTA_PCT_RE = re.compile(
    rf"^[+\-\u2212]?\s*{_VALUE_PCT}\s*{_UNIT_PCT}\s+({_KPI_NAME})\s*$"
)
_KPI_DELTA_MONEY_RE = re.compile(
    rf"^[+\-\u2212]?\s*\$\s*{_VALUE_PCT}\s*[KMB]?(?:/yr)?\s+({_KPI_NAME})\s*$"
)


def extract_kpi_name(kpi_field: str) -> str | None:
    """Pull the KPI name out of a delta string.

    Examples
    --------
    - ``"+2.4pp GM"``           → ``"GM"``
    - ``"+18% margin"``         → ``"margin"``
    - ``"-15% MAPE"``           → ``"MAPE"``
    - ``"+$2.8M/yr recovery"``  → ``"recovery"``
    - ``"−$18M inventory"``     → ``"inventory"`` (U+2212 minus accepted)

    Returns None if the string does not match either shape.
    """
    text = kpi_field.strip()
    m = _KPI_DELTA_PCT_RE.match(text) or _KPI_DELTA_MONEY_RE.match(text)
    if m is None:
        return None
    return m.group(1).strip()


def validate_kpis(
    scenarios: Iterable[Scenario],
    *,
    kpi_registry_names: set[str] | None = None,
) -> ValidationReport:
    """Every scenario's KPI must resolve to an Appendix-C entry.

    Args:
        scenarios: Rows to check.
        kpi_registry_names: Set of registered KPI names from BL.P.122
            (case-insensitive). If None, the validator only checks that
            the KPI delta string is parseable.
    """
    report = ValidationReport(name="kpis")
    for s in scenarios:
        report.nodes_checked += 1
        name = extract_kpi_name(s.kpi)

        if name is None:
            report.issues.append(
                ValidationIssue(
                    code="KPI_DELTA_UNPARSEABLE",
                    scope=f"{s.practice or '?'}::{s.service_code} '{s.title}'",
                    message=(
                        f"KPI string {s.kpi!r} does not match the canonical "
                        "delta pattern (e.g. '+2.4pp GM', '+18% margin')."
                    ),
                )
            )
            continue

        if kpi_registry_names is not None:
            if name.lower() not in {n.lower() for n in kpi_registry_names}:
                report.issues.append(
                    ValidationIssue(
                        code="KPI_UNRESOLVED",
                        scope=f"{s.practice or '?'}::{s.service_code} '{s.title}'",
                        message=(
                            f"KPI {name!r} is not registered in the KPI "
                            "Registry (BL.P.122 Appendix C)."
                        ),
                    )
                )
    return report


# ---------------------------------------------------------------------------
# Task 28.7.5 — Versioning rules
# ---------------------------------------------------------------------------


@dataclass
class VersioningClassification:
    """Result of comparing two scenario-library versions."""

    bump: str
    """One of 'PATCH', 'MINOR', 'MAJOR'."""

    rationale: str
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    field_schema_changed: bool = False


def classify_library_bump(
    before: list[Scenario],
    after: list[Scenario],
) -> VersioningClassification:
    """Classify the diff between two library versions per Task 28.7.5 rules.

    - **PATCH** — copy edits or KPI re-measurements only. No structural
      changes; same set of scenarios; no field-schema additions.
    - **MINOR** — at least one new scenario added (or removed). No
      field-schema change.
    - **MAJOR** — at least one field-schema change (a key added or
      removed from the :class:`Scenario` model on at least one row).
    """
    def _key(s: Scenario) -> str:
        return f"{s.practice or '?'}::{s.service_code}::{s.title}"

    def _fields(s: Scenario) -> set[str]:
        # All fields whose value is not the model's default
        data = s.model_dump(exclude_unset=True)
        return set(data.keys())

    before_keys = {_key(s) for s in before}
    after_keys = {_key(s) for s in after}

    added = sorted(after_keys - before_keys)
    removed = sorted(before_keys - after_keys)

    # Field-schema change: any row in `after` that has a key never seen
    # across all of `before`, or vice versa.
    before_field_set = set().union(*(_fields(s) for s in before)) if before else set()
    after_field_set = set().union(*(_fields(s) for s in after)) if after else set()
    field_schema_changed = before_field_set != after_field_set

    if field_schema_changed:
        return VersioningClassification(
            bump="MAJOR",
            rationale=(
                "Field schema changed across rows: "
                f"added={sorted(after_field_set - before_field_set)}, "
                f"removed={sorted(before_field_set - after_field_set)}"
            ),
            added=added,
            removed=removed,
            field_schema_changed=True,
        )

    if added or removed:
        return VersioningClassification(
            bump="MINOR",
            rationale=(
                f"Scenario set changed: added={len(added)}, "
                f"removed={len(removed)}, no field-schema change"
            ),
            added=added,
            removed=removed,
        )

    return VersioningClassification(
        bump="PATCH",
        rationale="No new/removed scenarios and no field-schema change. Copy or KPI re-measurement only.",
    )
