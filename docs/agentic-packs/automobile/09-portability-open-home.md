# 09 — Portability & Open-Home (Automobile Channel)

> _Draft — vehicle ownership history, financing records, insurance policy data all stay in the customer's vault. Multi-Telco portability extends to the partner ecosystem._

## 1. Automobile-specific portability commitments

| Commitment | Mechanism |
|---|---|
| Vehicle ownership history is yours | Every `Vehicle` + `VehicleListing` + `PurchaseOffer` + `ResaleListing` in vault; export-included |
| Financing record portable | `FinancingApplication` + decisions + APR history in vault (CPNI-tokenised) |
| Insurance policy + UBI history portable | `InsuranceQuote` + `AutoPolicy` + UBI-score history in vault |
| Fuel + charging transaction history portable | `FuelTransaction` + `ChargingSession` records mirrored |
| Resale records portable | Trade-in + private-sale + donation logs in vault |
| **Credit-pull authorization revocable any time** | Hard credit pulls require fresh, time-bounded consent per pull |
| **Insurance underwriting data revocable** | Telematics-feed authorization to carriers revocable; doesn't undo bound policies (already underwritten) but stops ongoing feed |

## 2. Vault export — automobile additions

```
vault-export-<household_id>-<timestamp>/
├── ...                                          # existing content
├── vehicles/
│   ├── vehicle-<vehicle_id>.json                # one per owned vehicle
│   ├── lifecycle-events-YYYY.parquet            # state transitions
│   └── telematics-rollup-YYYY-MM.parquet
├── automobile-listings/
│   └── shortlists-YYYY.parquet                  # research/shopping history
├── automobile-financing/
│   ├── applications-YYYY.parquet
│   └── apr-history-YYYY.parquet
├── automobile-insurance/
│   ├── quotes-YYYY.parquet
│   ├── policies.parquet
│   └── ubi-score-history-YYYY-MM.parquet
├── automobile-fueling/
│   ├── fuel-transactions-YYYY-MM.parquet
│   └── charging-sessions-YYYY-MM.parquet
├── automobile-aftermarket/
│   └── orders-YYYY.parquet
└── automobile-resale/
    └── resale-events-YYYY.parquet
```

## 3. MCP extension — `apex.tmt.mcp.automobile.v1`

Additional tools beyond base partner protocol:

```
- discovery_search(criteria) → listing_set
- discovery_compare(listing_ids) → comparison_table
- valuation_request(vehicle_descriptor) → valuation_quote
- financing_pre_approval(applicant_token, vehicle_listing_id, term, requested_amount) → pre_approval_decision
- financing_final_submit(application_id, accepted_terms) → final_decision
- insurance_quote(applicant_token, vehicle_listing_id, coverage) → quote
- insurance_bind(quote_id, payment_method, effective_date) → policy_confirmation
- ubi_enroll(policy_id, telematics_source) → enrollment_confirmation
- dealer_negotiation_initiate(listing_id, target_otd_price) → dealer_response
- dealer_reservation(listing_id, reservation_terms) → reservation_confirmation
- aftermarket_search(vehicle_id, part_or_accessory) → results
- charging_route_optimize(vehicle_id, destination, range_remaining) → route
- fueling_price_compare(vehicle_id, location) → price_table
- trade_in_offer(vehicle_id) → offer_set
- resale_listing_create(vehicle_id, channel, terms) → listing_confirmation
- dmv_pre_fill(purchase_offer_id, state) → dmv_application
```

## 4. The hard-credit-pull boundary

The Automobile Channel touches credit pulls — a class of action with unusual consumer-protection consequences. Channel design:

| Action | Pull type | Consent requirement |
|---|---|---|
| AUT-01 discovery / shortlisting | None | No credit-related consent needed |
| AUT-03 pre-approval shopping | Soft pull (Capital One Navigator-style) | Once-per-shopping-session OAuth |
| AUT-03 final financing submission | Hard pull | Per-application explicit HITL consent |
| AUT-04 insurance quote | Soft pull (some carriers) | Once-per-shopping-session OAuth |
| AUT-04 insurance bind | None additional | Pre-existing consent |
| AUT-02 dealer-side negotiation | None (dealers may pull when customer arrives) | Customer informed of dealer-side behaviour |

The principle: the **customer always knows when a credit pull will occur** and has affirmatively consented.

## 5. Partner openness commitments

Carriers (Progressive, State Farm, Geico, etc.) and lenders (Capital One, Ally, Chase, etc.) participating in the Channel commit to:

- **No exclusive routing** — household can switch carriers / lenders between events without penalty
- **Quote portability** — quote data shareable to other carriers / lenders during the shopping window
- **UBI-data ownership** — telematics-data the carrier received stays usable for that policy but is not transferable to non-participating carriers without consent

## 6. Why partners participate openly

| Partner type | What they gain |
|---|---|
| Dealer groups | Higher walk-in conversion + lower acquisition cost; multi-Telco distribution |
| Lenders | Lower CAC on auto loans; pre-qualified high-intent applicants |
| Insurance carriers | Verified-telematics underwriting + verified household context |
| Aftermarket retailers | Verified-vehicle parts orders + cross-Channel context (which vehicle, which mileage) |
| Fueling networks | Membership / loyalty enrolment funnel + data-rich routing |

Same shape as Travel Channel openness: partners gain distribution + verified-context customers in exchange for accepting the openness commitments.
