# APEX Independence Posture

**Audience:** Deloitte engagement teams, client architecture review boards, SEC Independence reviewers
**Status:** Authoritative — referenced by every APEX deliverable

## TL;DR

APEX is a multi-cloud framework with three sibling product variants on a shared protocol contract:

- **APEX-M** — Microsoft variant. **First shipped.**
- **APEX-G** — Google Cloud variant. Stub today; ships when commissioned.
- **APEX-A** — AWS variant. Stub today; ships when commissioned.

Microsoft is the **first shipped** variant — not the **preferred** cloud. Deloitte does not have an alliance posture with any cloud provider. APEX exists to honor a client's **existing cloud investment** as approved by their Cloud Architecture Board (CAB).

## Two Contracts (per Deployment Guide §3)

Every APEX engagement honors the two-contract model:

1. **Client–Microsoft (or Client–Google, or Client–AWS)** — the client holds and pays for cloud subscriptions, model deployments, storage, networking. Deloitte does not co-mingle ECIF.
2. **Client–Deloitte** — Deloitte provides the APEX framework + deployment + agent design + change management. Subscription costs flow through the client's contract with the cloud provider, not Deloitte.

For multi-cloud clients (e.g., Microsoft 365 + AWS data lake), each contract chain stands on its own. APEX-M handles the M365/Azure side; client-approved AWS adapters integrate the AWS side without Deloitte resale.

## Variant equality

The three APEX variants are **structurally equivalent**:

- All three implement the same 10 [APEX-Core protocols](Protocols-Reference.md)
- All three have a real `pyproject.toml`, README, LICENSE-ATTRIBUTION, source tree
- All three are listed in `apps/deploy-wizard/` as Cloud Variant choices
- All three have a port plan ([Multi-Cloud Port Plan](Multi-Cloud-Port-Plan.md))

The fact that APEX-M ships first is **commercial reality** (Deloitte's Microsoft Technology & Services Practice has the deepest staffing on Microsoft) — not a structural preference.

## Client-Approved Architecture Variance

A typical Fortune-500 client runs **mixed** infrastructure:

> *"Microsoft 365 for productivity + Azure for identity + AWS for the data lake (Snowflake on AWS) + Splunk for SIEM + Okta for federated identity"*

APEX honors this via the **adapter pattern**:

- **Primary variant** (one of M / G / A) hosts the agent runtime and orchestration substrate
- **Composed adapters** integrate non-primary services into APEX-Core protocols

The client picks the primary variant based on where they want agents to *run*. Adapters cover everything else. Per-tenant choice lives in `services/{ind}/{code}/use-cases/{slug}/use-case.yaml` under `client_approved_architecture`.

Adapters in scope today (stub — implementations build per-engagement):

- **cloud**: AWS S3 / RDS / EventBridge / KMS / Secrets Manager · GCP BigQuery / Pub/Sub / GCS / KMS / Secret Manager · Azure ADLS Gen2 / Event Grid / Storage
- **saas**: Salesforce, Snowflake, Databricks, ServiceNow, SAP, Workday
- **siem**: Splunk, Sumo Logic, Datadog, QRadar
- **identity**: Okta, Auth0, Ping Identity
- **collaboration**: Slack, Zoom, Google Workspace

Each adapter has a `sec_independence.md` recording that Deloitte does not resell, license, or have an alliance posture with the integrated provider.

## Language standards (enforced)

The `apex-compliance-lint` package (BL.P.194 in [Roadmap.md](../APEX%20-%20Design%20and%20Build/Roadmap.md)) blocks publication of any APEX deliverable using disallowed terminology:

- ❌ "preferred cloud" / "primary cloud" (when used commercially)
- ❌ "alliance" / "partner" / "partnership" (with cloud providers)
- ❌ "Microsoft alliance" / "AWS alliance" / "Google alliance"
- ❌ "Deloitte–Microsoft alliance" or any equivalent
- ✅ "Deloitte's Microsoft Technology & Services Practice"
- ✅ "APEX-M is the first shipped variant"
- ✅ "Honors the client's existing investment in [provider]"
- ✅ "Per the client's Cloud Architecture Board approval"

## Audit defensibility

When SEC Independence reviewers, client compliance officers, or audit teams examine APEX:

- They see **three sibling product packages** (`apex-m/`, `apex-g/`, `apex-a/`) with real Python imports
- They see **three LICENSE-ATTRIBUTION files** with structurally identical Independence statements
- They see **a single shared protocol surface** (`apex_core.protocols`) — APEX is portable by construction
- They see **a Multi-Cloud Port Plan** documenting how G and A get built when commissioned
- They see **per-adapter Independence statements** for every non-primary service integration
- They see **the deploy-wizard's Cloud Variant selector** treating M/G/A as equal choices

This satisfies the structural-Independence test articulated in Deployment Guide §3.3.

## When a client asks "is APEX Microsoft-only?"

The answer is: **No. APEX is multi-cloud.** APEX-M is the first shipped variant because Microsoft was where Deloitte's Microsoft Technology & Services Practice had the deepest staffing. APEX-G and APEX-A are sibling products on equal footing — same APEX-Core protocols, same wizard, same scenario catalog. Deloitte ships the variant matching your existing cloud investment. If your CAB has approved a mixed architecture, APEX composes adapters per your approved services.

## References

- [Variant Comparison](Variant-Comparison.md) — capability matrix per variant
- [Protocols Reference](Protocols-Reference.md) — the 10 shared protocols
- [Multi-Cloud Port Plan](Multi-Cloud-Port-Plan.md) — how APEX-G and APEX-A ship
- [Adapter Catalog](Adapter-Catalog.md) — full adapter inventory
- [APEX-M LICENSE-ATTRIBUTION](../../apex-m/LICENSE-ATTRIBUTION.md)
- [APEX-G LICENSE-ATTRIBUTION](../../apex-g/LICENSE-ATTRIBUTION.md)
- [APEX-A LICENSE-ATTRIBUTION](../../apex-a/LICENSE-ATTRIBUTION.md)
- [Deployment Guide §3 — Independence Posture for Deployment](../book/Professional-APEX-M-Deployment-Guide.html#ch-3)
