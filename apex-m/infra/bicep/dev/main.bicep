// apex-m/infra/bicep/dev/main.bicep
// APEX-M dev entry point for an EXISTING Foundry landing zone.
//
// Use this instead of platform/main.bicep when the client's landing zone
// already provides the Foundry account + project (e.g. AI-DEV-Subscription /
// rg-ai-dev / modtec-foundry / Demo-Agent). platform/main.bicep is not
// deployable there: it creates its own private-networked Foundry account,
// its identity module calls Microsoft Graph with permissions a dev
// deployment principal does not hold, and its ledger module creates a SQL
// server with no administrator configured.
//
// Provisions (all idempotent):
//   1. User-assigned managed identity for the agent runtime
//   2. Log Analytics + App Insights (reuses platform/monitoring.bicep)
//   3. Azure AI User (a.k.a. Foundry User) for that identity on the existing
//      Foundry account (optional; the deployer needs roleAssignments/write)
//   4. Model deployments on the existing Foundry account (optional; needs
//      quota in the subscription — off by default)

targetScope = 'resourceGroup'

@description('APEX tenant slug, used in resource names. Lowercase, dash-only.')
@minLength(3)
@maxLength(40)
param tenant string

@description('Azure region for new resources. Must match the Foundry account region for model deployments.')
param location string = resourceGroup().location

@description('Extra tags merged onto every new resource.')
param tags object = {}

@description('Name of the existing Foundry (Microsoft.CognitiveServices/accounts) resource in this resource group.')
param foundryAccountName string

@description('Resource name of the existing Foundry project under that account.')
param foundryProjectName string

@description('Grant the agent identity Azure AI User on the Foundry account. Requires Microsoft.Authorization/roleAssignments/write for the deployer.')
param assignFoundryRoles bool = true

@description('Create the model deployments below. Leave false until the subscription has quota for them.')
param deployModels bool = false

type modelDeployment = {
  @description('Deployment name that agent code calls (keep equal to the model name unless there is a reason not to).')
  name: string
  @description('Model publisher format, e.g. OpenAI.')
  format: string
  @description('Model name, e.g. gpt-4o.')
  model: string
  @description('Model version, e.g. 2024-11-20.')
  version: string
  @description('Deployment SKU, e.g. GlobalStandard.')
  sku: string
  @description('Capacity in units of 1K tokens per minute.')
  @minValue(1)
  capacity: int
}

@description('Model deployments to create on the Foundry account when deployModels=true.')
param modelDeployments modelDeployment[] = []

var allTags = union(
  {
    'apex-tenant': tenant
    'apex-component': 'platform'
    'apex-env': 'dev'
    'apex-variant': 'APEX-M'
  },
  tags
)

// Built-in role: Azure AI User (renamed Foundry User; the id is unchanged).
// Least-privilege Foundry role: read the account/project and call its data
// plane (agents, model inference).
var azureAiUserRoleId = '53ca6127-db72-4b80-b1b0-d745d6d5456d'

// ---------------------------------------------------------------------------
// Existing landing-zone resources (referencing them also fails fast if the
// names are wrong or the deployer cannot see them)
// ---------------------------------------------------------------------------
resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: foundryAccountName
}

resource foundryProject 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' existing = {
  parent: foundry
  name: foundryProjectName
}

// ---------------------------------------------------------------------------
// Agent runtime identity
// ---------------------------------------------------------------------------
resource agentIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-apex-${tenant}-agent'
  location: location
  tags: union(allTags, { 'apex-component': 'agent-runtime-identity' })
}

module monitoring '../platform/monitoring.bicep' = {
  name: 'apex-monitoring-${tenant}'
  params: {
    tenant: tenant
    location: location
    tags: allTags
  }
}

resource agentFoundryUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (assignFoundryRoles) {
  name: guid(foundry.id, agentIdentity.id, azureAiUserRoleId)
  scope: foundry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', azureAiUserRoleId)
    principalId: agentIdentity.properties.principalId
    principalType: 'ServicePrincipal'
    description: 'APEX-M agent runtime: Foundry data-plane access (dev).'
  }
}

// ---------------------------------------------------------------------------
// Model deployments — serialized; concurrent deployments on one account conflict
// ---------------------------------------------------------------------------
@batchSize(1)
resource models 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = [
  for m in (deployModels ? modelDeployments : []): {
    parent: foundry
    name: m.name
    sku: {
      name: m.sku
      capacity: m.capacity
    }
    properties: {
      model: {
        format: m.format
        name: m.model
        version: m.version
      }
      versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
    }
  }
]

// ---------------------------------------------------------------------------
// Outputs — wire these into agent configuration
// ---------------------------------------------------------------------------
output agentIdentityId string = agentIdentity.id
output agentIdentityClientId string = agentIdentity.properties.clientId
output agentIdentityPrincipalId string = agentIdentity.properties.principalId
output logAnalyticsWorkspaceId string = monitoring.outputs.workspaceId
output appInsightsConnectionString string = monitoring.outputs.appInsightsConnectionString
output foundryAccountId string = foundry.id
output foundryAccountEndpoint string = foundry.properties.endpoint
output foundryProjectId string = foundryProject.id
output modelDeploymentNames array = [for (m, i) in (deployModels ? modelDeployments : []): models[i].name]
