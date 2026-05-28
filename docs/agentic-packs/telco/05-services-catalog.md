# 05 — Services Catalog (`TMT-TEL-HOM-*`)

> Nine new service codes — eight subscribable sub-agents plus one meta-orchestrator. Each maps 1:1 to an agent YAML in `packages/apex-agents/src/apex_agents/catalogs/tmt/` and to a scenario folder in `docs/scenarios/TMT/customer-experience/`.

## Service codes

| Service code | Scenario folder | Agent YAML | Description | Headline KPI |
|---|---|---|---|---|
| `TMT-TEL-HOM-01` | `TMT-CX-21-home-grocery-replenishment` | `tmt/12-home-grocery-replenishment.yaml` | Pantry / fridge-driven grocery orchestration | Grocery time saved per HH |
| `TMT-TEL-HOM-02` | `TMT-CX-22-home-energy-optimizer` | `tmt/13-home-energy-optimizer.yaml` | Tariff-aware HVAC + load shifting | $/mo energy saved |
| `TMT-TEL-HOM-03` | `TMT-CX-23-home-eldercare-monitor` | `tmt/14-home-eldercare-monitor.yaml` | ADL deviation alerts to family / clinician | False-positive rate |
| `TMT-TEL-HOM-04` | `TMT-CX-24-home-maintenance-orchestrator` | `tmt/15-home-maintenance-orchestrator.yaml` | Filter, fluid, firmware, recall triage | Repair-avoidance $ |
| `TMT-TEL-HOM-05` | `TMT-CX-25-home-security-presence` | `tmt/16-home-security-presence.yaml` | Presence-aware arming + visitor verification | False-alarm reduction |
| `TMT-TEL-HOM-06` | `TMT-CX-26-home-wellness-coach` | `tmt/17-home-wellness-coach.yaml` | Wearable + sleep + glucose coaching | Adherence rate |
| `TMT-TEL-HOM-07` | `TMT-CX-27-home-vehicle-readiness` | `tmt/18-home-vehicle-readiness.yaml` | EV charge scheduling + maintenance | Avoided downtime |
| `TMT-TEL-HOM-08` | `TMT-CX-28-home-entertainment-concierge` | `tmt/19-home-entertainment-concierge.yaml` | Cross-device watch / listen orchestration | Engagement minutes |
| `TMT-TEL-HOM-99` | `TMT-CX-29-home-orchestrator` | `tmt/11-home-orchestrator.yaml` | Meta-orchestrator routing household intents | Successful intent rate |

## Archetype mapping

| Service code | Archetype | Oversight | Notes |
|---|---|---|---|
| `TMT-TEL-HOM-01` | `F3-predictive-trigger-workflow-aware` | HITL | HITL fires when `cart_total_usd > 150` |
| `TMT-TEL-HOM-02` | `F1-continuous-monitor-hitl-alert` | HOTL | Setpoint changes within user-defined band |
| `TMT-TEL-HOM-03` | `F1-continuous-monitor-hitl-alert` | HITL | Clinician escalation when `elder_adl_deviation_score > 2.5` |
| `TMT-TEL-HOM-04` | `F2-event-cluster-pattern-match` | HOTL | Auto-orders consumables under threshold |
| `TMT-TEL-HOM-05` | `F1-continuous-monitor-hitl-alert` | HITL | All 3rd-party access grants HITL-gated |
| `TMT-TEL-HOM-06` | `F3-predictive-trigger-workflow-aware` | HOTL | PHI-scoped, opt-in only |
| `TMT-TEL-HOM-07` | `F3-predictive-trigger-workflow-aware` | HOTL | Charge scheduling auto-runs; service-booking HITL |
| `TMT-TEL-HOM-08` | `F2-event-cluster-pattern-match` | HOTL | Read-only by default; write only for explicit content adds |
| `TMT-TEL-HOM-99` | `F4-orchestrator-with-subagents` | HOTL | Routes only — writes flow through sub-agents |

## Subscription bundles

Three packaging tiers proposed for the consumer-facing offer:

| Bundle | Included sub-agents | Monthly price (illustrative) |
|---|---|---|
| **Essential** | Orchestrator + Grocery + Energy | $9.99 |
| **Family** | Essential + Eldercare + Maintenance + Security | $19.99 |
| **Premium** | Family + Wellness + Vehicle + Entertainment | $29.99 |

The orchestrator is included free at every tier (it has no value without at least one sub-agent). À-la-carte sub-agent add-ons priced at $4.99 / mo each.

## Action-commerce take-rate envelope

| Service | Typical partner take rate | Notes |
|---|---|---|
| HOM-01 grocery | 4–7% of basket | Subject to grocer-of-choice; loyalty rebates pass through |
| HOM-02 energy | $/kWh-year capacity share | Demand-response aggregator splits MW payment with Telco |
| HOM-03 eldercare | PMPM ($20–80) | Sponsored by MA plan; not user-billed |
| HOM-04 maintenance | 3–6% on service-call dispatch | Plus warranty-co-sell rev-share |
| HOM-05 security | Premium-discount share | Insurance carrier funds the consumer discount |
| HOM-06 wellness | PMPM or per-event escalation fee | Payer / employer sponsored |
| HOM-07 vehicle | Per-charge / per-service fee | Charging network + service network |
| HOM-08 entertainment | Distribution rev-share | Streamer bundles standard 20–40% |

See [`06-partnership-map.md`](./06-partnership-map.md) for partner candidates and [`07-business-value-model.md`](./07-business-value-model.md) for the full unit-economic build.

## Cross-references

- Each service has a 1:1 agent YAML — see [`packages/apex-agents/src/apex_agents/catalogs/tmt/`](../../../packages/apex-agents/src/apex_agents/catalogs/tmt/)
- Each service has a 1:1 scenario folder — see [`docs/scenarios/TMT/customer-experience/`](../../scenarios/TMT/customer-experience/)
- Bronze/Silver/Gold lineage for each service — see [`04-medallion-bronze-silver-gold.md`](./04-medallion-bronze-silver-gold.md)
- The companion build-spec amendment — see [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../build-specs/apex-tmt-agentic-home-amendment.md)
