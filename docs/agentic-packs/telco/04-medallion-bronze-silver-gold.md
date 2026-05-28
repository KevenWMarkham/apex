# 04 — Medallion: Bronze, Silver, Gold

> APEX-conformant build-out for the `TMT-TEL-HOM-*` service line. Every Bronze landing follows the APEX envelope contract; Silver entities are Pydantic with SCD2 + tokenization hooks; Gold is T-SQL virtual views with `MeasureDefinition` pre- and post-measures.

## 1. Bronze — source registry

Each device family lands in one Bronze table that conforms to `BronzeLandingConfig` and emits the canonical envelope (`event_id`, `event_ts`, `entity_id`, `source_system`, `source_system_ts`, `ingest_ts`, `ingest_date`, `run_id`, `_raw_payload`, `_classification`).

| Bronze table | `source_system` | `source_pattern` | classification | partition columns | Feeds Silver entity |
|---|---|---|---|---|---|
| `bronze.tmt_hom.gateway_telemetry` | `telco-ont` | `eventstream` | `internal` | `ingest_date, household_id` | `HomeGateway` |
| `bronze.tmt_hom.device_registry` | `matter-hub` | `custom_endpoint` | `internal` | `ingest_date` | `Device, DeviceCapability` |
| `bronze.tmt_hom.appliance_events` | `samsung-smartthings`, `lg-thinq`, `whirlpool-6sense` | `eventstream` | `pii` | `ingest_date, household_id` | `ApplianceEvent, InventoryReading` |
| `bronze.tmt_hom.energy_meter` | `ami-meter`, `tesla-powerwall`, `enphase` | `dataflow_gen2` | `internal` | `ingest_date, household_id` | `EnergyReading` |
| `bronze.tmt_hom.climate` | `nest`, `ecobee`, `honeywell-resideo` | `eventstream` | `internal` | `ingest_date, household_id` | `ClimateReading` |
| `bronze.tmt_hom.security` | `ring`, `nest-cam`, `vivint`, `simplisafe` | `eventstream` | `pii` | `ingest_date, household_id` | `PresenceEvent, SecurityEvent` |
| `bronze.tmt_hom.wearable_health` | `apple-health`, `fitbit`, `oura`, `dexcom` | `mirrored_database` | `phi` | `ingest_date, person_id` | `HealthMetric` |
| `bronze.tmt_hom.entertainment` | `roku`, `lg-webos`, `sonos` | `eventstream` | `internal` | `ingest_date, household_id` | `MediaSessionEvent` |
| `bronze.tmt_hom.vehicle_telematics` | `tesla`, `ford-sync`, `gm-onstar` | `custom_endpoint` | `pii` | `ingest_date, household_id` | `VehicleEvent` |
| `bronze.tmt_hom.purchase_history` | `kroger`, `instacart`, `amazon` | `mirrored_database` | `pii` | `ingest_date, household_id` | `PurchaseEvent` |
| `bronze.tmt_hom.vendor_oauth` | `apex-identity` | `custom_endpoint` | `cpni` | `ingest_date, household_id` | `VendorIntegration` (tokenised) |

All landings conform to `BronzeLandingConfig` and `generate_bronze_ddl(...)` from `apex_medallion.bronze.schema`.

## 2. Silver — canonical Pydantic entities

These slot under a new entity package `packages/apex-tmtcml/entities/home/` (mirrors the shape of `apex-hlscml`). SCD2 fields (`scd2_valid_from`, `scd2_valid_to`, `scd2_is_current`, `row_hash`) inherited where the entity is a reference table; tokenization done via `apex_medallion.silver.transform.tokenise_and_stamp`.

### Reference entities (SCD2)

