# APEX Technical Pre-Clearance Checklist

Run before signing a Wave-1 SoW. Each item must be either confirmed or have a
mitigation plan. Tied to Sprint 14 / 15 / 16 / 17 / 18 deliverables.

## Capacity & infrastructure

- [ ] Microsoft Fabric F-SKU sized appropriately (F64 / F128 / F256) per Sprint 14 capacity blueprint
- [ ] Capacity blueprint type chosen (single-capacity-tenant / dev-prod-split / per-workload-isolation)
- [ ] Azure region selected with Fabric availability + appropriate data residency
- [ ] Private-endpoint posture confirmed (Sprint 14 isolation pattern)
- [ ] Subscription / EA enrollment confirmed; cost-center allocation defined
- [ ] Reserved-capacity vs. PAYG decision made

## SOR adapters (Sprint 15)

- [ ] All required SOR adapters present in `apex-adapters` catalog
- [ ] SOR access granted (read-mirror / API-token / service-principal as applicable)
- [ ] Mirroring CDC viable for primary SOR (SAP / Oracle / Epic / Manhattan / etc.)
- [ ] Schema mappings reviewed for schema-drift / source-system-version compatibility

## Canonical schemas (Sprint 22-24, downstream)

- [ ] Canonical schema families instantiated in Silver (SCML / MERML / PatientML / GridML / etc.)
- [ ] Schema package implementation (`apex-scml`, `apex-merml`, etc.) cloned/installed where Wave-1 needs it
- [ ] Cross-schema references (loyalty across RC + TH; HSE across ER + AXLE) identified

## Foundry / model

- [ ] Azure AI Foundry resource provisioned in target region
- [ ] Required model deployments (gpt-4o, gpt-4o-mini, o1) requested + capacity confirmed
- [ ] Embedding model (text-embedding-3-large) deployed
- [ ] Token budget / rate-limit posture acceptable for Wave-1 traffic estimates
- [ ] Prompt-SHA pinning + version-tracking process agreed

## Identity & networking

- [ ] Entra ID P2 in place; Conditional Access policies for Fabric / Foundry covered
- [ ] Workload identities for agents created (no long-lived secrets)
- [ ] Private endpoints for Fabric / Foundry / Purview
- [ ] DNS / firewall rules for SOR connectivity vetted

## Audit & telemetry

- [ ] Purview Audit Premium enabled; long-retention path confirmed
- [ ] Audit-row schema implemented per Sellers Guide §6.10
- [ ] Decision-record store provisioned (Fabric warehouse or dedicated KQL DB)
- [ ] Replay-token generation hooked

## Agent runtime

- [ ] Copilot Studio license posture clear (Standard or Agent Builder Kit)
- [ ] Teams Premium where rich HITL surfaces required
- [ ] HITL surface decisions made per agent (Teams card / Copilot Studio / dashboard)

## Cross-reference

- Sprint 14 capacity blueprints (Terraform)
- Sprint 15 adapter manifests
- Sprint 16 agent catalog
- Sprint 17 service catalog
- Sprint 18 reference deployment
