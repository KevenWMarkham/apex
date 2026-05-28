# 01 — Business Model

> Travel is the highest-value cross-sell on top of the Home Agentic platform — high transaction value, dense partner ecosystem, and a customer state (trip-mode) that already exists in the household calendar but is not yet orchestrated. Telco wins because the customer's billing relationship, consent ledger, and vault are already in place, and because trip-mode is just **a state transition of the same household**, not a separate platform.

## 1. Why travel is the next logical layer

The Home Agentic pack solved the household's at-home orchestration problem. The customer who subscribes to grocery + energy + eldercare + maintenance is the same customer who:

- Takes **2–6 leisure trips a year** ($2K–$15K spend per trip for a typical family)
- Books **3–8 business / weekend trips a year** if they're a knowledge worker
- Holds **4–10 active loyalty accounts** across airlines, hotels, rental cars, and OTAs
- Files **1–3 travel-disruption events per year** (IROPS, lost baggage, hotel walk, double-booking) that today require 30+ minutes of customer-side effort each to resolve

None of that orchestration happens on a Telco platform today. It happens fragmented across airline apps, hotel apps, OTA emails, SMS notifications, and the loyalty programs that fund each silo. The result is an orchestration deficit that the Telco can close, on the same bill the customer already pays.

## 2. The plug-in pattern

Travel & Hospitality is **not a new platform**. It is a new **posture** of the existing platform:

```
                  HOUSEHOLD STATE MACHINE
   ┌──────────────────────────────────────────────────────────┐
   │                                                          │
   │   AT-HOME  ──departure trigger──>  DEPARTING             │
   │      ▲                                  │                │
   │      │                                  ▼                │
   │   REUNIFIED  <──return trigger──  IN-TRANSIT             │
   │      ▲                                  │                │
   │      │                                  ▼                │
   │      └──────────────────────  ON-LOCATION                │
   │                                                          │
   └──────────────────────────────────────────────────────────┘

   AT-HOME           : HOM-01..08 run normally
   DEPARTING         : HOM-10 trip-mode orchestrator engages, HOM-13/14 finalize bookings
   IN-TRANSIT        : HOM-11 flight / HOM-15 ground mobility active
   ON-LOCATION       : HOM-12 hotel / HOM-14 STR active, HOM-16 local experience active
   REUNIFIED         : HOM-17 return reunification wakes home agents back up
```

Crucially, while the customer is in `DEPARTING` → `ON-LOCATION` states, the home agents do **not** stop. They run in a **vacation posture**:

- HOM-01 grocery: pauses recurring orders, schedules a fresh-restock for the day before return
- HOM-02 energy: sets vacation setback on HVAC; pre-cools/heats day-of-return
- HOM-03 eldercare: keeps running for any household member who didn't travel
- HOM-04 maintenance: defers any service-call dispatch to post-return
- HOM-05 security: switches to "vacation mode" arming; grants temporary access codes for pet sitter, neighbour
- HOM-06 wellness: pauses non-traveler signals; intensifies traveler wellness checks
- HOM-07 vehicle: schedules pre-trip charge for the EV; airport-parking telematics
- HOM-08 entertainment: switches to "watching-from-the-road" content delivery

The trip-mode sub-agents (`HOM-10..17`) are **on top of** the home agents, not replacements. Their job is to handle the partner-facing transactional layer.

## 3. The three revenue layers — restated for travel

Same three layers as the Home pack, with different absolute numbers per service:

| Layer | Payer | Travel-specific motion | Telco margin profile |
|---|---|---|---|
| **Consumer subscription** | Household | Trip-mode bundle ($5–15 / mo) on the monthly bill | 70–85% gross margin |
| **Action commerce** | Action partner (airline, hotel, OTA, STR, rental, restaurant) | % of booking value / per-booking fee / loyalty-share | 90%+ gross margin |
| **Outcome / risk-share** | Travel insurer, trip-protection program, airline IROPS economics | Per-disruption avoided, per-rebooking accepted | 60–80% gross margin |

The travel layer is **higher absolute transaction value per event** than home. A grocery order is $80–150; a hotel booking is $400–2,000; an airline ticket is $200–1,500; a vacation rental is $1,000–6,000. The action-commerce take rate even at 1–4% throws off meaningful $/event.

## 4. The unit-economic illustration

A "Family" Home Agentic subscriber (already paying $19.99 / mo for the Family bundle) who adds the Trip-Mode add-on at $7.99 / mo and takes a typical 4 leisure trips + 2 business trips per year:

