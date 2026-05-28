# APEX-TMT · Agentic Home — Build-Spec Amendment

**Amendment number:** TMT-AMD-001
**Amended document:** `docs/build-specs/apex-tmt-build-spec.md`
**Status:** Draft
**Author:** tmt-practice-lead@deloitte.com
**Date:** Draft

---

## 0. Why this amendment exists

The base TMT build-spec covers Telecom (TMT-TEL), Media (TMT-MED), and Technology (TMT-TEC) sub-variants tuned to the existing CSP / streamer / SaaS-platform persona set. This amendment introduces a **new consumer-facing service-code family — `TMT-TEL-HOM-*`** — for the Telco Home Agentic offering: orchestrated in-home services delivered on top of the Telco's gateway/ONT, a customer-owned data vault, and a subscribable agent marketplace.

The pack narrative lives in [`docs/agentic-packs/telco/`](../agentic-packs/telco/). This amendment is the **formal spec change** that registers the new service codes, Bronze landings, Silver entities, Gold views, agents, and scenario folders into the TMT Edition.

## 1. New service-code family — `TMT-TEL-HOM-*`

| Service code | Description | Headline KPI | Scenario folder | Agent YAML |
|---|---|---|---|---|
| `TMT-TEL-HOM-01` | Home grocery replenishment | Grocery time saved per HH | `TMT-CX-21-home-grocery-replenishment` | `tmt/12-home-grocery-replenishment.yaml` |
| `TMT-TEL-HOM-02` | Home energy optimizer | $/mo energy saved | `TMT-CX-22-home-energy-optimizer` | `tmt/13-home-energy-optimizer.yaml` |
| `TMT-TEL-HOM-03` | Home eldercare monitor | False-positive rate | `TMT-CX-23-home-eldercare-monitor` | `tmt/14-home-eldercare-monitor.yaml` |
| `TMT-TEL-HOM-04` | Home maintenance orchestrator | Repair-avoidance $ | `TMT-CX-24-home-maintenance-orchestrator` | `tmt/15-home-maintenance-orchestrator.yaml` |
| `TMT-TEL-HOM-05` | Home security & presence | False-alarm reduction | `TMT-CX-25-home-security-presence` | `tmt/16-home-security-presence.yaml` |
| `TMT-TEL-HOM-06` | Home wellness coach | Adherence rate | `TMT-CX-26-home-wellness-coach` | `tmt/17-home-wellness-coach.yaml` |
| `TMT-TEL-HOM-07` | Home vehicle readiness | Avoided downtime | `TMT-CX-27-home-vehicle-readiness` | `tmt/18-home-vehicle-readiness.yaml` |
| `TMT-TEL-HOM-08` | Home entertainment concierge | Engagement minutes | `TMT-CX-28-home-entertainment-concierge` | `tmt/19-home-entertainment-concierge.yaml` |
| `TMT-TEL-HOM-99` | Home orchestrator (meta-agent) | Successful intent rate | `TMT-CX-29-home-orchestrator` | `tmt/11-home-orchestrator.yaml` |

Service codes follow the base TMT convention `TMT-<SUBVARIANT>-<DOMAIN>-<NN>`. The new `HOM` domain registers under `TMT-TEL` because the Telco's gateway/ONT is the anchor asset.

## 2. New Bronze landings

The amendment registers the following Bronze tables under `apex-tmt/data/schemas.manifest.json`. All conform to the Core v1.2 envelope contract and `BronzeLandingConfig`.

| Bronze table | `source_system` | `source_pattern` | classification |
|---|---|---|---|
| `bronze.tmt_hom.gateway_telemetry` | `telco-ont` | `eventstream` | `internal` |
| `bronze.tmt_hom.device_registry` | `matter-hub` | `custom_endpoint` | `internal` |
| `bronze.tmt_hom.appliance_events` | `samsung-smartthings`, `lg-thinq`, `whirlpool-6sense` | `eventstream` | `pii` |
| `bronze.tmt_hom.energy_meter` | `ami-meter`, `tesla-powerwall`, `enphase` | `dataflow_gen2` | `internal` |
| `bronze.tmt_hom.climate` | `nest`, `ecobee`, `honeywell-resideo` | `eventstream` | `internal` |
| `bronze.tmt_hom.security` | `ring`, `nest-cam`, `vivint`, `simplisafe` | `eventstream` | `pii` |
| `bronze.tmt_hom.wearable_health` | `apple-health`, `fitbit`, `oura`, `dexcom` | `mirrored_database` | `phi` |
| `bronze.tmt_hom.entertainment` | `roku`, `lg-webos`, `sonos` | `eventstream` | `internal` |
| `bronze.tmt_hom.vehicle_telematics` | `tesla`, `ford-sync`, `gm-onstar` | `custom_endpoint` | `pii` |
| `bronze.tmt_hom.purchase_history` | `kroger`, `instacart`, `amazon` | `mirrored_database` | `pii` |
| `bronze.tmt_hom.vendor_oauth` | `apex-identity` | `custom_endpoint` | `cpni` |

See [`../agentic-packs/telco/04-medallion-bronze-silver-gold.md`](../agentic-packs/telco/04-medallion-bronze-silver-gold.md) for full Bronze schemas.

## 3. New Silver entity package

A new entity package is introduced: `packages/apex-tmtcml/`, mirroring the shape of `packages/apex-hlscml/`. It provides the canonical Pydantic models for the Home Agentic service line.

### Reference entities (SCD2)

- `Household` (CPNI)
- `Person` (PII)
- `Device`
- `DeviceCapability`
- `ConsentGrant`

### Event entities (append-only)

