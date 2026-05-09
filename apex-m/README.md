# APEX-M — Microsoft variant

The Microsoft implementation of the APEX framework. Implements every
APEX-Core protocol against the Microsoft platform: Azure, Microsoft 365,
Power Platform, Microsoft Foundry, Microsoft Fabric, Microsoft Purview,
Microsoft Defender, Microsoft Entra.

**Status: First-shipped variant.** APEX-M is the first concrete
implementation of APEX-Core protocols. APEX-G (Google Cloud) and APEX-A
(AWS) are sibling products at the same layer — see
[`apex-g/`](../apex-g/) and [`apex-a/`](../apex-a/).

## Layout

```
apex-m/
  src/apex_m/                     # APEX-Core protocol implementations
    runtime_foundry.py            # AgentRuntime → Microsoft Foundry Agent Service
    identity_entra.py             # AgentIdentityProvider → Microsoft Entra Agent ID
    secret_store_keyvault.py      # SecretStore → Azure Key Vault
    audit_purview.py              # AuditLedger → Microsoft Purview Audit (primary)
    data_lake_fabric.py           # DataLake → Microsoft Fabric (OneLake/Lakehouse/Eventhouse)
    embedding_eventhouse_slm.py   # EmbeddingService → Eventhouse SLM ai_embeddings
    message_bus_eventstream.py    # MessageBus → Fabric Eventstream + Activator
    classifier_purview_labels.py  # SensitivityClassifier → Purview Information Protection
    observability_appinsights.py  # Observability → Azure Monitor + App Insights
    threat_defender.py            # ThreatProtection → Defender for Cloud + Defender for AI
  infra/bicep/                    # APEX-M infrastructure as code
    platform/                     # Layer 1: Foundry hub + project + Container Apps env + KV + ACR
    modules/                      # reusable: agent-fleet, mcp-server, hitl-gate, service
    blueprints/                   # 3-wave blueprints (W1/W2/W3)
    control-plane/                # the wizard's own resources
  LICENSE-ATTRIBUTION.md          # Microsoft attribution
  pyproject.toml
```

## Microsoft platform coverage

APEX-M targets the entire Microsoft stack a Deloitte client has typically
already invested in:

| Layer | Microsoft service |
|---|---|
| Agent runtime | Microsoft Foundry Agent Service (Hosted Agents) |
| Agent identity | Microsoft Entra Agent ID (GA April 2026) |
| Identity governance | Microsoft Entra ID Governance |
| Conditional Access | Microsoft Entra Conditional Access |
| Secrets | Azure Key Vault Premium HSM |
| Data tier | Microsoft Fabric (OneLake / Lakehouse / Eventhouse / Mirroring / Direct Lake) |
| Real-time | Fabric Real-Time Intelligence + Eventstream + Activator |
| Embeddings | Eventhouse SLM `ai_embeddings` plugin |
| BI | Power BI Direct Lake |
| Sensitivity labels | Microsoft Purview Information Protection |
| Audit | Microsoft Purview Audit + DSPM for AI |
| DLP | Microsoft Purview Data Loss Prevention |
| Threat protection | Microsoft Defender for Cloud + Defender for AI services |
| Content safety | Azure AI Content Safety Prompt Shields |
| Productivity surface | Microsoft 365 Copilot (custom engine agents via M365 Agents Toolkit) |
| Low-code | Microsoft Copilot Studio |
| Workflow | Power Automate |
| Custom apps | Power Apps · Power Pages · Dataverse |
| Security posture | Microsoft Cloud Security Benchmark v2 (AI Security baseline) |

## Books

The 6 APEX books in [`docs/book/`](../docs/book/) describe APEX-M
specifically (renamed with `-M-` infix). Future variant books for APEX-G
and APEX-A live alongside.

## Independence

Microsoft is the **first shipped** variant — not the **preferred** one.
APEX-G and APEX-A exist as sibling products on equal footing. Per
[Independence Posture](../docs/apex-core/Independence-Posture.md), Deloitte
ships the variant matching the client's existing cloud investment; we do
not have an alliance posture with any cloud.

See also: [LICENSE-ATTRIBUTION.md](LICENSE-ATTRIBUTION.md).
