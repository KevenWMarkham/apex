# LICENSE-ATTRIBUTION — APEX-M

APEX-M integrates with the Microsoft platform at the client's tenant.
This document records the Microsoft products and SDKs that APEX-M
references at compile time and at runtime.

## Microsoft products referenced

APEX-M is **not a redistribution** of any Microsoft product. APEX-M is
deployed into a client's existing Microsoft tenant, and uses these
Microsoft products under the licenses the client already holds:

- **Microsoft Azure** — Container Apps, Key Vault, Cosmos DB, Storage, Monitor, App Insights, Log Analytics, Container Registry, Service Bus, Event Grid
- **Microsoft Foundry** — Agent Service (Hosted Agents), Foundry projects, model deployments
- **Microsoft Entra** — Entra ID, Entra Agent ID (GA April 2026), Conditional Access, Workload ID, ID Governance
- **Microsoft Fabric** — OneLake, Lakehouse, Eventhouse, Eventstream, Activator, Mirroring, Real-Time Intelligence, Direct Lake, Fabric SQL Database
- **Microsoft Purview** — Information Protection, Audit, DLP, DSPM for AI
- **Microsoft Defender** — Defender for Cloud (CSPM, AI security posture), Defender for AI services, Defender XDR
- **Microsoft 365** — Microsoft 365 Copilot, Copilot Studio, Microsoft 365 Agents Toolkit, Teams, SharePoint, Outlook
- **Power Platform** — Power BI, Power Automate, Power Apps, Power Pages, Dataverse, AI Builder
- **Azure AI** — Azure AI Content Safety, Azure AI Search, Azure OpenAI Service

## Independence posture

Per Deloitte's Microsoft Technology & Services Practice, this attribution
records integration with the client's existing Microsoft investment.
Deloitte does **not**:

- Resell or sublicense any Microsoft product
- Position Microsoft as a "preferred" cloud (Microsoft is the **first
  shipped** APEX variant; APEX-G and APEX-A are sibling products)
- Co-mingle Deloitte ECIF with client subscriptions
- Use "alliance" or "partner" language in any APEX-M deliverable

See also:

- [Independence Posture](../docs/apex-core/Independence-Posture.md)
- [Variant Comparison](../docs/apex-core/Variant-Comparison.md)
- [APEX-G LICENSE-ATTRIBUTION](../apex-g/LICENSE-ATTRIBUTION.md)
- [APEX-A LICENSE-ATTRIBUTION](../apex-a/LICENSE-ATTRIBUTION.md)

## SDK dependencies

Concrete SDKs APEX-M imports at runtime (subject to the dependent SDK's
own license — typically MIT or Apache 2.0):

- `azure-identity` — Microsoft Entra authentication
- `azure-keyvault-secrets` — Key Vault SDK
- `azure-cosmos` — Cosmos DB SDK
- `azure-monitor-opentelemetry` — App Insights SDK
- `azure-mgmt-cognitiveservices` — Foundry management SDK

All SDK licenses are reproduced under `apex-m/third-party-licenses/` at
build time.
