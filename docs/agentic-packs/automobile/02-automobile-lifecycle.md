# 02 — Automobile Lifecycle State Machine

> The vehicle ownership lifecycle, modeled as the household-vehicle state machine the Channel operates against. Each state has triggers, active sub-agents, and partner-side handoffs — mirrors the trip state machine pattern from the Travel Channel.

## 1. The lifecycle states

```
                ┌──────────────────────┐
                │                      │
                │     RESEARCHING      │ ← intent: "we may need a vehicle"
                │                      │
                └──────────┬───────────┘
                           │ candidate shortlist confirmed
                           ▼
                ┌──────────────────────┐
                │                      │
                │      SHOPPING        │ ← inventory + pricing comparison + test drives
                │                      │
                └──────────┬───────────┘
                           │ decision to purchase
                           ▼
                ┌──────────────────────┐
                │                      │
                │     PURCHASING       │ ← financing + insurance + dealer + DMV all align
                │                      │
                └──────────┬───────────┘
                           │ signature + drive home
                           ▼
                ┌──────────────────────┐
                │                      │
                │       OWNING         │ ← long steady-state
                │   (warranty period)  │   (5-7 years; 3-5 years for lease)
                │                      │
                └──────────┬───────────┘
                           │ ongoing-ownership signals
                           ▼
                ┌──────────────────────┐
                │                      │
                │       OWNING         │ ← long steady-state continued
                │   (post-warranty)    │   independent / aftermarket service
                │                      │
                └──────────┬───────────┘
                           │ replacement trigger
                           ▼
                ┌──────────────────────┐
                │                      │
                │   PREPARING-RESALE   │ ← valuation, listing, condition prep
                │                      │
                └──────────┬───────────┘
                           │ trade-in / sale / donate
                           ▼
                ┌──────────────────────┐
                │                      │
                │       RESOLD         │ ← terminal state for this vehicle
                │                      │
                └──────────────────────┘
                           │
                           ▼ (often loops back via RESEARCHING for replacement)
                       RESEARCHING (next vehicle)
```

The state lives on `vehicle.lifecycle_state` in Silver. A household typically has 1–4 vehicles each in different states simultaneously (Dad's truck is OWNING-post-warranty; family SUV is OWNING-warranty; teen-driver-candidate is RESEARCHING).

## 2. State definitions and triggers

| State | Trigger to enter | Typical duration |
|---|---|---|
| **Researching** | User intent OR proactive trigger (current vehicle approaching milestone) | 1–8 weeks |
| **Shopping** | Candidate shortlist of 2–4 vehicles confirmed | 1–4 weeks |
| **Purchasing** | Decision-to-buy committed; offer extended | 1–14 days |
| **Owning — Warranty** | Vehicle acquired, under OEM warranty | 3–5 years (lease) or 3–6 years (purchase) |
| **Owning — Post-warranty** | Manufacturer warranty expires | 0–15+ years |
| **Preparing-Resale** | Replacement trigger fires (age, mileage, repair-cost trend, family-size change, lease-end) | 2–8 weeks |
| **Resold** | Trade-in completed, private sale closed, or donation processed | terminal |

## 3. Proactive replacement triggers

The Channel's most valuable predictive signal: when to start surfacing the **Researching** state for a vehicle already in **Owning** state. Triggers:

| Trigger | Source | Signal strength |
|---|---|---|
| Lease-end within 6 months | TFS / Ford Credit / Ally lease data | Hard — must replace |
| Vehicle age > 10 years OR mileage > 150K | Telematics | Soft |
| Repair-cost trend > $200 / mo trailing 6 mo | Service history | Medium |
| Family-size change (new child, child driving age) | Vault calendar / consent updates | Hard for some families |
| Income increase signal | Banking integration (with consent) | Soft |
| Powertrain transition signal (gas → EV) | Customer preference shift; charging-network access | Soft |
| Recall severity > 4 + remedy unavailable | NHTSA + OEM | Hard occasionally |

The orchestrator weighs triggers; surfaces **Researching** state only when confidence is high enough not to be annoying.

## 4. Per-state active sub-agents

### Researching

- **AUT-01 Discovery** primary
- HOM-07 vehicle (Home Channel) reads current-vehicle telemetry to inform replacement
- MOB-03 next-vehicle (Mobility Channel) coordinates if customer has Toyota

### Shopping

- AUT-01 continues for ongoing comparison
- AUT-03 Financing begins pre-approval shopping
- AUT-04 Insurance begins quote shopping
- AUT-08 Resale-prep activates if trade-in candidate exists

### Purchasing

- **AUT-02 Purchase** primary
- AUT-03 Financing executes pre-approval
- AUT-04 Insurance binds policy
- AUT-08 Resale executes trade-in

### Owning — Warranty

- HOM-07 vehicle (Home), MOB-02 dealer (Mobility for Toyota), RTL-03 Walmart Auto Care (Retail)
- **AUT-05 Aftermarket** for accessories (low priority within warranty)
- **AUT-06 Charging / fueling** active
- AUT-07 Fleet if multi-vehicle

### Owning — Post-warranty

- Same as warranty except service routing shifts toward independent shops + AUT-05 parts
- AUT-04 Insurance reviews annually; potential to re-shop

### Preparing-Resale

- **AUT-08 Resale** primary
- AUT-01 Discovery activates for replacement vehicle
- AUT-08 coordinates valuation across CarMax, Carvana, AutoNation, KBB Instant Cash Offer, private-sale tools

### Resold

- Terminal for this vehicle
- AUT-04 Insurance removes vehicle from policy
- HOM-07 + MOB-* drop vehicle from device graph
- DMV automation if state requires

## 5. Multi-vehicle households

Per-vehicle state independent. Household-rollup:

```
household.vehicle_inventory_state =
    sum over vehicles {Researching, Shopping, Purchasing, Owning, Preparing-Resale, Resold}
```

Used to compute household-fleet-level metrics (e.g., `next_likely_purchase_window` for the next-vehicle-decisioning signal).

## 6. Failure modes

| Failure | Pack behaviour |
|---|---|
| Dealer-side data stale (vehicle "in stock" already sold) | AUT-02 falls back gracefully, requests fresh inventory |
| Financing pre-approval declined | AUT-03 surfaces; never silent failure |
| Insurance quote rejected (high risk household) | AUT-04 expands carrier set; surfaces tradeoffs |
| Trade-in valuation < expected | AUT-08 surfaces; private-sale option always offered as fallback |
| DMV / title delay | AUT-02 tracks; notifies customer |
| Lease-end deadline missed | Hard failure; AUT-08 / MOB-04 escalate with HITL |

State transitions logged in `silver.tmt_aut.vehicle_lifecycle_event` for audit + replay.
