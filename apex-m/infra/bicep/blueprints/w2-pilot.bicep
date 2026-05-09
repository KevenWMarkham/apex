// infra/bicep/blueprints/w2-pilot.bicep
// Wave 2 — pilot one service end-to-end with featured scenarios.
// The wizard supplies `selections` from the operator's checklist.

targetScope = 'resourceGroup'

param tenant string
param containerAppsEnvId string
param agentIdentityId string

@description('Per-service selections: array of { serviceCode, featuredScenarios, mcpServers }')
param selections array

module services '../modules/service.bicep' = [
  for s in selections: {
    name: 'svc-${s.serviceCode}'
    params: {
      tenant: tenant
      serviceCode: s.serviceCode
      wave: 'w2'
      featuredScenarios: s.featuredScenarios
      containerAppsEnvId: containerAppsEnvId
      agentIdentityId: agentIdentityId
      mcpServers: s.?mcpServers ?? []
    }
  }
]

output deployedServices array = [for i in range(0, length(selections)): services[i].outputs.serviceCode]
