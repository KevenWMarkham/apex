// infra/bicep/platform/identity.bicep
// User-assigned managed identity used by every agent Container App.

targetScope = 'resourceGroup'

param tenant string
param location string
param tags object = {}

resource agentIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-apex-${tenant}-agent'
  location: location
  tags: tags
}

output managedIdentityId string = agentIdentity.id
output managedIdentityClientId string = agentIdentity.properties.clientId
output managedIdentityPrincipalId string = agentIdentity.properties.principalId
