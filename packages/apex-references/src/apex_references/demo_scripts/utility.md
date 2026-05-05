# Utility — Demo Script

**Reference deployment:** `utility` (ER)
**Sellers Guide §11.9** — utility reference deployment narrative
**Audience:** VP Distribution Operations, Chief Reliability Officer, VP Wildfire & Vegetation
**Duration:** 30 minutes (15 walk-through, 15 Q&A)

---

## Scene 1 — PSPS decision under red-flag warning (6 min)

**Setup.** National Weather Service red-flag warning posted for
Service Area B. Fuel moisture < 8%, projected wind gusts to 50 mph,
RH below 15%. PSPS pre-trigger thresholds approaching.

**Show.** PSPS decision agent (reasoning-tier) opens executive Teams
card to VP Wildfire:

> **PSPS pre-trigger — Service Area B**
> Trigger composite: 0.91   |   Threshold: 0.85
> Affected: 47 circuit segments, 138,000 customers, 23 critical-load
> facilities (3 hospitals, 2 dialysis, 1 911 PSAP)
>
> **Recommendation:** De-energize Tiers 1+2 (29 segments, 84,000 customers)
> at 1400 local; hold Tier 3 pending 1100 weather-update review.
>
> Vegetation-risk priors: 14 segments with last-cycle defect rate >2x,
> all in Tier 1
>
> **Audit row:** er-psps-2026-04-23-areaB-001
> **PUC-defensible:** all input sources timestamped, model version
> pinned, weather-data provenance attached

VP Wildfire reviews the segment list, taps `Approve Tier 1+2 / Defer Tier 3`,
adds approval notes. Agent triggers customer-notification workflow,
crew pre-staging, hospital-care plans.

**Why it matters.** Past PSPS decisions took 4-6 hours of manual
triangulation across separate tools, with regulator pushback on audit
completeness. Here: under 6 hours from pre-trigger to defensible HITL
gate, audit row complete, every input timestamped and model-version
pinned.

---

## Scene 2 — Outage triage + restoration sequencing (5 min)

**Setup.** Severe thunderstorm rolls through Service Area C. SCADA
shows 31 distribution circuits offline, ~80,000 customers affected.

**Show.** Outage triage agent has clustered events by likely root
cause, identified affected critical customers, and computed restoration
complexity. Restoration sequencing agent has drafted a crew-dispatch
plan:

> **Restoration plan v1 — Service Area C**
> Crews available: 47 (mainline) + 12 mutual-aid (en route)
> Sequence: priority block A (critical loads, est. 90 min) → block B
> (largest customer-count, est. 4h) → block C (long-tail single laterals, est. 12h)
>
> Estimated time to restore (ETR): customer-facing publish at 1430,
> 1830, midnight respectively
>
> Crew-safety constraints: lightning lockout window through 1330, then
> de-energization confirmations required on three specific feeders

Dispatcher reviews on the ops-center wallboard, approves blocks A+B,
modifies block C ordering. ETR auto-publishes to customer channels.

---

## Scene 3 — Vegetation-risk inspection (2 min)

Show the vegetation-risk agent fusing LiDAR scans, satellite imagery,
and work-order history into per-span risk scores. Inspection foreman
gets a prioritized list with photo-evidence pre-staged. Defect-find
rate uplift: +30-50% target in Wave-2.

---

## Scene 4 — DER orchestration (2 min)

Show the DER orchestration agent dispatching solar + battery + V2G
during a forecasted peak; operator HITL on aggregate magnitude;
grid-stability constraints inviolable.

---

## Scene 5 — AMI billing-anomaly RCA (1 min)

Brief mention: cluster-detection on AMI bill exceptions catches a
metering-firmware regression in days vs. the prior weeks-long PUC
complaint cycle.

---

## Scene 6 — Architecture walk-through (2 min)

F128 Fabric capacity with **dev-prod split** for safe model promotion,
the Purview classifications (`critical-infrastructure`, `cip-014`,
`pii`), audit-row stream to the governance workspace meeting PUC and
FERC retention expectations, HITL surfaces with VP-level gate for PSPS.

**Cross-references:**
- Sellers Guide §11.9 — utility reference deployment scope
- Sprint 14 — capacity blueprint (`dev-prod-split`)
- Sprint 15 — adapters (OSI PI, ServiceNow, AS/400 CIS)
- Sprint 16 — 10 ER anchor agents
- Sprint 17 — services (ER-PU, ER-MN, ER-OG)

---

## Wave-1 commercial wrap (close)

> "10-14 weeks. Fixed-fee $1.0M-$2.0M envelope. You get the F128
> Fabric footprint with dev-prod isolation, three SOR adapters live,
> five agents in production including a regulator-grade PSPS decision
> support, CIP-014 + critical-infrastructure audit posture, and a
> Wave-2 proposal with named KPI commitments tied to SAIDI, PSPS audit
> completeness, vegetation defect-find rate, and AMI billing cycle
> time. Ready to schedule the operations-control review?"
