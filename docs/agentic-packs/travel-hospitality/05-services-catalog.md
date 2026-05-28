# 05 — Services Catalog (`TMT-TEL-HOM-10..17`)

> Eight new sub-agents that extend the Telco Home Agentic family. Each is independently subscribable on the same Telco bill, each conforms to the existing agent contract (archetype, oversight modes, HITL gates, KPIs), and each maps 1:1 to a scenario folder and a partner archetype.

## Service codes

| Service code | Scenario folder | Agent YAML | Description | Headline KPI |
|---|---|---|---|---|
| `TMT-TEL-HOM-10` | `TMT-CX-30-home-trip-orchestrator` | `tmt/20-home-trip-orchestrator.yaml` | Trip-mode meta-orchestrator; routes intents to HOM-11..17 | Successful trip intent rate |
| `TMT-TEL-HOM-11` | `TMT-CX-31-home-flight-concierge` | `tmt/21-home-flight-concierge.yaml` | Flight booking, status, IROPS rebooking, seat upgrade | IROPS recovery time (min) |
| `TMT-TEL-HOM-12` | `TMT-CX-32-home-hotel-concierge` | `tmt/22-home-hotel-concierge.yaml` | Hotel booking, mobile key, on-property orchestration | On-property NPS |
| `TMT-TEL-HOM-13` | `TMT-CX-33-home-ota-itinerary-builder` | `tmt/23-home-ota-itinerary-builder.yaml` | Multi-segment trip planning via OTA partners | Trip-build time saved |
| `TMT-TEL-HOM-14` | `TMT-CX-34-home-vacation-rental` | `tmt/24-home-vacation-rental.yaml` | STR check-in, host comms, local-services bundling | Check-in friction reduction |
| `TMT-TEL-HOM-15` | `TMT-CX-35-home-ground-mobility` | `tmt/25-home-ground-mobility.yaml` | Airport transfer, rental car, charging on route | Door-to-door time |
| `TMT-TEL-HOM-16` | `TMT-CX-36-home-local-experience` | `tmt/26-home-local-experience.yaml` | Dining, activities, tours, reservations | Bookings completed per trip |
| `TMT-TEL-HOM-17` | `TMT-CX-37-home-return-reunification` | `tmt/27-home-return-reunification.yaml` | Pre-arrival home prep + post-arrival reconciliation | Time-to-home-baseline post-trip |

## Anchor partner mapping (highlights — full set in `06-partnership-map.md`)

| Service | Anchor partners |
|---|---|
| HOM-11 Flight Concierge | **American Airlines (AA AAdvantage)**, Delta (SkyMiles), United (MileagePlus), Southwest, JetBlue, Alaska |
| HOM-12 Hotel Concierge | **Marriott (Bonvoy)**, Hilton (Honors), Hyatt (World), IHG (One Rewards), Accor (ALL), Four Seasons |
| HOM-13 OTA & Itinerary | **Expedia**, Booking.com, Kayak, Google Travel, Skyscanner |
| HOM-14 Vacation Rental | **Airbnb**, Vrbo, Plum Guide, Sonder |
| HOM-15 Ground Mobility | Uber, Lyft, Hertz, Avis, Enterprise, Turo, Zipcar, Tesla Supercharger, ChargePoint |
| HOM-16 Local Experience | OpenTable, Resy, Tock, Viator, GetYourGuide |

## Archetype mapping

| Service | Archetype | Oversight | Notable HITL gates |
|---|---|---|---|
| `TMT-TEL-HOM-10` | `F4-orchestrator-with-subagents` | HOTL | Routes only; writes flow through sub-agents |
| `TMT-TEL-HOM-11` | `F1-continuous-monitor-hitl-alert` | HITL | IROPS rebooking > $300 fare difference |
| `TMT-TEL-HOM-12` | `F3-predictive-trigger-workflow-aware` | HITL | Room-rate changes > 15% on rebook |
| `TMT-TEL-HOM-13` | `F2-event-cluster-pattern-match` | HITL | Booking total > $500 |
| `TMT-TEL-HOM-14` | `F3-predictive-trigger-workflow-aware` | HITL | Cancellation / refund flow |
| `TMT-TEL-HOM-15` | `F2-event-cluster-pattern-match` | HOTL | Auto-book within budget; HITL above |
| `TMT-TEL-HOM-16` | `F2-event-cluster-pattern-match` | HOTL | Reservation conflicts only |
| `TMT-TEL-HOM-17` | `F4-orchestrator-with-subagents` | HOTL | Resumes home agents only; no external writes |

## Subscription bundle additions

Three new packaging options on top of the Home Agentic bundles:

| Bundle | Adds | Monthly price (illustrative) |
|---|---|---|
| **Trip Add-On** | HOM-10, HOM-11, HOM-13, HOM-15, HOM-17 (orchestrator + flight + OTA + mobility + reunification) | +$7.99 |
| **Travel Premium** | Trip Add-On + HOM-12 hotel + HOM-14 STR + HOM-16 experience | +$14.99 |
| **Family Travel** | Travel Premium with up to 6 traveler profiles + minor-traveler protection | +$19.99 |

Trip Add-On stacks on any Home bundle. Travel Premium is the default upgrade path for the Family-bundle subscriber who travels > 4 times per year.

## Action-commerce take-rate envelope

| Service | Typical partner take rate | Notes |
|---|---|---|
| HOM-11 flight | 1–3% of ticket | Airlines pay low %; loyalty co-attribution often the real value |
| HOM-12 hotel | 5–10% of stay | Hotel-direct rates with brand take-share; OTA-routed share is smaller |
| HOM-13 OTA | 1–3% of booking | OTA-direct take rate after Expedia/Booking margin |
| HOM-14 STR | 3–6% of stay | Airbnb/Vrbo host-fee share or direct STR partnership |
| HOM-15 ground | 5–15% of fare | Ground mobility is the highest take-rate segment |
| HOM-16 dining | $1–3 per cover + experience-fee share | OpenTable/Resy diner-fee or Viator commission |
| HOM-17 reunification | $0 (Telco-paid orchestrator) | Indirect value via home-agent re-engagement |

See [`06-partnership-map.md`](./06-partnership-map.md) for per-partner archetype assignments and deal-structure heuristics.

## Cross-references

- Agent YAMLs: [`packages/apex-agents/src/apex_agents/catalogs/tmt/2{0..7}-*.yaml`](../../../packages/apex-agents/src/apex_agents/catalogs/tmt/)
- Scenario folders: [`docs/scenarios/TMT/customer-experience/TMT-CX-3{0..7}-*`](../../scenarios/TMT/customer-experience/)
- Bronze/Silver/Gold lineage: [`./04-medallion-bronze-silver-gold.md`](./04-medallion-bronze-silver-gold.md)
- Companion build-spec amendment: [`../../build-specs/apex-tmt-agentic-travel-amendment.md`](../../build-specs/apex-tmt-agentic-travel-amendment.md)
