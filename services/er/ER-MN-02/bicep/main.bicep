// services/er/ER-MN-02/bicep/main.bicep
// Service-level deployment for ER-MN-02. Composes the canonical agent-fleet
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

var serviceCode = 'ER-MN-02'

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
