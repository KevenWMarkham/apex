# 09 — Portability & Open-Home (Beverage Channel)

> _Draft — cellar inventory, allocation history, age-verification + tasting bookings all part of the lossless vault export._

## Commitments

| Commitment | Mechanism |
|---|---|
| Cellar inventory is yours, not Sazerac's or any retailer's | Local inventory + photo + receipt augmentation in vault |
| Allocation conversion history travels with you | Past allocation wins logged in vault; Sazerac partnership recognises customer's history across Telcos |
| Age-verification documents stay tokenised | `age_verification.doc_token` reference only; raw IDs vault-side |
| Tasting-event bookings + history portable | Like Travel Channel bookings |
| Cocktail recipe library — yours and partner-licensed — auditable | Recipe corpus licensing documented |

## MCP extension — `apex.tmt.mcp.beverage.v1`

```
- allocation_register_watch(sku_token, retailer_market) → ack
- allocation_alert(sku_token, retailer_id, quantity, drop_ts) → webhook
- allocation_reserve(sku_token, retailer_id, customer_token) → reservation_confirmation
- standard_order_search(query, state_code) → results[]
- standard_order_submit(items, payment, age_verification_token, fulfillment) → confirmation
- cocktail_recipe_match(cellar_inventory) → suggested_recipes[]
- cellar_inventory_read() → cellar_state
- cellar_inventory_update(item_id, change) → ack
- tasting_event_search(criteria) → events[]
- tasting_event_book(event_id, seats) → booking_confirmation
```

## State-compliance webhook

Most novel addition: every `standard_order_submit` requires a `state_eligibility_check` callback that confirms the order is legal under the destination-state rules at the moment of submission. This is the only Channel where compliance is enforced **inline** at every transaction.

## What stays partner-proprietary

- Sazerac's allocation algorithm (how they distribute scarce product)
- Retailer-side pricing
- State-by-state ABC regulator policies (sourced from public records; not Sazerac's IP)
- Distillery-tour content + heritage marketing
