# apex-references

**Sprint 18 — Reference Deployments.** Five turnkey Wave-1 deployment
blueprints, one per flagship Practice anchor, composing the work of
Sprints 14-17 into named, scoped, demo-able engagements.

## Coverage

| Reference        | Practice | Sellers Guide | Capacity              | Wave-1 fee band       | Demo script              |
|------------------|----------|---------------|-----------------------|-----------------------|--------------------------|
| big-box-store    | RC       | §16.13        | single-capacity-tenant| $0.75M – $1.5M       | `demo big-box-store`     |
| hospital         | HLS      | §10.9         | per-workload-isolation| $1.0M – $1.75M       | `demo hospital`          |
| utility          | ER       | §11.9         | dev-prod-split        | $1.0M – $2.0M        | `demo utility`           |
| plant            | AXLE     | §12.9A        | per-workload-isolation| $0.85M – $1.75M      | `demo plant`             |
| airline          | TH       | §14.8         | per-workload-isolation| $0.9M – $1.75M       | `demo airline`           |

Each reference composes:

- **Sprint 14** capacity blueprint (Terraform-defined Fabric F-SKU + workspace plan)
- **Sprint 15** SOR adapters (named, validated, schema-mapped)
- **Sprint 16** anchor agents (HITL/HOTL gated, audit-row instrumented)
- **Sprint 17** productized services (commercial envelopes per Wave)
- A canonical-schema set, model-pin recommendations, Purview classifications
- Triggering scenarios + use cases + KPI commitments + Wave-1 deliverables
- A markdown demo script tied to the Sellers Guide narrative

## CLI

```bash
apex references stats
apex references list
apex references list --practice rc
apex references inspect big-box-store
apex references demo hospital
apex references validate
```

## Validation

`validate_references()` cross-checks every manifest against the live
catalogs:

- service codes resolve in the apex-services catalog (Sprint 17)
- agents resolve in the apex-agents catalog (Sprint 16)
- adapters resolve in the apex-adapters manifests (Sprint 15)
- demo-script paths exist
- Wave-1 envelopes are coherent (low ≤ high) and within Sellers Guide §2.2 bounds (4-12 weeks)
- every reference declares ≥ 1 use case and ≥ 1 KPI target

## Cross-references

- **Sprint 13** governance — Purview classifications + DLP rules
- **Sprint 14** capacity — Terraform blueprints (`single-capacity-tenant`, `dev-prod-split`, `per-workload-isolation`)
- **Sprint 15** adapters — `apex-adapters` package
- **Sprint 16** agents — `apex-agents` package
- **Sprint 17** services — `apex-services` package
- **Sellers Guide** §10.9, §11.9, §12.9A, §14.8, §16.13 — reference deployment narratives
