# Plant — Demo Script

**Reference deployment:** `plant` (AXLE)
**Sellers Guide §12.9A** — plant reference deployment narrative
**Audience:** VP Manufacturing Operations, Plant Manager, Director of Quality
**Duration:** 30 minutes (15 walk-through, 15 Q&A)

---

## Scene 1 — OEE attribution + closed-loop improvement (5 min)

**Setup.** Flagship assembly line OEE stuck at 68% for two quarters
against a 78% target. Plant Manager has a budget review next week.

**Show.** Plant Manager opens the morning digest:

> **OEE Monitor — Line 7 (Assembly)**
> Trailing 7-day OEE: 67.4% (target 78%)
> Decomposition:
>   - Availability 82.1% (target 92%) — Δ from changeover #4 + breakdowns
>   - Performance 91.4% (target 95%) — minor stops on stations 12, 15
>   - Quality 89.8% (target 95%) — rework loop spike on welding cell
>
> **Top 3 levers (confidence):**
>   1. Reduce changeover #4 from 22m → 12m via SMED pattern (0.83)
>   2. Address station-12 minor stops — sensor noise root-cause (0.76)
>   3. Investigate welding cell rework — supplier coil correlation? (0.68)
>
> Andon-RCA correlation: 14 of 23 minor stops on station-12 traced
> to single sensor; supplier-coil correlation flagged 3 weeks ago.

Plant Manager assigns levers to maintenance + quality leads via the
digest. Wave-2 OEE target: +5-8pp on this pilot line.

---

## Scene 2 — Predictive maintenance with HITL work-order release (4 min)

**Setup.** Mid-shift. Predictive-maintenance agent flags a stamping
press.

**Show.** Maintenance planner Teams card:

> **Impending failure — Stamping Press 4, Servo motor**
> Score: 0.87   |   Threshold: 0.75
> Drivers: vibration spectrum shift on 240Hz harmonic, current draw
> trending up over 14 days
> Predicted MTBF if untreated: 96-144 hours
>
> **Proposed work order:** WO-AXLE-2026-0423-01
> - Replace servo motor (SAP part 4500-2298-A) — in stock at South Crib
> - Recommended schedule: this Friday 1800 changeover window (current
>   plan has Press 4 idle from 1830-2230)
>
> **Audit row:** axle-pdm-2026-04-23-press4

Planner taps `Approve`. Agent writes WO to SAP S/4HANA via the adapter,
reserves the part, schedules the maintenance technician.

**Why it matters.** Wave-2 unplanned-downtime target: -20-30% on
instrumented assets. Wave-3: -40%.

---

## Scene 3 — Quality defect + supplier surveillance (3 min)

**Setup.** Vision system on inspection cell flags a defect cluster
on bracket sub-assembly.

**Show.** Quality engineer dashboard:

> **Defect cluster — Bracket Sub-Assembly P/N 7714**
> 47 rejects in trailing 8 hours (baseline ~3/day)
> SPC chart: Cpk dropped from 1.42 to 0.78 since 0400 shift change
>
> **Root-cause hypothesis (0.81 confidence):**
> Supplier lot change on 4032-Steel: lot SKL-2026-04-19 → SKL-2026-04-22
> dimensional drift on 3 of 47 sampled measurements
>
> **Suggested supplier corrective action (draft):**
> 8D-1 issued to Supplier ACME Forge, sample retention requested,
> contained-shipment quarantine on Receiving Bay 3

Director of Quality reviews, edits, sends. Audit row tied to manufacturing
genealogy → traceable downstream if any product reaches the field.

---

## Scene 4 — Energy-optimization load shifting (2 min)

Show the energy-optimization agent recommending compressed-air load shift
out of the 1500-1700 demand-charge window using on-site battery + HVAC
flex; operator HITL on aggregate magnitude. Wave-2 target: -8-12% energy
cost per unit.

---

## Scene 5 — Production scheduling under constraint (2 min)

Show the production-scheduling agent re-sequencing Line 7 after a
material constraint (steel coil delay); planner HITL approves; SAP work
orders updated.

---

## Scene 6 — Architecture walk-through (2 min)

F128 Fabric capacity with **OT/IT workload isolation** (operational
telemetry separated from enterprise IT), Purview classifications
(`operations`, `intellectual-property`, `controlled-unclassified`),
audit-row stream protecting the engineering surface.

**Cross-references:**
- Sellers Guide §12.9A — plant reference deployment scope
- Sprint 14 — capacity blueprint (`per-workload-isolation`)
- Sprint 15 — adapters (GE Proficy, SAP S/4HANA, OSI PI)
- Sprint 16 — 10 AXLE anchor agents
- Sprint 17 — services (AXLE-Connected-Factory, AXLE-QMS, AXLE-Ops, AXLE-Aftermarket)

---

## Wave-1 commercial wrap (close)

> "8-12 weeks. Fixed-fee $850K-$1.75M envelope. You get the F128 Fabric
> footprint with OT/IT isolation, three SOR adapters live, six agents
> in production, IP + CUI audit posture, and a Wave-2 proposal with
> named KPI commitments tied to OEE, unplanned downtime, defect PPM,
> and energy cost per unit. Want to walk the line and schedule the
> implementation review?"
