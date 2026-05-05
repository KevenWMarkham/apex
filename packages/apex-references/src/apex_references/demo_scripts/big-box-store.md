# Big Box Store — Demo Script

**Reference deployment:** `big-box-store` (RC)
**Sellers Guide §16.13** — reference deployment narrative
**Audience:** Chief Merchant, Chief Supply Chain Officer, VP Store Operations
**Duration:** 30 minutes (15 walk-through, 15 Q&A)

---

## Scene 1 — Cold-chain excursion (5 min)

**Setup.** A heat dome rolls across the Mid-Atlantic. Refrigeration
telemetry shows a sustained excursion across 220 stores in the
pilot region.

**Show.** Open the Teams card on a tablet (Store Manager surface):

> **Cold-chain alert — Store 4127, Dairy case 3**
> Excursion: 4h 22m above 41°F threshold
> Estimated impact: 412 SKUs, $1,860 product value, FSMA 204 lot trace attached
>
> **Recommended action:** Mark down 187 SKUs to 50%, donate 142 (still within USDA window), destroy 83 (out-of-spec)
>
> Confidence: 0.84   |   Audit row: rc-cce-2026-04-23-04127-003

**Click `Approve`.** Cold-chain response agent emits audit row to the
governance workspace, writes markdown action to SAP S/4HANA via the
mirrored adapter, and pushes the donation list to the regional food bank
integration.

**Why it matters.** The Sellers Guide §10.2 cold-chain cadence used to
take 90+ minutes per store. Here: under 30 minutes, audit-row complete,
FSMA 204 defensible, store manager unblocked.

---

## Scene 2 — Markdown cadence reset (5 min)

**Setup.** Q3 markdown cadence on private-label apparel is 9pp under
plan.

**Show.** Open the Chief Merchant dashboard:

> **Markdown cadence proposal — Women's Fall Apparel**
> Sell-through gap to plan: -9.2pp at week 8
> Proposal: accelerate week-10 markdown from 25% to 35%; protect 12 hero SKUs at full price; clear long-tail at 50% in week 12
>
> Elasticity confidence: 0.78 (model-based) + 0.81 (analog-store override)
> Forecast lift: $2.1M GM recovery vs. status-quo cadence
>
> Linked SCML lots, supplier rebate eligibility, store-cluster overrides

**Approve at category level.** Markdown cadence agent writes to ERP,
notifies category captains, schedules store-execution via
store-ops-intelligence.

**Why it matters.** Same-day evidence-based reset; merchant retains
authority; agent does the orchestration.

---

## Scene 3 — Demand-sense replenishment under hurricane forecast (3 min)

**Setup.** Hurricane forecast triggers anticipatory buying on top-200
SKUs across coastal Carolinas.

**Show.** Demand-sensing agent has flagged the demand shift; replenishment
agent has staged proposals against allocation constraints; substitution
recommender pre-staged alternates for at-risk SKUs (cases of 24-pack
water if 12-pack is out, etc.).

The supply-chain VP sees a single dashboard: "47 SKUs at risk in
8 stores, here's the proposed substitution playbook, here's the
DC capacity check, here's the cost." One approval, full chain
moves.

---

## Scene 4 — Architecture walk-through (2 min)

Show the F128 Fabric capacity, the Bronze/Silver/Gold workspaces, the
Purview classifications applied (`pii`, `payment-card`,
`operations`), the audit-row stream into the governance workspace,
and the HITL surface for every consequential decision.

**Cross-references for the prospect:**
- Sellers Guide §16.13 — full reference deployment scope
- Sprint 14 — capacity blueprint (`single-capacity-tenant`, F128)
- Sprint 15 — adapter inventory (SAP S/4HANA, Manhattan WMS, Salesforce Marketing Cloud, etc.)
- Sprint 16 — agent catalog (10 RC anchor agents)
- Sprint 17 — service catalog (RC-E2E + RC-TTP)

---

## Wave-1 commercial wrap (close)

> "8-12 weeks. Fixed-fee $750K-$1.5M envelope. You get the F128 Fabric
> footprint, three SOR adapters live, four agents in production,
> the audit posture for FSMA 204, and a Wave-2 proposal with
> named KPI commitments. Want to schedule the architecture review?"
