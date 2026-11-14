// apex-m/infra/bicep/dev/ai-dev.bicepparam
// Esparza landing zone: AI-DEV-Subscription / rg-ai-dev (East US 2).
//
// Deploy:
//   az deployment group create -g rg-ai-dev \
//     --parameters apex-m/infra/bicep/dev/ai-dev.bicepparam
// Add `--parameters deployModels=true` once quota is granted.
using 'main.bicep'

param tenant = 'modtec-dev'
param location = 'eastus2'

param foundryAccountName = 'modtec-foundry'

// Resource name of the project, which can differ from its display name.
// Confirm with: az resource list -g rg-ai-dev --resource-type Microsoft.CognitiveServices/accounts/projects -o table
param foundryProjectName = 'Demo-Agent'

param assignFoundryRoles = true

// Off until the quota request for AI-DEV-Subscription is approved.
param deployModels = false

// Sized for a dev demo. gpt-4o 2024-11-20 is the pin used by most agents in
// packages/apex-agents catalogs; if the portal no longer offers that version,
// switch to gpt-4.1 and update the catalog pins to match.
param modelDeployments = [
  {
    name: 'gpt-4o'
    format: 'OpenAI'
    model: 'gpt-4o'
    version: '2024-11-20'
    sku: 'GlobalStandard'
    capacity: 100
  }
  {
    name: 'gpt-4o-mini'
    format: 'OpenAI'
    model: 'gpt-4o-mini'
    version: '2024-07-18'
    sku: 'GlobalStandard'
    capacity: 50
  }
  {
    name: 'text-embedding-3-large'
    format: 'OpenAI'
    model: 'text-embedding-3-large'
    version: '1'
    sku: 'GlobalStandard'
    capacity: 50
  }
]
