# 09 — Portability & Open-Home (Retail Channel)

> _Draft — extends marketplace-level commitments to retail-specific data: purchase history, prescription history, loyalty balances, membership data._

## 1. Retail-specific portability commitments

| Commitment | Mechanism |
|---|---|
| Retail purchase history is the customer's, not the retailer's | Mirrored to vault; export-included; never shared with other retailers without explicit consent |
| Prescription history (PHI) stays vault-side | Walmart Pharmacy mirrors metadata to vault; rx-numbers tokenised; full export possible per HIPAA |
| Loyalty balances exportable | Walmart+, Costco, Sam's, Target Circle all sync via OAuth and travel with the vault |
| Membership info portable | Tier status, annual-fee dates, benefits-used log all in vault |
| Sponsored placements always disclosed | Audit log preserves which Walmart Connect ads surfaced when |

## 2. Walmart-specific MCP extension

The Retail Channel's MCP spec extends `apex.tmt.mcp.partner.v1` with retail-specific tools:

```
- inventory_check(sku, location_id) → availability
- price_compare(sku) → cross-retailer prices
- chain_route_propose(intent_list, time_budget) → proposed errand chain
- prescription_refill_request(rx_token, pharmacy_id) → refill_confirmation
- tle_appointment_propose(vehicle_id, service_types[]) → appointment_options
- membership_tier_optimize(household_id) → recommended_tier_changes
```

These are namespaced as `apex.tmt.mcp.retail.v1` and additive to the base.

## 3. Cross-retailer portability

If the customer disconnects Walmart and connects Target Circle instead, the Channel continues to operate with Target as the new default. The vault retains Walmart's historical purchase data for the customer's own reference; the orchestrator stops routing to Walmart.

This is the **structural commitment** that distinguishes the Channel from a closed retailer app — the household's retail behaviour data is not Walmart-locked.

## 4. Anti-patterns

- **Cross-retailer data sharing without explicit consent.** Walmart never sees the customer's Target purchases. The orchestrator may use both internally for routing decisions, but the partner-side never receives competitor data.
- **PHI in non-pharmacy services.** Prescription data is RTL-02 only; never visible to RTL-01 / RTL-03 / RTL-04 agents.
- **Sponsored-placement opacity.** Walmart Connect sponsorship must be disclosed in-line in the orchestrator's UI.
