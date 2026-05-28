# APEX-TMT · Agentic Travel — Build-Spec Amendment

**Amendment number:** TMT-AMD-002
**Amended document:** `docs/build-specs/apex-tmt-build-spec.md`
**Prior amendment:** [`apex-tmt-agentic-home-amendment.md`](./apex-tmt-agentic-home-amendment.md) (TMT-AMD-001)
**Status:** Draft
**Author:** tmt-practice-lead@deloitte.com / th-practice-lead@deloitte.com
**Date:** Draft

---

## 0. Why this amendment exists

TMT-AMD-001 introduced the Home Agentic service line (`TMT-TEL-HOM-01..08`, `TMT-TEL-HOM-99`). This amendment extends that service line with eight additional sub-agents (`TMT-TEL-HOM-10..17`) that handle the **trip-mode posture** of the household — flight, hotel, OTA, vacation rental, ground mobility, local experience — and the **return-reunification** to home posture.

The pack narrative lives in [`docs/agentic-packs/travel-hospitality/`](../agentic-packs/travel-hospitality/). This amendment is the formal spec change.

## 1. New service codes — `TMT-TEL-HOM-10..17`

| Service code | Description | Headline KPI | Scenario folder | Agent YAML |
|---|---|---|---|---|
| `TMT-TEL-HOM-10` | Trip orchestrator | Successful trip intent rate | `TMT-CX-30-home-trip-orchestrator` | `tmt/20-home-trip-orchestrator.yaml` |
| `TMT-TEL-HOM-11` | Flight concierge | IROPS recovery time | `TMT-CX-31-home-flight-concierge` | `tmt/21-home-flight-concierge.yaml` |
| `TMT-TEL-HOM-12` | Hotel concierge | On-property NPS | `TMT-CX-32-home-hotel-concierge` | `tmt/22-home-hotel-concierge.yaml` |
| `TMT-TEL-HOM-13` | OTA & itinerary builder | Trip-build time saved | `TMT-CX-33-home-ota-itinerary-builder` | `tmt/23-home-ota-itinerary-builder.yaml` |
| `TMT-TEL-HOM-14` | Vacation rental | Check-in friction | `TMT-CX-34-home-vacation-rental` | `tmt/24-home-vacation-rental.yaml` |
| `TMT-TEL-HOM-15` | Ground mobility | Door-to-door time | `TMT-CX-35-home-ground-mobility` | `tmt/25-home-ground-mobility.yaml` |
| `TMT-TEL-HOM-16` | Local experience | Bookings completed | `TMT-CX-36-home-local-experience` | `tmt/26-home-local-experience.yaml` |
| `TMT-TEL-HOM-17` | Return reunification | Time-to-home-baseline | `TMT-CX-37-home-return-reunification` | `tmt/27-home-return-reunification.yaml` |

## 2. New Bronze landings

| Bronze table | Source systems | Classification |
|---|---|---|
| `bronze.tmt_hom.airline_pnr` | `american-airlines`, `delta-airlines`, `united-airlines`, `southwest`, `alaska`, `jetblue` | `pii` |
| `bronze.tmt_hom.airline_disruption` | Same airlines | `pii` |
| `bronze.tmt_hom.hotel_reservation` | `marriott-bonvoy`, `hilton-honors`, `hyatt-world`, `ihg-one`, `accor-all` | `pii` |
| `bronze.tmt_hom.hotel_stay_events` | `marriott-bonvoy`, `hilton-honors` | `pii` |
| `bronze.tmt_hom.ota_itinerary` | `expedia`, `booking-com`, `kayak`, `google-travel` | `pii` |
| `bronze.tmt_hom.str_booking` | `airbnb`, `vrbo`, `plum-guide`, `sonder` | `pii` |
| `bronze.tmt_hom.rental_car` | `hertz`, `avis`, `enterprise`, `turo`, `zipcar` | `pii` |
| `bronze.tmt_hom.rideshare` | `uber`, `lyft` | `pii` |
| `bronze.tmt_hom.dining_reservation` | `opentable`, `resy`, `tock` | `pii` |
| `bronze.tmt_hom.experience_booking` | `viator`, `getyourguide` | `pii` |
| `bronze.tmt_hom.loyalty_sync` | `aa-aadvantage`, `dl-skymiles`, `ua-mileageplus`, `marriott-bonvoy`, `hilton-honors`, `hertz-gold` | `cpni` |
| `bronze.tmt_hom.travel_document_refs` | `apex-identity` | `cpni` |
| `bronze.tmt_hom.travel_insurance` | `allianz-travel`, `aig-travel`, `travelguard` | `pii` |

