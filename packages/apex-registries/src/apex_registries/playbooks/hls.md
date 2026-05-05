# HLS (Healthcare & Life Sciences) — Wave 1 / 2 / 3 Playbook

**Practice anchor:** Acute-care hospital, IDN, payer, life-sciences study sponsor
**Sellers Guide:** §10.9–§10.11, §10.9 hospital reference deployment

---

## Wave 1 — Envision & Land (10-14 weeks, $1.0-1.75M fixed-fee)

**Objective.** Stand up F128 Fabric with clinical/revenue-cycle workload isolation,
light up sepsis early warning + claim triage in HITL, prove HIPAA + 42 CFR Part 2
audit posture.

### Deliverables

- F128 Fabric capacity with per-workload isolation (clinical Bronze/Silver/Gold separated from revenue cycle)
- Epic Clarity + HL7-FHIR + Workday adapters live in Bronze
- PatientML + ClaimML + EncounterML canonical schemas in Silver
- Sepsis early-warning agent live in HITL on 2 pilot units (typical: Med-Surg + Cardiac telemetry unit)
- Claim-triage agent live for top-3 payer queues
- Patient-identity agent at registration boundary
- HIPAA + 42 CFR Part 2 + state breach-notification classifications applied
- All audit rows tagged `phi` + `clinical-decision` and stored with crypto preservation
- Sellers Guide §10.9 demo deck + CMO/CNO/CFO readout
- Wave-2 commercial proposal with named SEP-1 / LOS / denial-rate / readmission KPI commitments

### Anchor agents to consider for Wave-1 light-up

| Agent | When to choose | Sprint 16 ref |
|-------|----------------|---------------|
| Sepsis early warning | SEP-1 compliance shortfall + alert-fatigue pain | `apex.hls.agents.sepsis-early-warning` |
| Claim triage | First-pass denial rate ≥ 8% + AR aging | `apex.hls.agents.claim-triage` |
| Utilization management | LOS variance gridlocking ED | `apex.hls.agents.utilization-management` |
| Patient identity | Duplicate-MRN backlog + HIM team capacity | `apex.hls.agents.patient-identity` |

### Exit criteria

- Sepsis alert → nurse acknowledgment median < 15 minutes on pilot units
- Claim-triage queue throughput ≥ 1.5x baseline
- All clinical agents emit audit rows tagged phi + clinical-decision
- Patient-identity duplicate-detection running with HIM HITL
- Wave-2 commercial proposal signed

---

## Wave 2 — Enable & Scale (6-12 months, $3-8M fixed-fee + value-share on revenue cycle)

**Objective.** Hospital-wide rollout, additional clinical agents, value-share on payer-cycle services.

### Deliverables

- Hospital-wide sepsis early warning across all inpatient units
- 6-8 additional clinical agents (drug interaction, adverse event, readmission risk, supply cold chain, study enrollment, clinical decision support)
- Utilization-management hospital-wide with case-manager workflow integration
- Claim triage extended to all payers, denial-rework playbook automation
- 30-day readmission risk model in production HOTL with care-management integration
- Value-share commercial on HLS-PAY-01 (claim cycle) and HLS-PAY-02 (denial reversal)
- Audit row consumption to QA committee dashboards

### Wave-2 KPI commitments (typical)

- SEP-1 bundle compliance: +12-20pp in pilot units → hospital-wide
- Med-surg LOS: -0.4 to -0.7 days
- First-pass denial rate: -15-25%
- 30-day readmission (CHF / pneumonia): -1.5pp to -3pp
- Patient-identity duplicate-merge cycle: -60%

### Exit criteria

- All Wave-2 clinical KPI commitments measurably met
- Revenue-cycle value-share contracts producing attributable money KPI delta
- Wave-3 mature-ops proposal signed

---

## Wave 3 — Sustain & Transform (24+ months, retainer + outcome-share)

**Objective.** IDN-wide deployment, autonomous-tier routine clinical decisions,
research-grade evidence pipeline.

### Deliverables

- IDN-wide deployment across all member hospitals
- 12+ agents in production with mature HOTL/HIC mix
- Autonomous-tier services for:
  - Routine drug-interaction screening (HITL only on novel interactions)
  - Routine claim triage (HITL only on appeals)
  - Routine patient-identity reconciliation (HITL only on conflicts)
- Population-health risk stratification feeding care-management workflows
- Clinical-research evidence pipeline (StudyML + adverse-event detection + FDA reporting)
- Continuous-improvement program tied to QA dashboards + value-based-care contracts

### Wave-3 KPI commitments (typical)

- SEP-1 compliance: > 90% sustained hospital-wide
- LOS: -1.0 day hospital-wide
- First-pass denial rate: -35%
- 30-day readmission: -4pp sustained
- Adverse-event detection precision: +25pp vs. prior pharmacovigilance baseline

---

## Cross-references

- Sprint 14 per-workload-isolation capacity blueprint
- Sprint 15 adapters (epic-clarity, hl7-fhir, workday-hcm, servicenow)
- Sprint 16 HLS anchor agents (10 anchors)
- Sprint 17 HLS service catalog (HLS-E2E + HLS-PAY + HLS-LS)
- Sprint 18 reference deployment: `hospital`
- Sellers Guide §10.9–§10.11
