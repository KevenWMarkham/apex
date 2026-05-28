# 08 — Consumer Business Case

> _Draft — the case made to a traveling household. IROPS recovery is the wedge event; loyalty-portfolio visibility is the everyday hook; vacation continuity is the trust differentiator._

## 1. Why the household says yes

Three things they recognize:

1. **The IROPS save.** Cancelled flight at 11 PM rebooked through to the right routing before the airline CSR queue clears. One save = a year of subscription paid for in customer perception.
2. **The loyalty-portfolio view.** A single household-level view of AA AAdvantage + Marriott Bonvoy + Hertz Gold + Airbnb + Expedia One Key. Today this is fragmented across six apps and three email accounts. The Telco delivers it in one place.
3. **The home-and-trip continuity.** Mom's still being monitored. The dog still gets fed. The HVAC still doesn't waste energy. The pantry still gets restocked the day before return.

## 2. WTP anchor — IROPS recovery

A typical leisure traveler experiences 1 significant trip disruption per year (delay > 3h, cancellation, baggage lost, hotel walk). Each disruption costs:

| Component | Per-event cost |
|---|---|
| Customer time on the phone with CSR | 45–90 min × $15/hr = $11–22 |
| Avoidable additional fares / fees (suboptimal rebook) | $50–200 |
| Emotional cost (missed event, child's recital, etc.) | $100–500 (high variance) |
| Hotel / per-diem cost when stranded | $150–400 |
| **Total per-event impact** | **$300–1,100** |

A consumer who experiences even one successful IROPS recovery in a year retroactively values the $7.99/mo Trip Add-On as **paying for itself ten times over**.

## 3. WTP — loyalty portfolio visibility

The average affluent traveler has 4–10 active loyalty accounts. Today:

| Friction | Today |
|---|---|
| Knowing total points value | Manually log into 4–10 apps, do math |
| Knowing tier-progress | Same |
| Knowing redemption opportunities | Email digests + manual search |
| Knowing transferable / partner programs | Specialty blogs (The Points Guy, etc.) |

The Telco delivers the household-level rollup automatically. Captured value: 10–20 min/wk of saved attention + ~$200–500/yr in better redemption choices.

## 4. WTP — vacation continuity

The largest source of trip anxiety for households with elderly parents, pets, or chronic-condition members is **what's happening at home while we're away**. Vacation Continuity converts that anxiety into a quiet reassurance signal:

- "Mom completed her ADL routine today — score within baseline"
- "Dog ate full meal at 6:42 PM (Rover-cam confirmed)"
- "Front door not opened since 9 AM Friday; security armed"
- "HVAC in vacation setback; pre-cool starts 16 hrs before your return"

This is the **trust-asymmetry argument** from the Home pack, but applied to a moment when the customer is most worried about home. Captured value: **emotional CLV impact** that doesn't show up cleanly in a P&L but drives retention and referral.

## 5. Adoption funnel — illustrative

| Stage | Conversion rate envelope | Notes |
|---|---|---|
| Home Agentic subscribers | 100% (denominator) | |
| Took ≥1 trip in last 12 mo | 70–85% | Strong correlation with broadband / 5G subscriber base |
| Aware of Travel Add-On | 60–75% | Bill-insert + in-app prompt at booking-confirmation parse |
| Trigger via wedge event | 20–35% | IROPS demo or loyalty-portfolio "wow" moment |
| Active subscriber 90 days post-trigger | 75–85% | Stickiness driven by next trip's perceived value |

## 6. What kills the consumer case

- **Bad first booking.** If the first trip the Home Trip Orchestrator manages mis-handles a connection, the customer extrapolates. **Pre-flight reliability testing is non-negotiable.**
- **Airline / hotel side breaks the MCP integration.** A partner-side outage that the customer experiences as a Telco failure is brand-damaging. The Trip Orchestrator must **fail gracefully** to airline-direct / hotel-direct apps with a clear handoff message.
- **Privacy headline on travel-document storage.** The pack stores only tokenised references to passport / TSA Pre / Global Entry. Any deviation from that — even briefly — kills the trust posture. See [`09-portability-open-home.md`](./09-portability-open-home.md).
