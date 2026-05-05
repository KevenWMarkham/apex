# TMT (Telecom, Media, Technology) — Wave 1 / 2 / 3 Playbook

**Practice anchor:** Tier-1 telecom carrier, media network, ad-tech platform, B2B SaaS
**Sellers Guide:** §13.9–§13.11

---

## Wave 1 — Envision & Land (8-12 weeks, $0.75-1.5M fixed-fee)

**Objective.** Stand up F128 Fabric with subscriber/network/content workload separation,
light up customer-care + IVT detection or churn-risk in HITL, prove privacy + content-safety
audit posture.

### Deliverables

- F128 Fabric capacity per Sprint 14 single-tenant or per-workload-isolation
- BSS adapter (Amdocs / NetCracker / Salesforce) + ITSM (ServiceNow) + content-platform adapter (where applicable)
- BSSML + SubscriberML + NetworkML + ContentSafetyML schemas in Silver
- Customer-care AHT-reduction agent live in HITL for top contact center
- Churn-risk agent in HOTL with marketing trigger
- IVT (invalid-traffic) detection agent live for ad-tech / content clients
- Content-safety review queue (where applicable) in HITL
- PII + payment-card classifications + DLP applied per Sprint 13
- Sellers Guide §13.9 demo deck + Chief Customer Officer / CMO / Network VP readout

### Anchor agents for Wave-1 light-up

| Agent | When to choose | Sprint 16 ref |
|-------|----------------|---------------|
| Customer-care AHT | High AHT + FCR shortfall | `apex.tmt.agents.contact-center-copilot` |
| Churn risk | Subscriber churn climbing | `apex.tmt.agents.churn-risk` |
| IVT detection | Ad-spend leakage to invalid traffic | `apex.tmt.agents.ivt-detection` |
| Content safety | Trust-and-safety review backlog | `apex.tmt.agents.content-safety` |
| Network ops | DORA / network reliability metrics | `apex.tmt.agents.network-ops` |

### Exit criteria

- AHT median reduction ≥ 8% in pilot contact center queue
- Churn-risk model PR-AUC ≥ 0.70 on pilot cohort
- IVT-detection precision ≥ 85% on pilot traffic slice
- Content-safety review throughput ≥ 1.5x baseline
- Wave-2 commercial proposal signed

---

## Wave 2 — Enable & Scale (8-12 months, $3-6M fixed-fee + value-share on IVT recovery)

**Objective.** Carrier-wide rollout, advanced subscriber-360, value-share on IVT
recovery and churn-save attribution.

### Deliverables

- Carrier-wide customer-care copilot across all queues
- Subscriber-360 with cross-channel orchestration (mobile, web, retail)
- Churn-risk model in production HOTL with automated save-offer triggering
- IVT-detection across all monetization surfaces with settlement-quality reporting
- Network-ops digest reaching all NOC tier-1 / tier-2 leads
- DevOps copilot (DORA-metrics-aware) for engineering team uplift

### Wave-2 KPI commitments (typical)

- AHT (handle time): -12-18%
- FCR: +5-8pp
- Churn rate: -1-2pp on at-risk segment
- IVT rate (where applicable): -25-40%
- Content-safety review throughput: +2x

### Exit criteria

- All Wave-2 KPI commitments measurably met
- IVT-recovery value-share producing attributable money KPI delta
- Wave-3 retainer proposal signed

---

## Wave 3 — Sustain & Transform (24+ months, retainer + outcome-share)

**Objective.** Multi-region carrier deployment, autonomous-tier routine customer
care, network-ops self-healing pattern.

### Deliverables

- Multi-region deployment with cross-region coordination
- Autonomous-tier services for:
  - Routine customer-care (HITL only on retention escalations)
  - Routine churn-save offers (HITL only on high-value tiers)
  - Routine IVT triage (HITL only on novel attack patterns)
- Network-ops self-healing for routine alarm resolution
- DevOps copilot in mainline engineering workflow

### Wave-3 KPI commitments (typical)

- AHT: -25% sustained
- FCR: 80%+ sustained
- Churn: -2-3pp sustained on full base
- IVT rate: -50% sustained
- DORA metrics: top-quartile across deploy frequency, lead time, MTTR, change-fail rate

---

## Cross-references

- Sprint 14 capacity blueprints (single-tenant or per-workload-isolation)
- Sprint 15 adapters (BSS family, ServiceNow, content platforms)
- Sprint 16 TMT anchor agents (10 anchors)
- Sprint 17 TMT service catalog (TMT-Care + TMT-Net + TMT-Content)
- Sellers Guide §13.9–§13.11
