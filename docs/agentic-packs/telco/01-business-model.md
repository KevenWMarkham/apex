# 01 — Business Model

> The Telco-owned, customer-controlled platform for agentic services in the home. FIOS made the home a venue for digital content. This makes the home a venue for **agentic outcomes**.

## The opportunity

Telcos already own three things that no other player owns together:

1. The **router / ONT / 5G CPE** — the single point through which every household device exchanges data with the internet.
2. A **monthly billing relationship** with the household — high trust, low churn relative to standalone SaaS.
3. A **brand position as utility / infrastructure**, not as an advertising-funded data harvester. This is the structural trust asymmetry vs. Big Tech.

What they do **not** own today is the layer on top — the orchestration of household intents (order groceries, lower the bill, look after Mom) across the dozens of connected devices and accounts a modern household runs.

## The proposition

A **three-layer stack** the Telco owns and operates, that the customer subscribes into:

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 3 — Agent Marketplace                                 │
│  Orchestrator + subscribable sub-agents:                     │
│  GroceryAgent · EnergyAgent · EldercareAgent ·               │
│  MaintenanceAgent · SecurityAgent · WellnessAgent ·          │
│  VehicleAgent · EntertainmentAgent                           │
├──────────────────────────────────────────────────────────────┤
│  Layer 2 — Device Graph & Context Engine                     │
│  Normalize, label, correlate signals across all categories.  │
│  Matter / Thread aware. Runs in the Telco's cloud region.    │
├──────────────────────────────────────────────────────────────┤
│  Layer 1 — Personal Data Vault                               │
│  Private cloud per customer. Customer-held KMS key.          │
│  The Telco operates it; the Telco does NOT read it.          │
└──────────────────────────────────────────────────────────────┘
                              ▲
              Gateway / ONT / 5G CPE / Smart Hub
                              ▲
                       Every home device
```

The vault is the **trust differentiator**. The device graph is the **technical asset**. The marketplace is the **monetization surface**.

## The FIOS parallel

FIOS sold a fatter pipe at a moment when the value migrated from "delivering bits" to "what those bits enable in the home" (HD video, then streaming, then bandwidth-heavy gaming). The Telco bundled the value-creating layer onto the connectivity layer. Standalone "fast internet" became a commodity; FIOS-as-a-content-experience captured the value.

Telco Home Agentic is the same play, one era later. Connectivity is the commodity again. The value-creating layer this time is **agentic services that act on household state**. The Telco bundles the orchestration layer onto the connectivity layer.

What FIOS did to DVDs and CDs, Home Agentic does to standalone smart-home apps: it collapses **N device-vendor experiences** into **one orchestrated household experience**.

## How money flows

Three revenue layers, each independently scalable:

| Layer | Payer | What they pay for | Take rate / unit price |
|---|---|---|---|
| **Consumer subscription** | Household | Sub-agent bundle on the monthly bill | $5–$15 / mo per active sub-agent |
| **Action commerce** | Partner (grocer, utility, OEM, insurer) | Each completed agent-initiated transaction | 3–8% of basket / per-event fee |
| **Outcome / risk-share** | Payer (MA plan, P&C carrier) | Verified outcomes (fall prevention, claim avoidance) | $20–80 PMPM or per-incident |

The consumer subscription is the **wedge** — it secures the household and the consent. The action commerce and outcome layers carry **the actual P&L**.

## Why the Telco wins this versus Big Tech

| Concern | Big Tech offer | Telco offer |
|---|---|---|
| Where does the data live? | Vendor cloud, vendor reads it | Customer vault, customer holds key |
| Who controls the device graph? | One vendor ecosystem (Apple Home, Google Home) | Open Matter-first, vendor-agnostic |
| What's the trust narrative? | "We're useful, trust us" | "We're a utility, regulators already watch us" |
| Monetization model | Ads + commerce kickbacks | Transparent monthly bill |
| What happens at vendor exit? | Data is stranded | Vault is portable by construction |

The Telco's **regulatory exposure** is, paradoxically, the asset here. Customers have been comfortable trusting their phone company with the wire into their house for a century. They have not been comfortable trusting their search engine with what's in the fridge.

## Adoption thesis

The platform does not need every household to subscribe to every agent. The unit economics work if a typical household:

1. Subscribes to **2.5 sub-agents on average** (the grocery wedge is universal; one of energy / eldercare / maintenance is typically attached).
2. Allows **partner-action commerce** to flow through at least one of those agents.
3. Becomes eligible for **one outcome-share program** (most often eldercare via an MA plan).

A household at this adoption level produces $30–70/mo of incremental gross profit to the Telco — at typical CSP household counts (10–50M), this is a **$3–35B annual GP line** layered on top of existing connectivity revenue.

See [`07-business-value-model.md`](./07-business-value-model.md) for the unit-economic build, [`08-consumer-business-case.md`](./08-consumer-business-case.md) for the willingness-to-pay assumptions, and [`06-partnership-map.md`](./06-partnership-map.md) for the partner economics.

## What this is not

- **Not a smart-home hub product.** SmartThings, Home Assistant, and Matter controllers already exist and are mostly excellent. The platform consumes them as upstream inputs.
- **Not a Big-Tech-style assistant.** Voice convenience is a UX surface, not the value proposition. The value is **outcome orchestration**.
- **Not a closed garden.** The vault is portable, the device graph is Matter-first, and the agent marketplace is open to third-party agents (with revenue share). Closed gardens are how Big Tech wins; open-by-construction is how the Telco wins.
