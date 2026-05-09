// infra/bicep/modules/agent-fleet.bicep
// The canonical APEX 6-agent fleet: assess → classify → quantify → decide
// → act → learn. One Container App per role, all sharing the same managed
// identity and registered with Agent Service via the deploy-wizard.

targetScope = 'resourceGroup'

@description('APEX tenant slug.')
param tenant string

@description('Service code (e.g., RC-E2E-03).')
param serviceCode string

@description('Featured scenario id (e.g., rc-cold-chain-excursion-mid-shift).')
param scenarioId string

@description('Wave: w1 | w2 | w3.')
@allowed([ 'w1', 'w2', 'w3' ])
param wave string

@description('Container Apps environment resource ID.')
param containerAppsEnvId string

@description('User-assigned managed identity resource ID.')
param agentIdentityId string

@description('Agent container image registry/path/tag.')
param agentImage string = 'mcr.microsoft.com/azuredocs/aci-helloworld:latest'

@description('Per-role config overrides keyed by role name.')
param roleOverrides object = {}

var roles = [ 'assess', 'classify', 'quantify', 'decide', 'act', 'learn' ]
var hitlRoles = [ 'decide', 'act' ]

var commonTags = {
  'apex-tenant': tenant
  'apex-service': serviceCode
  'apex-scenario': scenarioId
  'apex-wave': wave
}

resource agents 'Microsoft.App/containerApps@2024-03-01' = [
  for role in roles: {
    name: 'ca-${tenant}-${toLower(serviceCode)}-${scenarioId}-${role}'
    location: resourceGroup().location
    tags: union(commonTags, { 'apex-agent-role': role })
    identity: {
      type: 'UserAssigned'
      userAssignedIdentities: {
        '${agentIdentityId}': {}
      }
    }
    properties: {
      managedEnvironmentId: containerAppsEnvId
      configuration: {
        ingress: {
          external: false
          targetPort: 8080
        }
      }
      template: {
        containers: [
          {
            name: role
            image: agentImage
            env: [
              { name: 'APEX_TENANT', value: tenant }
              { name: 'APEX_SERVICE_CODE', value: serviceCode }
              { name: 'APEX_SCENARIO_ID', value: scenarioId }
              { name: 'APEX_AGENT_ROLE', value: role }
              { name: 'APEX_HITL_GATE', value: contains(hitlRoles, role) ? 'true' : 'false' }
            ]
            resources: {
              cpu: json('0.5')
              memory: '1Gi'
            }
          }
        ]
        scale: {
          minReplicas: 1
          maxReplicas: 5
        }
      }
    }
  }
]

output agentResourceIds array = [for i in range(0, length(roles)): agents[i].id]
output roles array = roles
