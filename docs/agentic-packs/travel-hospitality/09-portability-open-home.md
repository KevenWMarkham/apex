# 09 — Portability & Open-Home Commitments (Travel layer)

> _Draft — extends the open-home commitments from [`../telco/09-portability-open-home.md`](../telco/09-portability-open-home.md) to trip context, loyalty accounts, and travel documents._

## 1. Three additional commitments specific to travel

| Commitment | What it means | Enforcement |
|---|---|---|
| **Your loyalty accounts are yours, not the Telco's.** | The Telco brokers connections to AA AAdvantage, Marriott Bonvoy, Hertz Gold, etc., but it does not hold the master account. Member numbers stored as tokenised references only. | OAuth-style delegated access; Telco can disconnect any program in one click; loyalty balances synced into the vault are export-included. |
| **Your travel documents are never stored in the Telco's runtime.** | Passport, Global Entry, TSA Pre, Known Traveler numbers — only tokenised references in the vault. Raw documents stay in the customer's encrypted vault bucket, never in Telco-side databases. | `travel_document.doc_token` is a vault-side reference; runtime decryption requires the customer's KMS key. |
| **Trip history travels with the customer.** | The entire `trip` / `itinerary_segment` / `booking` / `disruption_event` history is part of the lossless vault export. If the customer switches Telcos, every PNR, every loyalty balance, every disruption resolution travels with them. | Export format §3. |

## 2. Vault export — additions for the travel layer

Extends the export from [`../telco/09-portability-open-home.md`](../telco/09-portability-open-home.md) §3:

```
vault-export-<household_id>-<timestamp>/
├── ...                                            # existing home-pack content
├── trips/
│   ├── trip-<uuid>.json                           # one file per trip
│   └── ...
├── itinerary-segments/
│   └── segments-YYYY.parquet
├── bookings/
│   └── bookings-YYYY.parquet
├── loyalty/
│   ├── programs.parquet                           # which programs are connected
│   └── balances-history-YYYY-MM.parquet           # monthly balance snapshots
├── travel-documents/
│   └── document-refs.json                         # tokenised references only — NEVER raw docs
└── disruptions/
    └── disruption-events-YYYY.parquet
```

## 3. New consent scopes (granular)

The pack introduces five new consent scopes (registered in [`./03-erd-and-postgres.md`](./03-erd-and-postgres.md) §6):

| Scope | What it grants |
|---|---|
| `travel` | Read of trip metadata (origin, destination, dates) for orchestrator routing |
| `travel.location` | Read of in-transit / on-location geo for trip-mode coordination |
| `travel.loyalty` | Read + sync of loyalty balances; never modifies underlying loyalty accounts |
| `travel.documents` | Read of tokenised travel-document references for partner check-in flows |
| `travel.payments` | Authorization to charge partner bookings to the customer's chosen payment method |

A customer can revoke any of these independently. Revoking `travel.location` while traveling pauses HOM-11/15 but leaves HOM-12/14 functional (they don't need geo).

## 4. Partner-side openness

The pack publishes an open MCP partner spec — `apex.tmt.mcp.travel.v1` — that any airline, hotel, OTA, STR, or experience partner can implement:

```
required tools:
  - search(origin, destination, dates, party_size, preferences) → results[]
  - book(result_id, traveler_info, payment_method) → booking_confirmation
  - status(booking_id) → current_status
  - modify(booking_id, change_request) → new_booking_confirmation
  - cancel(booking_id) → cancellation_confirmation

required webhooks:
  - disruption_event(booking_id, type, severity, recommended_action)
  - loyalty_balance_update(member_number_token, new_balance, tier_change)
  - status_change(booking_id, from_status, to_status)
```

Partners that implement the spec are eligible to list in the Telco's marketplace. The spec is **not Telco-proprietary** — any agent platform (Home Assistant, third-party orchestrator) can consume the same partner endpoints.

## 5. What this means for AA / Marriott / Expedia / Airbnb

| Partner | What the openness commitment buys them |
|---|---|
| American Airlines | A multi-Telco channel for AAdvantage enrolment without per-Telco bilateral integration |
| Marriott Bonvoy | Same — a single MCP endpoint serves every Telco that wires up |
| Expedia | Their existing API surface satisfies the spec with minor adaptation; no exclusivity demand |
| Airbnb | Verified-identity, verified-presence, verified-payment guest funnel without Telco-specific integration |

The openness is **mutual** — the Telco doesn't lock partners into one Telco, and partners don't lock the Telco into one set of partners. This is the marketplace flywheel.
