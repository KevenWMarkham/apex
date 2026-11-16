# APEX-M dev deploy: Esparza landing zone (AI-DEV-Subscription / rg-ai-dev)

`main.bicep` deploys into an **existing** Foundry landing zone. It does not
create a Foundry account. Use `../platform/main.bicep` only for substrates
that need their own private-networked Foundry, ledger and Fabric.

| Creates | Name |
|---|---|
| Agent runtime managed identity | `id-apex-modtec-dev-agent` |
| Log Analytics + App Insights | `log-apex-modtec-dev`, `appi-apex-modtec-dev` |
| Azure AI User role for that identity on `modtec-foundry` | (role assignment) |
| Model deployments on `modtec-foundry` (only with `deployModels=true`) | `gpt-4o`, `gpt-4o-mini`, `text-embedding-3-large` |

## One-time setup (subscription admin)

1. **Resource providers** on AI-DEV-Subscription: `Microsoft.CognitiveServices`,
   `Microsoft.ManagedIdentity`, `Microsoft.OperationalInsights`, `Microsoft.Insights`.
   (Later waves also need `Microsoft.App`, `Microsoft.ContainerRegistry`,
   `Microsoft.Storage`, `Microsoft.Search`, `Microsoft.DocumentDB`, `Microsoft.Sql`.)
2. **Model quota** in East US 2, Global Standard, matching `ai-dev.bicepparam`:
   gpt-4o 100K TPM, gpt-4o-mini 50K TPM, text-embedding-3-large 50K TPM.
3. **Deployment identity for GitHub Actions**: an app registration (or user-assigned
   identity) with a federated credential:
   - Issuer `https://token.actions.githubusercontent.com`
   - Subject `repo:kevenwmarkham/apex:environment:ai-dev`
   - Audience `api://AzureADTokenExchange`

   Roles on `rg-ai-dev`: **Contributor**, plus **Role Based Access Control
   Administrator** (can be constrained to assigning Azure AI User) so the
   template can grant the agent identity access to `modtec-foundry`. Without
   the second role, set `assignFoundryRoles = false` and have an admin assign
   Azure AI User to `id-apex-modtec-dev-agent` by hand.

## One-time setup (GitHub)

Create a repository environment named **`ai-dev`** with these secrets:
`AZURE_CLIENT_ID` (the deployment identity), `AZURE_TENANT_ID` (Esparza
tenant), `AZURE_SUBSCRIPTION_ID` (AI-DEV-Subscription). Add a required
reviewer if deploys should be approved.

## Deploy

Actions → **Deploy · AI-DEV (rg-ai-dev)** → Run workflow:

1. `mode = what-if`: previews changes and touches nothing.
2. `mode = deploy`: applies. Outputs are written to the run summary.
3. After quota is approved, run again with `deploy_models` checked.

From a workstation (as a member of AZ-AI-Consultant):

```bash
az login --tenant modtechconsulting.com
az account set --subscription AI-DEV-Subscription
az deployment group what-if -g rg-ai-dev --parameters apex-m/infra/bicep/dev/ai-dev.bicepparam
az deployment group create  -g rg-ai-dev --parameters apex-m/infra/bicep/dev/ai-dev.bicepparam
```

## Check before the first run

- `foundryProjectName` must be the project's **resource name**, not its display name:
  `az resource list -g rg-ai-dev --resource-type Microsoft.CognitiveServices/accounts/projects -o table`
- If the portal no longer offers gpt-4o `2024-11-20`, switch the param to
  `gpt-4.1` and update `model_pin` in `packages/apex-agents/.../catalogs/`.
