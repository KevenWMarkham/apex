# 08 — Consumer Business Case (Mobility Channel)

> _Draft — recall-reconciliation wedge; multi-vehicle household coordination; next-vehicle decisioning_

## Wedge — recall reconciliation

NHTSA estimates ~25% of recalled vehicles never get repaired despite multiple owner notifications. The Mobility Channel:

1. Cross-references NHTSA + OEM recall feeds against the household fleet
2. Auto-schedules service at the appropriate dealer / authorized shop
3. Coordinates loaner / rideshare via HOM-15
4. Tracks completion + closes the loop on the recall record

Per-household value: avoided one $4–15K safety incident per 5–10 years × probability = $200–600 / yr in expected-value safety improvement, **not even counting** the convenience of not having to remember.

## Multi-vehicle household coordination

The average US household owns 1.8 vehicles, often different OEMs. Today, this means:
- Two OEM apps, two service-due notifications, two recall feeds, two insurance carriers, two financing entities
- Disconnected — no household-level view

The Mobility Channel collapses all of this into a single household-fleet view. The single rollup is the daily-utility hook.

## Next-vehicle decisioning

Buying a vehicle is one of the highest-stakes household purchases (every 5–7 years). The Channel:
- Tracks repair-cost trend on existing vehicles → recommends replacement timing
- Tracks lease-end date → coordinates end-of-lease decisions
- Tracks family-size changes → recommends segment changes (sedan → SUV)
- Pulls real-time inventory from Toyota + bench OEMs → presents options matched to the household's needs

This is the kind of high-emotional-stakes, low-frequency, high-value decision that the Channel earns customer loyalty around.

## Adoption funnel

| Stage | Envelope |
|---|---|
| Home Channel subscribers | 100% |
| Aware of Mobility Channel | 60–75% |
| Triggered to trial | 20–30% |
| Active at 90 days | 80–88% |
| Cross-attach to MOB-04 finance / insurance | 40–55% over 24 months |

## What kills the Channel

- **OEM-direct app political resistance.** Toyota dealers see this as competition rather than collaboration.
- **Recall-completion liability.** The Channel must clearly delineate "we notified" vs "OEM is responsible" for compliance.
- **Insurance-state regulations.** UBI shares vary materially state-to-state.