```python
# packages/apex-tmtcml/src/apex_tmtcml/entities/home/household.py
from datetime import datetime
from pydantic import BaseModel, Field
from apex_core.types import Classification

class Household(BaseModel):
    household_id: str = Field(..., classification=Classification.PII)
    telco_account_id: str = Field(..., classification=Classification.CPNI)
    service_address_hash: str = Field(..., classification=Classification.PII)
    primary_market: str
    plan_tier: str                      # 'fiber-1g','5g-home','triple-play'
    home_agentic_subscribed: bool
    onboarded_at: datetime
    scd2_valid_from: datetime
    scd2_valid_to: datetime | None
    scd2_is_current: bool
    row_hash: str

class Person(BaseModel):
    person_id: str = Field(..., classification=Classification.PII)
    household_id: str
    role: str                           # 'primary','adult','child','dependent'
    consent_bundle_id: str | None

class Device(BaseModel):
    device_id: str
    household_id: str
    category_code: str                  # 'refrigerator','thermostat','wearable','vehicle'
    manufacturer: str
    model_number: str
    protocol: list[str]                 # ['matter','wifi','ble']
    location_label: str | None
    installed_at: datetime
    last_seen_ts: datetime
    health_status: str                  # 'active','offline','degraded'

class DeviceCapability(BaseModel):
    capability_id: str
    device_id: str
    capability_code: str                # 'temp.read','door.state','image.capture','glucose.read'
    unit: str | None
    sample_rate_seconds: int | None
    classification: Classification      # propagates to all data emitted by this capability

class ConsentGrant(BaseModel):
    grant_id: str
    household_id: str
    person_id: str | None
    scope: str                          # 'health','location','purchases','video','energy'
    purpose: str                        # 'grocery-agent','energy-agent','eldercare-agent'
    granted: bool
    granted_at: datetime
    revoked_at: datetime | None
```

### Event entities (append-only, no SCD2)

```python
class EnergyReading(BaseModel):
    event_id: str
    event_ts: datetime
    household_id: str
    device_id: str | None
    kwh: float
    cost_usd: float | None
    tariff_window: str                  # 'peak','off-peak','shoulder'
    _classification: Classification = Classification.INTERNAL

class ClimateReading(BaseModel):
    event_id: str
    event_ts: datetime
    household_id: str
    zone: str
    temp_f: float
    humidity_pct: float
    hvac_state: str                     # 'heat','cool','idle','fan'
    setpoint_f: float

class HealthMetric(BaseModel):
    event_id: str
    event_ts: datetime
    person_id: str
    household_id: str
    metric_code: str                    # 'hr','spo2','glucose','steps','sleep_score'
    value: float
    unit: str
    device_id: str
    _classification: Classification = Classification.PHI

class InventoryReading(BaseModel):
    event_id: str
    event_ts: datetime
    household_id: str
    device_id: str
    product_upc: str | None
    product_name: str | None
    quantity: float | None
    unit: str | None
    expires_on: str | None
    confidence: float

class PresenceEvent(BaseModel):
    event_id: str
    event_ts: datetime
    household_id: str
    person_id: str | None
    presence_state: str                 # 'home','away','sleep'
    source: str                         # 'geofence','door','motion','wearable'
    _classification: Classification = Classification.PII

class VehicleEvent(BaseModel):
    event_id: str
    event_ts: datetime
    household_id: str
    vehicle_id: str
    odometer_km: float
    fuel_or_charge_pct: float
    tpms_warning: bool
    maintenance_due: list[str]
    location_hash: str                  # geohash, not raw lat/lng

class PurchaseEvent(BaseModel):
    event_id: str
    event_ts: datetime
    household_id: str
    vendor_id: str                      # 'kroger','instacart','amazon'
    product_upc: str | None
    quantity: float
    unit_price_usd: float
    total_usd: float

class MediaSessionEvent(BaseModel):
    event_id: str
    event_ts: datetime
    household_id: str
    device_id: str
    person_id: str | None
    content_id: str
    content_type: str                   # 'tv','movie','music','game'
    duration_seconds: int

class VendorIntegration(BaseModel):
    integration_id: str
    household_id: str
    vendor_id: str
    oauth_token_token: str              # tokenised via apex-tokenizer
    refresh_token_token: str
    expires_at: datetime
    scopes: list[str]
    _classification: Classification = Classification.CPNI
```

All classified fields (`PII` / `PHI` / `CPNI`) are tokenised at Silver via `tokenise_and_stamp(...)` — raw values never leave Bronze.

