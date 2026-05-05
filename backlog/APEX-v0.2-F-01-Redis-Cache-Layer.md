# Feature: Redis Cache Layer for APEX Control Plane

**ID:** APEX-v0.2-F-01
**Priority:** High (blocks scale-up of the orchestration control plane beyond ~50 concurrent runs)
**Target release:** APEX v0.2
**Owner:** TBD (candidate: Tyson Thedinger — Azure delivery lead)
**Related:** APEX-v0.2 Orchestration Control Plane spec; APEX-CORE.md §4 (control-plane primitives); Sellers Guide §6.13.7 (Redis Cache — Control Plane Only)
**Created:** 2026-04-22
**Status:** Open — awaiting WS3 (codebase) and WS4 (workspace files) execution
**Source document:** `docs/APEX - Design and Build/APEX-v0.2-Build-Instructions.md` §6 (Redis governance rules) and Workstream 2

---

## User story

As an APEX engagement team delivering agentic AI on the Microsoft platform, we need a sub-millisecond control-plane cache so that child agents can poll cancellation tokens, track budget envelopes, emit heartbeats, and manage HITL deadline queues without incurring Cosmos DB round-trip latency or RU cost at every tool-call boundary.

## Problem statement

The current APEX control plane reads cancel tokens and budget state directly from Cosmos DB (or Durable Functions entities). At low run volumes this is adequate; at the target scale for the Nike R2R engagement (50+ concurrent orchestrations during close window, each with 3–8 child agents, each polling cancel tokens between tool calls) the Cosmos read pattern creates both latency (~10ms per poll) and RU cost issues.

Per APEX-CORE.md §4, children must poll cancel tokens between every tool call. Polling Cosmos on every tool call produces a measurable latency tax on every agent run and puts unnecessary pressure on the durable store.

Sellers Guide §6.13 documents the target architecture. Sellers Guide §6.13.7 documents the governance rules in seller-facing form. This backlog item is the engineering implementation that realizes that architecture.

## Proposed solution

Introduce Azure Cache for Redis (Enterprise tier, VNet-isolated, Entra-authenticated) as the **hot-path cache for control-plane primitives only**. Cosmos and Event Hubs remain the durable truth; Redis is the fast read layer.

Scope is strictly limited to control-plane use cases. Data-plane caching (canonical entities, customer data, financial records) is explicitly out of scope — see Sellers Guide §6.13.7.2 and APEX-v0.2 build file §6 for the full governance rules.

## In-scope use cases

1. **Cancellation token store** — `apex:run:{run_id}:cancel`
2. **Budget envelope counters** — `apex:run:{run_id}:child:{child_id}:tool_calls` (and `:tokens`, `:cost_cents`, `:wall_s`)
3. **Heartbeat liveness tracking** — `apex:run:{run_id}:child:{child_id}:heartbeat` with 60 s TTL
4. **HITL deadline queue** — Redis sorted set `apex:hitl:pending` keyed by deadline Unix timestamp
5. **MCP tool response cache** for whitelisted read-only tools — scope-aware keys only, never PII/PCI
6. **Per-session operator working state** — `apex:session:{session_id}:*` with TTL matching shift length
7. **Event Hubs consumer offset tracking** for the dashboard

## Out of scope — explicit

1. Canonical entity content caching (lives in Fabric Gold, served by MCP tools)
2. File-first context caching (CORE, CHARTER, ENGAGEMENT, OPERATOR, HEARTBEAT, AGENTS loaded at boot, held in agent context)
3. Substitute for `memory/MEMORY.md` (curated memory is file-first, not cache-first)
4. Caching Restricted-PII or Restricted-PCI data (governance violation)
5. Agent long-term memory across sessions
6. Knowledge-graph substitute (use a graph engine for relationship traversal)

## Acceptance criteria