## 3. New Silver entities (under `apex-tmtcml/entities/travel/`)

`Trip`, `ItinerarySegment`, `Booking`, `LoyaltyProgram`, `LoyaltyAccount`, `TravelDocument`, `TripStateEvent`, `DisruptionEvent`, `PartnerEndpoint`.

## 4. New Gold views

- `gold.v_tmt_hom_traveler_360_household`
- `gold.v_tmt_hom_trip_current_state`
- `gold.v_tmt_hom_disruption_inflight`
- `gold.v_tmt_hom_loyalty_balances`

## 5. New anchor measures

- `trip_days_away` (pre)
- `household_rollup_state` (pre) — used by both Home and Travel sub-agents to drive vacation-posture
- `disruption_recovery_minutes` (pre)
- `loyalty_portfolio_value_usd` (post)

## 6. Edition-level compliance additions (on top of TMT-AMD-001)

1. **Travel-document tokenization.** Passport / Global Entry / TSA Pre / Known Traveler / CLEAR / Real-ID numbers stored only as tokenised references in `travel_document.doc_token`. Raw documents reside only in the customer's vault bucket and are surfaced to partner check-in flows via short-lived signed references.
2. **Loyalty-credential brokering.** Member numbers stored as `loyalty_account.member_number_token`. The Telco never holds plaintext member numbers or passwords; partner connections use OAuth or partner-specific delegated-access flows.
3. **New consent scopes** registered in `consent.scope`: `travel`, `travel.location`, `travel.loyalty`, `travel.documents`, `travel.payments`. Each is independently revocable.
4. **Partner-side MCP spec** `apex.tmt.mcp.travel.v1` published as part of this amendment; partners implement it to be listable in the marketplace.

## 7. Cross-edition relationship with APEX-TH

The APEX TH Edition (`docs/build-specs/apex-th-build-spec.md`) already covers enterprise-side travel use cases (airline IROPS-recovery from the airline's ops centre, hotel demand-disruption from the chain's revenue-management view). This amendment introduces **consumer-side** counterparts. The two interoperate via MCP — a TH-Edition airline IROPS agent and a TMT-side Home Flight Concierge agent for the same disruption talk to each other through MCP.

## 8. Operational impact

| Area | Change |
|---|---|
| Schema manifest | 13 new Bronze tables, 9 new Silver entities, 4 new Gold views |
| Agent catalog | 8 new YAMLs (`tmt/20..27`) |
| Scenarios | 8 new folders (`TMT-CX-30..37`) |
| HITL gates | 8 new gate definitions covering IROPS rebook, room-rate change, booking total, cancellation, ground budget, reservation conflict |

## 9. Build order

1. Land this amendment.
2. Extend `packages/apex-tmtcml/` with the travel entity sub-package.
3. Register the new measures in `packages/apex-medallion/src/apex_medallion/gold/tmt_hom_travel_measures.py`.
4. Land the 8 new agent YAMLs.
5. Update the TMT manifest to register the new tables / views.
6. Populate scenario folders with demo manifests as partner integrations land.

## 10. References

- Pack narrative: [`../agentic-packs/travel-hospitality/`](../agentic-packs/travel-hospitality/)
- Prior amendment (Home): [`./apex-tmt-agentic-home-amendment.md`](./apex-tmt-agentic-home-amendment.md)
- Parent TMT build-spec: [`./apex-tmt-build-spec.md`](./apex-tmt-build-spec.md)
- Sibling TH build-spec: [`./apex-th-build-spec.md`](./apex-th-build-spec.md)
