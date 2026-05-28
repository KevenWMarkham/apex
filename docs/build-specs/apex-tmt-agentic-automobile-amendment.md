# APEX-TMT · Agentic Automobile — Build-Spec Amendment

**Amendment number:** TMT-AMD-006
**Amended document:** `docs/build-specs/apex-tmt-build-spec.md`
**Prior amendments:** TMT-AMD-001..005
**Sibling Mobility amendment:** [`./apex-tmt-agentic-mobility-amendment.md`](./apex-tmt-agentic-mobility-amendment.md) (Toyota-anchored connected-vehicle ops)
**Status:** Draft

## 0. Why this amendment exists

Introduces the **Automobile Channel** as Channel 6 of the marketplace. Adds the `TMT-TEL-AUT-*` service-code family for the **full vehicle ownership lifecycle** — discovery, purchase, financing, insurance, ownership-aftermarket, charging/fueling, fleet, resale. Multi-anchor partnerships: AutoNation (dealer + service), Cox Automotive (KBB / Autotrader / Manheim data), Progressive (UBI insurance).

Distinct from the Mobility Channel (TMT-AMD-004) which is Toyota-anchored and focused on connected-vehicle ongoing operations. The two Channels coordinate via the orchestrator.

Pack narrative: [`../agentic-packs/automobile/`](../agentic-packs/automobile/)

## 1. New service codes — `TMT-TEL-AUT-01..08`

| Service | Description | Headline KPI |
|---|---|---|
| `TMT-TEL-AUT-01` | Vehicle discovery + research | Time-to-shortlist; shortlist quality |
| `TMT-TEL-AUT-02` | Purchase orchestration | Walk-out time; OTD vs market |
| `TMT-TEL-AUT-03` | Auto financing pre-approval + execution | Best-APR delta |
| `TMT-TEL-AUT-04` | Auto insurance quote / bind / manage | Annual premium savings |
| `TMT-TEL-AUT-05` | Aftermarket parts + accessories | Cross-retailer price savings |
| `TMT-TEL-AUT-06` | Charging + fueling optimization | Annual cost reduction |
| `TMT-TEL-AUT-07` | Fleet management + mileage log | Tax deduction $ captured |
| `TMT-TEL-AUT-08` | Resale + end-of-life | Resale value delta |

## 2. New Bronze landings under `bronze.tmt_aut.*`

`kbb_listings`, `autonation_inventory`, `dealer_direct_inventory`, `carmax_carvana_inventory`, `financing_applications`, `insurance_quotes`, `aftermarket_orders`, `charging_sessions`, `fuel_transactions`, `kbb_valuations`, `dmv_status`, `fleet_mileage_logs`, `resale_listings`. (13 new tables)

## 3. New Silver entities (`apex-tmtcml/entities/automobile/`)

`VehicleListing`, `PurchaseOffer`, `FinancingApplication`, `InsuranceQuote`, `AftermarketOrder`, `ChargingSession`, `FuelTransaction`, `FleetAssignment`, `ResaleListing`, `VehicleLifecycleEvent`. Extensions to `Vehicle` for `lifecycle_state` + `lifecycle_state_since`.

## 4. New anchor measures

`shortlist_price_delta_usd`, `financing_apr_best_offer`, `insurance_premium_savings_annual_usd`, `fuel_cost_optimization_annual_usd`, `repair_cost_trend_6m_usd_per_month` (post), `resale_value_depreciation_pct_per_year` (post).

## 5. New Gold views

`household_vehicle_portfolio`, `shortlist_comparison`, `financing_offer_table`, `insurance_quote_table`, `fueling_cost_optimization`, `resale_value_track`, `fleet_mileage_log`. (7 new views)

## 6. New agent YAMLs

`tmt/40-vehicle-discovery.yaml`, `41-vehicle-purchase.yaml`, `42-auto-financing.yaml`, `43-auto-insurance.yaml`, `44-aftermarket.yaml`, `45-charging-fueling.yaml`, `46-fleet-management.yaml`, `47-resale-endoflife.yaml`.

