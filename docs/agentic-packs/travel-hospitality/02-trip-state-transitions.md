# 02 — Trip State Transitions

> The household state machine the pack operates against. Trip-mode is not a separate platform — it is a posture transition of the existing household. Every state transition has a **trigger**, a set of **sub-agent state changes**, and a set of **partner-side handoffs**.

## 1. The state machine

```
                     ┌──────────────────────┐
                     │                      │
                     │      AT-HOME         │
                     │  (steady-state)      │
                     │                      │
                     └──────────┬───────────┘
                                │ trip detected (calendar / booking)
                                │ T-minus 14 days
                                ▼
                     ┌──────────────────────┐
                     │                      │
                     │     DEPARTING        │
                     │ (T-14 → T-0 hours)   │
                     │                      │
                     └──────────┬───────────┘
                                │ "wheels up" / "drove away"
                                ▼
                     ┌──────────────────────┐
                     │                      │
                     │    IN-TRANSIT        │
                     │  (in motion)         │
                     │                      │
                     └──────────┬───────────┘
                                │ "wheels down + arrived at lodging"
                                ▼
                     ┌──────────────────────┐
                     │                      │
                     │    ON-LOCATION       │
                     │  (at destination)    │
                     │                      │
                     └──────────┬───────────┘
                                │ check-out / departure trigger
                                ▼
                     ┌──────────────────────┐
                     │                      │
                     │     RETURNING        │
                     │  (in motion home)    │
                     │                      │
                     └──────────┬───────────┘
                                │ "arrived home"
                                ▼
                     ┌──────────────────────┐
                     │                      │
                     │     REUNIFIED        │
                     │  (back at home)      │
                     │                      │
                     └──────────────────────┘
                                │
                                ▼ T+24 hours
                            AT-HOME
```

The state lives on `Trip.current_state` in the Silver layer (see [`03-erd-and-postgres.md`](./03-erd-and-postgres.md)) and is the **single source of truth** for which sub-agents are active and which postures are in effect.

## 2. State definitions and triggers

| State | Trigger to enter | Trigger to exit | Typical duration |
|---|---|---|---|
| **At-Home** | Trip completed > 24 h ago, or no trip booked within 14 days | First trip event detected within 14 days | Default state |
| **Departing** | Trip booking confirmed AND `trip.depart_ts - now() < 14 days` | Wheels-up event / vehicle-departure event | 0–14 days |
| **In-Transit** | Wheels-up / vehicle-departure detected | Arrival at lodging confirmed (geo / hotel check-in / STR keypad) | 1 h – 36 h |
| **On-Location** | Arrival confirmed at lodging | Check-out / vehicle-departure for return leg | 1 day – 30 days |
| **Returning** | Check-out / return-leg departure | Geofence + sustained Wi-Fi at home gateway | 1 h – 36 h |
| **Reunified** | Geofence + sustained Wi-Fi at home gateway | T+24h or first home agent action | 24 h |

Triggers are emitted by:

- **Calendar** events (Outlook, Google, iCloud) with travel keywords or PNR attachments
- **Booking confirmations** received via partner integrations (AA, Marriott, Expedia, Airbnb)
- **Geofence** signals from the customer's phone
- **Wi-Fi presence** at the household gateway / ONT
- **Vehicle telematics** (drove away, EV charge state, parking-lot geofence at airport)
- **Wearable signals** (heart rate during takeoff is a remarkably reliable wheels-up confirmation for short trips)

## 3. Per-state sub-agent posture

### At-Home (steady-state)

All home agents run normally:

| Home agent | Posture | Trip-mode interaction |
|---|---|---|
| HOM-01 grocery | Normal replenishment | — |
| HOM-02 energy | Tariff-aware optimization | — |
| HOM-03 eldercare | Normal monitoring | — |
| HOM-04 maintenance | Normal triage | — |
| HOM-05 security | Normal arming | — |
| HOM-06 wellness | Normal coaching | — |
| HOM-07 vehicle | Normal scheduling | — |
| HOM-08 entertainment | Normal personalization | — |

Trip-mode sub-agents (`HOM-10..17`) are **inactive** — they monitor calendar / booking inbox but emit no actions.

### Departing (T-14 → T-0)

