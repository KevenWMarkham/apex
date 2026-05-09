// infra/bicep/blueprints/w3-scale-fuse.bicep
// Wave 3 — enterprise scale + cross-service fusion + feedback loop.

targetScope = 'resourceGroup'

param tenant string
param containerAppsEnvId string
param agentIdentityId string

@description('Per-service selections (same shape as w2-pilot).')
param selections array

@description('Cross-service fusion edges: [{ from: scenarioId, to: scenarioId, signal: string }]')
param fusionEdges array = []

module services '../modules/service.bicep' = [
  for s in selections: {
    name: 'svc-${s.serviceCode}'
    params: {
      tenant: tenant
      serviceCode: s.serviceCode
      wave: 'w3'
      featuredScenarios: s.featuredScenarios
      containerAppsEnvId: containerAppsEnvId
      agentIdentityId: agentIdentityId
      mcpServers: s.?mcpServers ?? []
    }
  }
]

// Fusion edges materialize as Eventstream subscriptions wiring agent outputs
// from one scenario into the inputs of another. Resolved by the wizard at
// deploy time — concrete resources tracked in the wizard's audit row.
output deployedServices array = [for i in range(0, length(selections)): services[i].outputs.serviceCode]
output fusionEdgeCount int = length(fusionEdges)