## 7. New scenarios

`TMT-CX-50-vehicle-discovery`, `51-vehicle-purchase`, `52-auto-financing`, `53-auto-insurance`, `54-aftermarket-accessories`, `55-charging-fueling`, `56-fleet-management`, `57-resale-endoflife`.

## 8. New consent scopes

`vehicle.purchase`, `vehicle.financing`, `vehicle.insurance`, `vehicle.fueling`, `vehicle.aftermarket`.

## 9. Edition-level compliance additions

The Automobile Channel introduces three significant compliance frontiers on top of prior amendments:

1. **Credit-pull discipline (FCRA + CFPB).** All AUT-03 credit pulls must distinguish soft vs hard; every hard pull requires per-application HITL consent within a fresh time-bounded authorization window. Authorization audit trail preserved in vault.
2. **Insurance state-by-state regulation.** AUT-04 must clear all 50 states for quote / bind authority; UBI participation has different rules per state (CA, MA, IL have material restrictions). State-rules engine queried at every transaction.
3. **Dealer-pricing transparency.** AUT-02 must surface all dealer add-ons (extended warranty, paint protection, etc.) pre-arrival. No agent-mediated transaction may include undisclosed add-ons.

Additional standard compliance:

4. **Credit-bureau data classification.** Credit-pull results stored as `cpni`-classified; never exposed to non-AUT-03 agents.
5. **FTC dealer-disclosure compliance.** Pre-arrival pricing commitments must satisfy FTC's CARS Rule (2024) advance-disclosure requirements.
6. **DMV automation per-state.** State DMV integration via Vitu / ALG; each state has its own document set and submission flow.

## 10. Cross-Channel coordination contract

This Channel's relationship with sibling Channels is explicit:

| Channel | Coordination |
|---|---|
| `mobility-auto/` (Toyota Connected, MOB-01..04) | Toyota-specific ongoing operations; AUT-* handles purchase / finance / insurance / resale for any vehicle including Toyota |
| `telco/` Home Channel (HOM-07 vehicle) | HOM-07 provides raw telematics; AUT-04 consumes for UBI pre-computation; AUT-01 consumes for repair-cost-trend trigger |
| `retail/` Retail Channel (RTL-03 Walmart Auto Care) | RTL-03 handles out-of-warranty independent-network service; AUT-05 handles parts; orchestrator routes by household preference |
| `travel-hospitality/` Travel Channel (HOM-15 ground mobility) | HOM-15 handles in-trip rentals / rideshare; AUT-* handles owned-vehicle |

## 11. Operational impact

| Area | Change |
|---|---|
| Schema manifest | 13 new Bronze tables, 10 new Silver entities, 7 new Gold views |
| Agent catalog | 8 new YAMLs |
| Scenarios | 8 new folders |
| HITL gates | 14 new gate definitions across 8 services |
| MCP partner spec | New extension `apex.tmt.mcp.automobile.v1` |

## 12. Phasing

This Channel ships after Home, Travel, Retail, Mobility, and CPG are stable, because:

- Compliance footprint (insurance state-by-state, FCRA, FTC CARS Rule, DMV automation per state) is non-trivial
- Anchor partnerships (AutoNation, Cox, Progressive) require longer BD cycles than Walmart / Toyota / Sazerac
- Cross-Channel coordination with Mobility requires Mobility Channel to be stable first

Estimated launch: Year 3+ of marketplace rollout.

## 13. Cross-references

- Pack: [`../agentic-packs/automobile/`](../agentic-packs/automobile/)
- Sibling pack: [`../agentic-packs/mobility-auto/`](../agentic-packs/mobility-auto/)
- Marketplace: [`../agentic-packs/_marketplace/`](../agentic-packs/_marketplace/)
- Prior amendments: TMT-AMD-001..005
- Sibling AXLE Edition (Automotive enterprise side): [`./apex-axle-build-spec.md`](./apex-axle-build-spec.md) if extended
