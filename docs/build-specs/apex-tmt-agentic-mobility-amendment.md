# APEX-TMT · Agentic Mobility (Toyota) — Build-Spec Amendment

**Amendment number:** TMT-AMD-004
**Amended document:** `docs/build-specs/apex-tmt-build-spec.md`
**Prior amendments:** TMT-AMD-001 (Home), TMT-AMD-002 (Travel), TMT-AMD-003 (Retail)
**Status:** Draft

## 0. Why this amendment exists

Introduces the **Toyota Connected Channel** as Channel 4 of the marketplace. Adds the `TMT-TEL-MOB-*` service-code family for multi-OEM household-fleet mobility orchestration. Toyota-anchored (Toyota Connected Services + Toyota Financial Services + Toyota Insurance Management Solutions + dealer network); Ford, GM, Tesla, Honda, Hyundai, Stellantis bench.

Pack narrative: [`../agentic-packs/mobility-auto/`](../agentic-packs/mobility-auto/)

## 1. New service codes

| Service | Description |
|---|---|
| `TMT-TEL-MOB-01` | Multi-OEM connected vehicle (extends HOM-07) |
| `TMT-TEL-MOB-02` | Dealer service + recall coordination + OTA software updates |
| `TMT-TEL-MOB-03` | Next-vehicle decisioning + trade-in + configurator |
| `TMT-TEL-MOB-04` | TFS lease / loan / refi + TIMS UBI insurance |

## 2. New Bronze landings under `bronze.tmt_mob.*`

`oem_telematics`, `nhtsa_recall`, `oem_recall`, `dealer_dms`, `tfs_contracts`, `tims_policies`, `ford_credit`, `gm_financial`, `charging_session`.

## 3. New Silver entities (`apex-tmtcml/entities/mobility/`)

`Vehicle`, `VehicleRecall`, `DealerAppointment`, `AutoLoanLease`, `AutoPolicy`, `TelematicsSnapshot`, `OTASoftwareUpdate`.

## 4. New Gold views

`household_fleet_360`, `open_recalls`, `service_due`, `lease_end_horizon`, `insurance_renewal_horizon`.

## 5. New agent YAMLs

`tmt/32-toyota-connected.yaml`, `33-toyota-dealer.yaml`, `34-toyota-next-vehicle.yaml`, `35-toyota-finance.yaml`.

## 6. Scenarios

`TMT-CX-42-toyota-connected-plus`, `43-toyota-dealer-network`, `44-toyota-next-vehicle`, `45-toyota-finance-insurance`.

## 7. Edition-level compliance additions

1. **Embedded-SIM CPNI handling.** Each connected vehicle is treated as a CPNI-classified data source; vehicle-identity tokens treated identically to subscriber-identity tokens.
2. **TFS financial-data tokenization.** Account numbers, payment-history identifiers, lease-end balloon amounts all stored as `cpni`-classified tokens.
3. **UBI consent + state-level rules.** TIMS UBI participation requires per-state consent disclosure; some states (CA, MA) materially restrict UBI usage.
4. **Recall-completion liability.** Pack must clearly delineate "notified" vs "completed" — OEM remains the legally responsible party for recall remediation.

## 8. Operational impact

| Area | Change |
|---|---|
| Schema manifest | 9 new Bronze tables, 7 new Silver entities, 5 new Gold views |
| Agent catalog | 4 new YAMLs |
| Scenarios | 4 new folders |
| HITL gates | 4 new gate definitions |

## 9. Cross-references

- Pack: [`../agentic-packs/mobility-auto/`](../agentic-packs/mobility-auto/)
- Sibling AXLE Edition: [`./apex-axle-build-spec.md`](./apex-axle-build-spec.md) (if extended) — TMT-MOB is consumer-side; AXLE is enterprise-side
- Marketplace: [`../agentic-packs/_marketplace/`](../agentic-packs/_marketplace/)
