# AXLE (Industrial / Discrete Manufacturing) — Wave 1 / 2 / 3 Playbook

**Practice anchor:** Discrete-manufacturing plant (automotive Tier-1, industrial OEM, aerospace)
**Sellers Guide:** §12.9–§12.11, §12.9A plant reference deployment

---

## Wave 1 — Envision & Land (8-12 weeks, $0.85-1.75M fixed-fee)

**Objective.** Stand up F128 Fabric with OT/IT workload isolation, light up OEE monitor +
predictive maintenance + quality-defect agents on a flagship line, prove IP /
controlled-unclassified audit posture.

### Deliverables

- F128 Fabric capacity with OT/IT workload isolation per Sprint 14 (operational telemetry separated from enterprise IT)
- GE Proficy + SAP S/4HANA + OSI PI + analytics-platforms adapters live in Bronze
- MERML + QMSML + SCML canonical schemas in Silver
- OEE monitor + andon-RCA agents live for one flagship line
- Predictive-maintenance agent in shadow mode + HITL work-order proposal
- Quality-defect + supplier-quality agents live for top-5 part numbers
- Production-scheduling agent in HITL for one cell
- Energy-optimization agent in HOTL for compressed-air + HVAC
- IP + controlled-unclassified classifications applied per Sprint 13
- Sellers Guide §12.9A demo deck + Plant Manager / VP Operations readout

### Anchor agents for Wave-1 light-up

| Agent | When to choose | Sprint 16 ref |
|-------|----------------|---------------|
| OEE monitor + andon RCA | Flagship line OEE shortfall | `apex.axle.agents.oee-monitor` |
| Predictive maintenance | Unplanned downtime hours pain | `apex.axle.agents.predictive-maintenance` |
| Quality defect + supplier quality | Field defect PPM + supplier surveillance | `apex.axle.agents.quality-defect` + `apex.axle.agents.supplier-quality` |
| Production scheduling | Demand variance disrupting schedule | `apex.axle.agents.production-scheduling` |
| Energy optimization | Industrial electricity rate spike | `apex.axle.agents.energy-optimization` |

### Exit criteria

- OEE attribution dashboard validated by plant manager for ≥ 4 weeks
- Predictive maintenance hit-rate ≥ 70% precision on impending-failure alerts
- Quality-defect agent surfaces ≥ 1 supplier-lot correlation that prior process missed
- Energy load-shift produces ≥ 5% measurable demand-charge reduction
- Wave-2 commercial proposal signed

---

## Wave 2 — Enable & Scale (8-14 months, $3-7M fixed-fee + value-share on warranty)

**Objective.** Plant-wide rollout, additional lines, warranty-cost attribution
program, generative-engineering pilot.

### Deliverables

- Plant-wide OEE monitor + predictive maintenance across all critical lines
- Quality-defect + supplier-quality across all production cells
- Production scheduling integrated with SAP S/4HANA work-order writeback
- Energy optimization across all major loads (compressed air, HVAC, peak shaving)
- Warranty-cost attribution agent linking field claims to manufacturing genealogy
- Generative-engineering pilot for new-product introduction
- Vehicle-DTC pattern detection (automotive clients)

### Wave-2 KPI commitments (typical)

- OEE: +5-8pp on pilot line → +3-5pp plant-wide
- Unplanned downtime: -20-30% on instrumented assets
- Field-defect PPM: -25-40% on monitored part numbers
- Energy cost per produced unit: -8-12%
- Warranty cost per vehicle (auto clients): -3-5%

### Exit criteria

- All Wave-2 KPI commitments measurably met
- Warranty-cost attribution producing supplier 8D corrective-action wins
- Wave-3 retainer proposal signed

---

## Wave 3 — Sustain & Transform (36+ months, retainer + outcome-share)

**Objective.** Multi-plant deployment, autonomous-tier routine quality + maintenance,
generative engineering in NPI mainline.

### Deliverables

- Multi-plant deployment across the manufacturing network
- Autonomous-tier services for:
  - Routine OEE attribution (HITL only on novel loss patterns)
  - Routine predictive maintenance work-order release (HITL only on high-cost actions)
  - Routine quality-defect screening (HITL only on novel defect signatures)
- Generative engineering in NPI mainline (parameter optimization, design-for-manufacturability)
- Cross-plant supplier-quality program with proactive corrective-action management
- Continuous improvement tied to plant-management compensation

### Wave-3 KPI commitments (typical)

- OEE: +10pp plant-wide sustained
- Unplanned downtime: -40% sustained
- Field-defect PPM: -50% sustained
- Energy cost per unit: -15-20% sustained
- Warranty cost per vehicle: -8-12% sustained

---

## Cross-references

- Sprint 14 per-workload-isolation OT/IT capacity blueprint
- Sprint 15 adapters (ge-proficy, sap-s4hana, osi-pi, analytics-platforms, servicenow)
- Sprint 16 AXLE anchor agents (10 anchors)
- Sprint 17 AXLE service catalog (AXLE-Connected-Factory + AXLE-QMS + AXLE-Ops + AXLE-Aftermarket + AXLE-Supply)
- Sprint 18 reference deployment: `plant`
- Sellers Guide §12.9–§12.11
