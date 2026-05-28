# APEX-TMT · Agentic Retail (Walmart) — Build-Spec Amendment

**Amendment number:** TMT-AMD-003
**Amended document:** `docs/build-specs/apex-tmt-build-spec.md`
**Prior amendments:** TMT-AMD-001 (Home), TMT-AMD-002 (Travel)
**Status:** Draft

## 0. Why this amendment exists

Introduces the **Walmart Retail Channel** as Channel 3 of the agentic marketplace. Adds the `TMT-TEL-RTL-*` service-code family for everyday-retail orchestration (general merchandise, pharmacy, auto care, membership-tier optimization). Walmart-anchored; Target / Costco / Sam's Club / Best Buy / Home Depot / Lowes as bench partners.

Pack narrative: [`../agentic-packs/retail/`](../agentic-packs/retail/)
Marketplace meta-pack: [`../agentic-packs/_marketplace/`](../agentic-packs/_marketplace/)

## 1. New service codes — `TMT-TEL-RTL-01..04`

| Service | Description | Headline KPI |
|---|---|---|
| `TMT-TEL-RTL-01` | Multi-retailer GM + errand-chain orchestration | Errand-chain time saved |
| `TMT-TEL-RTL-02` | Pharmacy refills + Walmart Health + OTC reconciliation | Refill on-time rate |
| `TMT-TEL-RTL-03` | Walmart Auto Care (TLE) — oil / tire / battery | Avoided unplanned service |
| `TMT-TEL-RTL-04` | Walmart+ / Costco / Sam's / Prime tier optimization | Net annual savings on memberships |

## 2. New Bronze landings under `bronze.tmt_rtl.*`

`walmart_orders`, `walmart_rx`, `walmart_plus`, `walmart_tle`, `walmart_connect`, `target_orders`, `target_circle`, `costco_purchases`, `sams_club`, `bestbuy`, `homedepot`, `cpsc_recall`.

## 3. New Silver entities (under `apex-tmtcml/entities/retail/`)

`RetailOrder`, `RetailOrderLine`, `Prescription` (PHI), `AutoServiceAppointment`, `MembershipTier`, `ProductPriceHistory`.

## 4. New Gold views

`gold.v_tmt_rtl_household_retail_360`, `prescription_state`, `errand_chain_proposal`, `membership_payback`, `cross_retailer_price_tracker`.

## 5. New agent YAMLs

`tmt/28-walmart-merchandise.yaml`, `tmt/29-walmart-pharmacy.yaml`, `tmt/30-walmart-auto-care.yaml`, `tmt/31-membership-optimizer.yaml`.

## 6. Scenarios

`TMT-CX-38-walmart-merchandise`, `TMT-CX-39-walmart-pharmacy`, `TMT-CX-40-walmart-auto-care`, `TMT-CX-41-membership-optimizer`.

## 7. Edition-level compliance additions

1. **Walmart Health PHI handling.** RTL-02 requires HIPAA-compliant handling of prescription data. Refill / reconciliation actions are logged with PHI-classification stamping; HITL gating mandatory.
2. **Sponsored-placement disclosure.** Walmart Connect-sponsored item suggestions must be visibly labelled in orchestrator UI and logged in `retail_order_line.sponsored=true`.
3. **Cross-retailer data isolation.** Walmart never receives Target / Costco / Best Buy purchase history; orchestrator-internal routing only.

## 8. Operational impact

| Area | Change |
|---|---|
| Schema manifest | 12 new Bronze tables, 6 new Silver entities, 5 new Gold views |
| Agent catalog | 4 new YAMLs |
| Scenarios | 4 new folders |
| HITL gates | 4 new gate definitions |

## 9. Cross-references

- Pack: [`../agentic-packs/retail/`](../agentic-packs/retail/)
- Prior amendments: [`./apex-tmt-agentic-home-amendment.md`](./apex-tmt-agentic-home-amendment.md), [`./apex-tmt-agentic-travel-amendment.md`](./apex-tmt-agentic-travel-amendment.md)
- Marketplace: [`../agentic-packs/_marketplace/`](../agentic-packs/_marketplace/)
