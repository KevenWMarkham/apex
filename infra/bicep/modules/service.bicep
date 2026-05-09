// infra/bicep/modules/service.bicep
// Deploys one APEX service into a tenant resource group. The wizard composes
// blueprints from N invocations of this module.

targetScope = 'resourceGroup'

param tenant string
param serviceCode string
@allowed([ 'w1', 'w2', 'w3' ])
param wave string
param featuredScenarios array = []
param containerAppsEnvId string
param agentIdentityId string
param mcpServers array = []

module mcps 'mcp-server.bicep' = [
  for mcp in mcpServers: {
    name: 'mcp-${mcp.name}'
    params: {
      tenant: tenant
      mcpName: mcp.name
      containerAppsEnvId: containerAppsEnvId
      agentIdentityId: agentIdentityId
      image: mcp.image
    }
  }
]

module fleets 'agent-fleet.bicep' = [
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
output mcpFqdns array = [for i in range(0, length(mcpServers)): mcps[i].outputs.mcpFqdn]
