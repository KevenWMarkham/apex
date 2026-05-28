# 01 — Channel Marketplace Model

> The Telco's existing playbook for digital content (Hulu, ESPN, Discovery on the bill) restated as the playbook for agentic services (American Airlines, Marriott, Walmart, Toyota, Sazerac on the bill). The platform is not a destination — it is a **Channel Store**.

## 1. The streaming-bundle template

Today, a Telco like Verizon FIOS, AT&T, Comcast Xfinity, or T-Mobile offers customers something like:

```
Verizon Bundle Example:
  Connectivity (fiber 1G):          $89.99 / mo
  Disney+ included:                 (worth $13.99)
  Hulu (with ads) included:         (worth $9.99)
  ESPN+ included:                   (worth $11.99)
  Max add-on:                       $9.99 / mo
  Netflix Premium add-on:           $22.99 / mo
  Apple TV+ via partnership:        $4.99 / mo (discounted)
  Total Telco invoice:              $127.95 / mo
```

The customer pays one bill. The Telco settles with each content partner on the back end. The customer can drop / add Max next month without canceling the rest. The Telco brokers the bundle.

This is the **template** that the agentic marketplace runs on.

## 2. The agentic-bundle equivalent

```
Telco Agentic Bundle (illustrative):
  Connectivity (fiber 1G):                       $89.99 / mo
  Home Agentic Family bundle:                    $19.99 / mo  (HOM-01..08)
  Travel Premium Channel:                        $14.99 / mo  (HOM-10..17 incl. AA, Marriott, Expedia)
  Walmart Retail Channel:                        $7.99 / mo   (RTL-01..04)
  Toyota Mobility Channel:                       $9.99 / mo   (MOB-01..04)
  Sazerac Beverage Channel:                      $4.99 / mo   (BEV-01..04)
  Total Telco invoice:                           $147.94 / mo
```

Same shape. The customer pays one bill. The Telco settles with American Airlines, Marriott, Expedia, Airbnb, Walmart, Toyota, Sazerac on the back end. The customer can drop the Toyota channel next month without canceling the rest.

The difference vs. streaming: agentic Channels carry **action-commerce revenue on top of subscription** (the Telco earns a cut every time the channel transacts on behalf of the household — every American Airlines rebook, every Walmart grocery order, every Toyota service-call dispatch, every Sazerac allocation alert that becomes a purchase). The streaming Channels don't do this; the agentic ones do.

## 3. Three monetization layers, restated

| Layer | Streaming-bundle analogue | Agentic-marketplace expression |
|---|---|---|
| Carriage / wholesale | Per-subscriber wholesale rate paid by streamer to Telco | Per-Channel-subscriber rev-share to Telco (~$2–5 PMPM per Channel) |
| Content-affiliate revenue | (Limited — streaming has no transaction layer) | Per-action commerce take rate (3–8% of partner transaction value) |
| Bundle CAC offset | Lower churn on the connectivity line | Lower churn on the connectivity AND home-agentic lines |

The **action-commerce layer** is what makes the agentic marketplace meaningfully larger than the streaming bundle in steady state, even though the streaming bundle has more current scale.

## 4. The Channel Store operating model

Six functions the Telco runs at marketplace level:

| Function | Responsibility | Owned by |
|---|---|---|
| **Partner onboarding** | Vet brand, integrate to MCP spec, set commercial terms | Telco BD + Trust & Safety |
| **Channel catalog** | Maintain the registry of available Channels and bundles | Telco Marketplace Operations |
| **Bundle composition** | Decide which Channels can combine into which bundles | Telco Product |
| **Billing & settlement** | Aggregate subscriber bills, settle with each partner | Telco Finance |
| **Orchestrator routing** | Route household intents to the right Channel | Home Orchestrator (`HOM-99`) |
| **Trust & audit** | Vault-side consent enforcement, audit trails, partner-side compliance | Telco Privacy & Compliance |

The Telco does **not** decide which agents inside each Channel are best. Each brand publishes the agents they want under their Channel; the customer subscribes; the marketplace operates as an arms-length store.

## 5. Why brands say yes

A brand that publishes a Channel on the Telco marketplace gets:

| Brand benefit | Why it matters |
|---|---|
| Direct billing relationship via the Telco invoice | No card-on-file friction; lower payment fail rate (~2% vs ~8% for direct subscriptions) |
| Verified consumer identity + verified household context | Anti-fraud value far above what direct channels offer |
| Built-in cross-Channel intent routing | A Walmart pharmacy intent for a household member surfaces in front of Walmart, not in a generic search box |
| Loyalty-program enrolment funnel | Captive promo surface inside the orchestrator |
| Multi-Telco distribution from a single MCP integration | Build once, list across every Telco partner |
| Independent regulatory & trust posture | The Telco's privacy regulation envelope protects the brand from headline risk |

No brand can build this on their own. Every brand can rent it from the Telco.

## 6. Why some brands say no — and the marketplace still works

Some brands will refuse to publish a Channel:

- **Brands whose business model depends on closed-garden user data** (e.g., a hypothetical "Apple Channel" or "Google Channel" — they can't accept the openness commitment without breaking their core business)
- **Brands with weaker BD muscle** (regional retailers, niche CPG) — will join later as the marketplace scales
- **Brands whose vertical is in a contested partnership** (e.g., the Telco's incumbent grocery deal with Kroger may make Walmart hesitant initially — though the marketplace's openness commitment prevents exclusivity)

The marketplace's design tolerates non-participation. The Telco's competitive position **does not depend on any single brand** participating. This is the inverse of the streaming-bundle reality where losing Disney+ is meaningful — losing any single agentic brand is bounded.

## 7. What this is not

- **Not a search engine** for consumer brands. The customer brings the intent ("order milk", "rebook the flight"); the orchestrator picks the Channel.
- **Not a closed garden.** Open MCP protocol; partners are not locked into one Telco; customers are not locked into the marketplace.
- **Not a brand-owned platform.** No single brand has special status; the marketplace is brand-neutral.
- **Not an ad platform.** Agent suggestions can be "sponsored" (with explicit disclosure) but the marketplace is not funded by ad inventory.
- **Not a content-rights play.** Streaming partners are content rights holders; agentic partners are operating brands. Different legal shape.

## 8. The decade-out picture

In ten years, this looks like:

- **15–25 active Channels per Telco**, spread across Home, Travel, Retail, Mobility, Health, Finance, CPG / Beverage, Entertainment
- **Average household subscribed to 4–7 Channels**, with the typical household paying $30–80 / mo for the bundle
- **Action-commerce flow** of $300–1,500 / yr per household, with Telco take rate of 4–6%
- **Aggregate ARPU uplift** of $60–130 PMPM for the Telco's home-internet subscriber base — that's the prize
- **Partner ecosystem** of 100+ consumer brands listed; marketplace becomes the **default agentic distribution channel** for any consumer brand

This is materially larger than the streaming bundle in steady state. It is the **single biggest organic ARPU growth opportunity** available to a CSP this decade.
