# 04 — Medallion (Mobility Channel)

## Bronze landings

| Bronze table | Source systems | Classification |
|---|---|---|
| `bronze.tmt_mob.oem_telematics` | `toyota-connected`, `ford-sync`, `gm-onstar`, `tesla`, `hondalink`, `bluelink`, `uconnect` | pii + cpni |
| `bronze.tmt_mob.nhtsa_recall` | `nhtsa-api` | internal |
| `bronze.tmt_mob.oem_recall` | each OEM recall feed | pii (when matched to VIN) |
| `bronze.tmt_mob.dealer_dms` | dealer-DMS partner feeds | pii |
| `bronze.tmt_mob.tfs_contracts` | `toyota-financial-services` | cpni |
| `bronze.tmt_mob.tims_policies` | `toyota-insurance-mgmt-solutions` | cpni |
| `bronze.tmt_mob.ford_credit` | `ford-credit` | cpni |
| `bronze.tmt_mob.gm_financial` | `gm-financial` | cpni |
| `bronze.tmt_mob.charging_session` | already in HOM-07 Bronze | internal |

## Silver entities

Under `packages/apex-tmtcml/entities/mobility/`:
- `Vehicle`, `VehicleRecall`, `DealerAppointment`, `AutoLoanLease`, `AutoPolicy`, `TelematicsSnapshot`, `OTASoftwareUpdate`

## Anchor measures

```python
RECALL_OUTSTANDING_COUNT = MeasureDefinition(
    name="open_recall_count_household",
    kind=MeasureKind.PRE_MEASURE,
    description="Number of open recalls across household fleet",
    consumer_map=["tmt-mob-dealer-agent"],
)

NEXT_VEHICLE_TRIGGER_SCORE = MeasureDefinition(
    name="next_vehicle_trigger_score",
    kind=MeasureKind.PRE_MEASURE,
    description="Composite: lease-end-distance + mileage-curve + repair-cost-trend + family-size-change",
    consumer_map=["tmt-mob-next-vehicle-agent"],
)

UBI_PREMIUM_SAVINGS = MeasureDefinition(
    name="ubi_premium_savings_pct",
    kind=MeasureKind.POST_MEASURE,
    description="% savings on auto-insurance premium attributable to UBI score",
    consumer_map=["tmt-mob-finance-agent"],
)
```

## Gold views

- `gold.v_tmt_mob_household_fleet_360`
- `gold.v_tmt_mob_open_recalls`
- `gold.v_tmt_mob_service_due`
- `gold.v_tmt_mob_lease_end_horizon`
- `gold.v_tmt_mob_insurance_renewal_horizon`
