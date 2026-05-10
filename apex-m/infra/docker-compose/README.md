# APEX-M laptop substrate — Docker Compose templates

The laptop substrate runs APEX-M agents on Docker Desktop, with mock implementations standing in for every Microsoft SDK call. Same agent images that run on Foundry hosted agents in Azure prod run unchanged here — substrate-awareness is purely env-var-driven (per Deployment Guide §2).

**The wizard is the canonical path.** When an operator picks `substrate: laptop` in the wizard, the render endpoint emits a tailored `docker-compose.yml` based on:

- The selected practices / services / scenarios / agents
- The picked use case's `client_approved_architecture` block (adapter selections drop in as additional containers)
- The picked use case's `agent_overrides` block (model, episodic memory, prompt overrides flow as env vars)

This directory contains the **template fragments** the renderer composes. Operators who want to drive the laptop deploy from the CLI (without the wizard) can copy these directly.

## Files

| File | Purpose |
|---|---|
| `base.docker-compose.yml` | Always-present services — mocks for Foundry, Fabric, Purview, Redis. The operator's agent containers depend on these. |
| `agent.fragment.yml` | Per-agent service template; the renderer instantiates one per (service, scenario, role) selected. |
| `adapter.fragment.yml` | Per-adapter service template; the renderer instantiates one per `client_approved_architecture` adapter ref. |
| `.env.example` | Every env var the agent containers consume; substrate-aware defaults. |

## Mocks

Every Microsoft SDK call in `apex-m/src/apex_m/*` has a corresponding `Mock*` class that satisfies the same APEX-Core protocol. The compose file's `apex-mock-foundry`, `apex-mock-fabric`, `apex-mock-purview`, and `apex-mock-redis` containers expose HTTP shims that the agent's `MockAgentRuntimeFoundry`, `MockDataLakeFabric`, `MockAuditLedgerPurview`, etc. point at.

This means the same agent code path that runs against real Microsoft Foundry in prod runs against the mocks on the laptop — `APEX_FORCE_MOCK=true` flips the decision.

## Independence

Laptop substrate is **Independence-clean by construction**: no client cloud subscription touched, no Microsoft / Google / AWS API call billed. Engineers iterate on agent code, prompts, and orchestration without any cross-organization API call. Per [Independence Posture §Substrate](../../../docs/apex-core/Independence-Posture.md), this is the recommended substrate for engagement-team development before the client cloud is provisioned.

## Operator workflow

```bash
# Wizard renders docker-compose.yml + .env into the engagement folder
~/apex-deployments/<engagement>/
├── docker-compose.yml            # rendered by wizard
├── .env                           # rendered by wizard
└── README.md                      # operator-facing doc

# Bring up
cd ~/apex-deployments/<engagement>
docker-compose up

# Tear down
docker-compose down -v
```

Synthetic data fixtures live in `apex-m/test-fixtures/` (TBD per Sprint 47). Agent logs to stdout; `docker-compose logs -f apex-m-rc-e2e-03-cold-chain-pricing` to follow The Pricer specifically.

## What lands when

| Sprint | Scope |
|---|---|
| **46a** (this commit) | Compose template fragments + wizard renderer + README |
| **47** | Real mock service images (currently `ghcr.io/apex/mock-foundry:0.1.0` etc. don't exist; first client engagement Lab work builds them) |
| **48+** | Per-engagement adapter implementations cascade into adapter fragments |

## Cross-references

- [Deploy-UX-and-Substrates.md](../../../docs/APEX%20-%20Design%20and%20Build/Deploy-UX-and-Substrates.md) — the four-substrate model
- [Deployment Guide ch 2 — Substrate-Aware Architecture](../../../docs/book/Professional-APEX-M-Deployment-Guide.html#ch-2)
- [Use case schema](../../../services/_use-case.schema.md) — what the wizard composes from
