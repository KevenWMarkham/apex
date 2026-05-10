# ADR-006 · Microsoft Agent Framework as the canonical agent orchestrator

**Status:** Accepted
**Date:** 2026-05-09
**Resolves:** Open question — agent-orchestration substrate for laptop + cloud + relationship to Semantic Kernel + n8n
**Related:** [ADR-001](ADR-001-foundry-acr-public-egress.md), [Services Guide §14.5](../../book/Professional-APEX-M-Services-Guide.html#ch-14-5)

## Context

APEX has had a fluid story on agent orchestration:

- The framework's own Roadmap.md BL.P.65 references "47 orchestration archetypes."
- Earlier code prototypes used Semantic Kernel (SK) + AutoGen patterns.
- The Deployment Guide's §2.6 documents n8n as the laptop workflow substrate (with Logic Apps Hybrid as the cloud equivalent).

These three threads are not the same concern. As of 2026 GA Microsoft has formally separated:

- **Workflow orchestration** — n8n / Logic Apps Hybrid / Power Automate / Foundry workflows. Triggers, branches, HITL routing, ticket creation. The §14 / §15 vocabulary in the Services Guide.
- **Agent orchestration** — how the agent fleet *coordinates internally* during a single scenario step. Microsoft consolidated this in **Microsoft Agent Framework** (open-source, GA, succeeds Semantic Kernel and AutoGen).

APEX needs to pick one canonical agent orchestrator and align the framework to it.

## Decision

**Microsoft Agent Framework is the canonical agent orchestrator for APEX-M, on every substrate.**

Concretely:

1. **Cloud (dev / stage / prod)** — APEX-M agents are Foundry **Hosted Agents**, code-built with Microsoft Agent Framework. The 5 canonical Agent Framework patterns (Sequential / Concurrent / Handoff / Group Chat / Magentic) cover every featured RC scenario, with parameterization.

2. **Laptop** — Same Agent Framework code, same agent images, run unchanged on Docker Desktop. Substrate-awareness is env-var-driven; the only thing that swaps is which APEX-Core protocol implementations get injected (mocks on laptop, real Microsoft SDKs on Foundry).

3. **Semantic Kernel** is deprecated for new APEX code. Existing SK code stays valid; migration follows the [official Microsoft guide](https://learn.microsoft.com/agent-framework/migration-guide/from-semantic-kernel/).

4. **AutoGen** is deprecated for new APEX code. Same migration path applies via the [official AutoGen guide](https://learn.microsoft.com/agent-framework/migration-guide/from-autogen/).

5. **n8n** stays as the laptop **workflow** substrate — equivalent to Power Automate / Logic Apps Hybrid on cloud. n8n does NOT do agent orchestration; that lives entirely in Microsoft Agent Framework code that n8n's agent-call node invokes. APEX-M's `apps/deploy-wizard/` laptop-substrate render emits n8n workflows for the §14 primitives, with agent-call nodes pointing at the Foundry-style hosted-agent endpoint exposed by the laptop's mock-foundry container.

6. **Foundry Workflows** (visual + YAML) are the *alternative* on cloud for engagements that prefer low-code orchestration over Agent Framework code. APEX-M default is Agent Framework code; Foundry workflows surface when a use case sets `orchestration_runtime: foundry-workflows` instead of the default `agent-framework`.

7. **APEX's 47 archetypes** (Roadmap.md BL.P.65) are reconciled to Microsoft's 5 canonical patterns with parameterization. A spreadsheet (planned) maps each of the 47 to its canonical pattern + variant parameters; the BL.P.65 entry is rewritten as "5 patterns × N variants" in the next Roadmap amendment.

## Consequences

- **One framework to learn.** Engineers, agent designers, and engagement teams converge on a single agent orchestration vocabulary. SK / AutoGen / proprietary patterns retire.
- **Substrate parity is real.** Same Python / .NET code in `apex-m/src/apex_m/runtime_foundry.py` runs against Foundry Agent Service in Azure prod and against `mock-foundry` on Docker Desktop.
- **Use-case YAML carries the archetype choice.** New `orchestration_archetype` field in `services/_use-case.schema.md` accepts one of the 5 canonical names; the wizard validates.
- **Existing APEX 47-archetype work is preserved.** No code is deleted; the catalog entries are remapped to canonical patterns + variant parameters.
- **n8n's role narrows.** It's a workflow runtime, not an agent runtime. Anti-pattern of orchestrating agent-to-agent inside n8n is documented in Services Guide §14.5.4 with a warning callout.
- **Foundry Workflows are an opt-in.** Engagements that benefit from visual editing override the default Agent Framework runtime.

## Validation against current Microsoft documentation

This decision aligns with Microsoft's published guidance as of April 2026:

- **Agent Framework GA is the recommended substrate** for code-first multi-agent orchestration. Per [Agent Framework overview](https://learn.microsoft.com/agent-framework/overview/): *"The Agent Framework is the direct successor [to Semantic Kernel and AutoGen], created by the same teams."*
- **Foundry Agent Service explicitly endorses Agent Framework + LangGraph** for hosted agents per [Foundry Hosted Agents docs](https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent).
- **Connected Agents (classic) is deprecated**, retiring March 31, 2027 per Microsoft Learn. Migration guide directs to Foundry workflows + Agent Framework.
- **Semantic Kernel agent orchestration features** are flagged "experimental, under active development" per [Semantic Kernel agent architecture](https://learn.microsoft.com/semantic-kernel/frameworks/agent/agent-architecture).
- **Multi-agent reference architecture** ([Build a multiple-agent workflow](https://learn.microsoft.com/azure/architecture/ai-ml/idea/multiple-agent-workflow-automation)) is built on Container Apps + Microsoft Agent Framework — the exact substrate APEX-M targets.

## Status

Accepted. Concrete implementation:

- Services Guide §14.5 documents the three-layer model
- `services/_use-case.schema.md` adds `orchestration_archetype` field
- RC-E2E-03 cold-chain use case sets `orchestration_archetype: magentic` (worked example)
- Other 4 RC service _default use cases set the archetype per §14.5.7 table
- Sprint 41+ wires `apex_m.runtime_foundry` against real Microsoft Agent Framework SDK
- Existing apex-orchestrator package (per Roadmap.md BL.P.65–67) remains as the imperative-orchestration helper but its archetype catalog is reconciled to canonical Microsoft patterns

## When to revisit

Re-evaluate when:

- Microsoft introduces a 6th canonical pattern in Agent Framework
- Foundry workflows mature past "primarily nondeterministic" (per Microsoft Learn) and become viable for deterministic + audit-required APEX scenarios
- A client engagement requires a pattern not expressible in the 5 canonical archetypes (raise a new ADR)
