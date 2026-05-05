# RC (Retail & Consumer) — Wave 1 / 2 / 3 Playbook

**Practice anchor:** Big-box retail, grocery, drug, omnichannel CPG operations
**Sellers Guide:** §9.11–§9.13, §16.13 reference deployment

---

## Wave 1 — Envision & Land (4-12 weeks, $0.5-1.5M fixed-fee)

**Objective.** Stand up the Fabric F-SKU footprint, light up the highest-pain agent
in HITL mode for a controlled cluster, prove the audit posture, and sign a Wave-2
proposal with named KPI commitments.

### Deliverables

- F64 or F128 Fabric capacity provisioned via Sprint 14 single-capacity-tenant blueprint
- 2-3 SOR adapters live in Bronze (typically: SAP S/4HANA + WMS + Salesforce Marketing Cloud)
- SCML + CXML + MERML canonical schemas instantiated in Silver
- 1-2 anchor agents in production HITL mode, scoped to a regional pilot cluster (50-100 stores)
- Purview classifications applied per Sprint 13 governance baseline
- Audit-row stream emitting to governance workspace
- Sellers Guide §16.13 demo deck + Chief Merchant / Chief Supply Chain Officer readout
- Wave-2 commercial proposal with named KPI commitments

### Anchor agents to consider for Wave-1 light-up

| Agent | When to choose | Sprint 16 ref |
|-------|----------------|---------------|
| Cold-chain response | FSMA 204 exposure + recent excursion event | `apex.rc.agents.cold-chain-response` |
| Markdown cadence | Underperforming sell-through in named division | `apex.rc.agents.markdown-cadence` |
| Demand sensing | Stockout / OOS pain in top-200 SKUs | `apex.rc.agents.demand-sensing` |
| Shrink detection | Multi-quarter shrink trend + LP team capacity | `apex.rc.agents.shrink-detection` |

### Exit criteria

- Cold-chain alert → HITL approval median latency < 30 minutes (or applicable SLA per chosen agent)
- ≥ 80% audit-row completeness on every consequential decision
- Pilot cluster operational on agent for ≥ 4 weeks
- Wave-2 commercial proposal signed

---

## Wave 2 — Enable & Scale (6-12 months, $2-6M fixed-fee + value-share)

**Objective.** Scale the proven Wave-1 agent across the chain, light up 4-6 additional
agents, instrument the full RC service catalog, transition value-share-eligible
services off fixed-fee.

### Deliverables

- F128 → F256 capacity expansion as workload grows
- 4-6 additional adapters (Manhattan, BlueYonder, Snowflake mirror, dunnhumby data feed)
- 8-10 Sprint 16 agents in production with HITL/HOTL mix per Sellers Guide §2.2C
- RC-E2E + RC-TTP service families operational across pilot 500 stores
- Value-share commercial flips on RC-E2E-04 (cold chain), RC-E2E-06 (shrink), RC-E2E-09 (markdown)
- Cross-store ML pipeline mature (Demand sensing, replenishment, substitution recommender wired together)
- Store-ops digest reaching all pilot 500 store managers
- Audit row consumption pipeline supplying executive dashboards

### Wave-2 KPI commitments (typical)

- Gross margin: +150-300 bps in pilot category cluster
- Out-of-stock rate (top-200 SKUs): -20%
- Shrink as % of sales: -15-25%
- Cold-chain disposition latency: median 25 minutes
- Markdown cadence yield: +5-9% sell-through vs. plan

### Exit criteria

- All Wave-2 KPI commitments measurably met in pilot cluster
- Wave-3 mature-ops proposal signed with named retention commitments

---

## Wave 3 — Sustain & Transform (24+ months, retainer + outcome-share)

**Objective.** Chain-wide deployment, autonomous-tier services for routine decisions,
transformation of merchandising/supply-chain/store-ops org models around the agent
posture.

### Deliverables

- Chain-wide rollout across all 1000+ stores
- 15+ agents in production with mature HOTL/HIC oversight on routine
- Autonomous-tier (HOTL exception-only) services for:
  - Replenishment routine (HITL only on major substitutions)
  - Markdown cadence routine (HITL only on category-level overrides)
  - Cold-chain disposition routine (HITL only on multi-store excursions)
- Org-model changes: store-ops captains supported by digest, category captains using assortment-pricing copilot
- Continuous KPI improvement program tied to compensation
- Value-share contracts renegotiated based on Wave-2 baselines

### Wave-3 KPI commitments (typical)

- Gross margin: +200-400 bps chain-wide
- OOS rate (top-200 SKUs): -40%
- Shrink as % of sales: -30-40%
- Cold-chain disposition latency: median 12 minutes
- Markdown cadence yield: +10-15% sell-through

---

## Cross-references

- Sprint 14 capacity blueprints
- Sprint 15 SOR adapters (sap-s4hana, manhattan-wms, salesforce-marketing-cloud, oracle-ebs-fusion, snowflake-databricks)
- Sprint 16 RC anchor agents (10 anchors)
- Sprint 17 RC service catalog (RC-E2E + RC-TTP)
- Sprint 18 reference deployment: `big-box-store`
- Sellers Guide §9.11–§9.13 (Practice deep-dive), §16.13 (reference deployment)
