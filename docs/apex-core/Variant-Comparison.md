# APEX Variant Comparison

Capability matrix across the three sibling variants. Updated as APEX-G and APEX-A ship.

## Variants at a glance

| Property | APEX-M | APEX-G | APEX-A |
|---|---|---|---|
| Cloud | Microsoft Azure / M365 / Power Platform | Google Cloud Platform / Workspace | Amazon Web Services |
| Status | **First shipped** | Stub package | Stub package |
| Concrete impls | In progress (Phase I) | None — port plan | None — port plan |
| IaC | Bicep — `apex-m/infra/bicep/` | Terraform (planned) — `apex-g/infra/terraform-gcp/` | CloudFormation (planned) — `apex-a/infra/cloudformation/` |
| Agent runtime | Foundry Agent Service (Hosted Agents) | Vertex AI Agent Builder | Bedrock Agents |
| Books | 6 (renamed with `-M-` infix) | Future | Future |
| Wizard support | Full | Listed; render disabled | Listed; render disabled |

## Layer-by-layer comparison

### Compute
| | APEX-M | APEX-G | APEX-A |
|---|---|---|---|
| Containers (non-agent) | Azure Container Apps | Cloud Run | ECS Fargate |
| Functions | Azure Functions | Cloud Functions / Cloud Run Functions | Lambda |
| Kubernetes | AKS | GKE | EKS |

### Identity
| | APEX-M | APEX-G | APEX-A |
|---|---|---|---|
| Workforce | Microsoft Entra ID | Cloud Identity / Workspace | IAM Identity Center |
| Workload | UAMI + Workload Identity Federation | Workload Identity Federation | IAM Roles + Roles Anywhere |
| Agents | **Microsoft Entra Agent ID** (GA Apr 2026) | Cloud IAM service-account impersonation | IAM AssumeRole + Bedrock identity |
| Conditional Access | Entra Conditional Access | Context-Aware Access | IAM Identity Center policies |

### Data tier
| | APEX-M | APEX-G | APEX-A |
|---|---|---|---|
| Lakehouse | Microsoft Fabric Lakehouse + OneLake | BigQuery + Cloud Storage + Dataform | Lake Formation + S3 + Glue |
| Bronze (real-time) | Eventstream / Eventhouse / Mirroring | Pub/Sub → BigQuery streaming | Kinesis → S3 / Lake Formation |
| Bronze (batch) | Data Pipeline / Dataflow Gen2 | Cloud Composer / Dataflow | AWS Glue / Step Functions |
| Silver | Direct Lake / Warehouse / KQL | BigQuery views + Dataform models | Lake Formation governed tables |
| Gold | Direct Lake semantic models / KQL functions | BigQuery materialized views | Athena views + Lake Formation |
| Embeddings | Eventhouse SLM `ai_embeddings` (in-data-tier) | Vector Search + text-embedding-005 | OpenSearch Vector + Titan Embeddings |
| BI | Power BI Direct Lake | Looker / Looker Studio | QuickSight + Athena |

### Security & Governance
| | APEX-M | APEX-G | APEX-A |
|---|---|---|---|
| Sensitivity labels | Microsoft Purview Information Protection | Sensitive Data Protection (Cloud DLP) | Macie + Comprehend custom |
| DLP | Microsoft Purview DLP | Cloud DLP + Drive DLP | Macie + S3 + Network Firewall |
| Audit (system of record) | Microsoft Purview Audit | Cloud Audit Logs | CloudTrail |
| Threat protection (AI) | Defender for AI services + Defender for Cloud (CSPM) + Azure AI Content Safety | Vertex AI safety filters + Chronicle SecOps | Bedrock Guardrails + GuardDuty + Security Hub |
| AI security posture | Defender for Cloud DSPM for AI | Security Command Center | Security Hub + Inspector |
| SIEM (built-in) | Microsoft Sentinel | Chronicle SecOps | Security Lake |

### Productivity surface
| | APEX-M | APEX-G | APEX-A |
|---|---|---|---|
| Productivity suite | Microsoft 365 (Word, Excel, PowerPoint, Outlook, Teams) | Google Workspace (Docs, Sheets, Slides, Gmail, Chat) | WorkDocs / WorkMail (limited) |
| Copilot surface | Microsoft 365 Copilot + Copilot Studio | Gemini for Workspace + Vertex AI Agent Builder | Q in QuickSight / Q Business |
| Agent publishing | Microsoft 365 Agents Toolkit + Agent Service registration | Vertex Agent Engine deploy + Workspace add-on | Bedrock Agents endpoint + AppSync |
| Low-code | Power Platform (Power Apps / Power Automate / Power Pages / Dataverse) | AppSheet | Honeycode (sunset) / Step Functions |

### Cost management
| | APEX-M | APEX-G | APEX-A |
|---|---|---|---|
| FinOps surface | Microsoft Cost Management + Azure Advisor | Cloud Billing + Recommender | AWS Cost Explorer + Compute Optimizer |
| Per-agent cost attribution | Tags on Foundry projects + Cost Management views | BigQuery billing export + labels | CUR + tags |

## Capability gaps to track

When APEX-G or APEX-A ships, audit these feature gaps:

- **APEX-G gap (today)**: Vertex AI Agent Engine doesn't yet have a 1:1 equivalent for Microsoft Foundry's "Hosted Agents" container deploy pattern. Workaround: `gcloud run deploy` + Cloud IAM agent-binding. Track as port-plan item.
- **APEX-A gap (today)**: Bedrock Agents lacks the unified content-safety surface that Defender for AI provides. Workaround: layer Bedrock Guardrails + Macie + GuardDuty. Track as port-plan item.

## When this matrix updates

- APEX-G ships → entries become concrete, port-plan column collapses
- APEX-A ships → same
- New cloud capability (e.g., Microsoft Entra Agent ID GA in April 2026) → APEX-M column updates
- Defer terminology rebrands to a single Sprint 30.F batch
