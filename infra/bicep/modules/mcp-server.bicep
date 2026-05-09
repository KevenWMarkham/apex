// infra/bicep/modules/mcp-server.bicep
// Deploys an MCP server as a Container App. Used by services that need
// service-specific tools (e.g., merml-mcp, scml-mcp, tokenizer-mcp).

targetScope = 'resourceGroup'

param tenant string
param mcpName string
param containerAppsEnvId string
param agentIdentityId string
param image string

resource mcp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'ca-${tenant}-mcp-${mcpName}'
  location: resourceGroup().location
  tags: {
    'apex-tenant': tenant
    'apex-component': 'mcp'
    'apex-mcp': mcpName
  }
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
          name: 'mcp'
          image: image
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: { minReplicas: 1, maxReplicas: 3 }
    }
  }
}

output mcpResourceId string = mcp.id
output mcpFqdn string = mcp.properties.configuration.ingress.fqdn
