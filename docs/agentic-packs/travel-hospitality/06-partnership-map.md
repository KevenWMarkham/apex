# 06 — Strategic Partnership Map

> Travel & Hospitality partnerships using the same five archetypes (A/B/C/D/E) defined in the canonical telco pack. Concrete anchors — **American Airlines, Marriott, Expedia, Airbnb** — are called out at the top of each service; the deeper bench (Hilton, Hyatt, Delta, United, Hertz, Uber, OpenTable, Viator) sits underneath.

## 1. Archetype reminder

| Archetype | What flows to Telco | What flows to partner | Typical deal shape |
|---|---|---|---|
| A — Data-In | Partner telemetry / catalog | Customer reach + verified intent signal back | Reciprocal data + per-action share |
| B — Action-Out | Transactional fulfilment | Order / booking volume, lower CAC | Per-booking rev-share (1–10%) |
| C — Distribution / Bundle | Bundled subscriber growth | Discounted CAC | Wholesale / co-branded SKU |
| D — Co-Insurance / Risk-Share | Outcome monetization | Loss-ratio reduction / cohort risk | Outcome-based fees |
| E — Platform / Standards | Interoperability | Reference status | Strategic, low cash |

## 2. Service-by-service partner bench

### `TMT-TEL-HOM-11` — Flight Concierge

**Anchor partner — American Airlines.**

| Partner | Loyalty program | Archetype | Value exchange |
|---|---|---|---|
| **American Airlines** | AAdvantage | **B + D + E** | IROPS rebook fulfilment with attached loyalty number; AA pays a small rebook-attribution fee + co-branded "Home Concierge AAdvantage" partnership; in-trip IROPS share-of-recovery economics |
| Delta Air Lines | SkyMiles | B + E | Same shape as AA; Delta's Medallion tier-match programs add a C component for high-tier customers |
| United Airlines | MileagePlus | B + E | Same |
| Southwest | Rapid Rewards | B | Direct-only; no GDS routing; less rebook flexibility |
| JetBlue | TrueBlue | B + E | |
| Alaska Airlines | Mileage Plan | B + E | Particularly valuable for West-Coast Telco footprint |

**Why airlines say yes:** rebooking dispatched through the Telco's Home Flight Concierge has higher acceptance rates (because the agent already knows the customer's calendar and preferences) and lower CSR-handle-time than rebooking through airline-direct CSR queues. Airlines save $8–20 per rebook in handle-time alone; the Telco shares the savings.

**Deal-structure note:** Airline rebook-attribution fees are small (~$1–3 per accepted rebook). The bigger value is in **co-marketing AAdvantage / SkyMiles / MileagePlus enrolments on the Telco bill** — this is the C-archetype move that turns the Home Flight Concierge into a loyalty-acquisition engine for the airline.

### `TMT-TEL-HOM-12` — Hotel Concierge

**Anchor partner — Marriott Bonvoy.**

| Partner | Loyalty program | Archetype | Value exchange |
|---|---|---|---|
| **Marriott** | Bonvoy | **B + C + E** | Hotel-direct booking via Marriott Bonvoy with brand take-share (avoids OTA margin); mobile-key delivery into the household vault; co-branded "Home + Bonvoy" SKU; on-property orchestration (room prefs, amenities, dining) |
| Hilton | Honors | B + C + E | Same shape |
| Hyatt | World of Hyatt | B + C + E | Smaller chain but high-LTV traveler base; ideal for B2B2C through corporate travel partnerships |
| IHG | One Rewards | B + C | |
| Accor | ALL | B + C | International coverage; particularly strong in EU markets |
| Four Seasons | Four Seasons Preferred | C only | Luxury segment; no public-API mobile-key |
| Boutique chains | (various) | A + B | Aggregator role — Mews, Cloudbeds, StayNTouch hospitality PMSs |

**Why hotels say yes:** every hotel-direct booking the Telco routes (instead of through Expedia or Booking) saves the hotel 12–18% of the room rate in OTA commission. The Telco can capture half of that savings (6–9% take rate) and still leave the hotel ahead vs OTA. **Marriott + Hilton + Hyatt + IHG = ~70% of US room-night inventory by major-chain coverage**; that's enough to make the offer a serious OTA-disintermediation play.

### `TMT-TEL-HOM-13` — OTA & Itinerary Builder

**Anchor partner — Expedia.**

