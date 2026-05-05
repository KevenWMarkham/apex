"""W1 Foundation Catalog — Sprint 28 Task 28.2 (BL.P.171–173).

The W1 Foundation catalog enumerates the **reusable building blocks** that
compose into Wave-1 deliverables across engagements. Sellers Guide §2.2
treats Wave-1 as "Envision & Land" — the Foundation catalog is the
underlying primitives every Wave-1 SoW draws from.

Five canonical classes (per build instructions §28.2.1):

- **schema** — canonical-schema instantiations (Bronze→Silver mappings
  authored, DLP labels, Purview classifications)
- **ledger** — audit-row pipelines, replay-token plumbing, regulator-
  grade evidence stores
- **mcp** — MCP tool boots (read-only foundations + write-tool HITL
  surfaces wired)
- **hitl** — HITL-gate plumbing: Teams cards, Copilot Studio surfaces,
  approval-state machines, SLA timers
- **policy** — Sprint 13 governance baselines: Purview labels + DLP
  rules + Entra Conditional Access

Per-block fields (Task 28.2.2):

- ``name`` — short stable identifier
- ``cls`` — one of the five classes above
- ``description`` — what this block delivers
- ``schemas_touched`` — canonical schema codes (SCML, MERML, etc.)
- ``effort_story_points`` + ``effort_calendar_weeks`` — Wave-1 SoW-quotable
- ``prerequisites`` — other building blocks this depends on
- ``unblocks_w2_scenarios`` — list of Wave-2 scenario service codes whose
  delivery is unblocked by this Foundation block (Task 28.2.4)

The HTML tab (Task 28.2.3) is the front-end track's work; this module
ships the **data + tooling**: the 40 reusable blocks, the dependency-graph
walker (Task 28.2.4), and the SoW-quotable effort roll-up (Task 28.2.5).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Literal


FoundationClass = Literal["schema", "ledger", "mcp", "hitl", "policy"]
FOUNDATION_CLASSES: tuple[FoundationClass, ...] = (
    "schema", "ledger", "mcp", "hitl", "policy",
)


@dataclass(frozen=True)
class FoundationBlock:
    """One Wave-1 reusable building block."""

    name: str
    cls: FoundationClass
    description: str
    schemas_touched: tuple[str, ...] = ()
    effort_story_points: int = 0
    effort_calendar_weeks: float = 0.0
    prerequisites: tuple[str, ...] = ()
    """Names of other FoundationBlocks this depends on."""

    unblocks_w2_scenarios: tuple[str, ...] = ()
    """Wave-2 scenario service codes (e.g., ``RC-E2E-04``) this unblocks."""


@dataclass
class EffortRollup:
    """SoW-quotable effort sum across a chosen subset of blocks."""

    selected_count: int
    total_story_points: int
    total_calendar_weeks: float
    parallelizable_calendar_weeks: float
    """Effort assuming maximum parallelization — wall-clock duration if
    every prerequisite-respecting branch runs in parallel."""

    by_class: dict[FoundationClass, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Catalog — 40 reusable W1 building blocks
# ---------------------------------------------------------------------------


CATALOG: tuple[FoundationBlock, ...] = (
    # ----- schema (12) -----
    FoundationBlock(
        name="scml-bronze-silver", cls="schema",
        description="SCML (Supply Chain) Bronze→Silver mappings + Purview label propagation for FSMA 204 readiness.",
        schemas_touched=("SCML",), effort_story_points=8, effort_calendar_weeks=2.0,
        unblocks_w2_scenarios=("RC-E2E-03", "RC-E2E-04", "RC-E2E-06"),
    ),
    FoundationBlock(
        name="merml-bronze-silver", cls="schema",
        description="MERML (Merchandising) Bronze→Silver — assortment, markdown, pricing entities.",
        schemas_touched=("MERML",), effort_story_points=8, effort_calendar_weeks=2.0,
        unblocks_w2_scenarios=("RC-E2E-05", "RC-E2E-09"),
    ),
    FoundationBlock(
        name="cxml-bronze-silver", cls="schema",
        description="CXML (Customer Experience) Bronze→Silver — identity, journey, consent.",
        schemas_touched=("CXML",), effort_story_points=8, effort_calendar_weeks=2.0,
        prerequisites=("policy-pii-classification",),
        unblocks_w2_scenarios=("RC-E2E-07",),
    ),
    FoundationBlock(
        name="patientml-bronze-silver", cls="schema",
        description="PatientML Bronze→Silver — Epic Clarity mirroring + FHIR-shaped Silver.",
        schemas_touched=("PatientML",), effort_story_points=13, effort_calendar_weeks=3.0,
        prerequisites=("policy-phi-classification",),
        unblocks_w2_scenarios=("HLS-E2E-01", "HLS-E2E-02", "HLS-E2E-03"),
    ),
    FoundationBlock(
        name="claimml-bronze-silver", cls="schema",
        description="ClaimML (HLS revenue cycle) — 837/835/270/271 EDI ingest into Silver.",
        schemas_touched=("ClaimML",), effort_story_points=8, effort_calendar_weeks=2.0,
        prerequisites=("policy-phi-classification",),
        unblocks_w2_scenarios=("HLS-PAY-01",),
    ),
    FoundationBlock(
        name="encounterml-bronze-silver", cls="schema",
        description="EncounterML — clinical-encounter Silver rows for utilization-management agents.",
        schemas_touched=("EncounterML",), effort_story_points=5, effort_calendar_weeks=1.5,
        prerequisites=("patientml-bronze-silver",),
    ),
    FoundationBlock(
        name="gridml-bronze-silver", cls="schema",
        description="GridML (Utility) Bronze→Silver — substations, feeders, sections, assets per IEC CIM.",
        schemas_touched=("GridML",), effort_story_points=13, effort_calendar_weeks=3.0,
        prerequisites=("policy-cip-014-classification",),
        unblocks_w2_scenarios=("ER-PU-01", "ER-PU-02"),
    ),
    FoundationBlock(
        name="outageml-bronze-silver", cls="schema",
        description="OutageML — outage events + restoration ledger feeding the triage agent.",
        schemas_touched=("OutageML",), effort_story_points=5, effort_calendar_weeks=1.5,
        prerequisites=("gridml-bronze-silver",),
    ),
    FoundationBlock(
        name="qmsml-bronze-silver", cls="schema",
        description="QMSML (Quality) Bronze→Silver — non-conformances, supplier lots, corrective actions.",
        schemas_touched=("QMSML",), effort_story_points=8, effort_calendar_weeks=2.0,
        unblocks_w2_scenarios=("AXLE-QMS-01",),
    ),
    FoundationBlock(
        name="opsml-th-bronze-silver", cls="schema",
        description="OpsML-TH (Travel/Hospitality) — flight legs, crew pairings, gates per IATA SSIM.",
        schemas_touched=("OpsML-TH",), effort_story_points=13, effort_calendar_weeks=3.0,
        unblocks_w2_scenarios=("TH-AIR-01", "TH-AIR-04"),
    ),
    FoundationBlock(
        name="travelerml-bronze-silver", cls="schema",
        description="TravelerML — traveler-360 Silver with PII-tokenization at adapter boundary.",
        schemas_touched=("TravelerML",), effort_story_points=8, effort_calendar_weeks=2.0,
        prerequisites=("policy-pii-classification",),
        unblocks_w2_scenarios=("TH-AIR-03",),
    ),
    FoundationBlock(
        name="bssml-bronze-silver", cls="schema",
        description="BSSML (TMT subscriber) — Bronze→Silver from Amdocs/NetCracker.",
        schemas_touched=("BSSML",), effort_story_points=8, effort_calendar_weeks=2.0,
        prerequisites=("policy-pii-classification",),
    ),

    # ----- ledger (8) -----
    FoundationBlock(
        name="audit-row-pipeline", cls="ledger",
        description="Universal audit-row pipeline per Sellers Guide §6.10 — append-only, replay-token-bearing.",
        effort_story_points=8, effort_calendar_weeks=2.0,
    ),
    FoundationBlock(
        name="replay-token-store", cls="ledger",
        description="Forensic replay-token store; powers post-incident decision replay.",
        effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("audit-row-pipeline",),
    ),
    FoundationBlock(
        name="purview-audit-premium", cls="ledger",
        description="Purview Audit Premium tenant config + long-retention path — supports regulator-grade audit retention.",
        effort_story_points=3, effort_calendar_weeks=0.5,
    ),
    FoundationBlock(
        name="psps-evidence-ledger", cls="ledger",
        description="PSPS-decision evidence ledger — every input timestamp + provenance pinned for PUC/FERC defense.",
        effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("audit-row-pipeline", "purview-audit-premium"),
        unblocks_w2_scenarios=("ER-PU-01",),
    ),
    FoundationBlock(
        name="sep1-bundle-ledger", cls="ledger",
        description="SEP-1 bundle compliance ledger — CMS-reportable SEP-1 abstraction from EHR + agent-decision rows.",
        effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("patientml-bronze-silver", "audit-row-pipeline"),
        unblocks_w2_scenarios=("HLS-E2E-01",),
    ),
    FoundationBlock(
        name="fsma-204-ledger", cls="ledger",
        description="FSMA 204 traceability-event ledger — SCML lots + EPCIS events + disposition decisions.",
        effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("scml-bronze-silver", "audit-row-pipeline"),
        unblocks_w2_scenarios=("RC-E2E-04",),
    ),
    FoundationBlock(
        name="claim-cycle-ledger", cls="ledger",
        description="837→835 claim-cycle ledger with denial/recovery attribution for value-share.",
        effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("claimml-bronze-silver", "audit-row-pipeline"),
        unblocks_w2_scenarios=("HLS-PAY-01",),
    ),
    FoundationBlock(
        name="dispatch-decision-ledger", cls="ledger",
        description="Crew dispatch + ETR ledger for outage restoration audit trail.",
        effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("outageml-bronze-silver", "audit-row-pipeline"),
        unblocks_w2_scenarios=("ER-PU-02",),
    ),

    # ----- mcp (10) -----
    FoundationBlock(
        name="scml-mcp-readonly", cls="mcp",
        description="SCML MCP read-only tool surface (lot.get, hierarchy.tree, trace.get).",
        schemas_touched=("SCML",), effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("scml-bronze-silver",),
    ),
    FoundationBlock(
        name="merml-mcp-readonly", cls="mcp",
        description="MERML MCP read-only — assortment, markdown, pricing reads.",
        schemas_touched=("MERML",), effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("merml-bronze-silver",),
    ),
    FoundationBlock(
        name="cxml-mcp-readonly", cls="mcp",
        description="CXML MCP read-only with PII tokenization at the tool boundary.",
        schemas_touched=("CXML",), effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("cxml-bronze-silver",),
    ),
    FoundationBlock(
        name="patientml-mcp-readonly", cls="mcp",
        description="PatientML MCP read-only — patient.get, identity.lookup, encounter.get with PHI redaction.",
        schemas_touched=("PatientML",), effort_story_points=8, effort_calendar_weeks=1.5,
        prerequisites=("patientml-bronze-silver",),
    ),
    FoundationBlock(
        name="claimml-mcp-readonly", cls="mcp",
        description="ClaimML MCP read-only — denial.lookup, recovery.estimate, payer.policy.lookup.",
        schemas_touched=("ClaimML",), effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("claimml-bronze-silver",),
    ),
    FoundationBlock(
        name="gridml-mcp-readonly", cls="mcp",
        description="GridML MCP read-only — feeder.get, asset.health.score, weather.forecast.lookup.",
        schemas_touched=("GridML",), effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("gridml-bronze-silver",),
    ),
    FoundationBlock(
        name="qmsml-mcp-readonly", cls="mcp",
        description="QMSML MCP read-only — defect.cluster.get, supplier.lot.trace.",
        schemas_touched=("QMSML",), effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("qmsml-bronze-silver",),
    ),
    FoundationBlock(
        name="opsml-mcp-readonly", cls="mcp",
        description="OpsML-TH MCP read-only — flight.leg.state, crew.legality, gate.assignment.",
        schemas_touched=("OpsML-TH",), effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("opsml-th-bronze-silver",),
    ),
    FoundationBlock(
        name="write-tool-hitl-wiring", cls="mcp",
        description="Generic write-tool HITL wiring — Charter cacheable:false enforced, hitl_required gate fires before commit.",
        effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("audit-row-pipeline",),
    ),
    FoundationBlock(
        name="terminology-service-stub", cls="mcp",
        description="MockTerminologyService for SNOMED/LOINC/RxNorm lookups; production wires tenant terminology service.",
        effort_story_points=3, effort_calendar_weeks=0.5,
    ),

    # ----- hitl (5) -----
    FoundationBlock(
        name="teams-card-surface", cls="hitl",
        description="Teams adaptive-card HITL surface — Sprint 16 default for store-manager / charge-nurse / dispatcher gates.",
        effort_story_points=8, effort_calendar_weeks=2.0,
    ),
    FoundationBlock(
        name="copilot-studio-surface", cls="hitl",
        description="Copilot Studio HITL surface for richer approval flows (multi-step, attachments).",
        effort_story_points=8, effort_calendar_weeks=2.0,
    ),
    FoundationBlock(
        name="approval-state-machine", cls="hitl",
        description="HITL approval state machine — pending / approved / rejected / escalated / sla-breached.",
        effort_story_points=5, effort_calendar_weeks=1.0,
    ),
    FoundationBlock(
        name="sla-timer-redis", cls="hitl",
        description="HITL SLA timers via Redis sorted-set (Sprint 26 §11) — enqueue + pop-expired.",
        effort_story_points=3, effort_calendar_weeks=0.5,
        prerequisites=("approval-state-machine",),
    ),
    FoundationBlock(
        name="vp-level-gate", cls="hitl",
        description="VP-level HITL gate (e.g., PSPS de-energization) — extra signature step + counsel notification.",
        effort_story_points=3, effort_calendar_weeks=0.5,
        prerequisites=("approval-state-machine",),
    ),

    # ----- policy (5) -----
    FoundationBlock(
        name="policy-pii-classification", cls="policy",
        description="Sprint 13 PII classification baseline — Purview label, DLP rules, Conditional Access.",
        effort_story_points=5, effort_calendar_weeks=1.0,
    ),
    FoundationBlock(
        name="policy-phi-classification", cls="policy",
        description="HIPAA + 42 CFR Part 2 classification baseline.",
        effort_story_points=5, effort_calendar_weeks=1.0,
        prerequisites=("policy-pii-classification",),
    ),
    FoundationBlock(
        name="policy-pci-classification", cls="policy",
        description="Restricted-PCI classification baseline — payment-card data NEVER leaves canonical SOR.",
        effort_story_points=3, effort_calendar_weeks=0.5,
    ),
    FoundationBlock(
        name="policy-cip-014-classification", cls="policy",
        description="CIP-014 critical-infrastructure classification — utility OT/IT segmentation.",
        effort_story_points=5, effort_calendar_weeks=1.0,
    ),
    FoundationBlock(
        name="policy-ip-cui-classification", cls="policy",
        description="Intellectual-property + Controlled-Unclassified classification (engineering, defense-adjacent).",
        effort_story_points=3, effort_calendar_weeks=0.5,
    ),
)


assert len(CATALOG) >= 40, f"Sprint 28 §28.2.1 requires ≥ 40 blocks, got {len(CATALOG)}"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def all_blocks() -> tuple[FoundationBlock, ...]:
    """Return the full catalog."""
    return CATALOG


def get_block(name: str) -> FoundationBlock | None:
    """Lookup a block by stable name."""
    for b in CATALOG:
        if b.name == name:
            return b
    return None


def blocks_by_class(cls: FoundationClass) -> tuple[FoundationBlock, ...]:
    """All blocks of a given class."""
    if cls not in FOUNDATION_CLASSES:
        raise ValueError(
            f"unknown foundation class {cls!r}. Allowed: {FOUNDATION_CLASSES}"
        )
    return tuple(b for b in CATALOG if b.cls == cls)


def blocks_unblocking_scenario(service_code: str) -> tuple[FoundationBlock, ...]:
    """Wave-1 blocks whose delivery unblocks the named Wave-2 scenario."""
    return tuple(b for b in CATALOG if service_code in b.unblocks_w2_scenarios)


def transitive_prerequisites(name: str) -> tuple[FoundationBlock, ...]:
    """Return ``name`` itself plus every ancestor block in the prerequisite
    DAG. Topologically sorted so consumers can iterate directly."""
    target = get_block(name)
    if target is None:
        raise KeyError(f"unknown foundation block {name!r}")
    visited: set[str] = set()
    order: list[FoundationBlock] = []

    def walk(block: FoundationBlock) -> None:
        if block.name in visited:
            return
        for prereq_name in block.prerequisites:
            prereq = get_block(prereq_name)
            if prereq is None:
                raise KeyError(
                    f"block {block.name!r} declares unknown prerequisite "
                    f"{prereq_name!r}"
                )
            walk(prereq)
        visited.add(block.name)
        order.append(block)

    walk(target)
    return tuple(order)


def effort_rollup(blocks: Iterable[FoundationBlock]) -> EffortRollup:
    """SoW-quotable effort sum across the chosen subset.

    Sprint 28 §28.2.5 — `total_calendar_weeks` is the worst-case
    sequential ceiling; `parallelizable_calendar_weeks` is the
    longest-prerequisite-chain wall clock if every parallelizable
    branch ships in parallel.
    """
    blocks = tuple(blocks)
    by_class: dict[FoundationClass, int] = {}
    total_sp = 0
    total_cw = 0.0
    for b in blocks:
        total_sp += b.effort_story_points
        total_cw += b.effort_calendar_weeks
        by_class[b.cls] = by_class.get(b.cls, 0) + 1

    # Critical path = longest prereq-chain among the selected blocks
    selected_names = {b.name for b in blocks}
    memo: dict[str, float] = {}

    def chain_weeks(name: str) -> float:
        if name in memo:
            return memo[name]
        block = get_block(name)
        if block is None:
            memo[name] = 0.0
            return 0.0
        upstream = [
            chain_weeks(p) for p in block.prerequisites if p in selected_names
        ]
        result = block.effort_calendar_weeks + (max(upstream) if upstream else 0.0)
        memo[name] = result
        return result

    parallel_cw = max((chain_weeks(b.name) for b in blocks), default=0.0)

    return EffortRollup(
        selected_count=len(blocks),
        total_story_points=total_sp,
        total_calendar_weeks=round(total_cw, 2),
        parallelizable_calendar_weeks=round(parallel_cw, 2),
        by_class=by_class,
    )


def dependency_graph_edges() -> tuple[tuple[str, str], ...]:
    """Every (prerequisite_name → block_name) edge in the catalog DAG.

    Used by the Task 28.2.4 visualization layer to render the W1-to-W2
    dependency graph.
    """
    edges: list[tuple[str, str]] = []
    for b in CATALOG:
        for p in b.prerequisites:
            edges.append((p, b.name))
    return tuple(edges)
