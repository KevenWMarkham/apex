# ICE (Industrial Connected Electronics) — Wave 1 / 2 / 3 Playbook

**Practice anchor:** Connected-product OEM (industrial controls, consumer electronics, medical devices)
**Sellers Guide:** §15.9–§15.11

---

## Wave 1 — Envision & Land (8-12 weeks, $0.75-1.5M fixed-fee)

**Objective.** Stand up F128 Fabric with single-tenant capacity (typical for
homogeneous ICE telemetry estate), light up connected-product analytics + dealer-mgmt
agents in HITL, prove operations + IP audit posture.

### Deliverables

- F64 or F128 Fabric capacity per Sprint 14 single-capacity-tenant
- Connected-product telemetry adapter + dealer-channel adapter + ServiceNow
- ConnectedICEML + ConnectedProductML + AMML + DealerML + QMSML schemas in Silver
- Connected-product analytics agent live for top device family
- Dealer-management agent live for top channel partners
- Asset-management agent live in HITL
- Operator-coaching agent (HOTL — pure-HOTL is permitted per Sprint 16 governance)
- Operations + IP classifications applied
- Sellers Guide §15.9 demo deck + Connected-Product VP / Aftermarket Director readout

### Anchor agents for Wave-1 light-up

| Agent | When to choose | Sprint 16 ref |
|-------|----------------|---------------|
| Connected-product analytics | Telemetry-driven service opportunities | `apex.ice.agents.connected-product` |
| Dealer management | Allocation + service quality across dealer network | `apex.ice.agents.dealer-mgmt` |
| Asset management | Asset health + work-order optimization | `apex.ice.agents.asset-mgmt` |
| Operator coaching | Workforce productivity uplift | `apex.ice.agents.operator-coaching` |
| Quality program | Field defect detection across device population | `apex.ice.agents.quality-program` |

### Exit criteria

- Connected-product agent surfaces ≥ 1 firmware / behavioral correlation that prior process missed
- Dealer-mgmt agent acceptance rate ≥ 65% on pilot allocation decisions
- Asset-management work-order proposals approved at ≥ 70% rate
- Wave-2 commercial proposal signed

---

## Wave 2 — Enable & Scale (8-14 months, $2.5-6M fixed-fee + value-share on warranty)

**Objective.** Multi-product-family rollout, advanced telemetry analytics, value-share
on warranty cost recovery.

### Deliverables

- Multi-product-family connected-product analytics across full installed base
- Dealer-mgmt across all channel-partner regions
- Asset-management hospital-wide / field-wide
- Quality-program with proactive supplier corrective-action management
- Service-aftermarket agent for parts-distribution optimization
- Customer-care across product-support queues
- Value-share commercial on warranty-cost reduction and parts-fill-rate uplift

### Wave-2 KPI commitments (typical)

- Field-warranty PPM: -25-40%
- Parts-fill rate: +10-15%
- Asset MTBF: +20-30%
- First-time-fix rate (service): +8-12pp
- Dealer-allocation accuracy: +15-20%

### Exit criteria

- All Wave-2 KPI commitments measurably met
- Warranty-cost value-share producing attributable money KPI delta
- Wave-3 retainer proposal signed

---

## Wave 3 — Sustain & Transform (24+ months, retainer + outcome-share)

**Objective.** Global product-family deployment, autonomous-tier routine telemetry
ops, predictive-quality program at design boundary.

### Deliverables

- Global multi-product-family deployment
- Autonomous-tier services for:
  - Routine telemetry triage (HITL only on novel patterns)
  - Routine work-order release (HITL only on high-cost actions)
  - Routine dealer allocation (HITL only on policy edge cases)
- Predictive-quality at NPI design boundary (DfM analytics)
- Continuous improvement tied to warranty + NPS + dealer-CSAT dashboards

### Wave-3 KPI commitments (typical)

- Field-warranty PPM: -50% sustained
- Asset MTBF: +50% sustained
- Parts-fill rate: 95%+ sustained
- First-time-fix rate: 85%+ sustained

---

## Cross-references

- Sprint 14 single-capacity-tenant capacity blueprint
- Sprint 15 adapters (connected-product telemetry, dealer-channel, ServiceNow)
- Sprint 16 ICE anchor agents (10 anchors)
- Sprint 17 ICE service catalog (ICE-Connected + ICE-Dealer + ICE-Service)
- Sellers Guide §15.9–§15.11
