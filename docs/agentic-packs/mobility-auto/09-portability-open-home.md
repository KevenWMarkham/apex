# 09 — Portability & Open-Home (Mobility Channel)

> _Draft — Vehicle data, financing data, insurance policy data all part of the lossless vault export._

## Commitments

| Commitment | Mechanism |
|---|---|
| Telematics data is yours, not the OEM's | Mirrored to vault; VIN tokenised; the customer can export full vehicle history including charge / drive / service logs |
| Lease / loan history travels with you | TFS / Ford Credit / GM Financial data syncs to vault; tokenised account numbers |
| Insurance policy state portable | Policy metadata + UBI score history in vault |
| Recall completion history audit-trail-preserved | NHTSA campaign + completion timestamps in vault export |

## MCP extension — `apex.tmt.mcp.mobility.v1`

Additional tools on top of the base partner protocol:

```
- vehicle_health_read(vehicle_id) → telematics_snapshot
- recall_match(vehicle_id_list, recall_feed) → matched_recalls
- service_appointment_propose(vehicle_id, service_types, time_window) → appointment_options
- ota_software_status(vehicle_id) → pending_updates
- ota_software_approve(vehicle_id, update_id) → confirmation
- next_vehicle_inventory_search(criteria) → vehicle_options
- trade_in_valuation(vehicle_id) → valuation
- loan_quote(vehicle_id, term) → quote
- ubi_score_read(vehicle_id) → current_score
```

## Why OEMs participate openly

- Multi-Telco distribution from one MCP integration (no bilateral integration tax per Telco)
- Verified household-fleet context (multi-vehicle, multi-driver) the OEM-direct app can't see
- Standardized vehicle-data exchange — no proprietary one-off APIs

## What stays OEM-proprietary

- OEM-specific in-vehicle UX (head unit, voice assistant)
- OEM software-update content (only update status is in the spec)
- Dealer-side commercial terms (rebates, finance offers)

The line is the same as for streaming: open protocol for distribution, proprietary content / commercials for differentiation.