| Event | Avg ticket / booking | Take rate envelope | Annual revenue per HH |
|---|---|---|---|
| 4 leisure flights × 4 tickets | $400 each | 2–4% | $130–260 |
| 2 business flights × 1 ticket | $600 each | 2–4% | $25–50 |
| 4 hotel stays × 3 nights | $200/night | 3–6% | $70–140 |
| 1 vacation rental × 5 nights | $250/night | 3–6% | $40–75 |
| 4 ground-mobility (Uber/Hertz) bookings | $80 each | 5–10% | $15–30 |
| 6 dining reservations + 2 activities | $120 avg | 1–3% | $10–25 |
| **Subscription + commerce, blended** | | | **$385–675 / yr per HH** |
| **IROPS / disruption-protection share** | 1 event / yr | $20–50 per event | $20–50 / yr |

A typical-traveling Family-bundle household contributes **$400–700 / yr in incremental GP** from the travel layer alone — on top of the $250–420 / yr from the base Home Agentic pack. The trip add-on roughly **doubles the average household's annual contribution** to the Telco's agentic P&L.

## 5. Why the Telco wins this specific cross-sell

A separate set of disqualifiers, beyond the Big Tech disqualifiers from the Home pack:

| Alternative platform | Why they can't credibly own this |
|---|---|
| **OTAs (Expedia, Booking)** | Their business model depends on capturing the customer at the search / book moment and re-marketing to them. They cannot operate a vault-first model that doesn't track every click. |
| **GDS / Sabre / Amadeus** | B2B-only; no consumer-facing surface, no consumer billing relationship. |
| **Hotel-direct apps (Marriott Bonvoy, Hilton Honors)** | Single-brand only. The household stays at multiple chains across the year. |
| **Airline-direct apps (AA, Delta, United)** | Single-carrier only. The household flies multiple carriers. |
| **Google Travel / Apple Wallet** | Same data-monetization disqualifier as the Home pack. Apple has no commerce engine; Google has the wrong incentive structure. |
| **Credit card concierge (Chase Sapphire, Amex Platinum)** | Tied to one card; no device graph; no household state machine; no consent ledger. |

Only the Telco combines: **a multi-brand neutral position** + **a consumer billing relationship** + **a household state machine** + **a vault customers actually trust** + **partnership channels to airlines and hotels** through telematics and SIM-card business already in place.

## 6. The wedge events that drive subscription

Three high-emotional-cost moments where the customer feels the value immediately:

1. **The IROPS rebook.** Flight cancelled at 11 PM. American Airlines pushes the customer to a 36-hour-later rebook. The Home Flight Concierge pulls the AA disruption signal, cross-references the household calendar (kid's recital tomorrow afternoon), looks at alternate airlines via Expedia connection, finds a 6-hour-later Delta routing that gets the family home in time, **submits the rebook through AA's MCP partner endpoint with the customer's loyalty number attached**, and texts the customer "approved — Delta DL 1234, gets you home 4:15 PM". **This is the moment the customer remembers forever.**

2. **The hotel walk.** Marriott property is overbooked. The Home Hotel Concierge picks up the property-level signal before the customer arrives, pre-arranges a Hyatt sister-property walk (or, if no walk available, holds a comparable Marriott across the street), and notifies the customer en-route to ground transport.

3. **The vacation continuity.** The customer is on day 4 of a 10-day Airbnb stay in Mexico. Back home, Mom's ADL deviation score crosses 2.0. The Home Eldercare Monitor escalates to the designated family contact in-state, while the Home Trip Orchestrator pings the traveling customer with the situation status — **without** triggering a vacation-ruining alarm. Coordination is the value.

Each wedge event is a $200–600 disruption-equivalent value capture, and creates the kind of memorable customer moment that drives organic word-of-mouth. **One wedge event is worth more in CAC than a year of marketing.**

## 7. What the pack does not try to be

- **Not a search engine.** Customers will continue to use Expedia, Google Travel, Kayak to compare options. The pack picks up at the **booking-and-execution** layer, not the discovery layer.
- **Not a content site.** Customers will continue to use TripAdvisor, Lonely Planet, Reddit for inspiration. The pack assumes the customer already knows where they want to go.
- **Not a payment processor.** Customer cards / Apple Pay / Telco-bill financing carry the payments; the orchestrator is the intent-and-action layer.
- **Not a content moderation layer for vacation rentals.** Airbnb / Vrbo policies are the source of truth for STR; the pack consumes their decisions, doesn't override them.

Scope discipline is what makes the partnership map workable. See [`06-partnership-map.md`](./06-partnership-map.md).
