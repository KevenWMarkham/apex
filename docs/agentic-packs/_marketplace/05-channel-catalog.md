# 05 — Channel Catalog

> The registry of every Channel in the marketplace. Living document — updated as Channels are launched, paused, retired.

## Live & beta Channels

| Channel | Code | Category | Operator | Status | Anchor partner | Service codes |
|---|---|---|---|---|---|---|
| **Home** | `home` | Home | Telco-own | Live | Samsung Family Hub | `TMT-TEL-HOM-01..08`, `HOM-99` |
| **Travel & Hospitality** | `travel` | Travel | Telco-own | Beta | American Airlines (AAdvantage) | `TMT-TEL-HOM-10..17` |

## Planned Channels (this batch)

| Channel | Code | Category | Operator | Status | Anchor partner | Service codes |
|---|---|---|---|---|---|---|
| **Walmart Retail** | `retail-walmart` | Retail | Partner-Walmart | Planned | Walmart | `TMT-TEL-RTL-01..04` |
| **Toyota Connected** | `mobility-toyota` | Mobility | Partner-Toyota | Planned | Toyota | `TMT-TEL-MOB-01..04` |
| **Sazerac House** | `beverage-sazerac` | CPG | Partner-Sazerac | Planned | Sazerac (Buffalo Trace, Pappy) | `TMT-TEL-BEV-01..04` |

## Roadmap candidates (next 12–24 months)

| Channel | Category | Notes |
|---|---|---|
| Target Retail | Retail | Walmart-bench partner; could become its own Channel if BD lands |
| Costco Membership Plus | Retail | Membership-orchestration heavy |
| Ford BlueCruise | Mobility | Ford-anchored counterpart to Toyota Channel |
| GM Ultium / OnStar | Mobility | GM-anchored counterpart |
| Tesla Energy + Vehicle | Mobility | Crosses into Home energy (HOM-02 already covers Powerwall) |
| Diageo Reserve | CPG / Beverage | Premium-spirit counterpart to Sazerac |
| CVS Care | Health | Wedge: prescription orchestration |
| Walgreens MyW | Health | Counterpart to CVS |
| Chase Sapphire+ | Finance | Card concierge + travel sub-channel |
| Amex Platinum+ | Finance | Same shape |
| State Farm Connect | Insurance | Multi-line (home + auto) |
| Disney+ Channel | Entertainment | Already a streaming-bundle Channel; could publish agentic services |
| Spotify Channel | Entertainment | Agentic music + podcast |
| Microsoft 365 Family | Productivity | Cross-cuts with Home calendar / wellness |

## Retired / suspended

_None yet._

## Status definitions

| Status | Meaning |
|---|---|
| `planned` | Pack authored, partner BD in early conversation |
| `onboarding` | Partner-side MCP integration in progress |
| `beta` | Available to selected households for testing |
| `live` | Available to all eligible households on the marketplace |
| `suspended` | Available but no new subscriptions accepted (partner-side issue) |
| `retired` | Withdrawn from the marketplace; existing subscriptions honored to end-of-cycle |

## Channel rollout phasing

Mirror of the phasing from `../telco/06-partnership-map.md` §5, extended:

| Phase | Quarter | Channels going live |
|---|---|---|
| Phase 0 — Foundation | Q1–Q2 | Marketplace platform stand-up; Hyperscaler + Matter membership |
| Phase 1 — Home Channel | Q3 | Home goes live; full HOM-01..08 + HOM-99 |
| Phase 2 — Travel Channel | Q4 | Travel goes live; AA + Marriott + Expedia + Airbnb anchor partners |
| Phase 3 — Retail Channel | Year 2 Q1 | Walmart Retail Channel goes live |
| Phase 4 — Mobility Channel | Year 2 Q2 | Toyota Connected Channel goes live |
| Phase 5 — CPG / Beverage Channel | Year 2 Q3 | Sazerac House Channel goes live (with age-gated commerce ready) |
| Phase 6 — Marketplace at scale | Year 2 Q4+ | Health, Finance, Entertainment, additional Mobility / Retail brands |

## How a Channel gets added to the catalog

1. Author the 10-section pack under `docs/agentic-packs/<channel-slug>/`
2. Build-spec amendment registers the service-code family
3. Partner implements `apex.tmt.mcp.partner.v1`
4. Channel registered via INSERT into the `channel` table
5. Marketplace Operations marks status `beta` → `live` after gate checks pass

## Cross-references

- Marketplace ERD: [`./03-erd-and-postgres.md`](./03-erd-and-postgres.md)
- Partner onboarding: [`./06-partnership-marketplace.md`](./06-partnership-marketplace.md)
- Open MCP spec: [`./09-channel-portability.md`](./09-channel-portability.md)
