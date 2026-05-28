# Agentic Channel Marketplace — APEX Meta-Pack

> The FIOS-of-AI metaphor at its fullest expression. The Telco operates a **Channel Store for agentic services** the way it operates a Channel Store for digital content today (Hulu, ESPN, Discovery, Disney+, Max). Every major consumer brand publishes a **Channel** — a packaged set of agentic services — that the household subscribes to on its existing Telco bill. The Home Orchestrator routes intents across channels. Channels share the vault, the consent ledger, and the partner MCP protocol.

**Status:** Draft
**Primary author:** tmt-practice-lead@deloitte.com
**Sibling packs:** [`telco/`](../telco/) (Channel 1 — Home), [`travel-hospitality/`](../travel-hospitality/) (Channel 2 — Travel), [`retail/`](../retail/) (Channel 3 — Retail), [`mobility-auto/`](../mobility-auto/) (Channel 4 — Mobility), [`cpg-adult-beverage/`](../cpg-adult-beverage/) (Channel 5 — CPG / Beverage)

## The thesis in one paragraph

Telcos already make billions by bundling other people's content on their bill (Hulu, ESPN, Discovery, Disney+, Max, Paramount+, Peacock, Netflix). The bundle is the entire business. Connectivity is the commodity layer underneath; the **bundle is what the customer feels**. The same play works one era later for **agentic services**: the Telco bundles other people's **brand-operated agents** (American Airlines, Marriott, Walmart, Toyota, Sazerac) on the same bill, with the same trust posture, with the same single point of orchestration. Every consumer brand becomes a Channel; the Telco's store decides which Channels the household can subscribe to; the Home Orchestrator routes intents across them. This document is the umbrella that defines the pattern. The per-vertical packs are individual Channels.

## The streaming-bundle → agentic-marketplace parallel

| Streaming bundle pattern (today) | Agentic marketplace pattern (the play) |
|---|---|
| Hulu, ESPN, Discovery, Disney+, Max, Paramount+, Netflix, Peacock | American Airlines (`TMT-TEL-HOM-11`), Marriott (`HOM-12`), Walmart (`RTL-*`), Toyota (`MOB-*`), Sazerac (`BEV-*`), CVS, Chase, … |
| Each app individually billable, OR bundled by the Telco | Each Channel individually subscribable, OR bundled by the Telco |
| Telco does not produce the content | Telco does not produce the agents |
| Customer trusts the Telco to deliver the bits | Customer trusts the Telco to deliver the intent-routing + privacy posture |
| Bundle pricing 30–50% off à-la-carte | Bundle pricing 25–40% off à-la-carte |
| Telco gets ~$3–8 PMPM rev-share per included app | Telco gets ~$5–15 PMPM rev-share + action-commerce flow per included Channel |
| Customer can churn an app independently | Customer can churn a Channel independently |
| Closed garden (Apple TV, Roku, etc.) loses to open | Closed orchestrator (Big Tech) loses to open Telco |

The parallel is not metaphor — it is the actual operating playbook the Telco already runs. The agentic marketplace is the **next monetization surface on top of the same bundling muscle**.

## Pack contents

| # | Document | Purpose |
|---|---|---|
| 01 | [Channel marketplace model](./01-channel-marketplace-model.md) | The streaming-bundle pattern, restated for agentic services. The Telco as Channel Store operator |
| 02 | [Channel categories](./02-channel-categories.md) | The seven channel categories — Home, Travel, Retail, Mobility, Health, Beverage / CPG, Finance — and what each can monetize |
| 03 | [ERD & Postgres — channel registry](./03-erd-and-postgres.md) | Shared schema additions: `channel`, `channel_subscription`, `channel_bundle`, `partner_directory` |
| 04 | [Medallion cross-channel patterns](./04-medallion-cross-channel.md) | How Bronze / Silver / Gold scale across channel verticals |
| 05 | [Channel catalog](./05-channel-catalog.md) | The marketplace registry — every channel's code, anchor partners, status |
| 06 | [Partner onboarding](./06-partnership-marketplace.md) | The 5-archetype framework applied to Channel-Store onboarding |
| 07 | [Marketplace economics](./07-marketplace-economics.md) | Three revenue layers across all channels; aggregate household-level math |
| 08 | [Consumer experience](./08-consumer-experience.md) | How the household discovers, subscribes, uses, and churns Channels |
| 09 | [Channel portability](./09-channel-portability.md) | Marketplace-wide openness — partner MCP spec, exit rights |
| 10 | [Marketplace differentiators](./10-marketplace-differentiators.md) | Why no other player can credibly run this marketplace |

### Diagrams

- [`diagrams/marketplace-architecture.md`](./diagrams/marketplace-architecture.md) — system architecture of the Channel Store

## The seven channel categories (initial coverage)

| Category | Anchor partners | Pack location |
|---|---|---|
| **Home** | Samsung, LG, Whirlpool, Nest, Ring, Dexcom, Ford OnStar | [`../telco/`](../telco/) |
| **Travel** | American Airlines, Marriott, Expedia, Airbnb, Hertz, Uber | [`../travel-hospitality/`](../travel-hospitality/) |
| **Retail** | Walmart (anchor), Target, Costco, Kroger, Best Buy, Home Depot | [`../retail/`](../retail/) |
| **Mobility / Auto** | Toyota (anchor), Ford, GM, Tesla, Honda, Hyundai | [`../mobility-auto/`](../mobility-auto/) |
| **CPG / Adult Beverage** | Sazerac (anchor), Diageo, Pernod Ricard, Constellation Brands | [`../cpg-adult-beverage/`](../cpg-adult-beverage/) |
| **Health & Pharmacy** | CVS, Walgreens, UnitedHealth Optum, Walmart Health | _Future pack_ |
| **Finance & Insurance** | Chase, Amex, State Farm, Progressive, Plaid | _Future pack_ |

Adding a new Channel category is a **net-additive** activity — it does not require touching any existing pack, existing agent YAML, or existing schema. That is the marketplace property the architecture protects.

## Three things that make the marketplace work

1. **Open partner protocol.** Every Channel implements `apex.tmt.mcp.partner.v1` (an MCP profile extending the travel-specific `apex.tmt.mcp.travel.v1`). Partners that implement the protocol are listable; partners that don't, aren't. No bilateral integration code per partner.
2. **Vault-shared consent.** Every Channel reads from and writes to the same household vault. Subscribing to a new Channel grants scopes; unsubscribing revokes them. The consent ledger is the marketplace's audit trail.
3. **Single bill, single churn surface.** Every Channel is a line item on the Telco invoice. The customer can subscribe / unsubscribe / pause any Channel independently, in the same UI, with the same trust posture. This is the **structural advantage** the marketplace has over standalone vertical apps.
