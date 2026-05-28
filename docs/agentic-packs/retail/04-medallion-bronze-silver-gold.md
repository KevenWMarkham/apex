# 04 — Medallion: Bronze, Silver, Gold (Walmart Retail Channel)

> APEX-conformant build for the `TMT-TEL-RTL-*` service line. Same envelope, classification, SCD2, and tokenization conventions as the Home and Travel packs.

## 1. New Bronze landings

| Bronze table | source_system | pattern | classification |
|---|---|---|---|
| `bronze.tmt_rtl.walmart_orders` | `walmart` | `mirrored_database` | pii |
| `bronze.tmt_rtl.walmart_rx` | `walmart-pharmacy`, `walmart-health` | `mirrored_database` | phi |
| `bronze.tmt_rtl.walmart_plus` | `walmart-plus` | `mirrored_database` | pii |
| `bronze.tmt_rtl.walmart_tle` | `walmart-auto-care` | `mirrored_database` | pii |
| `bronze.tmt_rtl.walmart_connect` | `walmart-connect` | `eventstream` | pii |
| `bronze.tmt_rtl.target_orders` | `target` | `mirrored_database` | pii |
| `bronze.tmt_rtl.target_circle` | `target-circle` | `mirrored_database` | pii |
| `bronze.tmt_rtl.costco_purchases` | `costco` | `mirrored_database` | pii |
| `bronze.tmt_rtl.sams_club` | `sams-club` | `mirrored_database` | pii |
| `bronze.tmt_rtl.bestbuy` | `bestbuy` | `mirrored_database` | pii |
| `bronze.tmt_rtl.homedepot` | `homedepot` | `mirrored_database` | pii |
| `bronze.tmt_rtl.cpsc_recall` | `cpsc-recall` | `custom_endpoint` | internal |

## 2. New Silver entities

Under `packages/apex-tmtcml/entities/retail/`:

- `RetailOrder`, `RetailOrderLine`
- `Prescription` (PHI)
- `AutoServiceAppointment`
- `MembershipTier`
- `LoyaltyAccount` (extends the travel-pack model with retail-program tiers)
- `ProductPriceHistory` (cross-retailer price tracking)

## 3. New anchor measures

```python
ERRAND_CHAIN_FEASIBILITY = MeasureDefinition(
    name="errand_chain_feasibility_score",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    description="Composite score: # store visits chainable / time-budget / distance",
    consumer_map=["tmt-rtl-merchandise-agent"],
)

PRESCRIPTION_DUE_IN_7D = MeasureDefinition(
    name="prescription_due_in_7d_count",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    classification=Classification.PHI,
    description="Count of active prescriptions with next_due_at within 7 days",
    consumer_map=["tmt-rtl-pharmacy-agent","tmt-hom-eldercare-agent"],
)

MEMBERSHIP_PAYBACK_RATIO = MeasureDefinition(
    name="membership_payback_ratio",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.TSQL,
    description="Ratio of benefits used USD value / annual fee for each membership",
    consumer_map=["tmt-rtl-membership-agent"],
)
```

## 4. New Gold views (anchor projections)

- `gold.v_tmt_rtl_household_retail_360`
- `gold.v_tmt_rtl_prescription_state`
- `gold.v_tmt_rtl_errand_chain_proposal`
- `gold.v_tmt_rtl_membership_payback`
- `gold.v_tmt_rtl_cross_retailer_price_tracker`

## 5. End-to-end flow — errand chain

```
HOM-01 pantry signal + HOM-03 medication-due + HOM-07 oil-change-due + calendar gap
   ↓ Silver:   RetailOrder draft + Prescription refresh + AutoService trigger
   ↓ Gold:     v_tmt_rtl_errand_chain_proposal (chain with ETA + cost estimate)
   ↓ Agent:    apex.tmt.agents.walmart-merchandise (composes the chain)
   ↓ Action:   Walmart Pickup order + Walmart Pharmacy refill + TLE booking + (Target / Home Depot sub-orders if needed)
   ↓ HITL gate: chain total > $200 → mobile_push approval
   ↓ Audit:    agent_run + agent_action + view_definition_sha
```

## 6. Build order

1. Stand up `packages/apex-tmtcml/entities/retail/`
2. Register retail measures in `tmt_rtl_measures.py`
3. Land the 4 agent YAMLs (`tmt/28..31`)
4. Update manifest for `apex-validate.js` to pick up the new tables / views
