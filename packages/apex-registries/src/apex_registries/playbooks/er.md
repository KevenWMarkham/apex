# ER (Energy & Resources) — Wave 1 / 2 / 3 Playbook

**Practice anchor:** Investor-owned electric utility, integrated oil & gas, mining, water
**Sellers Guide:** §11.9–§11.11, §11.9 utility reference deployment

---

## Wave 1 — Envision & Land (10-14 weeks, $1.0-2.0M fixed-fee)

**Objective.** Stand up F128 Fabric with dev-prod isolation for safe model promotion,
light up outage triage + restoration sequencing in HOTL, PSPS decision in HITL with
VP-level gate, prove regulator-grade audit posture (CIP-014, FERC, PUC).

### Deliverables

- F128 Fabric capacity with dev-prod split per Sprint 14
- OSI PI + ServiceNow + AS/400 CIS + Oracle EBS adapters live in Bronze
- GridML + OutageML + MeterML canonical schemas in Silver
- Outage triage + restoration sequencing agents live in HOTL for one operating district
- PSPS decision agent in HITL with VP-level gate (regulator-grade audit row)
- Vegetation-risk agent live for one operating district
- AMI billing-anomaly agent live for top-2 customer-care escalation patterns
- CIP-014 + critical-infrastructure + PII classifications applied
- Audit-row stream meeting PUC + FERC retention expectations
- Sellers Guide §11.9 demo deck + Operations / Reliability / Wildfire VP readout

### Anchor agents for Wave-1 light-up

| Agent | When to choose | Sprint 16 ref |
|-------|----------------|---------------|
| Outage triage | Storm-driven outage surge pain | `apex.er.agents.outage-triage` |
| Restoration sequencing | ETR accuracy + crew dispatch optimization | `apex.er.agents.restoration-sequencing` |
| PSPS decision | Wildfire-prone territory + regulator scrutiny | `apex.er.agents.psps-decision` |
| Vegetation risk | Seasonal vegetation defect-find rate target | `apex.er.agents.vegetation-risk` |
| AMI billing anomaly | PUC complaint volume + customer-care backlog | `apex.er.agents.ami-billing-anomaly` |

### Exit criteria

- PSPS decision audit row emitted for every model run regardless of disposition
- Outage triage suggestion accepted by dispatcher ≥ 75% of the time
- Vegetation inspection defect-find rate ≥ +25% versus prior cycle
- AMI anomaly RCA cycle time < 5 days median in pilot district
- Wave-2 commercial proposal signed

---

## Wave 2 — Enable & Scale (8-15 months, $3-8M fixed-fee)

**Objective.** Service-territory-wide rollout, DER orchestration in HITL, expanded
agent set, value-share on AMI billing recovery.

### Deliverables

- Territory-wide outage triage + restoration sequencing
- DER orchestration agent live in HITL (solar + battery + V2G dispatch)
- Vegetation-risk inspection across all priority-fire districts
- AMI billing-anomaly across all customer-care escalation patterns
- Well operations / drilling safety / fleet-mining agents (oil-gas-mining clients)
- HSE incident agent across all field operations
- Audit-row stream supporting NERC CIP audit responses

### Wave-2 KPI commitments (typical)

- SAIDI: -8-12% in pilot region
- SAIFI: -10-15% in pilot region
- PSPS-decision audit completeness: 100% (regulator-attested)
- Vegetation inspection yield (defect-find rate): +30-50%
- AMI billing-complaint cycle time: -50%
- HSE near-miss reporting rate: +30% (leading indicator)

### Exit criteria

- All Wave-2 KPI commitments measurably met
- DER dispatch producing attributable demand-charge reduction or peaker-MWh avoided
- Wave-3 retainer proposal signed

---

## Wave 3 — Sustain & Transform (36+ months, retainer + outcome-share)

**Objective.** Multi-territory deployment, autonomous-tier routine grid operations,
predictive maintenance program tied to capital-plan optimization.

### Deliverables

- Multi-territory deployment with cross-territory coordination
- Autonomous-tier services for:
  - Routine outage triage (HITL only on multi-circuit events)
  - Routine vegetation prioritization (HITL only on policy edge cases)
  - Routine AMI billing (HITL only on novel anomaly patterns)
- DER orchestration with grid-stability constraint integration
- Predictive maintenance feeding capital-plan optimization
- HSE program with leading-indicator dashboards + corrective-action loop
- Audit posture sustained across multi-year regulator review cycles

### Wave-3 KPI commitments (typical)

- SAIDI: -15-20% sustained system-wide
- PSPS audit completeness: 100% maintained + regulator-attested
- Vegetation defect-find rate: +60% sustained
- AMI billing RCA cycle time: -75% sustained
- DER dispatch demand-charge reduction: 5-10% peak shaving

---

## Cross-references

- Sprint 14 dev-prod-split capacity blueprint
- Sprint 15 adapters (osi-pi, servicenow, as400-db2, oracle-ebs-fusion)
- Sprint 16 ER anchor agents (10 anchors)
- Sprint 17 ER service catalog (ER-PU + ER-OG + ER-MN)
- Sprint 18 reference deployment: `utility`
- Sellers Guide §11.9–§11.11
