# Travel & Hospitality — APEX Agentic Pack

> A plug-in to the Telco Home Agentic platform that extends orchestration **beyond the front door**. When the household goes from "occupied home mode" to "trip mode", the same vault, the same consent grants, and the same single bill keep working — coordinating airlines, hotels, OTAs, vacation rentals, ground mobility, and local experiences as partner agents on the customer's Telco invoice. The house doesn't go offline when the customer travels; it **changes posture**.

**Parent Editions:** `TMT` (Telco Home Agentic) **+** `TH` (Travel & Hospitality)
**Sibling pack:** [`docs/agentic-packs/telco/`](../telco/)
**New service-code family:** `TMT-TEL-HOM-10..17` (Trip-mode sub-agents)
**Companion build-spec amendment:** [`docs/build-specs/apex-tmt-agentic-travel-amendment.md`](../../build-specs/apex-tmt-agentic-travel-amendment.md)
**Status:** Draft
**Primary author:** tmt-practice-lead@deloitte.com / th-practice-lead@deloitte.com

## The thesis in one paragraph

The Telco Home Agentic platform already knows everything that matters about a household — the calendar that says "we leave Friday", the eldercare context that says "Mom's alone for ten days", the vehicle that says "EV needs charge before the drive", the pantry that says "stop the milk delivery, start it again on the 22nd". The Travel & Hospitality pack treats **the trip itself** as a continuation of household orchestration — not a separate app, not a separate subscription, not a separate vault. American Airlines, Marriott, Expedia, Airbnb, Hertz, Uber, OpenTable, and Viator all plug in as **partner agents** the customer's existing Home Orchestrator can route to, with the same trust model and the same monthly bill.

## What changes when you plug in T&H

| Dimension | Home Agentic alone | + Travel & Hospitality |
|---|---|---|
| Customer state | "At home" | "At home" / "Departing" / "In transit" / "On location" / "Returning" — explicit state-machine |
| Sub-agent set | 8 home services + orchestrator | + 8 trip-mode services (`HOM-10..17`) |
| Partner ecosystem | Grocers, utilities, MA payers, OEMs | + Airlines, hotels, OTAs, STRs, ground mobility, experiences |
| Outcome layer (D-archetype) | MA payer (eldercare) + P&C insurer | + Travel insurance, IROPS rebooking economics, trip-protection programs |
| Revenue layers | Consumer subscription + action commerce + outcome | Same three layers — same single bill |
| Trust model | Vault + customer-held KMS key | Same vault — travel context is just another scope in the same `ConsentGrant` model |

## Pack contents

| # | Document | Purpose |
|---|---|---|
| 01 | [Business model](./01-business-model.md) | Why Travel & Hospitality is the natural cross-sell on top of Home Agentic |
| 02 | [Trip state transitions](./02-trip-state-transitions.md) | The household state machine: At-Home → Departing → In-Transit → On-Location → Returning → Reunified |
| 03 | [ERD & Postgres extensions](./03-erd-and-postgres.md) | New entities (`Trip`, `Itinerary`, `Booking`, `LoyaltyProgram`, `TravelDocument`) extending the telco schema |
| 04 | [Medallion (Bronze / Silver / Gold)](./04-medallion-bronze-silver-gold.md) | New Bronze landings for airline, hotel, OTA, STR; new Silver entities; new Gold views |
| 05 | [Services catalog](./05-services-catalog.md) | Eight new sub-agents (`TMT-TEL-HOM-10..17`) plus orchestrator extensions |
| 06 | [Partnership map](./06-partnership-map.md) | Concrete anchors: American Airlines, Marriott, Expedia, Airbnb, Uber, Hertz, OpenTable, Viator |
| 07 | [Business value model](./07-business-value-model.md) | Per-service unit economics + ARPU uplift from the travel cohort |
| 08 | [Consumer business case](./08-consumer-business-case.md) | Trip-mode willingness-to-pay, IROPS recovery as the wedge |
| 09 | [Portability / open-home](./09-portability-open-home.md) | How trip state, loyalty balances, and travel history travel with the vault |
| 10 | [Ecosystem differentiators](./10-retailer-differentiators.md) | Why the Telco wins this against OTAs, GDS, and hotel-direct apps |

