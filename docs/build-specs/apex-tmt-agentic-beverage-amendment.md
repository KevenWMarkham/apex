# APEX-TMT · Agentic Beverage (Sazerac) — Build-Spec Amendment

**Amendment number:** TMT-AMD-005
**Amended document:** `docs/build-specs/apex-tmt-build-spec.md`
**Prior amendments:** TMT-AMD-001..004
**Status:** Draft

## 0. Why this amendment exists

Introduces the **Sazerac House Channel** as Channel 5 of the marketplace. Adds the `TMT-TEL-BEV-*` service-code family for age-gated adult-beverage orchestration — replenishment with state-shipping compliance, allocation alerts (BTAC, Pappy, Eagle Rare 17), cocktail concierge with cross-Channel ingredient routing, distillery-tour and tasting-event bookings. Sazerac-anchored; Diageo, Pernod Ricard, Brown-Forman, Constellation Brands bench.

Pack narrative: [`../agentic-packs/cpg-adult-beverage/`](../agentic-packs/cpg-adult-beverage/)

## 1. New service codes

| Service | Description |
|---|---|
| `TMT-TEL-BEV-01` | Age-verified replenishment + state-shipping compliance |
| `TMT-TEL-BEV-02` | Buffalo Trace / Pappy / Eagle Rare 17 allocation alerts with reserved holds |
| `TMT-TEL-BEV-03` | Cocktail concierge + ingredient orchestration |
| `TMT-TEL-BEV-04` | Distillery tours + tasting events |

## 2. New Bronze landings under `bronze.tmt_bev.*`

`sazerac_allocation`, `sazerac_standard`, `diageo`, `pernod_ricard`, `brown_forman`, `constellation`, `retailer_inventory`, `age_verification`, `state_rules`, `tasting_events`.

## 3. New Silver entities (`apex-tmtcml/entities/beverage/`)

`BeverageOrder`, `AllocationAlert`, `AgeVerification`, `CellarItem`, `TastingEvent`, `TastingBooking`.

## 4. New Gold views

`household_cellar`, `active_alerts`, `state_eligibility`, `upcoming_tastings`.

## 5. New agent YAMLs

`tmt/36-sazerac-replenishment.yaml`, `37-allocation-alerts.yaml`, `38-cocktail-concierge.yaml`, `39-tasting-events.yaml`.

## 6. Scenarios

`TMT-CX-46-sazerac-replenishment`, `47-sazerac-allocation-alerts`, `48-sazerac-cocktail-concierge`, `49-sazerac-tasting-events`.

## 7. Edition-level compliance additions

> **Adult-beverage commerce is the most regulated vertical in the marketplace.** These compliance constraints are NON-OPTIONAL.

1. **Age verification at every transaction.** Every `BeverageOrder` requires verified age within a max-age-of-verification window. Age-verification provider partnership (Veratad / BlueCheck / AgeChecker) mandatory.
2. **State-by-state rules engine.** Per-state DTC, retailer-direct-ship, 3-tier compliance, dry-county geofencing all enforced at order-validation time. State-rules engine (Avalara Beverage Alcohol or equivalent partnership) required.
3. **TTB labelling compliance.** Federal labelling rules enforced on any cross-state delivery.
4. **Tied-house compliance.** Tasting-event referral fees and brand-funded marketing must comply with state-specific tied-house laws.
5. **Underage-purchase protection.** Single underage-purchase incident is irreparable trust damage; HITL gates and verification redundancy are non-negotiable.
6. **Two-step ID verification.** Once at order; again at pickup (in 3-tier states where licensed retailer fulfills). Webhook-confirmation from retailer required for delivery / pickup acceptance.

## 8. Operational impact

| Area | Change |
|---|---|
| Schema manifest | 10 new Bronze tables, 6 new Silver entities, 4 new Gold views |
| Agent catalog | 4 new YAMLs |
| Scenarios | 4 new folders |
| HITL gates | 4 new gate definitions (all-mandatory) |
| Compliance footprint | Significant; deferred from Phase 0-2 launch waves |

## 9. Phasing

This Channel ships **after** Home + Travel + Retail + Mobility are stable, because the compliance footprint extends beyond the marketplace's standard trust framework.

## 10. Cross-references

- Pack: [`../agentic-packs/cpg-adult-beverage/`](../agentic-packs/cpg-adult-beverage/)
- Marketplace: [`../agentic-packs/_marketplace/`](../agentic-packs/_marketplace/)
- Prior amendments: TMT-AMD-001..004
