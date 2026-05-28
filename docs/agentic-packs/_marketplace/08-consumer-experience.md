# 08 — Consumer Experience

> _Draft — how a household discovers, subscribes to, uses, and churns Channels. The UX is modelled directly on the Telco's existing streaming-bundle UX, because that pattern is already validated in this customer base._

## 1. The "My Channels" surface

The customer's primary interaction is a single "My Channels" view, accessible from:

- The Telco's account-management app (mobile + web)
- The Home Orchestrator's voice interface
- The monthly bill (each Channel is a line item)

Each Channel surfaces with:

- Subscription status (active / paused / trial)
- Monthly price
- Bundle membership (if any)
- Engagement summary (runs in the last 30 days, actions executed)
- Direct controls (pause / resume / cancel / change plan)

## 2. Discovery and trial

| Stage | UX |
|---|---|
| Awareness | Bill insert + in-app card + cross-channel orchestrator suggestion ("households like yours added the Walmart Channel") |
| Demo | 14-day free trial of any new Channel; no card-on-file required (Telco bill is the billing instrument) |
| First use | Wedge event guided by the new Channel agent ("Try a Sazerac allocation alert for Buffalo Trace") |
| Conversion | After 14 days, subscription auto-activates; customer can cancel in one tap |
| Bundle upsell | After 60 days of multi-Channel use, surface bundle pricing ("save 30% on the Family Bundle") |

## 3. Consent and trust UX

When a customer adds a Channel, they see exactly:

| Element | Example for the Walmart Channel |
|---|---|
| What data the Channel reads | "Your grocery purchase history; your pantry signals; your pharmacy preferences" |
| What actions the Channel can take | "Place orders, request prescription refills, schedule auto-service" |
| What scopes are required | `purchases`, `health` (limited to pharmacy reconciliation), `vehicle` |
| What you can revoke later | "Any scope, any time — Channel pauses if a required scope is revoked" |

This consent panel is **always one tap deep** from the "My Channels" surface. The customer can revoke any scope at any time without contacting support.

## 4. Cross-Channel intent routing UX

When the customer issues an intent ("we need to restock", "book the flight", "schedule the oil change", "find a bottle of Eagle Rare"), the Home Orchestrator decides which Channel handles it:

| Intent | Channel | Backing service code |
|---|---|---|
| "We need milk" | Home → Walmart | `HOM-01` + `RTL-01` |
| "I need to reschedule my Sunday flight" | Travel | `HOM-11` |
| "Set up my service appointment" | Mobility | `MOB-02` |
| "Get me a bottle of Eagle Rare" | CPG / Beverage | `BEV-01` |
| "Mom didn't seem right today" | Home eldercare | `HOM-03` |

The customer does not have to know which Channel handles which intent. The orchestrator routes; if multiple Channels could plausibly handle an intent, it picks the best one based on subscription, preferences, and confidence — and surfaces the choice for transparency ("Routing to Walmart Retail — change to Costco?").

## 5. Subscription management

| Action | UX |
|---|---|
| Add Channel | One tap from "My Channels"; trial starts immediately |
| Pause Channel | Pauses the Channel without losing settings; un-pause anytime |
| Cancel Channel | One tap; immediate effective for next bill cycle |
| Bundle swap | One tap from "à la carte" to "Family Bundle" — Telco settles the prorating |
| Per-Channel preferences | Edit defaults (e.g., "always prefer Marriott") inside each Channel's page |

This is **the same UX pattern** as streaming-bundle management today. No new mental model required.

## 6. Failure-mode UX

| Failure | What the customer sees |
|---|---|
| Channel partner-side outage | Banner in Channel page: "Marriott connection temporarily unavailable. Booking via Expedia fallback." |
| MCP integration broken | Orchestrator silently falls back to partner-direct apps; banner explains briefly |
| Consent revoked mid-action | Action queued; customer prompted to restore scope or confirm cancellation |
| Bundle eligibility lost | Auto-converts to à-la-carte pricing; notification sent |
| Multiple Channels disagree on routing | Orchestrator surfaces the choice; never silently picks behind the customer's back |

The principle: **the customer is never surprised**. Every Channel state change, every orchestrator decision, every consent change is auditable in the vault and surfaced in the "My Channels" view.

## 7. Mobile / desktop / voice parity

| Surface | Required parity |
|---|---|
| Mobile app | Full feature set; primary surface for HITL approvals |
| Web (browser) | Full feature set; primary surface for bundle / billing changes |
| Voice (smart speaker) | Subset focused on intent issuance and approval confirmations |
| Bill (PDF + paper) | Read-only summary; line-item explanation per Channel |
| Telco contact center | CSR can see (with appropriate consent) the same "My Channels" view; cannot read vault data |

The marketplace UX is the **first major Telco surface** that is built with vault-side privacy from day one — the contact-center CSR sees what the customer chose to share with the CSR, no more.

## 8. International / localization

| Element | US default | Localization considerations |
|---|---|---|
| Currency | USD | Per-market FX for action commerce |
| Loyalty programs | US-anchored | EU / APAC need separate program seeds |
| Compliance | US privacy regs | GDPR / EU AI Act / APAC privacy each materially change consent UX |
| Age-gating (CPG) | State-by-state | Different national frameworks abroad |

These are addressed in market-specific extensions of each Channel pack as international rollout phases land.
