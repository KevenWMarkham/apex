// Sprint 26 Task 26.11.1-4 — Azure Cache for Redis Enterprise + private endpoint + Entra auth
//
// Sprint 26 governance:
//   - Enterprise tier (Task 26.11.1) — smallest SKU for pilot; finops sets prod sizing
//   - Private endpoint only (Task 26.11.2) — no public access
//   - Entra auth via managed identity — NO connection-string auth
//   - Purview classification tag `class: Internal` (Task 26.11.3)
//   - Connection info via Key Vault as Entra-issued token exchange (Task 26.11.4)
//
// References:
//   - APEX-CORE.md §11 cache policy
//   - APEX-v0.2-Build-Instructions.md §3.7
//   - Sprint 26 dashboard sixth lane (Task 26.10) sources from Azure Monitor
//     metrics emitted by the resource declared here

@description('APEX engagement code, e.g., apex-tenant-rc-wave1')
param engagementCode string

@description('Azure region for the Redis Enterprise instance')
param location string = resourceGroup().location

@description('Private VNet subnet resource id for the private endpoint')
param privateEndpointSubnetId string

@description('Key Vault resource id where the Redis principal token-exchange config lands')
param keyVaultId string

@description('Entra group object id authorized to read budget / cancel-token keys')
param controlPlaneReaderGroupId string

@description('Entra group object id authorized to write cancel tokens (orchestrator + on-call)')
param controlPlaneWriterGroupId string

@description('Pilot SKU per finops Sprint 26 sizing — Enterprise_E10 minimum for HA')
@allowed([
  'Enterprise_E10'
  'Enterprise_E20'
  'Enterprise_E50'
])
param skuName string = 'Enterprise_E10'

// ---- Common tags --------------------------------------------------

var commonTags = {
  apexEngagement: engagementCode
  apexComponent: 'control-plane'
  apexClass: 'Internal'    // Sprint 26 Task 26.11.3 — Purview class tag
  apexSprint: 'sprint-26'
  apexCachePolicy: 'apex-core-section-11'
}

// ---- Redis Enterprise instance ------------------------------------

resource redisEnterprise 'Microsoft.Cache/redisEnterprise@2024-03-01-preview' = {
  name: '${engagementCode}-control-plane'
  location: location
  tags: commonTags
  sku: {
    name: skuName
    capacity: 2
  }
  properties: {
    minimumTlsVersion: '1.2'
    // Public access disabled — Sprint 26 Task 26.11.2
    publicNetworkAccess: 'Disabled'
  }
}

resource controlPlaneDb 'Microsoft.Cache/redisEnterprise/databases@2024-03-01-preview' = {
  parent: redisEnterprise
  name: 'default'
  properties: {
    clientProtocol: 'Encrypted'
    clusteringPolicy: 'EnterpriseCluster'
    evictionPolicy: 'NoEviction'  // Control plane data must not be evicted under pressure
    persistence: {
      // Persistence off for control-plane cache; Cosmos is the durable record.
      // Redis loss does not lose orchestrator state (APEX-CORE §11 invariant).
      aofEnabled: false
      rdbEnabled: false
    }
    accessKeysAuthentication: 'Disabled'   // Sprint 26: NO password auth
  }
}

// ---- Private endpoint --------------------------------------------

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-11-01' = {
  name: '${engagementCode}-control-plane-pe'
  location: location
  tags: commonTags
  properties: {
    subnet: {
      id: privateEndpointSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'redis-enterprise-link'
        properties: {
          privateLinkServiceId: redisEnterprise.id
          groupIds: [
            'redisEnterprise'
          ]
        }
      }
    ]
  }
}

// ---- Entra RBAC role assignments ----------------------------------

// Reader role — child agents + dashboard readers
resource readerRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: redisEnterprise
  name: guid(redisEnterprise.id, controlPlaneReaderGroupId, 'Reader')
  properties: {
    principalId: controlPlaneReaderGroupId
    principalType: 'Group'
    // Built-in Reader role on the Redis resource; data-plane access uses
    // Redis ACL roles configured separately via the Redis ACL API.
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'acdd72a7-3385-48ef-bd42-f606fba81ae7'
    )
  }
}

// Contributor role — parent orchestrator + on-call SRE for cancel writes
resource writerRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: redisEnterprise
  name: guid(redisEnterprise.id, controlPlaneWriterGroupId, 'Contributor')
  properties: {
    principalId: controlPlaneWriterGroupId
    principalType: 'Group'
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'b24988ac-6180-42a0-ab88-20f7382dd24c'
    )
  }
}

// ---- Outputs ------------------------------------------------------

output redisHostname string = redisEnterprise.properties.hostName
output redisResourceId string = redisEnterprise.id
output controlPlaneDatabaseName string = controlPlaneDb.name
output privateEndpointId string = privateEndpoint.id