| Partner | Archetype | Value exchange |
|---|---|---|
| **Expedia** (Expedia Group: Expedia, Hotels.com, Vrbo, Travelocity) | **B + A** | Multi-segment trip planning where direct partners can't cover the routing; Expedia provides search + book API; Telco pays Expedia per-booking rate; Expedia gets a high-intent customer with the customer's actual calendar context |
| Booking.com | B + A | Same shape; particularly strong in EU and international hotel inventory |
| Kayak (Priceline) | A | Meta-search, pre-book price intelligence; Telco pays for search; no booking transactions directly |
| Google Travel | A | Search-side intelligence; no commerce |
| Skyscanner | A | Same |

**The Expedia-vs-direct tension:** for any given hotel night, the Telco prefers to route direct to Marriott/Hilton/Hyatt because the take rate is better. Expedia is the **fallback** when (a) the customer's preferred chain has no availability, (b) the destination is a long-tail market where chain coverage is weak, or (c) the customer wants a one-stop package (flight + hotel + car). The Trip Orchestrator (HOM-10) makes the routing decision; the customer never sees the difference except in the price.

### `TMT-TEL-HOM-14` — Vacation Rental

**Anchor partner — Airbnb.**

| Partner | Archetype | Value exchange |
|---|---|---|
| **Airbnb** | **B + A + E** | STR booking via Airbnb API; check-in instructions auto-flow to household vault; host-comms surface in the Home Orchestrator (not in the Airbnb app); local-services bundling (Airbnb Experiences); identity-verification handoff (the household vault already has KYC'd identity) |
| Vrbo (Expedia Group) | B + A | Same shape; family-rental focus |
| Plum Guide | B + C | Curated luxury STR; higher take rate, lower volume |
| Sonder | B + C | Hospitality-flavoured STR (closer to a hotel-STR hybrid) |

**Why Airbnb says yes:** the household vault gives Airbnb a verified-identity, verified-presence, verified-calendar customer with low cancellation risk. The Home Vacation Rental Concierge also handles the **post-booking friction layer** (check-in instructions, host messages, key-pad codes, local-services bundling) that Airbnb currently solves with email + in-app messaging — the Telco's orchestrator delivers it more reliably and gets paid for doing so.

**Deal-structure note:** Airbnb's published take rate is 14–16% (combined host + guest fee). A Telco partnership at 3–5% per booking, in exchange for the Telco delivering verified high-quality guests, is well inside Airbnb's value envelope.

### `TMT-TEL-HOM-15` — Ground Mobility

| Partner | Type | Archetype | Value exchange |
|---|---|---|---|
| Uber | Rideshare | B + A | Airport transfer + in-destination mobility; per-ride rev-share |
| Lyft | Rideshare | B + A | Same |
| Hertz | Rental car | B + C | Loyalty-linked rental at corporate rates; Telco shares mobility revenue |
| Avis | Rental car | B + C | Same |
| Enterprise / National | Rental car | B + C | Same; B2B angle for corporate travel |
| Turo | P2P car-share | B + A | STR-of-cars model; Airbnb partnership pattern |
| Zipcar | Car-share | B | Urban niche |
| ChargePoint / EVgo / Tesla Supercharger | EV charging | A + B | Already in HOM-07 vehicle (home pack); extends to road-trip route planning |

**Strategic note:** ground mobility has the highest take-rate of any travel partner category (5–15%) because it's the most fragmented. Customers don't care which rideshare or rental brand wins their trip — they care about door-to-door time and cost. The Telco can be the neutral router and capture the routing margin.

### `TMT-TEL-HOM-16` — Local Experience

| Partner | Type | Archetype | Value exchange |
|---|---|---|---|
| OpenTable | Dining reservations | B + A | Per-cover fee ($1–3); Telco's customer pre-trip dining-prefs feed back to OpenTable |
| Resy (American Express) | Dining reservations | B + C | Higher-end dining; Amex-card co-marketing opportunity |
| Tock | Dining + experiences | B | Reservation deposits and tasting menus |
| Viator (Tripadvisor) | Tours & activities | B | 10–15% commission on tour bookings |
| GetYourGuide | Tours & activities | B | Same |
| Local-market specialists (e.g., Klook in APAC) | Tours | B | Regional coverage |

### `TMT-TEL-HOM-10` and `TMT-TEL-HOM-17` — Orchestrator and Reunification

These are Telco-owned services; no external partners. They consume signals from the other sub-agents and the home-pack agents. Partner attribution flows through whichever sub-agent executed the action.

## 3. Cross-cutting / foundational partners specific to travel

| Layer | Candidates | Why |
|---|---|---|
| Travel insurance | Allianz Travel, AIG Travel, TravelGuard, Berkshire Hathaway Travel Protection | D-archetype outcome share on trip-disruption coverage |
| Credit-card travel concierge | Chase Sapphire, Amex Platinum, Capital One Venture | C / displacement — Telco offering can either bundle with cards or displace card concierges |
| Identity verification | CLEAR, TSA Pre, Global Entry, Verified.Me | E-archetype standards; the household vault holds the tokenised reference, not the document |
| GDS (legacy) | Sabre, Amadeus, Travelport | B (limited) — only matters where direct-partner APIs are absent |
| Government APIs | TSA precheck status, FAA flight-status feeds, NOAA weather, State Dept travel advisories | A (free) — public data that improves agent quality |
| Loyalty exchanges | Points.com (Plusgrade), Capital One travel-points portal | A + B — points-as-currency rails |
| Payment | Telco bill-on-invoice, Apple Pay, Google Wallet, Stripe, Wise (FX) | Foundational; FX-aware for international |
| Pet care (during travel) | Rover, Wag | B — bundled into HOM-15 vacation continuity for pet-owning households |
| Home security during travel | ADT, Vivint (already HOM-05) | C — vacation arming mode is already covered by Home pack |

## 4. The three platform-defining partnerships for the Travel layer

Mirror of the canonical Home-pack analysis. The three that decide whether the Travel layer wins:

1. **At least one top-3 US airline (American, Delta, United).** Without a flagship airline partnership, IROPS recovery — the **wedge event** for the entire pack — has no demo. AA is the natural anchor for a Telco footprint that overlaps DFW / CLT / MIA hubs; Delta for ATL / DTW / SLC; United for ORD / IAH / SFO. Pick based on the Telco's regional concentration.
2. **Marriott Bonvoy or Hilton Honors.** The hotel mobile-key experience is the most viscerally differentiated travel UX the pack can deliver. **Bonvoy is the better partnership target** because Marriott has the deepest brand portfolio (30+ chains from Ritz-Carlton to Fairfield Inn) and the most-traveled loyalty base.
3. **Expedia Group OR a direct-merchant alternative.** Either Expedia / Booking.com to handle the long-tail and packages, or a direct-merchant model where the Telco builds bilateral relationships with the top 20 chains + 6 airlines and skips OTAs entirely. The Expedia partnership is **faster to launch** but **more dilutive on take rate**.

## 5. Phasing

| Phase | Timing | Partnerships to close |
|---|---|---|
| Phase 0 — Foundation (overlaps Home Pack Phase 0) | Q1–Q2 | Travel insurance partner (Allianz or similar); CSA Matter membership already in place from Home pack |
| Phase 1 — Anchor flight | Q3 | American Airlines (or Delta/United depending on footprint) — make IROPS recovery the first demo |
| Phase 2 — Anchor hotel | Q4 | Marriott Bonvoy — mobile-key + room-prefs as the second demo |
| Phase 3 — Coverage breadth | Year 2 | Hilton, Hyatt, IHG, Accor; Expedia or Booking; Airbnb |
| Phase 4 — Mobility + experience | Year 2 | Uber, Hertz, OpenTable, Viator |
| Phase 5 — Marketplace | Year 3+ | Open MCP listing for any travel partner (small chains, regional OTAs, niche experiences) |

## 6. Deal-structure heuristics (travel-specific)

| Archetype | Heuristic |
|---|---|
| A (Data-In) | For airlines & hotels, exchange disruption / inventory signal in return for **verified-intent customer signal** — the Telco knows who will fly Friday before the customer even searches |
| B (Action-Out) | Don't accept airline rebook-attribution at < $1 per accepted rebook; demand co-marketing of loyalty enrolments on the Telco bill as the C-archetype layer |
| C (Distribution) | Tie hotel-direct bundle pricing to OTA-rate-parity rules — never let the partner penalize the customer for booking through the Telco's orchestrator |
| D (Risk-share) | Travel insurance is the natural D-partner; demand independent disruption-event attribution methodology so payouts are auditable |
| E (Standards) | Push for MCP as the partner-API standard; the Telco's reference implementation should be open-source for non-commercial reuse |

## 7. Cross-references

- Services catalog this maps to: [`./05-services-catalog.md`](./05-services-catalog.md)
- Companion build-spec amendment: [`../../build-specs/apex-tmt-agentic-travel-amendment.md`](../../build-specs/apex-tmt-agentic-travel-amendment.md)
- Canonical archetype framework: [`../telco/06-partnership-map.md`](../telco/06-partnership-map.md)
