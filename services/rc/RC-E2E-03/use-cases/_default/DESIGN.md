# RC-E2E-03 — Default + Canonical Worked-Example Use Case

This is the **first fully-runnable use case** in APEX-M. Other RC service use cases (RC-E2E-04 / -05 / -07 / -09) start as template stubs and use this directory as their reference for the `chain_execution` + `persona_kpi_attribution` + `smoke_test` blocks.

## Files

| File | Purpose |
|---|---|
| [`use-case.yaml`](use-case.yaml) | Fully populated 24-step `chain_execution`, persona-KPI attribution for Marisol Reyes (Store Operations Lead) and Daniel Chen (Merchandising Director), and a runnable smoke test |
| [`../../scenarios/rc-cold-chain-excursion-mid-shift/fixtures/excursion-event.json`](../../scenarios/rc-cold-chain-excursion-mid-shift/fixtures/excursion-event.json) | Canonical synthetic excursion event that drives the chain end-to-end on the laptop substrate |

## Why cold-chain over dynamic-markdown

RC-E2E-03 has two featured scenarios. The use case here covers the **cold-chain excursion** scenario (the more complex of the two: real-time, HITL-required, cross-Service via RC-E2E-09 lot provenance). The dynamic-markdown scenario shares the same agent fleet, personas, and KPI attribution paths but operates on a weekly batch cadence instead of real-time. Engagements adopting dynamic-markdown clone this `_default/` directory and adjust:

- `scenario_id` → `rc-dynamic-markdown-optimization`
- `chain_execution.steps` — step 8 trigger becomes weekly cron, step 14 HITL paged to Daniel Chen instead of Marisol Reyes
- `smoke_test.fixture_path` → a markdown-batch fixture instead of the cold-chain event

For first-iteration first-client engagement (Sprint 47 per [Sprint-Plan.md](../../../../../docs/APEX%20-%20Design%20and%20Build/Sprint-Plan.md)), cold-chain is what gets deployed; dynamic-markdown follows in Sprint 48 / 49.

## What this use case demonstrates

- **Persona × KPI attribution** — Marisol's HITL approvals at step 14 affect `shrink-cost-reduction-pct` and `decision-loop-time-sec`; Daniel's weekly review at step 18 affects `gm-pp-lift`, `markdown-to-clear-pct`, and `doh-reduction-pct`. Each tied back to a specific Gold mart.
- **Pricer learning loop** — step 16 (Learn) writes back to Redis episodic memory + LEDGER, which step 12 (The Pricer / Quantify) reads on the next event for similarity search per Services Guide §25.8.
- **Cross-service composition** — step 10 (Assess) reads `SCML.Lot` which is owned by RC-E2E-09 (Product Tracking) per Services Guide §17.4. The `client_approved_architecture` block exposes RC-E2E-09's MCP surface as a consumed tool.
- **Audit row chain** — every decision step writes to Microsoft Purview Audit (system of record per ADR-003) and to the Fabric SQL ledger overlay for KPI attribution.

## Deploying this use case

### Laptop substrate (Independence-clean)

1. Open the wizard at `/wizard`
2. Pick `APEX-M` / `laptop` / `rc-e2e-03--default` / both featured RC-E2E-03 scenarios
3. Click "Render docker-compose.yml"
4. `cd ~/apex-deployments/<engagement> && docker-compose up -d`
5. Inject the smoke-test fixture per `smoke_test.laptop_command` in the YAML

The chain executes against mocks; no client cloud touched.

### Cloud substrates (dev/stage/prod)

1. Open the wizard at `/wizard`
2. Pick `APEX-M` / `dev` (or stage / prod) / use case slug / scenarios
3. Pre-deployment Security Gate runs (per substrate)
4. Render Bicep parameters; review
5. Click "Deploy" — `bicep_runner.py` shells out to `az`

## Cross-references

- [Use Case Template — Runnable Chain](../../../../../docs/APEX%20-%20Design%20and%20Build/Use-Case-Template-Runnable-Chain.md) — the template doc this use case implements
- [Services Guide §18.1](../../../../../docs/book/Professional-APEX-M-Services-Guide.html#ch-18-flagship) — the canonical RC-E2E-03 envelope
- [`services/_personas.yaml`](../../../../../_personas.yaml) — Marisol Reyes + Daniel Chen entries
- [`services/_kpis.yaml`](../../../../../_kpis.yaml) — gm-pp-lift, doh-reduction-pct, markdown-to-clear-pct, shrink-cost-reduction-pct, decision-loop-time-sec
- [`services/_use-case.schema.md`](../../../../../_use-case.schema.md) — full use-case YAML schema