| Home agent | Posture change |
|---|---|
| HOM-01 grocery | Schedule a "pause" date for recurring orders; schedule "fresh restock" for `trip.return_ts - 24h` |
| HOM-02 energy | Schedule vacation setback for `trip.depart_ts + 6h`; pre-heat/cool for `trip.return_ts - 6h` |
| HOM-03 eldercare | Confirm coverage plan with designated in-state contact; intensify monitoring for non-traveling members |
| HOM-04 maintenance | Defer non-urgent service-call dispatches to post-return |
| HOM-05 security | Stage "vacation arming" with temp access codes (pet sitter, neighbour) |
| HOM-06 wellness | Pre-trip wellness baselining for travelers (sleep, hydration, stress) |
| HOM-07 vehicle | Pre-trip EV charge to 90%; ensure airport-parking telematics enabled; vehicle-left-at-home flag |
| HOM-08 entertainment | Sync offline content for the trip; pause home-only DVR / live recordings |

Trip-mode sub-agents become **active**:

- HOM-10 trip-orchestrator: takes over routing of trip intents
- HOM-13 OTA & itinerary: finalizes any unbooked legs
- HOM-14 vacation rental: confirms STR check-in instructions, arranges greeter/host comms
- HOM-15 ground mobility: books airport transfer, rental car pickup

### In-Transit

| Home agent | Posture |
|---|---|
| All home agents | Vacation-posture; no proactive household actions; HITL gates pause |

Trip-mode sub-agents active:

- HOM-11 flight concierge: tracks flight status, IROPS detection, gate changes, baggage status
- HOM-15 ground mobility: connects to ride-hail or rental car
- HOM-10 trip-orchestrator: coordinates handoff to ON-LOCATION on arrival

### On-Location

Home agents continue in vacation posture. Trip-mode sub-agents active:

- HOM-12 hotel concierge: mobile-key delivery, room preferences, on-property orchestration
- HOM-14 vacation rental: host comms, local services bundling
- HOM-16 local experience: dining, activities, tours
- HOM-15 ground mobility: in-destination mobility

The orchestrator may also surface **eldercare alerts from home** (HOM-03) on a separate "back-home status" channel, decoupled from trip-mode actions.

### Returning

Mirror of In-Transit. Trip-mode sub-agents active for return flight / vehicle / mobility.

HOM-17 return-reunification begins preparing the home:

- Pre-cool/heat HVAC for arrival
- Place fresh-restock grocery order (HOM-01)
- Re-arm security to standard mode (HOM-05)
- Resume maintenance triage (HOM-04)

### Reunified (T+24h)

Welcome-home posture:

- Wellness check on traveler (sleep debt, hydration recovery — HOM-06)
- Vehicle post-trip status (mileage delta, maintenance flags — HOM-07)
- Pet-related catch-up notifications (HOM-15 / vacation continuity)
- Reconciliation of any deferred home actions

At T+24h, the household returns to **At-Home** steady state.

## 4. Cross-trip state — the calendar dimension

A household can have multiple trips in different states simultaneously:

- Customer A is on a business trip (ON-LOCATION) while Customer B (same household) is mid-flight (IN-TRANSIT) to a different destination
- Family is mid-trip (ON-LOCATION) but has a separate trip booked for next month (DEPARTING-not-yet)

The state machine is **per-person**, not per-household, with a household-level **rollup state** that drives home-agent posture:

```
household.rollup_state =
    "fully-occupied"    if all members at home
    "partially-away"    if some members away
    "fully-away"        if no household members at home
```

Home agents key off `household.rollup_state` for posture (e.g., HVAC vacation setback fires only on `fully-away`). Trip sub-agents key off `person.trip_state` for per-traveler actions.

## 5. Failure modes and graceful degradation

| Failure | Pack behaviour |
|---|---|
| Calendar parse miss (trip not detected) | Customer can manually create a `Trip` via app. Booking confirmation auto-attaches retroactively. |
| Booking confirmation arrives after wheels-up | State machine catches up; no consumer-facing inconsistency |
| Geofence flap (false IN-TRANSIT) | Wi-Fi-at-home signal overrides; state corrects within 5 minutes |
| Wearable / phone offline during trip | Calendar + partner-side check-in signals carry the state machine |
| Multi-traveler partial-state mismatch | Per-person state; household-rollup recomputed every state change |
| Customer cancels trip mid-state | All trip-mode agents flush queues; home agents revert to At-Home posture |

State transitions are logged in `silver.tmt_hom.trip_state_event` for auditability. The household can replay the full state history in their vault export (see [`09-portability-open-home.md`](./09-portability-open-home.md)).