1. Azure Cache for Redis provisioned in the APEX subscription, VNet-isolated, Entra-authenticated, geo-replication enabled for the pilot region (East US 2 for Nike NA).
2. Control-plane client library (TypeScript or Python, matching existing codebase) exposes typed methods for the seven in-scope use cases. All methods **fail-closed**: Redis unreachable → assume cancel / exit / escalate, never silent-success.
3. `APEX-CORE.md` §11 added, declaring Redis as a control-plane primitive with explicit permitted and prohibited use cases (content per Sellers Guide §6.13.7, verbatim).
4. `CHARTER.md` §3 updated — every MCP tool annotated with `cacheable: bool` and `cache_ttl_s: int`. Writes always `cacheable: false`. PII and PCI entities always `cacheable: false`. Static reference data (hierarchy, location, item master) cacheable with short TTL.
5. MCP tool framework wrapper updated to consult the Charter annotations before reading or writing Redis cache. Cache keys include the caller's Entra scope to prevent cross-scope leaks.
6. Durable Functions orchestrator updated to write cancel tokens and budget envelopes to Redis at spawn, refresh on state change, and use Redis as the primary read path for control-plane reads.
7. Child-agent base class updated to poll Redis (not Cosmos) for cancel tokens and budget state between tool calls, with Cosmos as the fallback if Redis is unreachable.
8. Failure-mode tests — Redis unreachable, Redis partial availability, Redis stale data, concurrent writers for the same key — all pass.
9. Independence language review of all added documentation and code comments.
10. Monitoring dashboard (the five-lane orchestration dashboard) extended to show Redis health as a sixth lane.

## Dependencies

- Azure Cache for Redis capacity provisioning (coordinate with Microsoft relationship lead on Deloitte side — Shalini Chandrashekar — for any ECIF or capacity planning)
- Entra security group creation for Redis read and write scopes
- Purview classification tags applied to the Redis instance (Internal class declaration; higher classes never cached)
- Update to the Azure landing zone bicep templates to include the Redis resource
- Workstream 4 completion (HEARTBEAT.md, AGENTS.md) for orchestrator parsing of periodic routines that rely on the heartbeat TTL pattern

## Risks

- **Cross-scope cache leaks** if cache keys do not include the caller's Entra scope.
  *Mitigation:* cache key schema review in PR; unit tests verifying scope isolation; CI lint rule rejects keys missing the Entra scope suffix.
- **Stale reads during cancellation** if TTL is too long.
  *Mitigation:* short TTLs on control plane; pub/sub invalidation for immediate propagation of cancel signals.
- **Governance drift** if data-plane caching creeps in over time.
  *Mitigation:* CI lint rule that rejects any cache put that references a tool marked `cacheable: false`.
- **Cost** at scale.
  *Mitigation:* pilot on smallest Enterprise tier; measure; scale up before EMEA rollout.
- **Independence posture** — Redis is a Microsoft/Azure service; no partnership language creeps into design docs.
  *Mitigation:* all documentation passes the Independence language lint referenced in APEX-v0.2 build file preamble.

## Non-goals for v0.2

- Cross-region Redis replication beyond the active pilot region
- Persistent Redis (AOF / RDB) — the cache is ephemeral by design
- Redis as the status channel (Event Hubs remains the source of truth for status events)

## Cross-references

- **Sellers Guide §6.13** — Parent-Child Agent Orchestration (control plane)
- **Sellers Guide §6.13.7** — Redis Cache — Control Plane Only (full governance rules)
- **Sellers Guide §6.12** — File-First Context Architecture (why the canonical context is *not* cached)
- **APEX-v0.2 Build Instructions §6** — Redis Cache Governance Rules (source of truth)
- **APEX-v0.2 Build Instructions Workstream 3** — Codebase implementation (Redis client, lint rule, MCP wrapper, orchestrator, child-agent base, dashboard, IaC)
- **APEX-v0.2 Build Instructions Workstream 4** — HEARTBEAT.md (periodic autonomy) and AGENTS.md (operating rules) workspace files
- **`apex-workspace/APEX-CORE.md` §4** (existing) — control-plane primitives
- **`apex-workspace/APEX-CORE.md` §11** (new, per WS3) — Redis cache policy
- **`apex-workspace/CHARTER.md` §3** (existing, updated per WS3) — MCP tool catalog with `cacheable` annotations

## Notes for later execution

This backlog entry is authored as part of APEX v0.2 Workstream 2. Workstreams 3 (codebase) and 4 (HEARTBEAT/AGENTS workspace files) consume this backlog entry and realize its acceptance criteria. The sellers-guide sections §6.12 and §6.13 were delivered in Workstream 1 of the same release.

**Execution order for downstream workstreams:**

1. WS4 first — create HEARTBEAT.md and AGENTS.md; add APEX-CORE Appendix A (OpenClaw provenance); bump manifest.json to 0.2.0.
2. WS3 second — implement the Redis client module, CI lint rule, MCP wrapper updates, orchestrator changes, child-agent base changes, dashboard lane, IaC.
3. Validate against this backlog entry's acceptance criteria.
4. Close as delivered when all ten acceptance criteria met.

---

*End of APEX-v0.2-F-01-Redis-Cache-Layer.md. Source: `docs/APEX - Design and Build/APEX-v0.2-Build-Instructions.md` Workstream 2. Sellers Guide cross-reference: §6.13.7.*