### Diagrams

- [`diagrams/mermaid-trip-state.md`](./diagrams/mermaid-trip-state.md) — household trip state machine
- [`diagrams/flow-irops-end-to-end.md`](./diagrams/flow-irops-end-to-end.md) — irregular-operations recovery flow from gate notification to vault update

## Anchor partner mapping

| Service code | Anchor partner examples | Archetype | Where they plug in |
|---|---|---|---|
| `TMT-TEL-HOM-10` Trip Orchestrator | — (Telco-owned) | — | Routes trip intents to the right sub-agent |
| `TMT-TEL-HOM-11` Flight Concierge | **American Airlines**, Delta, United, Southwest, JetBlue, Alaska | B + D | IROPS rebooking, seat upgrade, baggage tracking |
| `TMT-TEL-HOM-12` Hotel Concierge | **Marriott**, Hilton, Hyatt, IHG, Accor, Four Seasons | B + C | Mobile key, room prefs, on-property orchestration |
| `TMT-TEL-HOM-13` OTA & Itinerary Builder | **Expedia**, Booking.com, Kayak, Google Travel | B + A | Multi-segment trip planning, price-watch |
| `TMT-TEL-HOM-14` Vacation Rental | **Airbnb**, Vrbo, Plum Guide, Sonder | B + A | STR check-in, host-comms, local-services bundling |
| `TMT-TEL-HOM-15` Ground Mobility | Uber, Lyft, Hertz, Avis, Turo, Zipcar, ChargePoint | B | Airport transfer, rental pickup, charging on route |
| `TMT-TEL-HOM-16` Local Experience | OpenTable, Resy, Viator, GetYourGuide, Tock | B + A | Dining, activities, tours, reservations |
| `TMT-TEL-HOM-17` Return Reunification | — (orchestrator function) | — | Wakes home agents on arrival, restocks pantry |

See [`06-partnership-map.md`](./06-partnership-map.md) for the full archetype-by-partner matrix and deal-shape heuristics.

## Relationship to the existing TH Edition

The APEX TH Edition (`docs/build-specs/apex-th-build-spec.md`, 104 scenarios already in `docs/scenarios/TH/`) is built **enterprise-side** — it serves airline operations, hotel operations, cruise lines, OTAs as enterprises looking at travelers. This pack is built **consumer-side** — it serves the household looking at travel.

The two are **complementary, not redundant**:

- A TH-Edition agent (e.g., `apex.th.agents.irops-recovery`) acts inside an **airline's** ops centre, optimizing rebooking decisions across all impacted passengers.
- A TMT-TEL-HOM-11 agent acts inside a **single household's** vault, advocating for that household's preferred rebooking outcome and surfacing it to the customer.

When American Airlines' IROPS agent decides to reroute, the Home Flight Concierge picks up the disruption signal, cross-references the family's calendar, eldercare context, and EV-charge timing back home, and proposes the option that minimizes household disruption — then submits the preferred rebooking back to AA through MCP. **Two agents, two sides of the same disruption, talking through MCP.**

## Three things that make this pack work

1. **The vault doesn't move.** Trip context lives in the same household vault as home context. The customer doesn't reauthorize a new platform every time they fly — the existing `ConsentGrant` is extended with a `travel` scope and bound to the trip-mode sub-agents.
2. **Loyalty and bookings stay portable.** AA AAdvantage, Marriott Bonvoy, Hertz Gold, Airbnb identity — every loyalty linkage and every booking confirmation lands in the customer's vault, not in a Telco-controlled silo. If the customer leaves the Telco, the trip history goes with them. This is the inverse of every OTA's data strategy.
3. **The home keeps running while the customer is away.** Vacation Continuity (`HOM-15`) is not a new agent — it's the same eldercare, pet, security, and energy sub-agents from the Home pack running in a different posture. The home agents don't go to sleep when the customer travels; they coordinate with the trip agents to make sure the household keeps working.
