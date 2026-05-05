# TH (Travel & Hospitality) — Wave 1 / 2 / 3 Playbook

**Practice anchor:** Network airline, hotel chain, cruise line, theme-park operator
**Sellers Guide:** §14.8–§14.10, §14.8 airline reference deployment

---

## Wave 1 — Envision & Land (8-12 weeks, $0.9-1.75M fixed-fee)

**Objective.** Stand up F128 Fabric with ops-control / commercial workload isolation,
light up IROPS recovery (reasoning-tier) + traveler-360 in HITL, prove PII + PCI
audit posture.

### Deliverables

- F128 Fabric capacity with ops-control / commercial workload isolation per Sprint 14
- Salesforce + ServiceNow + Workday + analytics-platforms adapters live in Bronze
- TravelerML + OpsML + LoyaltyML + RevML + IROPsML schemas in Silver
- IROPS recovery agent live in HITL for one hub
- Crew-scheduling + disruption-comms agents wired into ops-control workflow
- Yield-management agent in HITL for one revenue region
- Traveler-360 + loyalty-personalization agents live for elite tier
- Ground-ops agent live for one hub station
- PII + payment-card + operations classifications applied
- Sellers Guide §14.8 demo deck + SVP Ops Control / SVP CX / VP RM readout

### Anchor agents for Wave-1 light-up

| Agent | When to choose | Sprint 16 ref |
|-------|----------------|---------------|
| IROPS recovery | Hub-disruption recovery time pain | `apex.th.agents.irops-recovery` |
| Yield management | Competitive yield pressure | `apex.th.agents.yield-management` |
| Traveler 360 | Elite-tier retention pain | `apex.th.agents.traveler-360` |
| Ground ops | D0 / on-time performance shortfall | `apex.th.agents.ground-ops` |
| Demand disruption | Demand-shock response (weather, events) | `apex.th.agents.demand-disruption` |

### Exit criteria

- IROPS recovery plan generated under 60 minutes for ≥ 3 live IROPS events
- Yield agent acceptance rate ≥ 65% on pilot O&Ds
- Top-tier traveler service-recovery offers achieve ≥ 80% engagement
- Ground-ops at-risk-turn precision ≥ 70% on pilot station
- Wave-2 commercial proposal signed

---

## Wave 2 — Enable & Scale (8-14 months, $4-9M fixed-fee + value-share on yield)

**Objective.** Network-wide rollout, full-fleet IROPS coverage, expanded loyalty
personalization, value-share on yield uplift attribution.

### Deliverables

- Network-wide IROPS recovery + crew-scheduling + disruption-comms
- Yield management across all revenue regions with corporate-contract protection
- Traveler-360 across full loyalty base with cross-channel orchestration
- Ground-ops at-risk-turn detection across all hub stations
- F&B / ancillary recommendation in HOTL across all flights
- Guest-experience personalization across cabin classes
- Value-share commercial on yield optimization (TH-AIR-02) and demand-disruption recovery (TH-AIR-07)

### Wave-2 KPI commitments (typical)

- D0 (on-time departure): +2-4pp on pilot stations
- IROPS recovery cycle time: median 35 minutes
- Yield per ASM: +1-3% on instrumented O&Ds
- Top-tier loyalty retention: +2-3pp 12-month
- F&B capture: +5-10% on pilot routes

### Exit criteria

- All Wave-2 KPI commitments measurably met
- Yield value-share producing attributable money KPI delta on instrumented O&Ds
- Wave-3 retainer proposal signed

---

## Wave 3 — Sustain & Transform (24+ months, retainer + outcome-share)

**Objective.** Multi-carrier or alliance-wide deployment, autonomous-tier routine
ops, traveler-360 as commercial hub.

### Deliverables

- Alliance-wide deployment across multiple carriers (where applicable)
- Autonomous-tier services for:
  - Routine yield actions (HITL only on magnitude > threshold or corporate-contract impact)
  - Routine traveler service-recovery (HITL only on top-tier escalations)
  - Routine F&B / ancillary recommendations (HITL on novel cabin mixes only)
- Traveler-360 powering commercial decisions across loyalty, marketing, and CX
- IROPS recovery as ops-control mainline (not exception path)
- Continuous improvement tied to NPS + retention + yield dashboards

### Wave-3 KPI commitments (typical)

- D0: +5pp network-wide
- IROPS recovery cycle: median 20 minutes
- Yield per ASM: +3-5% network
- Elite retention: +5pp sustained
- Baggage mishandle rate: -30% sustained

---

## Cross-references

- Sprint 14 per-workload-isolation capacity blueprint
- Sprint 15 adapters (salesforce, salesforce-marketing-cloud, servicenow, workday-hcm, analytics-platforms)
- Sprint 16 TH anchor agents (10 anchors)
- Sprint 17 TH service catalog (TH-AIR + TH-HOT)
- Sprint 18 reference deployment: `airline`
- Sellers Guide §14.8–§14.10
