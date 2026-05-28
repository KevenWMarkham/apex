# Telco Home Agentic — APEX Agentic Pack

> A new business model for Communication Service Providers: deliver **agentic services in the home** on top of the customer base they already own, the router/ONT they already operate, and the data substrate the household already generates. Position the offering the way FIOS positioned digital content — the platform that lets the home **orchestrate**, not just consume.

**Parent Edition:** `TMT` (Technology, Media, Telecom)
**New service-code family:** `TMT-TEL-HOM-*` (Telco Home Agentic)
**Companion build-spec amendment:** [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../build-specs/apex-tmt-agentic-home-amendment.md)
**Status:** Draft
**Primary author:** tmt-practice-lead@deloitte.com

## The thesis in one paragraph

Telcos already sit at the **data choke point** in every household — the router, the ONT, the 5G CPE, and the gateway are theirs. The same network they sell as a utility is, simultaneously, the lowest-trust-cost place to host a **personal data vault**, the most natural place to run **device-graph inference**, and the only place to route **orchestrated intents** ("order groceries", "lower the bill", "make sure Mom's OK") across the household's devices. The FIOS-of-AI metaphor: FIOS made the home a venue for digital content; Telco Home Agentic makes the home a venue for **agentic outcomes**.

## Pack contents

| # | Document | Purpose |
|---|---|---|
| 01 | [Business model](./01-business-model.md) | Three-layer stack — Vault → Device Graph → Agent Marketplace |
| 02 | [Device & data feeds](./02-device-data-feeds.md) | 70+ device classes across 10 categories |
| 03 | [ERD & Postgres](./03-erd-and-postgres.md) | Logical ERD, DDL with TimescaleDB + pgvector, RLS-enforced tenant isolation |
| 04 | [Medallion (Bronze / Silver / Gold)](./04-medallion-bronze-silver-gold.md) | APEX-conformant Bronze landings, Silver entities, Gold views, anchor measures |
| 05 | [Services catalog](./05-services-catalog.md) | Eight subscribable sub-agents + meta-orchestrator (`TMT-TEL-HOM-01..08`, `TMT-TEL-HOM-99`) |
| 06 | [Partnership map](./06-partnership-map.md) | Per-service partner archetypes + the three platform-defining partnerships |
| 07 | [Business value model](./07-business-value-model.md) | Per-service unit economics, the three revenue layers, and aggregate ARPU uplift |
| 08 | [Consumer business case](./08-consumer-business-case.md) | Per-household willingness-to-pay, the grocery-time wedge, and the trust-asymmetry argument vs Big Tech |
| 09 | [Portability / open-home](./09-portability-open-home.md) | Matter-first device coverage, vault export commitments, and why open-by-construction is a moat not a liability |
| 10 | [Ecosystem differentiators](./10-retailer-differentiators.md) | What a Telco can do here that Amazon, Google, Apple, and the big retailers structurally cannot |

### Diagrams

- [`diagrams/mermaid-erd.md`](./diagrams/mermaid-erd.md) — full ERD as a Mermaid block
- [`diagrams/flow-grocery-end-to-end.md`](./diagrams/flow-grocery-end-to-end.md) — Bronze → Silver → Gold → Agent → Vendor for the grocery scenario

## Anchor scenarios

| Service code | Scenario folder | Sub-agent YAML |
|---|---|---|
| `TMT-TEL-HOM-01` | [`TMT-CX-21-home-grocery-replenishment`](../../scenarios/TMT/customer-experience/TMT-CX-21-home-grocery-replenishment/) | `tmt/12-home-grocery-replenishment.yaml` |
| `TMT-TEL-HOM-02` | [`TMT-CX-22-home-energy-optimizer`](../../scenarios/TMT/customer-experience/TMT-CX-22-home-energy-optimizer/) | `tmt/13-home-energy-optimizer.yaml` |
| `TMT-TEL-HOM-03` | [`TMT-CX-23-home-eldercare-monitor`](../../scenarios/TMT/customer-experience/TMT-CX-23-home-eldercare-monitor/) | `tmt/14-home-eldercare-monitor.yaml` |
| `TMT-TEL-HOM-04` | [`TMT-CX-24-home-maintenance-orchestrator`](../../scenarios/TMT/customer-experience/TMT-CX-24-home-maintenance-orchestrator/) | `tmt/15-home-maintenance-orchestrator.yaml` |
| `TMT-TEL-HOM-05` | [`TMT-CX-25-home-security-presence`](../../scenarios/TMT/customer-experience/TMT-CX-25-home-security-presence/) | `tmt/16-home-security-presence.yaml` |
| `TMT-TEL-HOM-06` | [`TMT-CX-26-home-wellness-coach`](../../scenarios/TMT/customer-experience/TMT-CX-26-home-wellness-coach/) | `tmt/17-home-wellness-coach.yaml` |
| `TMT-TEL-HOM-07` | [`TMT-CX-27-home-vehicle-readiness`](../../scenarios/TMT/customer-experience/TMT-CX-27-home-vehicle-readiness/) | `tmt/18-home-vehicle-readiness.yaml` |
| `TMT-TEL-HOM-08` | [`TMT-CX-28-home-entertainment-concierge`](../../scenarios/TMT/customer-experience/TMT-CX-28-home-entertainment-concierge/) | `tmt/19-home-entertainment-concierge.yaml` |
| `TMT-TEL-HOM-99` | [`TMT-CX-29-home-orchestrator`](../../scenarios/TMT/customer-experience/TMT-CX-29-home-orchestrator/) | `tmt/11-home-orchestrator.yaml` |

> **Numbering note.** The orchestrator agent YAML is `11-home-orchestrator.yaml` (sorted first in the catalog directory because it routes intents to the sub-agents), while its scenario is `TMT-CX-29` (sorted last in the customer-experience folder because it composes the others). The scenario IDs run 21–29 (9 scenarios); the agent YAMLs run 11–19 (9 agents).

## Three things that make this pack work

1. **The Telco is the trusted host, not a content originator.** The customer's data lives in **their own** cloud vault — encrypted with their own KMS key — and the Telco runs the orchestration layer **on top of** it. This is the structural defence against Big Tech's data-monetization model. See [`09-portability-open-home.md`](./09-portability-open-home.md).
2. **Subscriptions stack on a single bill.** Every sub-agent is independently subscribable, every action it takes is independently billable, and all of it lands on the Telco invoice the customer already pays. This is the structural defence against the SaaS-fatigue churn that kills standalone IoT plays. See [`07-business-value-model.md`](./07-business-value-model.md).
3. **Value lives at the partnership boundary, not inside the agent.** Grocers, utilities, MA payers, P&C insurers, and OEMs all pay for outcomes the agents produce — the consumer subscription is the wedge, not the whole business. See [`06-partnership-map.md`](./06-partnership-map.md).
