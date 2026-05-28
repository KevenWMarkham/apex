# 01 — Business Model

> Toyota anchors a Channel that orchestrates multi-OEM household-fleet mobility — telematics, dealer service, recalls, next-vehicle decisioning, financing, insurance. Toyota gains a high-LTV customer surface that Toyota-direct apps cannot replicate alone; the Telco gains the deepest action-commerce vertical in the marketplace.

## 1. What the Toyota Channel is

Toyota already has:

- Toyota Connected Services (telematics, remote-start, vehicle health)
- Toyota Financial Services (loans, leases, end-of-lease coordination)
- Toyota Insurance Management Solutions (telematics-based UBI)
- ~1,200 US Toyota / Lexus dealers
- ~30M vehicles in the active US installed base
- The ToyotaCare scheduled maintenance program

The Toyota Channel surfaces all of these inside the Home Orchestrator as a coordinated set of subscribable agents. It does **not** replace the Toyota app for Toyota-direct power users; it **adds** the multi-vehicle, multi-OEM, household-state orchestration layer that the Toyota app cannot deliver.

## 2. Why Toyota says yes

| Benefit to Toyota | Why it matters |
|---|---|
| Direct billing on Telco bill for Toyota Connected subscription | Lower CAC + lower churn vs Toyota-direct paid acquisition |
| Verified-context household signal | Eldercare-aware service scheduling, family-size aware next-vehicle |
| TFS lease / loan refi cross-sell at scale | Captive-finance attach without the dealer-only friction |
| TIMS UBI enrolment via the marketplace | Telematics-data-rich underwriting funnel |
| Recall-completion rate improvement | Reduces NHTSA exposure; improves dealer-side throughput |
| Multi-Telco distribution from one MCP integration | Build once, list across every Telco partner |

## 3. The recall-reconciliation wedge

```
Household: 2 Toyotas + 1 Honda + 1 e-bike.

NHTSA recall feed → Toyota Sienna 2021 floor-mat retention recall (campaign 21V-573).
Honda recall feed → 2019 CR-V fuel-pump recall (campaign 23V-340).

Mobility Channel orchestrator:
  1. Cross-references recalls against household-fleet inventory
  2. Pulls dealer availability (nearest Toyota + nearest Honda)
  3. Reads HOM-07 vehicle telematics → schedules during a "low-usage" window
  4. Coordinates with HOM-15 (ground mobility) for rideshare during service
  5. Surfaces single notification: "Two recalls. Toyota: 45 min at Lakeside Toyota
     Thursday 9 AM. Honda: 30 min at Honda West Saturday 11 AM. Tap to confirm."
```

The customer would have ignored both NHTSA emails. The orchestrator collapses them into a single approval. Toyota's recall-completion rate goes up; the customer's safety goes up; the Telco gets a coordinated commerce signal.

## 4. Three revenue layers — applied

| Layer | Mobility-specific motion |
|---|---|
| Consumer subscription | $9.99 / mo (Toyota Channel includes the multi-OEM fleet view) |
| Action commerce | 3–6% on dealer service-call commerce; per-quote attribution on TFS refi |
| Outcome / risk-share | TIMS UBI premium-discount share; auto-insurance loss-ratio reduction |

## 5. Per-household economic envelope

| Source | Annual per Toyota-Channel HH |
|---|---|
| Subscription ($9.99 / mo × 12) | $120 |
| MOB-01 connected-services attribution | $20–40 |
| MOB-02 dealer service action commerce (4 visits × $200 × 5%) | $40 |
| MOB-03 next-vehicle decisioning (every 5–7 years × commission share) | $80–150 amortized |
| MOB-04 TFS + TIMS rev-share | $40–100 |
| **Blended GP / HH / yr** | **$300–450** |

At 20–35% attach × 20M HH, the Mobility Channel produces **~$1.2–3.2B / yr in Telco GP**.

## 6. Why other OEM apps can't displace this

| Alternative | Disqualifier |
|---|---|
| Toyota app (direct) | Toyota-only; cannot orchestrate Honda or Ford |
| Ford SYNC app | Same — Ford-only |
| GM OnStar | Same — GM-only |
| Tesla app | Same — Tesla-only |
| CarGurus / AutoTrader | No telematics; no service network; no household state |
| Insurance-carrier apps (State Farm Drive Safe, etc.) | UBI-only; no service / next-vehicle |

The Channel's neutrality is the moat. Toyota wins by being the default for Toyota vehicles in the household, not by being the only option for everything.
