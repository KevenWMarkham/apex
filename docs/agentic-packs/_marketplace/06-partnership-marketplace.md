# 06 — Partner Onboarding for the Marketplace

> The 5-archetype framework (A / B / C / D / E from [`../telco/06-partnership-map.md`](../telco/06-partnership-map.md)) applied to **whole Channel onboarding** rather than to individual partner deals.

## 1. Channel-level archetype assignment

When a brand publishes a Channel, the entire Channel's economic shape is dominated by one or two archetypes:

| Channel | Dominant archetype | Why |
|---|---|---|
| Home | A + B | Device-data-in + action commerce on grocery / energy |
| Travel | B + C + D | Booking commerce + loyalty-bundling + IROPS risk-share |
| Walmart Retail | B + C | Action commerce + bundle distribution (Walmart+) |
| Toyota Mobility | A + B + D | Vehicle telematics + service commerce + insurance / financing |
| Sazerac CPG | A + B | Allocation data + age-gated commerce |
| Health (future) | D dominant | PMPM outcome-share with payers |
| Finance (future) | B + D | Transaction routing + risk-share with insurers |

The archetype mix determines the deal-structure heuristics that apply to that Channel's launch negotiation.

## 2. Onboarding workflow

```
Brand expresses interest
        ↓
[1] Channel-design workshop
    - 10-section pack drafted
    - Service-code family reserved
    - Anchor wedge event identified
        ↓
[2] MCP integration design
    - apex.tmt.mcp.partner.v1 implementation plan
    - Authentication / authorization model
    - Webhook footprint
        ↓
[3] Commercial-terms workshop
    - Archetype assignment (per-Channel)
    - Take-rate envelope
    - Bundle eligibility
        ↓
[4] Trust & compliance audit
    - Privacy attestation
    - Security attestation (SOC 2 or equivalent)
    - Accessibility attestation
    - Data-residency posture
        ↓
[5] Beta launch
    - 1-3 metro markets, selected household cohort
    - 90-day observation window
        ↓
[6] Live launch
    - Marketplace status flips to 'live'
    - Bundle inclusion eligibility activated
```

Median onboarding timeline: **4–8 months** for an anchor Channel partner, **6–10 weeks** for a bench partner joining an existing Channel.

## 3. Commercial terms — standard archetype envelopes

| Archetype | Standard term for new Channel | Heuristic |
|---|---|---|
| A (Data-In) | No cash; attribution back to partner | Data has no scarcity value at marketplace scale |
| B (Action-Out) | 3–8% of partner action value | Travel bookings lower (1–3%); ground mobility higher (5–15%) |
| C (Distribution) | 40–60% off retail for bundle inclusion | Brand co-presented; Telco controls the retention surface |
| D (Risk-Share) | Outcome share with control-cohort methodology | Up-front methodology agreement non-negotiable |
| E (Standards) | No cash; reference-design status | Marketplace's MCP spec is the standard |

## 4. Trust & compliance gate

Before any Channel can go live, the partner must complete:

| Attestation | Source / framework | Scope |
|---|---|---|
| Privacy | SOC 2 Type II, ISO 27701, or equivalent | Data handling of household-vault-sourced data |
| Security | SOC 2 Type II + pen-test report | API endpoints, vault-access flows |
| Accessibility | WCAG 2.2 AA | All consumer-facing surfaces |
| Age verification (CPG / Beverage only) | State-by-state legal review | Age-gated commerce flow |
| HIPAA BAA (Health / future) | BAA executed | All PHI flows |
| GLBA & PCI (Finance / future) | PCI DSS 4.0 + GLBA attestation | Payment + account flows |

Telco-side Marketplace Trust & Compliance owns the gate. Brands without these are not listable.

## 5. The bench-partner model

Each Channel has an **anchor partner** (the named brand on the pack) and a **bench** of additional brands that participate in the same Channel with the same orchestration shape. For example:

- Travel Channel: AA is anchor; Delta, United, Southwest, JetBlue are bench
- Retail Channel: Walmart is anchor; Target, Costco, Best Buy, Home Depot are bench
- Mobility Channel: Toyota is anchor; Ford, GM, Tesla, Honda are bench
- CPG Channel: Sazerac is anchor; Diageo, Pernod Ricard, Brown-Forman are bench

The anchor:

- Funds the bulk of the Channel-launch cost
- Gets exclusive co-branding ("Marriott — official hotel partner of Telco Home")
- Receives the **flagship distribution slot** in the marketplace UI

The bench:

- Pays a smaller onboarding fee
- Gets standard listing
- Competes with anchor on equal-footing for any **brand-neutral routing** (e.g., the orchestrator may route a hotel booking to Hilton if the customer's Bonvoy account has no relevant tier)

This is **how the marketplace stays customer-aligned**: the customer's preferences (loyalty tier, price, geography) drive routing, not the anchor's exclusivity.

## 6. Conflict-of-interest avoidance

The marketplace's neutrality commitments:

1. **No exclusive routing.** The Telco does not enter exclusive routing agreements with any Channel — the orchestrator must always consider all live Channels for a given intent.
2. **Disclosed sponsorship.** When a partner pays for promoted placement, the orchestrator UI labels the suggestion as "sponsored" — same standard as streaming-bundle promoted titles.
3. **Customer-controlled defaults.** The customer can set per-Channel preferences ("always use Marriott for hotels", "never use Uber") that override routing logic.
4. **Independent audit log.** Every routing decision is logged in `agent_run.parent_run_id` with the alternatives considered. Customer can audit any decision in their vault export.
5. **No Telco-owned competitive Channels in vertical conflict.** The Telco does not launch a Telco-branded Channel that competes with anchor partners in the same vertical — the marketplace is brand-neutral.

These commitments are **structural defences** against the marketplace becoming a closed garden. They are also the trust-narrative basis for the partnerships to work in the first place.
