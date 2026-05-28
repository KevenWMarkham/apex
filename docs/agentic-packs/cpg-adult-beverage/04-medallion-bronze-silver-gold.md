# 04 — Medallion (Beverage Channel)

## Bronze landings

| Bronze table | Source | Classification |
|---|---|---|
| `bronze.tmt_bev.sazerac_allocation` | `sazerac-allocation-api` | pii |
| `bronze.tmt_bev.sazerac_standard` | `sazerac` | pii |
| `bronze.tmt_bev.diageo` | `diageo` | pii |
| `bronze.tmt_bev.pernod_ricard` | `pernod-ricard` | pii |
| `bronze.tmt_bev.brown_forman` | `brown-forman` | pii |
| `bronze.tmt_bev.constellation` | `constellation-brands` | pii |
| `bronze.tmt_bev.retailer_inventory` | `total-wine`, `bevmo`, `binnys`, etc. | pii |
| `bronze.tmt_bev.age_verification` | `veratad`, `bluecheck`, `agechecker` | cpni |
| `bronze.tmt_bev.state_rules` | `state-alcohol-control-boards` | internal |
| `bronze.tmt_bev.tasting_events` | distillery + venue feeds | pii |

## Silver entities

Under `packages/apex-tmtcml/entities/beverage/`:
- `BeverageOrder`, `AllocationAlert`, `AgeVerification`, `CellarItem`, `TastingEvent`, `TastingBooking`

## Anchor measures

```python
ALLOCATION_HIT_RATE = MeasureDefinition(
    name="allocation_hit_rate_pct",
    kind=MeasureKind.PRE_MEASURE,
    description="% of allocation alerts that result in customer conversion",
    consumer_map=["tmt-bev-allocation-agent"],
)

CELLAR_VALUE_USD = MeasureDefinition(
    name="cellar_value_usd_estimated",
    kind=MeasureKind.POST_MEASURE,
    description="Estimated retail value of household cellar inventory",
    consumer_map=["tmt-bev-replenishment-agent","customer-portal"],
)

STATE_ELIGIBILITY = MeasureDefinition(
    name="state_eligibility_flag",
    kind=MeasureKind.PRE_MEASURE,
    description="Binary: household can legally receive this SKU via this fulfillment path",
    consumer_map=["tmt-bev-replenishment-agent","tmt-bev-allocation-agent"],
)
```

## Gold views

- `gold.v_tmt_bev_household_cellar`
- `gold.v_tmt_bev_active_alerts`
- `gold.v_tmt_bev_state_eligibility`
- `gold.v_tmt_bev_upcoming_tastings`
