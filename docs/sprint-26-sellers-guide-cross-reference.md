# Sprint 26 — Sellers Guide Cross-Reference

**Sprint 26 Task 26.12.** Maps Sprint 26 deliverables to the Sellers
Guide chapters that document them. The build script (`build-sellers-
guide.cjs`) regenerates the Sellers Guide from these sources at release
time; this doc is the change-list to apply to the script's chapter
content + ToC.

## Chapter additions

### §6.11 — File-First Context Architecture

**Reference Sprint 26 deliverables:**

- `apex-workspace/APEX-CORE.md` — constitutional rules + Appendix A
  (OpenClaw provenance) + §11 Cache Policy
- `apex-workspace/CHARTER.md` — Practice rules + MCP catalog with
  cacheable annotations
- `apex-workspace/HEARTBEAT.md` — periodic autonomy declarations
- `apex-workspace/AGENTS.md` — operating rules in four bands
- `apex-workspace/manifest.json` — v0.2.0 with 10-step boot sequence
- `apex_orchestrator.heartbeat.parse_heartbeat` — orchestrator-startup
  parser

**Cross-references to existing chapters:**

- §1.6 (file-first context) — link to APEX-CORE.md change-control
  procedure for constitutional changes
- §2.2C (oversight spectrum) — AGENTS.md §2-§5 four-band taxonomy
  operationalizes HITL / HOTL / HIC
- §6.10 (audit row contract) — every Sprint 26 control-plane operation
  emits one (cache_hit / cache_miss / heartbeat / cancel_level_change)

### §6.12 — Agent Orchestration: Control Plane

**Reference Sprint 26 deliverables:**

- `apex_orchestrator.control_plane.RedisControlPlane` — 10-method API
  with fail-closed semantics (Sprint 26 Task 26.4)
- `apex_orchestrator.orchestrator.parent.ParentOrchestrator` — Cosmos
  + Redis dual-write on spawn / cancel / complete (Task 26.7)
- `apex_orchestrator.agents.base_agent.BaseAgent` — Redis-first cancel
  polling + Cosmos fallback + self-cancel on dual-failure (Task 26.8)
- `apex_orchestrator.heartbeat.scheduler.HeartbeatScheduler` —
  trigger-source `heartbeat:<routine>` propagation (Task 26.9)

### §6.13 — Redis Cache in the APEX Stack

**Reference Sprint 26 deliverables:**

- `APEX-CORE.md` §11 — verbatim cache governance rules (this is the
  source of truth; Sellers Guide §6.13 mirrors it for sellers)
- `apex_orchestrator.mcp.dispatcher.MCPDispatcher` — cache-aware
  dispatch with CHARTER annotation gating (Task 26.6)
- `tools/lint_cache_governance.py` — CI lint enforcing
  `cacheable: false` rules at commit time (Task 26.5)
- `infra/bicep/redis_control_plane.bicep` + Terraform equivalent —
  Enterprise tier, private endpoint, Entra auth, Purview Internal tag
  (Task 26.11)
- `docs/dashboard/sixth-lane-redis-health.md` — operational dashboard
  spec sourcing from Azure Monitor (Task 26.10)

## OpenClaw lineage subsection (~150 words for §1.6)

Add to the end of the file-first context chapter:

> **The OpenClaw lineage.** APEX's file-first context paradigm derives
> from the OpenClaw community's SOUL.md pattern, demonstrated in the
> agentic AI community in early 2026. APEX adopts four primitives from
> OpenClaw — persistent identity, periodic autonomy, accumulated
> memory, social context — and adds enterprise hardening: signed
> manifests, Purview class per file, Entra-gated reads, version
> pinning, immutability during run. The hardening makes the
> ClawHavoc-class attacks (file-poisoning / prompt-injection
> exploiting weakly-bound agent identity) infeasible against regulated
> APEX deployments. See APEX-CORE Appendix A for the full provenance
> attribution. APEX is not partnered with OpenClaw — it adopts the
> community pattern and credits the source.

## Periodic-autonomy paragraph (for §1.2)

Add to the orchestration chapter:

> **Periodic autonomy is the second OpenClaw primitive.** APEX
> operationalizes it via `HEARTBEAT.md` — declarations of cron-like
> routines parsed at orchestrator-process startup and registered as
> Azure Durable Functions timers. Triggers fire fresh agent runs
> through the full 10-step boot sequence, with a
> `trigger_source: heartbeat:<routine_name>` tag flowing through the
> audit row. Missed triggers do not auto-catch-up; they emit a
> `heartbeat_missed` event. See Sprint 26 Task 26.9 deliverables and
> APEX-CORE §11 cache policy for the operating contract.

## ToC + version metadata

Update `build-sellers-guide.cjs` ToC to include the three new chapter
references (§6.11, §6.12, §6.13). Bump Sellers Guide version metadata
from v1.3 to v1.4.

## Independence-language scan

Per Sprint 26 acceptance criteria, every Sprint 26 cross-reference uses
"adopt" / "credit" / "community pattern" — never "partner" /
"alliance" / "endorsed by" — when referring to OpenClaw or any other
external community. Independence-language CI lint (Sprint 19 / Sprint
27 deliverable) catches violations at commit.