## 3. Gold — virtual views + measures

Two measure layers (matching `MeasureKind`):

1. **Pre-measures** — PySpark, Silver → Gold, embodied as Gold columns
2. **Post-measures** — T-SQL / DAX / KQL, query-time, appended in views

### 3.1 Anchor measures

```python
# packages/apex-medallion/src/apex_medallion/gold/tmt_hom_measures.py

PANTRY_DAYS_REMAINING = MeasureDefinition(
    name="pantry_days_remaining",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="tmt-practice-lead",
    description="Days until product is depleted at trailing 30-day consumption rate.",
    classification=Classification.PII,
    formula=(
        "F.when(F.col('avg_daily_consumption') > 0, "
        "F.col('current_quantity') / F.col('avg_daily_consumption')).otherwise(F.lit(None))"
    ),
    depends_on=["current_quantity", "avg_daily_consumption"],
    consumer_map=["tmt-hom-grocery-agent"],
)

ENERGY_COST_FORECAST_30D = MeasureDefinition(
    name="energy_cost_forecast_30d_usd",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="tmt-practice-lead",
    description="Forward 30-day cost projection using trailing 30-day kWh and posted tariff.",
    formula=(
        "F.col('trailing_30d_kwh') / F.lit(30) * F.lit(30) * F.col('posted_tariff_usd_per_kwh')"
    ),
    depends_on=["trailing_30d_kwh", "posted_tariff_usd_per_kwh"],
    consumer_map=["tmt-hom-energy-agent"],
)

HOME_PRESENCE_STATE = MeasureDefinition(
    name="home_presence_state",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="tmt-practice-lead",
    description="Composite presence: home / away / asleep / mixed.",
    formula=(
        "F.when(F.col('motion_last_15m') == 0, F.lit('away'))"
        ".when(F.col('hour_local').between(0,5), F.lit('asleep')).otherwise(F.lit('home'))"
    ),
    depends_on=["motion_last_15m", "hour_local"],
    consumer_map=["tmt-hom-security-agent","tmt-hom-energy-agent"],
)

ELDER_BASELINE_DEVIATION = MeasureDefinition(
    name="elder_adl_deviation_score",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="tmt-practice-lead",
    description="Z-score of daily activity-of-daily-living signals vs trailing 60-day baseline.",
    classification=Classification.PHI,
    formula=(
        "(F.col('adl_score_today') - F.col('adl_score_60d_mean')) / F.col('adl_score_60d_std')"
    ),
    depends_on=["adl_score_today","adl_score_60d_mean","adl_score_60d_std"],
    consumer_map=["tmt-hom-eldercare-agent"],
)

# Post-measures (query-time)

ROLLING_KWH_24H_TSQL = MeasureDefinition(
    name="kwh_rolling_24h",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.TSQL,
    owner="tmt-practice-lead",
    description="Rolling 24-hour kWh per household.",
    formula=(
        "SUM(kwh) OVER (PARTITION BY household_id "
        "ORDER BY event_ts ROWS BETWEEN 95 PRECEDING AND CURRENT ROW)"
    ),
    depends_on=["kwh","event_ts"],
    consumer_map=["tmt-hom-energy-agent","customer-portal"],
)

CHURN_PROPENSITY_DAX = MeasureDefinition(
    name="home_agentic_churn_propensity",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.DAX,
    owner="tmt-practice-lead",
    description="Composite churn score for Home Agentic subscribers.",
    formula=(
        "VAR _engage = [days_active_30d] / 30 "
        "VAR _value  = [actions_completed_30d] * 1.0 "
        "RETURN 1 - DIVIDE(_engage * _value, [tenure_months])"
    ),
    depends_on=["days_active_30d","actions_completed_30d","tenure_months"],
    consumer_map=["tmt-hom-retention-agent"],
)
```

### 3.2 Gold virtual views (T-SQL)

Generated via `generate_warehouse_view(...)`. Anchor projections:

