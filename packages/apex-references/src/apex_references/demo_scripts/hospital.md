# Hospital — Demo Script

**Reference deployment:** `hospital` (HLS)
**Sellers Guide §10.9** — hospital reference deployment narrative
**Audience:** Chief Medical Officer, Chief Nursing Officer, VP Revenue Cycle
**Duration:** 30 minutes (15 walk-through, 15 Q&A)

---

## Scene 1 — Sepsis early warning + HITL escalation (5 min)

**Setup.** Med-surg unit overnight. Patient in Bed 412, post-op day 2.
Vitals trending; lactate not yet drawn.

**Show.** Charge nurse Teams card pings:

> **Sepsis early warning — Bed 412, MR# REDACTED**
> Composite score: 0.82 (threshold 0.65)
> Drivers: HR 118 → 124, RR 22 → 26, MAP trending down, WBC delta from 0500 draw
>
> **Suggested SEP-1 bundle steps pre-staged:** lactate, blood culture x2, broad-spectrum coverage per protocol
>
> **Audit row:** hls-sepsis-2026-04-23-412   |   PHI redacted

**Charge nurse taps `Escalate to MD`.** Audit row captures decision +
timestamp. The clinical-decision-support agent is now standing by to
surface drug-interaction and adverse-event flags as orders are placed.

**Why it matters.** The CMO's SEP-1 compliance was 62%. Median
score-to-acknowledgment was 47 minutes. With the agent in HITL on the
pilot units: target median under 15 minutes, audit row for every
decision, regulator-defensible posture.

---

## Scene 2 — Length-of-stay outlier + utilization management (5 min)

**Setup.** Morning census on Med-Surg 4. 28 patients, 6 flagged as
predicted-LOS outliers.

**Show.** Case manager dashboard:

> **LOS outlier — Bed 419, day 4 of predicted 3**
> Predicted barrier: SNF placement (insurance prior-auth pending)
> Suggested action: warm hand-off to discharge planner; pre-stage
> alternate SNF that has open beds + accepts payer
>
> Linked: payer-policy snippet, prior-auth status, SDoH flag
> (transportation barrier)

Case manager works the prioritized list — three discharges accelerated
by end-of-shift, ED freed up by midday.

**Why it matters.** The CNO has a med-surg LOS variance gridlocking the
ED. Wave-2 target: -0.4 to -0.7 days. Wave-3: -1.0 day hospital-wide.
Clean attribution via difference-in-differences against control units.

---

## Scene 3 — Claim triage on first-pass denials (3 min)

**Setup.** Revenue cycle queue: 1,847 denied claims, three specialists
working.

**Show.** Triage agent has scored every claim on `recoverable_value × P(overturn)`:

> **Top of queue — Claim CLM-99213-A**
> Payer: regional MA plan
> Denial reason: lack of medical necessity, code 197
> Recoverable: $4,820   |   P(overturn): 0.78
> Suggested rework: attach progress note from 2026-04-15, reference
> NCD 80.3, refile within 30-day window
>
> **Adverse-event flag:** clinical reviewer should confirm — drug
> interaction noted on related encounter

Specialist works 1.5x as many claims, prioritized by yield. AR aging
moves the right direction.

---

## Scene 4 — Patient identity at the registration boundary (2 min)

Show the patient-identity agent catching a duplicate-MRN at registration
in under 60 seconds, with HIM HITL gate for the merge proposal. Brief
mention of PHI / 42 CFR Part 2 classification + DLP enforcement at every
boundary.

---

## Scene 5 — Architecture walk-through (2 min)

Show the F128 Fabric capacity with **per-workload isolation** (clinical
Bronze/Silver/Gold separated from revenue-cycle), the Purview
classifications (`phi`, `42-cfr-part-2`, `pii`), the audit-row stream
to the governance workspace, and HITL surfaces for every clinical
decision.

**Cross-references:**
- Sellers Guide §10.9 — hospital reference deployment scope
- Sprint 14 — capacity blueprint (`per-workload-isolation`)
- Sprint 15 — adapters (Epic Clarity, HL7-FHIR, Workday)
- Sprint 16 — 10 HLS anchor agents
- Sprint 17 — services (HLS-E2E, HLS-PAY, HLS-LS)

---

## Wave-1 commercial wrap (close)

> "10-14 weeks. Fixed-fee $1.0M-$1.75M envelope. You get the F128
> Fabric footprint with clinical-vs-revcycle isolation, three core
> adapters live, four agents in production, HIPAA + 42 CFR Part 2
> compliant audit posture, and a Wave-2 proposal with named KPI
> commitments tied to SEP-1, LOS, denial rate, and readmission.
> Want to schedule the clinical advisory review?"
