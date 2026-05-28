# `<pack-name>` Agentic Pack

> One-paragraph elevator pitch — the business model, the customer it serves, the data substrate it stands on, and the parent Edition(s) it extends.

**Parent Edition(s):** `<TMT | HLS | RC | ER | AXLE | TH | ICE>`
**New service-code family:** `<EDITION>-<SUB>-<DOMAIN>-*`
**Status:** Draft / Reviewed / Approved
**Primary author:** `<owner>@deloitte.com`

## Pack contents

| # | Document | Purpose |
|---|---|---|
| 01 | [Business model](./01-business-model.md) | Strategic framing — who pays, for what outcome, how the platform is defensible |
| 02 | [Device & data feeds](./02-device-data-feeds.md) | Inventory of systems / devices / accounts whose data fuels the pack |
| 03 | [ERD & Postgres](./03-erd-and-postgres.md) | Logical ERD + reference DDL including tenant isolation |
| 04 | [Medallion (Bronze / Silver / Gold)](./04-medallion-bronze-silver-gold.md) | APEX-conformant Bronze landings, Silver canonical entities, Gold virtual views, measures |
| 05 | [Services catalog](./05-services-catalog.md) | The orchestrator + sub-agent service codes the pack introduces |
| 06 | [Partnership map](./06-partnership-map.md) | Strategic partner archetypes (data-in, action-out, distribution, risk-share, standards) |
| 07 | [Business value model](./07-business-value-model.md) | Revenue, margin, and unit-economics framing per service |
| 08 | [Consumer business case](./08-consumer-business-case.md) | Per-household / per-subscriber willingness-to-pay and adoption thesis |
| 09 | [Portability / open-home](./09-portability-open-home.md) | Data-portability commitments, open standards, and switching costs |
| 10 | [Ecosystem differentiators](./10-retailer-differentiators.md) | What this platform does that an incumbent in an adjacent vertical cannot |

### Diagrams

- [`diagrams/mermaid-erd.md`](./diagrams/mermaid-erd.md) — full ERD as a Mermaid block
- [`diagrams/flow-<anchor-scenario>.md`](./diagrams/) — end-to-end signal flow for the headline scenario

## Authoring guidance

- Every numbered section is **required**. If a section has not been authored, leave a `> _Draft — TBD_` stub so reviewers can see the gap.
- Cite **specific service codes** (`<EDITION>-<SUB>-<DOMAIN>-NN`) wherever an agent, scenario, or KPI is referenced — the codes are the linking primitives across the pack, the Edition spec, the scenario folders, and the agent YAMLs.
- Quantitative claims in sections 07 and 08 should be **sourceable** — cite the dataset or assumption block, not a bare number.
- Section 06 (partnerships) must classify each candidate against one of the five archetypes (A/B/C/D/E) defined in the canonical telco pack — this keeps deal-structure heuristics comparable across packs.