```sql
-- v_household_360: single-row-per-household reference view
CREATE OR ALTER VIEW gold.v_tmt_hom_household_360 AS
SELECT
  household_id,
  telco_account_id,
  service_address_hash,
  plan_tier,
  home_agentic_subscribed,
  device_count,
  consented_scopes,
  vault_status,
  active_agent_subscriptions,
  _classification
FROM silver.tmt_hom.household_current
;

-- v_pantry_state: per-product inventory with pre-measure
CREATE OR ALTER VIEW gold.v_tmt_hom_pantry_state AS
SELECT
  household_id,
  product_upc,
  product_name,
  current_quantity,
  unit,
  expires_on,
  avg_daily_consumption,
  pantry_days_remaining,            -- pre-measure
  last_observed_ts,
  _classification
FROM silver.tmt_hom.inventory_state
;

-- v_energy_household_hourly: time-series rollup
CREATE OR ALTER VIEW gold.v_tmt_hom_energy_household_hourly AS
SELECT
  household_id,
  event_ts_hour,
  kwh,
  cost_usd,
  tariff_window,
  (SUM(kwh) OVER (PARTITION BY household_id
       ORDER BY event_ts_hour
       ROWS BETWEEN 23 PRECEDING AND CURRENT ROW)) AS kwh_rolling_24h,   -- post-measure
  energy_cost_forecast_30d_usd,                                          -- pre-measure
  _classification
FROM silver.tmt_hom.energy_reading_hourly
;

-- v_wellness_person_daily: PHI-classified view, behind RLS
CREATE OR ALTER VIEW gold.v_tmt_hom_wellness_person_daily AS
SELECT
  person_id,
  household_id,
  event_date,
  resting_hr_avg,
  steps,
  sleep_score,
  glucose_avg_mgdl,
  elder_adl_deviation_score,        -- pre-measure
  _classification
FROM silver.tmt_hom.health_metric_daily
;

-- v_subscriber_engagement: powers retention / churn / billing surfaces
CREATE OR ALTER VIEW gold.v_tmt_hom_subscriber_engagement AS
SELECT
  household_id,
  agent_code,
  days_active_30d,
  actions_proposed_30d,
  actions_completed_30d,
  tenure_months,
  monthly_revenue_usd,
  _classification
FROM silver.tmt_hom.agent_run_rollup
;
```

Every view DDL gets stamped with `view_definition_sha(ddl)` so audit rows can prove which definition produced any tool result.

## 4. End-to-end flow — grocery example

```
Fridge camera + pantry scale + trash scanner
   ↓ Bronze:  bronze.tmt_hom.appliance_events (raw vendor JSON)
   ↓ Silver:  InventoryReading (tokenised) + SCD2 InventoryState
   ↓ Gold:    v_tmt_hom_pantry_state (with pantry_days_remaining)
   ↓ Agent:   apex.tmt.agents.home-grocery-replenishment (HITL gate $150)
   ↓ Action:  apex.tmt.mcp.kroger.submit_order (write tool)
   ↓ Audit:   agent_run + view_definition_sha + tools_called.result_hash
```

The same pipeline shape applies to all eight services — each one binds to a different Gold view and a different write-side tool. See [`diagrams/flow-grocery-end-to-end.md`](./diagrams/flow-grocery-end-to-end.md) for the rendered diagram.

## 5. Build order

1. `packages/apex-tmtcml/` — new entity package mirroring `apex-hlscml` structure, with the Silver Pydantic models above.
2. `packages/apex-medallion/src/apex_medallion/gold/tmt_hom_measures.py` — registers the four anchor pre-measures + post-measures via `MeasureRegistry`.
3. `packages/apex-agents/src/apex_agents/catalogs/tmt/11..19-home-*.yaml` — nine new agent YAMLs (1 orchestrator + 8 sub-agents).
4. `docs/scenarios/TMT/customer-experience/TMT-CX-21..29-home-*` — scenario folders with `README.md`, `manifests/`, `artifacts/` per existing TMT-CX convention.
5. L2 manifest update in the TMT edition (`apex-th/data/schemas.manifest.json` or equivalent) to register the new Silver / Gold tables for `apex-validate.js`.
