---
file: HEARTBEAT.md
version: 0.1.0
scope: engagement
class: Internal
required: true
immutable_during_run: true
inherits_from:
  - APEX-CORE.md
  - CHARTER.md
  - ENGAGEMENT.md
authors:
  - Deloitte DMTSP — Consumer Industry
  - Keven Markham (VP, APEX)
purpose: >
  Declare periodic autonomous routines — the "cron for your agent, expressed
  in plain English" pattern from the OpenClaw community, adapted for
  enterprise APEX governance. Routines fire on a schedule, spawn fresh agent
  runs through the full 10-step boot sequence, and respect all HITL gates and
  budget envelopes declared in CHARTER and AGENTS.
paradigm_provenance: >
  Periodic autonomy is the OpenClaw community pattern. See APEX-CORE.md
  Appendix A for the paradigm-provenance record.
---

# HEARTBEAT — Periodic Autonomy

> **Read first.** HEARTBEAT.md is parsed by the orchestrator process at
> startup (not at per-agent boot). Each declared routine registers as an
> Azure Durable Functions timer. When the timer fires, the orchestrator
> spawns a fresh agent run that boots through the full 10-step sequence.
> HEARTBEAT does **not** shortcut the boot.

---

## Operating rules (apply to every routine)

1. **Boot discipline.** Every HEARTBEAT-triggered run performs the full
   10-step boot sequence. No shortcuts, no cached context, no partial
   identity.
2. **Gate inheritance.** Routines respect every HITL gate declared in CHARTER
   and every operating rule in AGENTS. A routine cannot bypass a gate.
3. **No auto-catch-up.** Missed triggers (Redis unreachable at fire time,
   orchestrator down, manifest integrity failure) emit a
   `heartbeat_missed` event to the status channel and escalate per the
   routine's `on_failure` clause. The orchestrator does **not** run skipped
   routines retroactively.
4. **Close-window acceleration.** When ENGAGEMENT declares an active close
   window, HITL deadlines declared in this file are compressed per the
   ENGAGEMENT acceleration policy. Routines do not reset to normal
   deadlines mid-window.
5. **Trigger-source tag.** Every HEARTBEAT-triggered run propagates
   `trigger_source: heartbeat:<routine_name>` through the status channel
   and the audit row (§6.10). A regulator or auditor can always
   distinguish a scheduled run from an interactive run.
6. **Budget envelope.** Each routine's declared budget is enforced by the
   control-plane Redis cache (see APEX-CORE §11). Budget exhaustion triggers
   a soft cancel; the routine's audit row records the cause.

---

## Routine 1 — Monthly close reconciliation

- **Id:** `HB-01-monthly-close-recon`
- **Trigger:** day 1 through day 8 of every month, 06:00 UTC, weekdays only
- **Orchestration:** `ORCH-RC-04` (Close Period Reconciliation)
- **Budget:** 2 hours wall-clock, 500 tool calls, USD 50 per run
- **Oversight:** HITL at checkpoint after each domain (inventory, vendor
  payables, margin, store operations)
- **On failure:** escalate to engagement controller per ENGAGEMENT
  escalation chain; do not retry automatically
- **On anomaly:** variance > 5% against prior-month baseline in any domain
  → escalate to engagement finance lead for manual review
- **Reasoning:** close cycles are time-bounded and regulator-facing;
  agentic acceleration is justified where HITL checkpoints preserve
  auditability.

## Routine 2 — Weekly vendor scorecard

- **Id:** `HB-02-weekly-vendor-scorecard`
- **Trigger:** Monday 08:00 local time (engagement-defined time zone)
- **Orchestration:** `ORCH-RC-04` (Vendor Performance Summary)
- **Budget:** 30 minutes wall-clock, 100 tool calls, USD 10 per run
- **Oversight:** HIC (review-and-distribute) — engagement merchandising
  lead reviews the assembled scorecard before distribution
- **On failure:** log and escalate to engagement merchandising lead;
  distribution skipped that week
- **On anomaly:** top-quartile vendor drops to bottom quartile
  week-over-week → flag for merchandising review
- **Reasoning:** scorecards are operationally routine and the HIC mode
  lets the agent do the aggregation without checkpoint approvals on
  every decision.

## Routine 3 — Daily inventory valuation health

- **Id:** `HB-03-daily-valuation-health`
- **Trigger:** 05:00 UTC daily, every day
- **Orchestration:** `ORCH-RC-05` (Inventory Valuation Integrity Check)
- **Budget:** 15 minutes wall-clock, 80 tool calls, USD 5 per run
- **Oversight:** HIC — valuation lead sees the daily health summary; no
  action needed when health is green
- **On failure:** log and alert engagement inventory lead
- **On anomaly:** valuation variance > 5% versus prior day → escalate
  to engagement inventory lead with named likely cause
- **Reasoning:** detecting drift early prevents cascade into month-end
  close pressure (Routine 1).

## Routine 4 — Hourly run-state health

- **Id:** `HB-04-hourly-run-state-health`
- **Trigger:** every hour on the hour, 24×7
- **Orchestration:** *management operation*, not an agent run — this routine
  reaps the Redis heartbeat store and reconciles against the durable
  status stream
- **Budget:** 2 minutes wall-clock, 20 control-plane calls, USD 0.10 per run
- **Oversight:** HOTL — routine runs unattended; results post to the
  orchestration dashboard (six-lane; Redis health is lane six)
- **On failure:** if the reaper itself fails, page the on-call engineer
  via engagement ops channel
- **On anomaly:** any run with an expired heartbeat (child stuck),
  or split-brain HITL detected, or budget breach in an active run →
  open an incident in the engagement ticket queue
- **Reasoning:** §6.13.5 of the Sellers Guide names zombie children,
  split-brain HITL, cost runaway, stuck HITL, and partial-success
  ambiguity as the five production failure modes. Routine 4 is the
  reaper that observes and escalates them.

---

## Change control

- This file is the engagement-specific heartbeat declaration. Routines
  are added, modified, or retired by engagement leads with CHARTER-level
  approval.
- Changes bump the file version and re-sign the workspace manifest.
- Version bumps follow the `classify-bump` rules in APEX-CORE conventions
  (PATCH: clarification / typo; MINOR: add / extend routine; MAJOR:
  change a trigger or oversight mode on an existing routine).

## Cross-reference

- **Sellers Guide §6.13.8** — Periodic autonomy overview
- **Sellers Guide §6.12** — File-first context architecture
- **APEX-CORE.md §11** — Cache policy (Redis control plane)
- **APEX-CORE.md Appendix A** — OpenClaw paradigm provenance
- **AGENTS.md** — Operating rules (just-do-it / ask-first / escalate /
  never bands) that this file's routines inherit
- **CHARTER.md §3** — MCP tool catalog with `cacheable` annotations that
  affect routine-time cache behavior

---

*End of HEARTBEAT.md v0.1.0. See APEX-CORE.md Appendix A for the OpenClaw
paradigm provenance and attribution.*