- `EnergyReading`
- `ClimateReading`
- `HealthMetric` (PHI)
- `InventoryReading`
- `PresenceEvent` (PII)
- `VehicleEvent` (PII)
- `PurchaseEvent` (PII)
- `MediaSessionEvent`
- `VendorIntegration` (CPNI, tokenised)

All classified fields are tokenised at Silver via `apex_medallion.silver.transform.tokenise_and_stamp`. Raw values never leave Bronze.

## 4. New Gold views and measures

### Views (registered in `apex-tmt/data/schemas.manifest.json`)

- `gold.v_tmt_hom_household_360`
- `gold.v_tmt_hom_pantry_state`
- `gold.v_tmt_hom_energy_household_hourly`
- `gold.v_tmt_hom_wellness_person_daily` (PHI, RLS-enforced)
- `gold.v_tmt_hom_subscriber_engagement`

### Anchor measures (registered in `MeasureRegistry`)

| Measure | Kind | Language | Consumed by |
|---|---|---|---|
| `pantry_days_remaining` | Pre | PySpark | `tmt-hom-grocery-agent` |
| `energy_cost_forecast_30d_usd` | Pre | PySpark | `tmt-hom-energy-agent` |
| `home_presence_state` | Pre | PySpark | `tmt-hom-security-agent`, `tmt-hom-energy-agent` |
| `elder_adl_deviation_score` | Pre | PySpark (PHI) | `tmt-hom-eldercare-agent` |
| `kwh_rolling_24h` | Post | T-SQL | `tmt-hom-energy-agent`, customer portal |
| `home_agentic_churn_propensity` | Post | DAX | `tmt-hom-retention-agent` |

## 5. New agents (catalog YAMLs)

All nine YAMLs land under `packages/apex-agents/src/apex_agents/catalogs/tmt/` and conform to the Core agent contract.

```
tmt/
├── 11-home-orchestrator.yaml              # TMT-TEL-HOM-99
├── 12-home-grocery-replenishment.yaml     # TMT-TEL-HOM-01
├── 13-home-energy-optimizer.yaml          # TMT-TEL-HOM-02
├── 14-home-eldercare-monitor.yaml         # TMT-TEL-HOM-03
├── 15-home-maintenance-orchestrator.yaml  # TMT-TEL-HOM-04
├── 16-home-security-presence.yaml         # TMT-TEL-HOM-05
├── 17-home-wellness-coach.yaml            # TMT-TEL-HOM-06
├── 18-home-vehicle-readiness.yaml         # TMT-TEL-HOM-07
└── 19-home-entertainment-concierge.yaml   # TMT-TEL-HOM-08
```

## 6. New scenario folders

Nine new folders under `docs/scenarios/TMT/customer-experience/`, IDs `TMT-CX-21` through `TMT-CX-29`. Each folder follows the existing TMT-CX convention (`README.md`, `manifests/`, `artifacts/`, `tests/`).

## 7. Edition-level compliance additions

This amendment introduces additional compliance constraints layered on top of the base TMT compliance set (content rights, network identity, developer data):

1. **Vault residency.** Every `bronze.tmt_hom.*` table containing `PII` / `PHI` / `CPNI` fields must support per-household partitioning compatible with object-store-tier export to the customer's vault bucket. Cold-archive tiering must be **per-household-addressable**.
2. **Consent-bound reads.** Silver and Gold projections derived from `phi` / `cpni` Bronze tables must enforce `ConsentGrant.scope` and `ConsentGrant.purpose` at the agent-run boundary. No agent run may read a projection if the consent for the requesting agent's `purpose` is revoked.
3. **Customer-key encryption.** All vault buckets are encrypted with a **customer-held KMS key**. The Telco runtime obtains read access only via short-lived, per-agent-run signed tokens that the customer may revoke at any time.
4. **Open MCP interface contract.** The orchestrator and all sub-agents communicate over MCP. Third-party agents may list against the household vault under the same consent-grant contract as Telco-native agents.
5. **Lossless vault export.** The Telco must publish a documented export format that allows a household to rebuild full agentic state in an alternative runtime. See [`../agentic-packs/telco/09-portability-open-home.md`](../agentic-packs/telco/09-portability-open-home.md) §3.

## 8. Operational impact

| Area | Change |
|---|---|
| Schema manifest | 11 new Bronze tables, 14 new Silver entities, 5 new Gold views — all registered for `apex-validate.js` |
| Entity package | New `packages/apex-tmtcml/` package |
| Agent catalog | 9 new YAMLs under `packages/apex-agents/.../tmt/` |
| Scenarios | 9 new folders under `docs/scenarios/TMT/customer-experience/` |
| Design system | No new accent token; uses existing `--tmt-accent: #8b5cf6` |
| HITL gates | 5 new HITL gate definitions (grocery order, clinician escalation, third-party access, telehealth booking, vehicle service appointment) |

## 9. Build order (recommended)

1. Land this amendment to capture intent.
2. Stand up `packages/apex-tmtcml/` and the Silver Pydantic models.
3. Register the new measures in `packages/apex-medallion/src/apex_medallion/gold/tmt_hom_measures.py`.
4. Land the 9 agent YAMLs.
5. Update the TMT manifest (`apex-tmt/data/schemas.manifest.json` or equivalent) so `apex-validate.js` picks up the new tables / views.
6. Populate the scenario folders with manifests as the demo data lands.

## 10. References

- Pack narrative: [`../agentic-packs/telco/`](../agentic-packs/telco/)
- Parent build-spec: [`./apex-tmt-build-spec.md`](./apex-tmt-build-spec.md)
- Core spec: [`./apex-core-build-spec.md`](./apex-core-build-spec.md)
- Core amendment registry: [`./apex-core-v1.2-amendment.md`](./apex-core-v1.2-amendment.md)
