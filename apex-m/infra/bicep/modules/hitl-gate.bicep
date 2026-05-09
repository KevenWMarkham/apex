// infra/bicep/modules/hitl-gate.bicep
// Provisions the Teams Adaptive Card webhook + audit-row binding for a
// human-in-the-loop approval gate. Used by `decide` and `act` agents.

targetScope = 'resourceGroup'

param tenant string
param serviceCode string
param scenarioId string

@description('Teams incoming-webhook URL stored in Key Vault.')
param teamsWebhookSecretUri string

@description('Threshold above which HITL approval is required.')
param threshold object = {
  markdownPercent: 30
  refundUsd: 500
}

resource cfg 'Microsoft.App/managedEnvironments/storages@2024-03-01' existing = if (false) {
  // placeholder — actual resource: a JSON config blob in storage referenced
  // by the agent at runtime. Resolved by the deploy-wizard.
  name: 'placeholder/placeholder'
}

output hitlConfig object = {
  tenant: tenant
  serviceCode: serviceCode
  scenarioId: scenarioId
  teamsWebhookSecretUri: teamsWebhookSecretUri
  threshold: threshold
}
