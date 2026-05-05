# APEX v0.2 — Build Instructions for Claude Code

**File:** `APEX-v0.2-Build-Instructions.md`
**Purpose:** Single build instruction file for Claude Code to execute three coordinated changes in the APEX repo
**Owner:** Keven Markham — VP, Deloitte DMTSP Consumer Industry
**Version target:** APEX v0.2
**Estimated scope:** 3 workstreams · ~15–25 files modified or created
**Execution mode:** Claude Code agentic session with filesystem + shell access against the APEX repo

---

## Mission

Deliver four coordinated updates to APEX in a single coherent v0.2 release:

1. **Update the APEX Sellers Guide** to reflect the file-first context paradigm, the parent-child orchestration patterns, and the Redis cache architecture.
2. **Add a new backlog feature** for the Redis Cache Layer integration, formatted consistently with the existing APEX backlog.
3. **Update the existing APEX codebase** to implement the Redis Cache Layer at the control-plane level, with strict governance rules preventing misuse at the data-plane level.
4. **Complete the OpenClaw-derived file-first pattern** by adding `HEARTBEAT.md` (periodic autonomy), `AGENTS.md` (autonomous-vs-approval operating rules), and a paradigm-provenance appendix to `APEX-CORE.md` that names the OpenClaw source and the four primitives.

All four workstreams share the same governance principles (Redis in §6, file-first in §7 of this file). Do not deviate from them.

---

## Prerequisites — files to read before executing

Before making any changes, read and internalize these files. They define the constraints and the design vocabulary.

### Required reads

- `apex-workspace/APEX-CORE.md` — cross-edition principles and Independence language rules
- `apex-workspace/CHARTER.md` — RC canonical schema, 44 MCP tools, governance inheritance
- `apex-workspace/ENGAGEMENT.md` — Nike R2R engagement context
- `apex-workspace/manifest.json` — version and integrity spine
- `apex-workspace/README.md` — workspace structure and boot sequence
- `docs/APEX-Orchestration-Guide.html` (if present) — parent-child orchestration primitives
- `docs/APEX-File-First-Context.html` (if present) — file-first paradigm explanation

### Discovery steps if paths differ

If the actual repo structure differs from the paths above:

1. Run `find . -type f -iname "APEX-CORE.md" -o -iname "CHARTER.md" -o -iname "manifest.json" 2>/dev/null | head -20` to locate workspace files.
2. Run `find . -type f \( -iname "*sellers*guide*" -o -iname "*sellers_guide*" \) 2>/dev/null` to locate the Sellers Guide.
3. Run `find . -type d \( -iname "*backlog*" -o -iname "*roadmap*" \) 2>/dev/null` to locate the backlog directory.
4. Report the discovered paths at the top of the PR description. Do not proceed with writes until paths are confirmed.

### Compliance rules — non-negotiable across all workstreams

Before writing any content into any file, verify:

- **Independence language.** Never use "partner," "partnership," "alliance," "strategic alliance," or "joint offering" to describe the Deloitte–Microsoft relationship. Approved substitutes: "Deloitte's Microsoft practice," "DMTSP," "Microsoft platform capabilities," "Microsoft-native deployment." This rule applies to Sellers Guide content, backlog entries, code comments, commit messages, and PR descriptions.
- **Client naming.** Any reference to Nike, Samsonite, Sonepar, or other named clients in Sellers Guide examples must be generic ("a Consumer Industry retail client," "a global travel-goods client") unless an approved reference case is already documented.
- **APEX positioning.** APEX is an internal Deloitte accelerator. Never imply clients license, purchase, or buy APEX.

Independence violations are blocker-grade. If uncertain, flag for human review rather than ship.

---

## Workstream 1 — Update the APEX Sellers Guide

### Target file

The APEX Sellers Guide. Locate via discovery step 2 above. Expected location: `docs/sellers-guide/` or `sellers-guide/APEX-Sellers-Guide.md` or similar. If the guide exists as multiple files (one per chapter), update the relevant files and the table of contents.

### Changes to make

#### 1.1 Add a new chapter: "File-First Context Architecture"

Insert a new top-level chapter after the existing architecture chapter. Title: **"File-First Context — Beyond Knowledge Graphs and Vectors"**. The chapter must cover:

- **The paradigm shift.** Index-first retrieval (RAG, vectors, knowledge graphs) vs. file-first identity injection. Explain that file-first is the right default for agent identity, canonical schema, and governance rules. Vectors and graphs remain appropriate for unstructured content search and relationship traversal respectively. Name the OpenClaw community's SOUL.md pattern as the paradigm's origin and credit it briefly (~1–2 sentences). Length: ~400 words.

- **The APEX workspace file hierarchy.** Describe the seven-file cascade: `APEX-CORE.md` → `CHARTER.md` → `ENGAGEMENT.md` → `OPERATOR.md` → `HEARTBEAT.md` → `AGENTS.md` → `memory/`. Each layer refines, never silently overrides. Include a mapping table showing which OpenClaw file each APEX file corresponds to (see §7 of this build instruction for the canonical mapping). Include a simple ASCII or Mermaid diagram showing the cascade. Length: ~400 words plus diagram.

