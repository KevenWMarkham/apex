# 04 — Medallion: Bronze, Silver, Gold (Automobile Channel)

> APEX-conformant build for the `TMT-TEL-AUT-*` service line. Reuses common patterns from mobility-auto where applicable; introduces new entities for lifecycle, transaction, and aftermarket layers.

## 1. New Bronze landings

| Bronze table | source_system | pattern | classification |
|---|---|---|---|
| `bronze.tmt_aut.kbb_listings` | `kbb`, `autotrader`, `edmunds`, `cargurus`, `truecar` | `mirrored_database` | pii |
| `bronze.tmt_aut.autonation_inventory` | `autonation` | `eventstream` | pii |
| `bronze.tmt_aut.dealer_direct_inventory` | per-dealer-group feeds | `eventstream` | pii |
| `bronze.tmt_aut.carmax_carvana_inventory` | `carmax`, `carvana` | `mirrored_database` | pii |
| `bronze.tmt_aut.financing_applications` | `capital-one-auto`, `ally-auto`, `chase-auto`, `usaa-auto`, `autonation-finance` | `mirrored_database` | cpni |
| `bronze.tmt_aut.insurance_quotes` | `progressive`, `state-farm`, `geico`, `allstate`, `usaa`, `root`, `lemonade-car` | `mirrored_database` | pii + cpni |
| `bronze.tmt_aut.aftermarket_orders` | `autozone`, `advance-auto`, `oreilly`, `napa`, `rockauto` | `mirrored_database` | pii |
| `bronze.tmt_aut.charging_sessions` | `chargepoint`, `evgo`, `electrify-america`, `tesla-supercharger` | `eventstream` | pii |
| `bronze.tmt_aut.fuel_transactions` | `shell`, `chevron`, `bp`, `exxonmobil`, `costco-gas`, `gasbuddy` | `mirrored_database` | pii |
| `bronze.tmt_aut.kbb_valuations` | `kbb`, `manheim`, `vauto` | `mirrored_database` | pii |
| `bronze.tmt_aut.dmv_status` | per-state DMV feeds, `vitu` | `custom_endpoint` | pii + cpni |
| `bronze.tmt_aut.fleet_mileage_logs` | telematics-derived | `eventstream` | pii |
| `bronze.tmt_aut.resale_listings` | `carmax-icoffer`, `carvana-offer`, `peddle`, `kbb-instant-cash-offer` | `mirrored_database` | pii |

## 2. New Silver entities (`apex-tmtcml/entities/automobile/`)

- `VehicleListing` (PII)
- `PurchaseOffer` (PII)
- `FinancingApplication` (CPNI)
- `InsuranceQuote` (PII + CPNI)
- `AftermarketOrder` (PII)
- `ChargingSession` (PII)
- `FuelTransaction` (PII)
- `FleetAssignment` (PII)
- `ResaleListing` (PII)
- `VehicleLifecycleEvent` (PII, audit)
- Extensions to existing `Vehicle` entity for `lifecycle_state` + `lifecycle_state_since`

## 3. Anchor measures

```python
SHORTLIST_PRICE_DELTA = MeasureDefinition(
    name="shortlist_price_delta_usd",
    kind=MeasureKind.PRE_MEASURE,
    description="Difference between highest and lowest price across the household's shortlisted listings (decision support)",
    consumer_map=["tmt-aut-discovery-agent","tmt-aut-purchase-agent"],
)

FINANCING_APR_BEST = MeasureDefinition(
    name="financing_apr_best_offer",
    kind=MeasureKind.PRE_MEASURE,
    description="Lowest APR across active pre-approval offers for the household",
    classification=Classification.CPNI,
    consumer_map=["tmt-aut-financing-agent","tmt-aut-purchase-agent"],
)

INSURANCE_PREMIUM_SAVINGS = MeasureDefinition(
    name="insurance_premium_savings_annual_usd",
    kind=MeasureKind.PRE_MEASURE,
    description="Annual premium savings if customer switches from current carrier to best quote",
    consumer_map=["tmt-aut-insurance-agent"],
)

FUEL_COST_OPTIMIZATION = MeasureDefinition(
    name="fuel_cost_optimization_annual_usd",
    kind=MeasureKind.PRE_MEASURE,
    description="Annual savings from routing fueling to lowest-cost station within practical range",
    consumer_map=["tmt-aut-fueling-agent"],
)

REPAIR_COST_TREND_6M = MeasureDefinition(
    name="repair_cost_trend_6m_usd_per_month",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.TSQL,
    description="Trailing 6-month repair-cost-per-month — drives replacement signal",
    formula=(
        "AVG(cost_usd) OVER (PARTITION BY vehicle_id "
        "ORDER BY service_completed_at "
        "RANGE BETWEEN INTERVAL '6 months' PRECEDING AND CURRENT ROW)"
    ),
    consumer_map=["tmt-aut-discovery-agent","tmt-aut-resale-agent"],
)

RESALE_VALUE_DEPRECIATION = MeasureDefinition(
    name="resale_value_depreciation_pct_per_year",
    kind=MeasureKind.POST_MEASURE,
    description="Year-over-year % depreciation in vehicle valuation",
    consumer_map=["tmt-aut-resale-agent"],
)
```

## 4. Gold views

- `gold.v_tmt_aut_household_vehicle_portfolio`
- `gold.v_tmt_aut_shortlist_comparison`
- `gold.v_tmt_aut_financing_offer_table`
- `gold.v_tmt_aut_insurance_quote_table`
- `gold.v_tmt_aut_fueling_cost_optimization`
- `gold.v_tmt_aut_resale_value_track`
- `gold.v_tmt_aut_fleet_mileage_log`

## 5. End-to-end flow — purchase orchestration

```
Household intent: "we should look at replacing the Highlander"
   ↓ Bronze:   bronze.tmt_aut.kbb_listings + bronze.tmt_aut.autonation_inventory
   ↓ Silver:   VehicleListing entries (shortlisted) + repair-cost-trend from mobility-auto
   ↓ Gold:     v_tmt_aut_shortlist_comparison + v_tmt_aut_resale_value_track
   ↓ Agent:    apex.tmt.agents.vehicle-discovery (composes shortlist)
              → routes to AUT-03 financing pre-approval
              → routes to AUT-04 insurance quote shopping
              → routes to AUT-02 purchase (dealer negotiation)
              → routes to AUT-08 resale (trade-in)
   ↓ Actions:  Capital One Auto pre-approval submitted
              Progressive Snapshot UBI quote with household telematics discount
              AutoNation reservation placed on target vehicle
              CarMax Instant Cash Offer for trade-in
              DMV pre-fill via Vitu
   ↓ HITL gates:  Purchase price > $15K above MSRP, financing total > $50K, insurance premium > $300/mo all gate
   ↓ Audit:    agent_run + agent_action + view_definition_sha
```

## 6. Cross-references with other Channels

- HOM-07 (Home) — vehicle telematics; Automobile reads for discovery + insurance signals
- MOB-02 (Mobility) — dealer service; coordinates on warranty boundary
- RTL-03 (Retail) — Walmart Auto Care for routine maintenance (out of warranty)
- HOM-15 (Travel) — rideshare during trade-in handover
- BEV-03 (CPG / Cocktail Concierge) — irrelevant; this is the most cross-Channel-isolated pack

## 7. Build order

1. Stand up `packages/apex-tmtcml/entities/automobile/`
2. Register measures in `tmt_aut_measures.py`
3. Land the 8 agent YAMLs (`tmt/40..47`)
4. Update schema manifest for `apex-validate.js`
