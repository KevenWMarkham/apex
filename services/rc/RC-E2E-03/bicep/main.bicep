// services/rc/RC-E2E-03/bicep/main.bicep
// Service-level deployment for RC-E2E-03. Composes the canonical agent-fleet
// module with service-specific schemas, personas, and HITL policy.

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

@description('Sprint 32.10 — markdown percent above which Operations Lead HITL fires.')
@minValue(0)
@maxValue(100)
param markdownPctAbove int = 30

@description('Sprint 32.10 — destroy decision HITL routing: any / none / critical_only.')
@allowed([ 'any', 'none', 'critical_only' ])
param destroyDecision string = 'any'

@description('Sprint 32.10 — markdown percent above which dual-control (Marisol + Daniel) is required.')
@minValue(0)
@maxValue(100)
param requiresDualControlAbovePct int = 60

var serviceCode = 'RC-E2E-03'

// -----------------------------------------------------------------------------
// Sprint 32.10 — HITL threshold + Adaptive Card webhook secrets in Key Vault
// -----------------------------------------------------------------------------
module hitl 'hitl.bicep' = {
  name: 'hitl-${serviceCode}'
  params: {
    tenant: tenant
    keyVaultName: keyVaultName
    agentIdentityId: agentIdentityId
    markdownPctAbove: markdownPctAbove
    destroyDecision: destroyDecision
    requiresDualControlAbovePct: requiresDualControlAbovePct
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
