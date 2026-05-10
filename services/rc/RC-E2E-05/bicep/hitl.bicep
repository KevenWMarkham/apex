// services/rc/RC-E2E-05/bicep/hitl.bicep
//
// Sprint 35.2c. Materialises RC-E2E-05 HITL threshold + Adaptive Card webhook
// from `services/rc/RC-E2E-05/config/hitl-thresholds.yaml` as Azure Key Vault
// secrets. Decide agent reads via Managed Identity + Key Vault Secrets User.

targetScope = 'resourceGroup'

@description('APEX tenant slug — keyvault secret prefix.')
param tenant string

@description('Existing Key Vault name in the platform RG.')
param keyVaultName string

@description('Resource ID of the agent runtime managed identity (granted Get permission).')
param agentIdentityId string

@description('Max total tasks Decide auto-clears without HITL.')
@minValue(0)
@maxValue(200)
param autoClearMaxTotalTasks int = 8

@description('Max P0_critical tasks tolerated before HITL fires.')
@minValue(0)
@maxValue(50)
param autoClearMaxP0Tasks int = 0

@description('Max unassignable tasks tolerated before HITL fires.')
@minValue(0)
@maxValue(50)
param autoClearMaxUnassignableTasks int = 0

@description('Whether `raise_replenishment_request` tasks require HITL.')
param requireHitlForReplenishmentRequest bool = true

@description('Teams webhook URL for HITL Adaptive Cards.')
@secure()
param teamsWebhookUrl string

var serviceCode = 'rc-e2e-05'
var secretPrefix = 'apex-hitl-${tenant}-${serviceCode}'

resource kv 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}

resource secAutoClearMaxTotal 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--auto-clear-max-total-tasks'
  properties: {
    value: string(autoClearMaxTotalTasks)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=count'
  }
}

resource secAutoClearMaxP0 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--auto-clear-max-p0-tasks'
  properties: {
    value: string(autoClearMaxP0Tasks)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=count'
  }
}

resource secAutoClearMaxUnassignable 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--auto-clear-max-unassignable-tasks'
  properties: {
    value: string(autoClearMaxUnassignableTasks)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=count'
  }
}

resource secRequireHitlReplen 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--require-hitl-for-replenishment-request'
  properties: {
    value: string(requireHitlForReplenishmentRequest)
    contentType: 'application/x-apex-hitl-threshold; type=boolean'
  }
}

resource secTeamsWebhook 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--teams-webhook'
  properties: {
    value: teamsWebhookUrl
    contentType: 'application/x-apex-hitl-webhook; channel=teams'
  }
}

var keyVaultSecretsUserRoleId = '4633458b-17de-408a-b874-0445c86b69e6'

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: kv
  name: guid(kv.id, agentIdentityId, keyVaultSecretsUserRoleId, serviceCode)
  properties: {
    principalId: agentIdentityId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      keyVaultSecretsUserRoleId
    )
  }
}

output hitlSecretIds object = {
  autoClearMaxTotalTasks: secAutoClearMaxTotal.id
  autoClearMaxP0Tasks: secAutoClearMaxP0.id
  autoClearMaxUnassignableTasks: secAutoClearMaxUnassignable.id
  requireHitlForReplenishmentRequest: secRequireHitlReplen.id
  teamsWebhook: secTeamsWebhook.id
}

output secretPrefix string = secretPrefix
