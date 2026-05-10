// services/rc/RC-E2E-05/bicep/main.bicep
// Service-level deployment for RC-E2E-05 Store Operations / On-Shelf Availability.
// Composes the canonical agent-fleet module with service-specific schemas,
// personas (Jamie O'Connor), and HITL policy.

targetScope = 'resourceGroup'

@description('APEX tenant slug (e.g., contoso-prod).')
param tenant string

@description('Wave being deployed: w1 | w2 | w3.')
@allowed([ 'w1', 'w2', 'w3' ])
param wave string

@description('Featured scenario IDs to deploy in this wave.')
param featuredScenarios array = []

@description('Container Apps environment resource ID.')
param containerAppsEnvId string

@description('Managed identity resource ID for agent runtime.')
param agentIdentityId string

@description('Existing Key Vault name in the platform RG (HITL secrets land here).')
param keyVaultName string

@description('Tenant Teams webhook for HITL Adaptive Cards.')
@secure()
param teamsWebhookUrl string

@description('Sprint 35.2c — max total tasks Decide auto-clears without HITL.')
@minValue(0)
@maxValue(200)
param autoClearMaxTotalTasks int = 8

@description('Sprint 35.2c — max P0_critical tasks tolerated before HITL fires.')
@minValue(0)
@maxValue(50)
param autoClearMaxP0Tasks int = 0

@description('Sprint 35.2c — max unassignable tasks tolerated before HITL fires.')
@minValue(0)
@maxValue(50)
param autoClearMaxUnassignableTasks int = 0

@description('Sprint 35.2c — whether `raise_replenishment_request` requires HITL.')
param requireHitlForReplenishmentRequest bool = true

var serviceCode = 'RC-E2E-05'

// -----------------------------------------------------------------------------
// Sprint 35.2c — HITL threshold + Adaptive Card webhook in Key Vault
// -----------------------------------------------------------------------------
module hitl 'hitl.bicep' = {
  name: 'hitl-${serviceCode}'
  params: {
    tenant: tenant
    keyVaultName: keyVaultName
    agentIdentityId: agentIdentityId
    autoClearMaxTotalTasks: autoClearMaxTotalTasks
    autoClearMaxP0Tasks: autoClearMaxP0Tasks
    autoClearMaxUnassignableTasks: autoClearMaxUnassignableTasks
    requireHitlForReplenishmentRequest: requireHitlForReplenishmentRequest
    teamsWebhookUrl: teamsWebhookUrl
  }
}

module fleet '../../../../apex-m/infra/bicep/modules/agent-fleet.bicep' = [
  for sid in featuredScenarios: {
    name: 'fleet-${sid}'
    params: {
      tenant: tenant
      serviceCode: serviceCode
      scenarioId: sid
      wave: wave
      containerAppsEnvId: containerAppsEnvId
      agentIdentityId: agentIdentityId
    }
  }
]

output serviceCode string = serviceCode
output deployedScenarios array = featuredScenarios
output hitlSecretIds object = hitl.outputs.hitlSecretIds
output hitlSecretPrefix string = hitl.outputs.secretPrefix