- **The boot sequence.** Walk through the ten boot steps (verify manifest integrity → load CORE → load CHARTER → load ENGAGEMENT → load OPERATOR → load HEARTBEAT → load AGENTS → load today's memory → load curated memory → emit booted event). Emphasize that this sequence is identical every session. Length: ~300 words.

- **Governance primitives.** Enumerate the six hardening primitives: signed manifests, Purview class per file, author provenance, Entra-gated reads, version pinning, immutability during run. Length: ~250 words.

- **The hybrid model.** A table mapping question types to paradigms — identity questions to files, unstructured semantic search to vectors, relationship traversal to graphs. Close with the one-line rule: *"Files define the agent. MCP tools expose the canonical data. Vectors and graphs inform the world the agent acts in."* Length: ~200 words plus table.

Reference the existing `APEX-File-First-Context.html` artifact for voice and framing. Do not copy verbatim — adapt for Sellers Guide context (seller-facing, slightly less technical than the internal HTML).

#### 1.2 Add a new chapter: "Agent Orchestration — Control Plane"

Insert after the file-first chapter. Title: **"Parent-Child Agent Orchestration"**. Cover:

- **The four concerns.** Spawning, monitoring, control, reconciliation. Emphasize that conflating them is the source of most multi-agent framework pain. Length: ~200 words.

- **The four patterns.** DAG, supervisor-worker, hierarchical, swarm — with supervisor-worker with a DAG spine named as the APEX default. Length: ~250 words.

- **The three control-plane primitives.** Cancellation token, budget envelope, append-only status channel. Include a concrete example of how they compose into a cooperative kill. Length: ~400 words.

- **The four kill levels.** Pause, soft cancel, hard cancel, abort. Include the table mapping level to state-preservation guarantees. Length: ~250 words.

- **Five failure modes to plan for.** Zombie children, split-brain HITL, cost runaway from recursion, stuck HITL, partial success ambiguity. Length: ~350 words.

- **The Azure stack mapping.** Durable Functions as parent, Azure AI Agent Service as child, Event Hubs as status channel, Cosmos or DF entities as control store, Redis as the hot-path cache for cancel/budget/heartbeat (forward reference to §1.3). Length: ~300 words.

Reference the existing `APEX-Orchestration-Guide.html` artifact. Again, adapt for the Sellers Guide audience — sellers and engagement leads, not engineers.

#### 1.3 Add a new section: "Redis Cache in the APEX Stack"

Insert within the orchestration chapter, after the Azure stack mapping. Title: **"Redis Cache — Control Plane Only"**. Cover exactly the content in §6 of this build file (the Redis governance rules), adapted for Sellers Guide framing. The section must include:

- The headline rule: *"Redis is for the control plane, not the data plane."*
- The seven places Redis belongs (cancellation tokens, budget counters, heartbeats, HITL deadline queues, MCP response caching with strict limits, session state, Event Hubs offsets).
- The six places Redis does not belong (canonical schema content, file-first context files, substitute for `MEMORY.md`, Purview-classified data, agent long-term memory, knowledge-graph substitute).
- The key naming convention.
- The cross-reference to CHARTER.md `cacheable` and `cache_ttl_s` tool annotations (added in workstream 3).

Length: ~700 words. Use the content in §6 as the source of truth.

#### 1.4 Update existing chapters that reference context architecture

Search the Sellers Guide for references to:

- "knowledge graph" — if used as the primary context mechanism, update to clarify that knowledge graphs support relationship traversal but do not carry identity or canonical schema.
- "vector database" or "RAG" — if positioned as the primary context mechanism, update to clarify the hybrid model: vectors for unstructured semantic search, file-first for identity and canonical, graphs for relationships.
- "agent memory" — if described as a vector store, clarify that APEX agent memory is file-first (`memory/MEMORY.md`) with vectors as a supporting retrieval layer.

For each update, preserve the existing chapter structure. Add clarifying text; do not delete content unless it directly contradicts the hybrid model.

#### 1.5 Update the Sellers Guide table of contents

Reflect the two new chapters (File-First Context, Agent Orchestration) and the new section (Redis Cache). Maintain existing chapter numbering conventions.

#### 1.6 Update the Sellers Guide version metadata

Bump to v0.2. Add a changelog entry describing the three changes above.

### Acceptance criteria — Workstream 1

- Two new chapters added, in correct position, with required subsections.
- New Redis section inside the orchestration chapter.
- Existing chapters updated to reflect the hybrid model without contradiction.
- Table of contents and version metadata updated.
- No Independence-forbidden language anywhere in the added or modified content.
- All client references are generic unless an approved reference case exists.
- A git diff summary in the PR description listing every file touched.

---

## Workstream 2 — Add Redis Cache Layer to the APEX backlog

### Target location

Locate via discovery step 3 above. Expected location: `backlog/`, `roadmap/`, or `.github/ISSUE_TEMPLATE/` depending on the repo convention. If the backlog is tracked in an external system (Azure DevOps, Jira), write a standalone feature brief to `backlog/APEX-v0.2-Redis-Cache-Layer.md` and note in the PR description that the external backlog system requires manual creation.

### Feature entry to add

Use whatever format the existing backlog uses (user-story format, feature-brief format, issue template). If the existing format is unclear, use the structure below.

```markdown
# Feature: Redis Cache Layer for APEX Control Plane

**ID:** APEX-v0.2-F-01
**Priority:** High (blocks scale-up of the orchestration control plane beyond ~50 concurrent runs)
**Target release:** v0.2
**Owner:** TBD (candidate: Tyson Thedinger — Azure delivery lead)
**Related:** APEX-v0.2 Orchestration Control Plane spec; APEX-CORE.md §4 (control-plane primitives)

## User story

As an APEX engagement team delivering agentic AI on the Microsoft platform, we need a sub-millisecond control-plane cache so that child agents can poll cancellation tokens, track budget envelopes, emit heartbeats, and manage HITL deadline queues without incurring Cosmos DB round-trip latency or RU cost at every tool-call boundary.

## Problem statement

The current APEX control plane reads cancel tokens and budget state directly from Cosmos DB (or Durable Functions entities). At low run volumes this is adequate; at the target scale for the Nike R2R engagement (50+ concurrent orchestrations during close window, each with 3–8 child agents, each polling cancel tokens between tool calls) the Cosmos read pattern creates both latency (~10ms per poll) and RU cost issues.

Per APEX-CORE.md §4, children must poll cancel tokens between every tool call. Polling Cosmos on every tool call produces a measurable latency tax on every agent run and puts unnecessary pressure on the durable store.

## Proposed solution

Introduce Azure Cache for Redis (Enterprise tier, VNet-isolated, Entra-authenticated) as the **hot-path cache for control-plane primitives only**. Cosmos and Event Hubs remain the durable truth; Redis is the fast read layer.

Scope is strictly limited to control-plane use cases. Data-plane caching (canonical entities, customer data, financial records) is explicitly out of scope — see §6 of the v0.2 build file for the full governance rules.

## In-scope use cases

1. Cancellation token store — `apex:run:{run_id}:cancel`
2. Budget envelope counters — `apex:run:{run_id}:child:{child_id}:tool_calls`
3. Heartbeat liveness tracking — `apex:run:{run_id}:child:{child_id}:heartbeat` with TTL
4. HITL deadline queue — Redis sorted set keyed by deadline Unix timestamp
5. MCP tool response cache for whitelisted read-only tools — scope-aware keys only, never PII/PCI
6. Per-session operator working state — `apex:session:{session_id}:*` with TTL matching shift length
7. Event Hubs consumer offset tracking for the dashboard

## Out of scope — explicit

1. Canonical entity content caching (lives in Fabric Gold, served by MCP tools)
2. File-first context caching (CORE, CHARTER, ENGAGEMENT, OPERATOR files are loaded at boot and held in agent context)
3. Substitute for `memory/MEMORY.md` (curated memory is file-first, not cache-first)
4. Caching Restricted-PII or Restricted-PCI data (governance violation)
5. Agent long-term memory across sessions
6. Knowledge-graph substitute (use a graph engine for relationship traversal)

## Acceptance criteria

1. Azure Cache for Redis provisioned in the APEX subscription, VNet-isolated, Entra-authenticated, geo-replication enabled for the pilot region (East US 2 for Nike NA).
2. Control-plane client library (TypeScript or Python, matching existing codebase) exposes typed methods for the seven in-scope use cases. All methods fail-closed: Redis unreachable → assume cancel / exit / escalate, never silent-success.
3. `APEX-CORE.md` §11 added, declaring Redis as a control-plane primitive with explicit permitted and prohibited use cases.
4. `CHARTER.md` §3 updated — every MCP tool annotated with `cacheable: bool` and `cache_ttl_s: int`. Writes always `cacheable: false`. PII and PCI entities always `cacheable: false`. Static reference data (hierarchy, location, item master) cacheable with short TTL.
5. MCP tool framework wrapper updated to consult the Charter annotations before reading or writing Redis cache. Cache keys include the caller's Entra scope to prevent cross-scope leaks.
6. Durable Functions orchestrator updated to write cancel tokens and budget envelopes to Redis at spawn, refresh on state change, and use Redis as the primary read path for control-plane reads.
7. Child-agent base class updated to poll Redis (not Cosmos) for cancel tokens and budget state between tool calls, with Cosmos as the fallback if Redis is unreachable.
8. Failure mode tests — Redis unreachable, Redis partial availability, Redis stale data, concurrent writers for the same key — all pass.
9. Independence language review of all added documentation and code comments.
10. Monitoring dashboard (the five-lane orchestration dashboard) extended to show Redis health as a sixth lane.

## Dependencies

- Azure Cache for Redis capacity provisioning (coordinate with Microsoft relationship lead on Deloitte side — Shalini Chandrashekar — for any ECIF or capacity planning)
- Entra security group creation for Redis read and write scopes
- Purview classification tags applied to the Redis instance (Internal class declaration; higher classes never cached)
- Update to the Azure landing zone bicep templates to include the Redis resource

## Risks

- **Cross-scope cache leaks** if cache keys do not include the caller's Entra scope. Mitigation: cache key schema review in PR; unit tests verifying scope isolation.
- **Stale reads during cancellation** if TTL is too long. Mitigation: short TTLs on control plane; pub/sub invalidation for immediate propagation of cancel signals.
- **Governance drift** if data-plane caching creeps in over time. Mitigation: CI lint rule that rejects any cache put that references a tool marked `cacheable: false`.
- **Cost** at scale. Mitigation: pilot on smallest Enterprise tier; measure; scale up before EMEA rollout.

## Non-goals for v0.2

- Cross-region Redis replication beyond the active pilot region
- Persistent Redis (AOF / RDB) — the cache is ephemeral by design
- Redis as the status channel (Event Hubs remains the source of truth for status events)

## References

- `apex-workspace/APEX-CORE.md` — control-plane primitives (§4)
- `apex-workspace/CHARTER.md` — MCP tool catalog (§3)
- `docs/APEX-Orchestration-Guide.html` — orchestration patterns
- `APEX-v0.2-Build-Instructions.md` §6 — Redis governance rules (this file)
```

### Acceptance criteria — Workstream 2

- Feature entry added to the backlog in the existing format (if discoverable) or as a standalone feature brief.
- All sections above populated.
- Cross-references to APEX-CORE.md, CHARTER.md, and the orchestration guide are correct.
- No Independence-forbidden language.
- PR description notes the feature ID and links to the added entry.

---

## Workstream 3 — Update the existing codebase for Redis Cache integration

### Target codebase

The APEX implementation repo. Locate by running `find . -type f \( -name "*.ts" -o -name "*.py" -o -name "*.cs" \) | head -20` and scanning for orchestrator, agent, and MCP tool module structures.

Expected structure (based on prior APEX context):

- Orchestrator layer in Python or TypeScript, running on Azure Durable Functions
- Child agent base class using Azure AI Agent Service SDK
- MCP tool framework wrapper
- Control-plane client (Cosmos or DF entities today)

If the structure differs, adapt the changes below to the actual structure and document the mapping in the PR description.

### Changes to make

#### 3.1 Add a Redis client module

Create `src/control_plane/redis_client.py` (or `.ts` equivalent) implementing a typed interface over `redis-py` (or `ioredis`). Methods:

```python
class RedisControlPlane:
    def set_cancel_token(self, run_id: str, level: Literal["pause","soft","hard","abort"]) -> None
    def get_cancel_token(self, run_id: str) -> Optional[str]
    def increment_budget_counter(self, run_id: str, child_id: str, field: str, amount: int = 1) -> int
    def get_budget_counters(self, run_id: str, child_id: str) -> dict
    def heartbeat(self, run_id: str, child_id: str, ttl_s: int = 60) -> None
    def is_child_alive(self, run_id: str, child_id: str) -> bool
    def enqueue_hitl(self, hitl_id: str, deadline_unix: int, payload: dict) -> None
    def pop_expired_hitl(self, now_unix: int) -> list
    def cache_mcp_response(self, tool: str, arg_hash: str, entra_scope: str, value: Any, ttl_s: int) -> None
    def get_cached_mcp_response(self, tool: str, arg_hash: str, entra_scope: str) -> Optional[Any]
```

Implementation requirements:

- **Fail-closed on Redis unavailability.** Every method wraps Redis exceptions. Control-plane reads (cancel token, budget) default to "cancel" / "exhausted" when Redis is unreachable. Do not silent-succeed.
- **Entra auth.** Use Azure Identity library with managed identity. Do not use connection-string auth.
- **VNet endpoint.** Configure for private endpoint only. No public access.
- **Structured logging.** Every method emits structured logs with `run_id`, `child_id`, and operation; no cache values logged for entries above Internal class.
- **Unit tests with a Redis test container.** Every method has at least one happy-path and one failure-mode test.

#### 3.2 Add CI lint rule for cache governance

Create `scripts/lint_cache_governance.py` (or equivalent) that:

- Parses `CHARTER.md` to extract the MCP tool catalog with `cacheable` annotations.
- Scans the codebase for any call to `cache_mcp_response()` or `get_cached_mcp_response()`.
- Cross-references the tool name with the Charter. If the tool is marked `cacheable: false`, fail the lint.
- Runs in CI on every PR that touches either the MCP wrapper or CHARTER.md.

Integrate into existing `pre-commit` or GitHub Actions workflow.

#### 3.3 Update the MCP tool framework wrapper

Locate the wrapper that dispatches MCP tool calls (likely `src/mcp/dispatcher.py` or similar). For every tool invocation:

1. Parse the Charter annotations for the tool at boot time (read once, hold in memory).
2. Before executing a read-only tool, check the cache by key `apex:mcp:{tool}:{arg_hash}:{entra_scope}`.
3. If hit and fresh, return cached value (log a `cache_hit` event).
4. If miss, execute the tool, then conditionally cache the response if:
   - Tool has `cacheable: true` in Charter
   - Tool is read-only (no write side effects)
   - Response does not carry Restricted-PII or Restricted-PCI class
   - Response does not exceed 100KB (configurable)
5. Never cache write tools. Never cache responses for classes above Confidential.

Add clear code comments referencing `APEX-CORE.md` §11 (once added) and `CHARTER.md` §3 for the governance reasoning.

#### 3.4 Update the Durable Functions orchestrator

Locate the orchestrator (likely `src/orchestrator/parent.py` or similar).

- On child spawn, write cancel token (initial value: `null`) and budget envelope (from spawn config) to Redis.
- On pause, soft-cancel, hard-cancel, or abort: write new cancel-token level to Redis. Cosmos / DF entity remains the durable record.
- On child completion: TTL-expire the child's Redis keys within 5 minutes.

Cosmos DB / DF entities remain the source of truth. Redis is the fast read path. A Redis loss does not lose orchestrator state — only the fast path.

#### 3.5 Update the child-agent base class

Locate the base class (likely `src/agents/base_agent.py` or similar).

- Replace Cosmos-backed cancel-token polling with the Redis client.
- Replace Cosmos-backed budget-counter reads with the Redis client's atomic INCR-then-GET pattern.
- Emit heartbeats via `heartbeat(run_id, child_id, ttl_s=60)` every 30 seconds while running.
- On Redis unreachable: fall back to Cosmos with an exponential backoff. If both fail, self-cancel with reason `control_plane_unreachable`.

#### 3.6 Update the monitoring dashboard

Locate the dashboard (likely `src/dashboard/` or `frontend/dashboard/`).

- Add a sixth lane: "Redis health." Shows Redis reachability, p50/p95 latency for cancel-token reads, and cache hit rate for MCP tools.
- Source the data from Azure Monitor metrics for the Redis instance, not from the Redis instance itself.

#### 3.7 Update infrastructure-as-code

Locate the landing zone templates (likely `infra/` with Bicep or Terraform).

- Add an Azure Cache for Redis resource declaration (Enterprise tier, smallest SKU for pilot — coordinate with finops for final sizing).
- Configure private endpoint, Entra authentication, VNet integration.
- Add Purview classification tag: `class: Internal`.
- Add the Redis connection info to the Key Vault config (not as a connection string with password — as an Entra-issued token exchange).

### Acceptance criteria — Workstream 3

- `src/control_plane/redis_client.py` implemented with all ten methods, full test coverage including failure modes.
- CI lint rule active and passing against the current CHARTER.md.
- MCP wrapper dispatches through Redis cache with Charter-annotation gating.
- Orchestrator writes cancel tokens and budgets to Redis on spawn.
- Child base class reads cancel tokens and budgets from Redis with Cosmos fallback.
- Dashboard shows Redis health lane.
- IaC templates add the Redis resource with correct security and governance settings.
- All changes pass Independence language lint.
- PR description includes a git diff summary and a test-run summary.

---

## Workstream 4 — Complete the OpenClaw-derived file-first pattern

The workspace as of v0.1 implements five of the seven files in the OpenClaw SOUL.md pattern. Two remain: `HEARTBEAT.md` (periodic autonomy) and `AGENTS.md` (autonomous-vs-approval operating rules). In addition, `APEX-CORE.md` needs a provenance appendix that names OpenClaw explicitly and makes the intellectual lineage auditable — both for reviewers and for the agent's own self-description when asked about its architecture.

### Target files

- New: `apex-workspace/HEARTBEAT.md`
- New: `apex-workspace/AGENTS.md`
- Modified: `apex-workspace/APEX-CORE.md` — add Appendix A (paradigm provenance)
- Modified: `apex-workspace/manifest.json` — add the two new files to the boot sequence and file registry
- Modified: `apex-workspace/README.md` — update workspace structure section
- Modified: orchestrator codebase — parse HEARTBEAT.md at boot to register scheduled wakes

### Changes to make

#### 4.1 Create `HEARTBEAT.md`

Create `apex-workspace/HEARTBEAT.md` with YAML frontmatter consistent with the other workspace files (version, scope, class Internal, inherits_from CORE+CHARTER+ENGAGEMENT). The body declares periodic autonomous routines — OpenClaw's "cron for your agent, expressed in plain English" pattern, adapted for enterprise governance.

Each routine declares:

- **Trigger** — schedule expression (cron-like or named window, e.g. "day 1–8 of every month at 06:00 UTC")
- **ORCH** — which orchestration from CHARTER catalog is invoked
- **Budget** — wall-clock, tool calls, cost envelope (same envelope shape as agent spawns)
- **Oversight** — HITL / HOTL / HIC posture for the routine
- **On failure** — named escalation path (collaborator from ENGAGEMENT)
- **On anomaly** — optional rule with threshold and escalation (e.g. ">5% variance → escalate to Scott Rodgers")

Routines to include for the Nike R2R engagement:

1. **Monthly close reconciliation.** Trigger: day 1–8 of every month, 06:00 UTC. ORCH: `ORCH-RC-04` (or dedicated close ORCH). Budget: 2 hours, 500 tool calls, $50. Oversight: HITL at checkpoint after each domain. On failure: escalate to Rob Goldberg.

2. **Weekly vendor scorecard.** Trigger: Monday 08:00 local. ORCH: `ORCH-RC-04`. Budget: 30 minutes, 100 tool calls. Oversight: HIC (review-and-distribute).

3. **Daily inventory valuation health.** Trigger: 05:00 UTC daily. ORCH: `ORCH-RC-05` (dedicated valuation check). Budget: 15 minutes, 80 tool calls. Oversight: HIC. On anomaly (>5% variance vs prior day): escalate to Scott Rodgers.

4. **Hourly run-state health.** Trigger: every hour on the hour. Action: verify active runs are heartbeat-fresh. No agent run — this is a management operation against the Redis heartbeat store (§6).

Add an operating-rules section at the bottom:

- HEARTBEAT routines use the same file-first boot sequence as any other agent run.
- HEARTBEAT routines never bypass HITL gates declared in CHARTER or AGENTS.
- Missed runs (e.g. Redis unavailable at trigger time) do not auto-catch-up — they log and escalate.
- Close-window acceleration (compressed HITL deadlines per ENGAGEMENT) applies to HEARTBEAT routines during active close.

#### 4.2 Create `AGENTS.md`

Create `apex-workspace/AGENTS.md` with YAML frontmatter consistent with other files. The body defines operating rules in four bands — the "just do it / ask first / escalate / never" taxonomy that OpenClaw's AGENTS.md captures, adapted to APEX governance.

Structure:

```
## Just do it — no HITL required
(read-only canonical tools, HIC tools from CHARTER, summaries, memory logging)

## Ask first — HITL required before execution
(any write, any HITL-marked tool from CHARTER, any refund above operator threshold,
any inventory reservation above operator threshold)

## Escalate immediately — minute-level HITL deadline
(PII/PCI exposure detected, Independence language near-miss, budget breach during close,
source-drift between SAP and canonical)

## Never — regardless of context
(cross-reference APEX-CORE §7 and CHARTER §7 — do not duplicate, reference only)
```

Populate each band with specific rules drawn from CHARTER and ENGAGEMENT. Do not restate hard limits from CORE and CHARTER — reference them. AGENTS.md is the *operating* rules; CORE and CHARTER are the *constitutional* rules.

#### 4.3 Add Appendix A to `APEX-CORE.md` — paradigm provenance

Append at the end of `APEX-CORE.md`, after the existing "Change control for this file" section. New section title: **"Appendix A — Paradigm provenance"**. Content:

- A one-paragraph attribution: the file-first context paradigm derives from the OpenClaw community's SOUL.md pattern, demonstrated in the agentic AI community in early 2026. Credit OpenClaw as the source.
- The four OpenClaw primitives, named: **persistent identity** (identity survives restarts), **periodic autonomy** (agents wake on their own schedule), **accumulated memory** (learnings persist and curate over time), **social context** (who the operator is, who the peers are, what the rules are).
- The file-family mapping (see §7 of this build instruction for the canonical table).
- An attribution to the ClawHavoc attack research as the motivation for APEX's enterprise hardening primitives — signed manifests, Purview class per file, Entra-gated reads, version pinning, immutability during run. Explicit note that APEX's governance layer is designed to make the attack class infeasible for regulated deployments.
- A closing note: when the agent is asked for its architectural lineage, it may reference this appendix; it does not speculate beyond it.

Length: ~400 words.

#### 4.4 Update `manifest.json` — add new files to boot sequence and registry

- Add steps 6 and 7 to `boot_sequence`: load HEARTBEAT.md after OPERATOR.md, load AGENTS.md after HEARTBEAT.md. Shift existing steps 6–8 to 8–10. Total boot steps: 10.
- Add entries for `HEARTBEAT.md` and `AGENTS.md` in the `files` object. Both: version 0.1.0, class Internal, read_scope `apex-nike-r2r-agents`, modify_scope `apex-nike-engagement-leads`, inherits_from `[APEX-CORE.md, CHARTER.md, ENGAGEMENT.md]`, `required: true`, `immutable_during_run: true`.
- Bump manifest_version from `0.1.0` to `0.2.0`. Re-sign.

#### 4.5 Update `README.md` — reflect new file hierarchy

- Update the directory-structure tree block to include HEARTBEAT.md and AGENTS.md after OPERATOR.md.
- Update the boot-sequence section from eight steps to ten.
- Update the cascade diagram to show seven layers (CORE → CHARTER → ENGAGEMENT → OPERATOR → HEARTBEAT → AGENTS → memory).
- Add a paragraph referencing the OpenClaw lineage (brief — the detail belongs in APEX-CORE Appendix A).
- Update the "How to propose a change" table to include the new files.

#### 4.6 Update orchestrator to parse `HEARTBEAT.md`

Locate the orchestrator entry point (likely `src/orchestrator/bootstrap.py` or similar).

- At orchestrator startup (not per-agent boot — orchestrator-process startup), parse `HEARTBEAT.md` frontmatter and body.
- For each declared routine, register a scheduled trigger in Azure Durable Functions using the Durable Timer pattern or Azure Function timer trigger.
- At trigger fire, the orchestrator spawns a fresh agent run under the declared ORCH. The agent boots through the full 10-step boot sequence — HEARTBEAT does not shortcut the boot.
- Each HEARTBEAT-triggered run carries a `trigger_source: heartbeat:<routine_name>` tag that propagates through the status channel for audit.
- Missed triggers (Redis unavailable, orchestrator down) produce a `heartbeat_missed` event to the status channel. The orchestrator does not auto-catch-up — it logs and proceeds.

Add unit tests:

- Parse valid HEARTBEAT.md → routines registered.
- Parse malformed HEARTBEAT.md → orchestrator refuses to start, surfaces parse error.
- Simulated trigger fire → correct ORCH spawned with correct budget envelope.
- Missed trigger → correct event emitted, no catch-up run created.

#### 4.7 Update Sellers Guide to reference the completed pattern

In Workstream 1's file-first chapter (§1.1 of this build file), the workspace hierarchy subsection was already updated to reflect the seven-file family. Now also:

- Add a short subsection at the end of the chapter titled **"The OpenClaw lineage"** (~150 words). Credit OpenClaw; name the four primitives; note APEX's enterprise hardening additions.
- Add a paragraph in the orchestration chapter (§1.2) about periodic autonomy as an OpenClaw primitive, operationalized in APEX through HEARTBEAT.md. Link to §4.1 of this build file for specifics on how routines are declared.

### Acceptance criteria — Workstream 4

- `HEARTBEAT.md` created with valid YAML frontmatter, four routines specified, operating-rules section present.
- `AGENTS.md` created with four bands populated from CHARTER and ENGAGEMENT content, no duplication of hard limits from CORE.
- `APEX-CORE.md` Appendix A added; attribution to OpenClaw and ClawHavoc present; four primitives named; file-family mapping included.
- `manifest.json` updated — manifest_version 0.2.0, boot_sequence 10 steps, file registry includes HEARTBEAT.md and AGENTS.md with correct scopes and inheritance.
- `README.md` updated — tree, boot sequence, cascade, change-control table all reflect the seven-file pattern.
- Orchestrator parses HEARTBEAT.md at startup, registers scheduled triggers, spawns runs at trigger time with correct ORCH and budget.
- Unit tests for HEARTBEAT parsing and trigger behavior pass.
- Sellers Guide updated with OpenClaw lineage subsection and periodic-autonomy paragraph.
- Independence language scan: clean across all new and modified content.
- No Independence-forbidden language in the OpenClaw references (OpenClaw is not "partnered" with Deloitte — it's a community pattern being adopted).

---

## §6 — Redis Cache Governance Rules (source of truth)

These rules are the single source of truth for Redis usage across all four workstreams. Every use of Redis in code, docs, backlog entries, or Sellers Guide content must comply. When updating `APEX-CORE.md` §11 (as part of workstream 3, or as a separate follow-up), these rules go in verbatim.

### The headline rule

**Redis is for the control plane, not the data plane.** Anything about how the agent is running — cancel tokens, budgets, heartbeats, HITL timers, session state — is fair game. Anything about what the agent is reasoning *over* — canonical entities, customer data, financial records, audit evidence — stays in Fabric Gold, with MCP tools as the only access path.

### Where Redis belongs — seven use cases

1. **Cancellation token store.** Sub-millisecond GET between every tool call. TTL auto-cleans after run end. Atomic SET on cancel. Pub/sub for immediate propagation. Key: `apex:run:{run_id}:cancel`. Fail-closed: Redis unreachable → assume cancel.

2. **Budget envelope counters.** Atomic INCR on tool-call counters. Fast GET on envelope limits. Key: `apex:run:{run_id}:child:{child_id}:{metric}` where metric ∈ {tool_calls, tokens, cost_cents, wall_s}. Use `INCR`, never read-modify-write.

3. **Heartbeat and liveness.** 60-second TTL on `apex:run:{run_id}:child:{child_id}:heartbeat`. Expired key = stuck child. Parent reconciles against the durable status stream for audit.

4. **HITL deadline queue.** Redis sorted set `apex:hitl:pending` with score = deadline Unix timestamp. `ZRANGEBYSCORE 0 {now}` every few seconds finds expired entries. The HITL decision itself lives in the durable audit log, not Redis.

5. **MCP tool response caching — with strict rules.** Short TTL for read-only tools whose responses are stable-ish (`rc.item.get`, `rc.hierarchy.tree`). Key must include caller's Entra scope: `apex:mcp:{tool}:{arg_hash}:{entra_scope}`. **Never** cache: writes, PII (class Restricted-PII), PCI (class Restricted-PCI), "current state" claims without TTL in the tool response.

6. **Per-session operator state.** Live working state of the current operator's decisions in-shift. Key: `apex:session:{session_id}:operator:*`. TTL matches shift length. End-of-shift summary writes to `memory/YYYY-MM-DD.md` for durability.

7. **Event Hubs consumer offset tracking.** Standard Redis use for multiple dashboard instances to share offset state and enable failover. No APEX-specific governance concerns.

### Where Redis does not belong — six prohibitions

1. **Canonical schema content.** The 34 RC entities live in `CHARTER.md` (file-first) and materialize at Fabric Gold (durable). Caching canonical definitions in Redis inverts the architecture.

2. **File-first context files.** `APEX-CORE.md`, `CHARTER.md`, `ENGAGEMENT.md`, `OPERATOR.md` are read at boot once and held in the model's context. Caching in Redis achieves nothing and adds a failure mode.

3. **Substitute for `memory/MEMORY.md`.** Curated memory is operator-authored, Git-versioned, audit-recoverable markdown. Redis loses all those properties. Redis is ephemeral session working state; markdown is the durable record.

4. **Purview-classified data above Internal.** Redis in Azure supports Entra auth and VNet isolation but does not natively carry Purview classification. Confidential, Restricted-PII, and Restricted-PCI data never sits in Redis in this architecture.

5. **Agent long-term memory across sessions.** Long-term memory is the memory file, operator-curated. Redis is for the current session only.

6. **Knowledge-graph substitute.** For three-hop supplier traversal or fraud-pattern topology queries, use a graph engine. Redis is key-value with some structure, not a graph.

### Key naming convention (required)

```
apex:run:{run_id}:cancel                              TTL: run duration + 5min
apex:run:{run_id}:child:{child_id}:tool_calls         TTL: run duration + 5min
apex:run:{run_id}:child:{child_id}:tokens             TTL: run duration + 5min
apex:run:{run_id}:child:{child_id}:cost_cents         TTL: run duration + 5min
apex:run:{run_id}:child:{child_id}:heartbeat          TTL: 60s
apex:hitl:pending                                     sorted set, score = deadline unix ts
apex:hitl:{hitl_id}                                   full record, TTL: deadline + 1h
apex:session:{session_id}:operator:{field}            TTL: shift duration
apex:mcp:{tool}:{arg_hash}:{entra_scope}              TTL: tool-declared; never PII/PCI
apex:eh:consumer:{consumer_group}:offset              standard EH offset pattern
```

Every key that could cross scope dimensions includes the scope in the key. Keys that don't respect this convention are a lint violation.

### Additions to CORE and CHARTER (required)

1. **`APEX-CORE.md` §11 — Cache policy.** Declare Redis as a control-plane primitive with the permitted and prohibited use cases verbatim from this section. Include the key naming convention.

2. **`CHARTER.md` §3 tool annotations.** Every one of the 44 MCP tools adds two fields: `cacheable: bool` and `cache_ttl_s: int | null`. Write tools: always `cacheable: false`. PII and PCI tools: always `cacheable: false`. Stable reference tools (`rc.item.get`, `rc.location.get`, `rc.hierarchy.tree`): `cacheable: true, cache_ttl_s: 30`. Everything else: default `cacheable: false, cache_ttl_s: null`.

These additions are the enforcement surface. Code lint against the Charter; Charter referenced in CORE.

---

## §7 — OpenClaw File-Family Mapping (source of truth)

When Workstream 4 updates `APEX-CORE.md` Appendix A, the Sellers Guide file-first chapter, and the `README.md` workspace description, all three must reference the same canonical mapping. This table is that source.

| OpenClaw primitive | OpenClaw file | APEX file (this workspace) | Notes |
|---|---|---|---|
| Persistent identity | `SOUL.md` | `APEX-CORE.md` + `CHARTER.md` | APEX splits identity across two files — cross-edition principles (CORE) and edition-specific identity (CHARTER). The split is an enterprise concession; consumer OpenClaw keeps them unified. |
| Social context — rules of the house | `AGENTS.md` | `AGENTS.md` (this workspace) | Same name, same role: autonomous-vs-approval operating rules. |
| Periodic autonomy — scheduled routines | `HEARTBEAT.md` | `HEARTBEAT.md` (this workspace) | Same name, same role: declarative periodic routines in plain language. |
| Social context — user model | `USER.md` | `OPERATOR.md` + `ENGAGEMENT.md` | APEX splits user context into session-level (OPERATOR — who is on shift) and engagement-level (ENGAGEMENT — who the client is and what the scope is). |
| Accumulated memory | `MEMORY.md` + `memory/YYYY-MM-DD.md` | Same (unchanged) | One-to-one mapping. |
| Tool guidance | `TOOLS.md` | `CHARTER.md` §3 (tool catalog) + inline annotations | APEX embeds tool contracts in the edition Charter with structured annotations (`cacheable`, `cache_ttl_s`, oversight, class). Consumer OpenClaw keeps a separate file; APEX folds it into the Charter for governance inheritance. |
| Identity root | `IDENTITY.md` | Folded into `APEX-CORE.md` §1 | Consumer OpenClaw uses a minimal identity stub; APEX treats identity as a chapter of CORE. |
| First-run setup | `BOOTSTRAP.md` | Not used | APEX workspaces are initialized through the Git provisioning process, not a runtime bootstrap. |

### The four OpenClaw primitives — how APEX operationalizes each

1. **Persistent identity** — every agent wakes with the same CORE + CHARTER + ENGAGEMENT + OPERATOR cognitive baseline. Identity is manifest-pinned and signature-verified; the agent cannot drift silently between sessions.

2. **Periodic autonomy** — `HEARTBEAT.md` declares routines that wake agents on schedule. The orchestrator registers these at process startup. Missed triggers do not auto-catch-up — they log and escalate.

3. **Accumulated memory** — daily run logs append-only; weekly operator curation promotes durable facts to `MEMORY.md`. Neither file is agent-writable in curation form — the operator owns the curation step.

4. **Social context** — `OPERATOR.md` (current human-in-the-loop), `ENGAGEMENT.md` (named collaborators, escalation chain), `AGENTS.md` (operating rules for what runs without asking). Together these give the agent a concrete picture of its environment, its peers, and its governance.

### Additions to CORE (required, via Workstream 4.3)

`APEX-CORE.md` Appendix A names the OpenClaw source, the four primitives, the file mapping, and the ClawHavoc research as the driver for enterprise hardening. This is the paradigm-provenance record for the agent's self-description when asked about its architecture.

---

## Validation checklist — run before opening the PR

- [ ] All four workstreams complete.
- [ ] Discovery step results documented in PR description if paths differed from expected.
- [ ] Independence language scan: zero hits for "partner," "partnership," "alliance," "strategic alliance," "joint offering" in all added or modified content.
- [ ] Client naming scan: no specific client names in Sellers Guide examples unless approved reference cases.
- [ ] `APEX-CORE.md` §11 added with Redis cache policy.
- [ ] `APEX-CORE.md` Appendix A added with OpenClaw paradigm provenance.
- [ ] `CHARTER.md` §3 updated with `cacheable` annotations on all 44 tools.
- [ ] `HEARTBEAT.md` created with four routines (monthly close, weekly vendor scorecard, daily valuation, hourly run-state health).
- [ ] `AGENTS.md` created with four bands (just do it, ask first, escalate, never).
- [ ] `manifest.json` version bumped to 0.2.0, boot_sequence shows 10 steps, HEARTBEAT.md and AGENTS.md in file registry, hashes re-computed for all modified files.
- [ ] `README.md` reflects seven-file workspace hierarchy, 10-step boot sequence, updated change-control table.
- [ ] Orchestrator parses HEARTBEAT.md at startup; registered triggers fire correctly in unit tests.
- [ ] Sellers Guide table of contents updated.
- [ ] Sellers Guide file-first chapter references OpenClaw lineage (not as a partnership; as a credited community pattern).
- [ ] Backlog entry created.
- [ ] Redis client module tests pass.
- [ ] MCP wrapper tests pass with the new cache layer.
- [ ] CI lint rule for cache governance active and passing.
- [ ] IaC validates (`bicep build` or `terraform plan` clean).
- [ ] Dashboard Redis health lane renders with test data.
- [ ] All tests pass in CI.

---

## Delivery format

### PR title

`APEX v0.2 — file-first Sellers Guide chapters, Redis control-plane cache, OpenClaw pattern completion, backlog entry`

### PR description template

```
## Summary

This PR delivers APEX v0.2 per `APEX-v0.2-Build-Instructions.md`:

1. Sellers Guide: new chapters on file-first context architecture and parent-child orchestration, including the Redis cache governance section and the OpenClaw lineage subsection.
2. Backlog: APEX-v0.2-F-01 Redis Cache Layer feature entry added.
3. Codebase: Redis control-plane client module, MCP wrapper cache integration, orchestrator and agent-base updates, CI lint rule, IaC for Azure Cache for Redis.
4. Workspace: HEARTBEAT.md and AGENTS.md added; APEX-CORE.md Appendix A (OpenClaw paradigm provenance) added; manifest.json bumped to 0.2.0 with updated boot sequence; README.md reflects seven-file pattern; orchestrator registers scheduled wakes from HEARTBEAT.md.

## Discovery results

- Sellers Guide located at: `<actual path>`
- Backlog located at: `<actual path or "external system — manual creation required">`
- Primary codebase language: `<Python | TypeScript | other>`

## Files changed

`<git diff --stat summary>`

## Test results

`<summary of test run>`

## Independence compliance

- Independence language scan: clean.
- Client naming scan: clean.
- `APEX-CORE.md` §11 (Redis policy) added.
- `APEX-CORE.md` Appendix A (OpenClaw provenance) added.
- `CHARTER.md` §3 tool annotations added.
- OpenClaw references credited as a community pattern, not as a partnership.

## Reviewers required

- DMTSP practice (for CORE changes): Keven Markham
- Edition Steward (for CHARTER + HEARTBEAT + AGENTS changes): Keven Markham
- Azure delivery (for Redis integration + orchestrator HEARTBEAT parsing): Tyson Thedinger
- Independence Office (for Sellers Guide content): per practice process

## Manual follow-ups

- Compute file hashes and sign the manifest before tagging the release.
- Provision the Redis instance in the target subscription.
- Create the Entra groups referenced in manifest scopes.
```

### Changelog entry

Add to `CHANGELOG.md`:

```markdown
## v0.2 — 2026-04-22

### Added
- APEX-CORE.md §11 — Redis cache policy declaring control-plane-only usage with explicit prohibitions.
- APEX-CORE.md Appendix A — paradigm provenance, naming OpenClaw SOUL.md as source, crediting the four primitives (persistent identity, periodic autonomy, accumulated memory, social context), and attributing the ClawHavoc research as the driver for enterprise hardening.
- CHARTER.md §3 — `cacheable` and `cache_ttl_s` annotations on all 44 MCP tools.
- HEARTBEAT.md — periodic autonomy declarations (monthly close, weekly vendor scorecard, daily valuation, hourly run-state health).
- AGENTS.md — operating rules in four bands (just do it, ask first, escalate immediately, never).
- Sellers Guide chapters on file-first context architecture and parent-child agent orchestration.
- Sellers Guide section on Redis cache governance.
- Sellers Guide subsection on the OpenClaw lineage.
- Backlog feature APEX-v0.2-F-01 — Redis Cache Layer for APEX Control Plane.
- Redis control-plane client module (`src/control_plane/redis_client.py`).
- CI lint rule for cache governance (`scripts/lint_cache_governance.py`).
- Orchestrator HEARTBEAT.md parser registering scheduled agent wakes through Durable Functions timers.
- Azure Cache for Redis resource in landing zone IaC.
- Dashboard "Redis health" lane (sixth lane).

### Changed
- MCP tool framework wrapper routes through Redis cache with Charter-annotation gating.
- Durable Functions orchestrator writes cancel tokens and budget envelopes to Redis on spawn; parses HEARTBEAT.md at process startup.
- Child agent base class reads control-plane state from Redis with Cosmos fallback.
- Sellers Guide chapters that previously referenced vector stores as primary context clarified to hybrid model.
- README.md reflects seven-file workspace hierarchy and 10-step boot sequence.
- manifest.json version bumped to 0.2.0; boot_sequence extended to 10 steps; HEARTBEAT.md and AGENTS.md added to file registry; hashes recomputed for all modified files.

### Governance
- All changes pass Independence language compliance scan.
- OpenClaw references credited as community pattern; no language implying a partnership, alliance, or joint offering between Deloitte and OpenClaw, the OpenClaw community, or Microsoft.
```

---

## Notes for Claude Code execution

- Execute workstreams in order: 1 (Sellers Guide) → 4 (OpenClaw context files — do this before 2 so the backlog entry and codebase changes can reference the completed workspace) → 2 (backlog) → 3 (codebase). Each informs the next.
- If any workstream cannot complete cleanly, halt and flag rather than work around. Partial deliveries with "TODO" markers are acceptable only for discrete blocked items (e.g., external backlog system requires manual creation).
- Commit incrementally — one commit per logical change, with messages referencing this build file and the workstream number.
- Run the full test suite and lint after each workstream completes.
- If the Independence language lint finds a hit, do not auto-fix silently — surface the hit in the PR description for human review. There are legitimate contextual uses (forbidden-word lists, quoted source material) that the lint cannot distinguish from actual violations.
- If any discovered path, file structure, or convention differs materially from the expectations in this build file, document the divergence in the PR description and proceed with the adapted approach.

---

## References

- `apex-workspace/APEX-CORE.md` — cross-edition principles (v0.1.0)
- `apex-workspace/CHARTER.md` — RC edition identity (v0.1.0)
- `apex-workspace/ENGAGEMENT.md` — Nike R2R context (v0.1.0)
- `apex-workspace/manifest.json` — version and integrity spine
- `docs/APEX-Orchestration-Guide.html` — orchestration patterns and primitives
- `docs/APEX-File-First-Context.html` — file-first paradigm explanation
- `docs/APEX-RC-Logical-Architecture-v0.1.md` — the RC architecture source-of-truth

---

*End of APEX-v0.2-Build-Instructions.md. Owner: Keven Markham. Intended for Claude Code execution against the APEX repo.*
