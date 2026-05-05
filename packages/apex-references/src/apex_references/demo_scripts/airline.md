# Airline — Demo Script

**Reference deployment:** `airline` (TH)
**Sellers Guide §14.8** — airline reference deployment narrative
**Audience:** SVP Operations Control, SVP Customer Experience, VP Revenue Management
**Duration:** 30 minutes (15 walk-through, 15 Q&A)

---

## Scene 1 — IROPS recovery from hub-station weather (7 min)

**Setup.** 1430 local. Convective weather closes the hub for two
hours during the afternoon rolling bank. 200+ flights at risk.
30,000+ passengers. Crew-legality clock ticking on a dozen
multi-leg pairings.

**Show.** Duty manager opens the IROPS recovery card on the
ops-control wallboard:

> **IROPS Recovery Plan v1 — Hub closure 1430-1630**
> Affected: 217 flight legs, 31,400 PAX, 84 crew pairings
>
> **Proposed actions:**
>   - Cancel: 23 turns (lowest revenue + highest re-accommodation feasibility)
>   - Swap: 14 aircraft re-assignments to preserve crew legality
>   - Delay: 142 flights with new ETDs (median +1h17m)
>   - Hold: 38 flights (no change recommended)
>
> **Crew impact:** 11 crews repositioned, 3 crews exceeding legality
> by ≥30 min — deadhead rebook recommended
>
> **Customer impact:** 4,200 PAX with elite-tier loyalty status —
> proactive rebook + apology offers staged
>
> **Network-effect:** projected next-day knock-on at 7%, mitigated to
> 3% by recommended overnight aircraft swap at outstation B
>
> **Audit row:** th-irops-2026-04-23-hub-001
> **Reasoning chain available:** o1 model log attached for ops review

Duty manager reviews scenario, taps `Approve plan v1 / Hold one`.
Disruption-comms agent fires customer notifications, crew rebooks,
gate reassignments, ground-ops updates simultaneously across all
channels.

**Why it matters.** This used to be 90+ minutes of phone-tree
coordination across ops, crew, and customer-care, with
inconsistent communication across channels. Here: under 60 minutes
from trigger to HITL gate, integrated across all three
constituencies, audit row complete.

---

## Scene 2 — Yield management with competitor watch (3 min)

**Setup.** Low-cost competitor entered three core leisure markets
last week.

**Show.** Revenue analyst dashboard:

> **Yield action — O&D LAX-LAS**
> Competitor fare: $89 (was $129)   |   Booking-curve velocity: +18% on competitor, -12% on us
>
> **Recommendation:** drop bottom three RBDs to $99 / $109 / $129;
> protect top three RBDs unchanged; trigger corporate-contract
> protection rule for top 12 corporate accounts on this O&D
>
> Expected revenue effect: +$340K / 7 days (vs. -$220K status-quo)
> Loyalty impact: +0.3pp elite booking share
>
> **Audit row:** th-yield-2026-04-23-laxlas-014

Revenue analyst reviews and approves. Yield agent writes to inventory
system; corporate-contract protection layer ensures elite + corporate
fares remain shielded.

---

## Scene 3 — Traveler 360 + loyalty personalization (3 min)

**Setup.** Top-tier loyalty member had a service event two weeks ago
(IROPS-related missed connection).

**Show.** Customer-care dashboard surfaces a service-recovery offer
proposal: choice of 25K bonus miles + lounge pass, or upgrade certificate,
or partner-hotel night. Personalization confidence: 0.84 based on past
redemption pattern. CSR HITL approves; traveler-360 agent fires the
delivery via Salesforce Marketing Cloud with PII-redaction at the
boundary.

---

## Scene 4 — Ground ops on-time performance (1 min)

Brief glance at the at-risk-turn precision dashboard for the pilot hub
station. Top-of-shift digest, dispatcher-friendly format.

---

## Scene 5 — Architecture walk-through (1 min)

F128 Fabric capacity with **ops-control / commercial workload
isolation**, Purview classifications (`pii`, `payment-card`,
`operations`), audit-row stream supporting both ops-control event
investigation and commercial revenue attribution.

**Cross-references:**
- Sellers Guide §14.8 — airline reference deployment scope
- Sprint 14 — capacity blueprint (`per-workload-isolation`)
- Sprint 15 — adapters (Salesforce, ServiceNow, Workday, analytics platforms)
- Sprint 16 — 10 TH anchor agents
- Sprint 17 — services (TH-AIR series)

---

## Wave-1 commercial wrap (close)

> "8-12 weeks. Fixed-fee $900K-$1.75M envelope. You get the F128
> Fabric footprint with ops-control/commercial isolation, four
> adapters live, five agents in production including a reasoning-tier
> IROPS recovery, PII + PCI audit posture, and a Wave-2 proposal with
> named KPI commitments tied to D0 on-time performance, IROPS recovery
> cycle time, yield per ASM, and elite-tier retention. Ready to
> schedule the ops-control + revenue-management review?"
