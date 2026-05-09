# Pre-deployment Security Gate

**Audience:** Tenant SREs, engagement security leads, Independence reviewers
**Purpose:** The operator-facing checklist that every APEX-M tenant deployment must satisfy before the wizard emits Bicep parameters.

**Authoritative reference:** [APEX-M Deployment Guide ch 13.5](../book/Professional-APEX-M-Deployment-Guide.html#ch-13-5)
**Wizard surface:** `/security-gate` page (Phase I.7 follow-up sprint to wire live polling)

---

## How this works

The wizard's **render endpoint** refuses to emit Bicep parameters when any required gate is **red**. Operator workflow:

1. Open the wizard's `/security-gate` page; pick the target tenant.
2. The page polls Microsoft Defender for Cloud, Microsoft Purview, and Microsoft Entra and reports per-gate state (`green` / `yellow` / `red`).
3. Click into any non-green gate to see the remediation steps.
4. Once all required gates are green, click "Approve gate" — evidence (Defender posture report, Purview labels report, AI Model Security scan output) attaches to the engagement audit trail.
5. The render endpoint is now unblocked for this tenant + this wave.

---

## Substrate-aware enforcement

| Substrate | Required gates | Waivable gates |
|---|---|---|
| `lab` | 1, 2, 3, 4, 9, 10, 11, 12, 14 | 5, 6, 7, 8, 13 (with documented sign-off) |
| `dev` | 1, 2, 3, 4, 9, 10, 11, 12, 14 | 5, 6, 7, 8, 13 |
| `stage` | **all 14** | none |
| `prod` | **all 14** | none |
| `pilot` | **all 14** | none |
| `ga` | **all 14** | none |

A waiver requires sign-off from the engagement's tenant SRE + the Deloitte Independence Office (per gate #14).

---

## Structural gates (one-time per tenant)

### Gate 1 · Defender for Cloud CSPM with AI security posture
- **Microsoft control**: [Defender CSPM plan with DSPM for AI](https://learn.microsoft.com/azure/defender-for-cloud/ai-security-posture)
- **MCSB v2**: AI-1, AI-2
- **Verify**: Azure portal → Defender for Cloud → Environment Settings → subscription → CSPM enabled, "AI Security Posture Management" toggled on.
- **Remediate**: enable Defender CSPM plan; ensure the subscription is onboarded to Defender for Cloud.

### Gate 2 · Defender for AI services on Foundry project
- **Microsoft control**: [Defender for AI services threat protection](https://learn.microsoft.com/azure/defender-for-cloud/ai-threat-protection)
- **MCSB v2**: AI-3
- **Verify**: Defender for Cloud → Environment Settings → Defender for AI services plan = ON.
- **Remediate**: enable Defender for AI services on the subscription.

### Gate 3 · Microsoft Entra Agent ID tenant root blueprint
- **Microsoft control**: [Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/what-is-microsoft-entra-agent-id) per [Deployment Guide §5.1.1](../book/Professional-APEX-M-Deployment-Guide.html#ch-5-1-1)
- **MCSB v2**: AI-7
- **Verify**: `apex-m/infra/bicep/platform/identity.bicep` deployment script succeeded; Microsoft Graph `GET /agentIdentities/blueprints/apex-m-tenant-root` returns 200.
- **Remediate**: run the platform Bicep with the `apex-m-tenant-root` blueprint provisioned.

### Gate 4 · Purview sensitivity labels enabled for SharePoint and OneDrive
- **Microsoft control**: [Purview Information Protection](https://learn.microsoft.com/purview/sensitivity-labels-sharepoint-onedrive-files)
- **MCSB v2**: AI-4
- **Verify**: Microsoft Purview portal → Information Protection → Labels → "Sensitivity labels for Office files in SharePoint and OneDrive" = enabled.
- **Remediate**: run `Enable-SPOSensitivityLabel` PowerShell.

### Gate 5 · Purview Audit retention configured
- **Microsoft control**: [Purview Audit retention policies](https://learn.microsoft.com/purview/audit-log-retention-policies)
- **MCSB v2**: AI-5
- **Verify**: Purview portal → Audit → Retention → minimum 90d, default 7y, regulated industry (HLS) 10y.
- **Remediate**: create retention policies per the engagement's regulatory overlay.

### Gate 6 · Customer Managed Keys (CMK) for Storage + Cognitive Services
- **Microsoft control**: [Microsoft.KeyVault Premium HSM](https://learn.microsoft.com/azure/key-vault/keys/hsm-protected-keys)
- **MCSB v2**: DP-2
- **Verify**: Storage Account encryption uses CMK from tenant Key Vault Premium HSM; Cognitive Services account encryption uses CMK.
- **Remediate**: configure CMK on both resources.

### Gate 7 · Customer Lockbox enabled
- **Microsoft control**: [Customer Lockbox for Microsoft Azure](https://learn.microsoft.com/azure/security/fundamentals/customer-lockbox-overview)
- **MCSB v2**: GS-7
- **Verify**: Azure portal → Customer Lockbox = enabled at subscription scope.
- **Remediate**: enable Customer Lockbox.

### Gate 8 · Workspace-level IP firewall on Fabric workspaces
- **Microsoft control**: [Fabric workspace IP Firewall (Preview)](https://learn.microsoft.com/fabric/security/security-workspace-level-firewall-overview)
- **MCSB v2**: NS-2
- **Verify**: Fabric admin portal → workspace → IP Firewall = configured with allow list.
- **Remediate**: configure IP firewall rules per tenant network policy.

---

## Per-deployment gates (per wave)

### Gate 9 · AI Model Security scan green
- **Microsoft control**: [Defender AI Model Security (Preview)](https://learn.microsoft.com/azure/defender-for-cloud/ai-model-security)
- **MCSB v2**: AI-3
- **Verify**: Defender portal → AI security → Model scan results for every agent image used in this deployment = no critical findings.
- **Remediate**: re-scan; remediate findings; replace image.

### Gate 10 · Conditional Access on the service blueprint
- **Microsoft control**: [Microsoft Entra Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/overview)
- **MCSB v2**: AC-2
- **Verify**: Microsoft Graph `GET /agentIdentities/blueprints/apex-m-{service-code}-blueprint` includes CA policy ids for compliant device + MFA on HITL approver session.
- **Remediate**: attach the CA policies to the service blueprint via the wizard's Identity tab.

### Gate 11 · HITL threshold config in Key Vault
- **Microsoft control**: Azure Key Vault + APEX-M HITL gate config (per Deployment Guide ch 9)
- **MCSB v2**: DP-3
- **Verify**: every `decide` and `act` agent in scope has a Key Vault secret at `apex-hitl-{tenant}-{service}-{scenario}-{role}` with current threshold values.
- **Remediate**: configure thresholds via the wizard's HITL tab.

### Gate 12 · Use case `client_approved_architecture` resolves
- **Microsoft control**: APEX wizard validator
- **Verify**: every adapter ref in the use case's `client_approved_architecture` block resolves to `packages/apex-adapters/src/apex_adapters/protocol_adapters/{adapter}/`; every persona id in `_personas.yaml`; every KPI id in `_kpis.yaml`.
- **Remediate**: fix the use-case YAML; re-run the wizard validator.

### Gate 13 · Foundry Standard Setup with Private Networking
- **Microsoft control**: [Foundry Agent Service private networking](https://learn.microsoft.com/azure/foundry/agents/how-to/virtual-networks)
- **MCSB v2**: NS-1
- **Required for**: `stage` and `prod` substrates only (waived for lab/dev with sign-off).
- **Verify**: Foundry account public network access = Disabled; agent subnet delegated to `Microsoft.App/environments`; six private DNS zones configured (cognitiveServices, openAi, servicesAi, aiSearch, cosmosDb, storageBlob).
- **Remediate**: redeploy `apex-m/infra/bicep/platform/foundry.bicep` with private-networking params populated.

### Gate 14 · Independence consultation per adapter
- **Microsoft control**: Deloitte Independence Office
- **Verify**: every adapter in `client_approved_architecture` has an Independence consultation record in the engagement's audit trail.
- **Remediate**: schedule Independence consultation; record sign-off; re-run the gate.

---

## Evidence artifacts

The wizard's "Approve gate" workflow attaches the following to the engagement audit trail:

- **Gate 1+2 evidence**: Defender for Cloud posture report PDF (export from portal)
- **Gate 4+5 evidence**: Purview labels & retention export
- **Gate 6+7 evidence**: Azure Resource Graph query result showing CMK + Customer Lockbox state
- **Gate 9 evidence**: AI Model Security scan JSON output for each image
- **Gate 10 evidence**: Microsoft Graph response for the service blueprint with CA policy ids visible
- **Gate 11 evidence**: Key Vault secret listing (names only — never values)
- **Gate 13 evidence**: Bicep what-if output for the Foundry account showing `publicNetworkAccess: Disabled`
- **Gate 14 evidence**: Independence Office sign-off email per adapter

---

## When this checklist updates

- Microsoft adds a new pre-prod control (e.g., a new MCSB v2 AI control) → add a gate
- A waivable gate proves to be required in practice → upgrade it to required for that substrate
- A vendor adapter joins `apex-adapters/.../protocol_adapters/` → trigger Gate 14 for the engagements that adopt it

The wizard tracks gate definitions in `services/_security-gate.yaml` (TBD) so updates ship without code changes.
