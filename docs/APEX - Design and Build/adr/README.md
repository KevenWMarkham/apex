# Architecture Decision Records (ADRs)

Each ADR captures a single accepted architectural decision with its context, consequences, and status. ADRs are immutable once accepted — supersession produces a new ADR that references the prior.

## Index

| ADR | Title | Status | Resolves |
|---|---|---|---|
| [ADR-001](ADR-001-foundry-acr-public-egress.md) | Foundry hosted-agent ACR public-reachability constraint | Accepted | H.1 |
| [ADR-002](ADR-002-tenant-manifest-vs-entra-blueprints.md) | APEX tenant manifest vs Entra Agent ID blueprints | Accepted | H.2 |
| [ADR-003](ADR-003-audit-row-vs-purview-audit.md) | APEX audit row vs Purview Audit (system of record) | Accepted | H.3 |
| [ADR-004](ADR-004-foundry-region-coverage.md) | Foundry region coverage vs client target regions | Accepted | H.4 |
| [ADR-005](ADR-005-classification-tier-mapping.md) | APEX T1–T4 ↔ Purview sensitivity-label mapping | Accepted | H.5 |
| [ADR-006](ADR-006-agent-orchestrator-canonical.md) | Microsoft Agent Framework as the canonical agent orchestrator | Accepted | Agent orchestration substrate question |

## Format

Each ADR follows:

- **Status** — Proposed / Accepted / Superseded / Deprecated
- **Date** — when the decision was made
- **Context** — what's the situation, what alternatives were considered
- **Decision** — what we picked and why
- **Consequences** — what becomes easier / harder / different
- **Status** — operational state (where this is implemented, what's left)

## When to write an ADR

- A non-obvious architectural choice with multiple defensible options
- A decision that an outsider would need explained ("why didn't they just use X?")
- Anything that changes a contract — schema, protocol, deployment model, security posture
- Resolution of an open question from a planning doc

## When NOT to write an ADR

- Routine implementation choices with one obvious answer
- Code style or formatting decisions (those go in `ruff.toml` / `pyproject.toml`)
- Per-engagement client-specific choices (those go in the engagement's plan, not the framework)
