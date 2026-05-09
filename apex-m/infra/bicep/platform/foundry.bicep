// apex-m/infra/bicep/platform/foundry.bicep
// Microsoft Foundry account + project for APEX-M Layer 3 agents.
// Standard Setup with Private Networking — required for stage/prod
// substrates per Pre-deployment Security Gate item #13.
//
// Reference: https://learn.microsoft.com/azure/foundry/agents/how-to/virtual-networks
// Reference: https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/ai-ml/ai-foundry
//
// IMPORTANT: Standard Setup requires Bring Your Own (BYO) for:
//   - Storage Account (file/thread storage)
//   - Azure AI Search (vector store)
//   - Azure Cosmos DB (conversation state)
// All three pre-exist as separate Bicep modules; this module wires
// them into the Foundry account at create time. Network injection
// MUST be configured at Foundry account creation — cannot be added
// later for hosted agents.

targetScope = 'resourceGroup'

@description('APEX tenant slug.')
param tenant string

@description('Region.')
param location string

@description('Tags.')
param tags object = {}

@description('User-assigned managed identity for the Foundry runtime.')
param agentIdentityPrincipalId string

@description('BYO Storage Account resource id (required for Standard Setup).')
param byoStorageAccountId string

@description('BYO Azure AI Search service resource id.')
param byoSearchServiceId string

@description('BYO Cosmos DB account resource id.')
param byoCosmosAccountId string

@description('Delegated subnet for agent compute (must be /27 or larger, delegated to Microsoft.App/environments).')
param agentSubnetResourceId string

@description('Private endpoint subnet for ingress.')
param privateEndpointSubnetResourceId string

@description('Private DNS zone resource ids — one per Foundry-attached service.')
param privateDnsZones object = {
  cognitiveServices: ''
  openAi: ''
  servicesAi: ''
  aiSearch: ''
  cosmosDb: ''
  storageBlob: ''
}

@description('Disable public network access (true for stage/prod).')
param disablePublicNetwork bool = true

// AVM ai-foundry module — pinned version. Bump per Multi-Cloud Port Plan.
module foundry 'br/public:avm/ptn/ai-ml/ai-foundry:0.5.0' = {
  name: 'apex-m-foundry-${tenant}'
  params: {
    baseName: 'foundry-apex-${tenant}'
    aiFoundryConfiguration: {
      accountName: 'foundry-apex-${tenant}'
      allowProjectManagement: true
      createCapabilityHosts: true
      disableLocalAuth: true
      location: location
      networking: {
        agentServiceSubnetResourceId: agentSubnetResourceId
        aiServicesPrivateDnsZoneResourceId: privateDnsZones.servicesAi
        cognitiveServicesPrivateDnsZoneResourceId: privateDnsZones.cognitiveServices
        openAiPrivateDnsZoneResourceId: privateDnsZones.openAi
      }
      project: {
        desc: 'APEX-M Foundry project for tenant ${tenant}. Hosts every Layer 3 agent.'
        displayName: 'apex-m-${tenant}'
        name: 'apex-m-${tenant}'
      }
      roleAssignments: [
        {
          principalId: agentIdentityPrincipalId
          principalType: 'ServicePrincipal'
          roleDefinitionIdOrName: 'Cognitive Services OpenAI User'
        }
      ]
      sku: 'S0'
    }
    aiSearchConfiguration: {
      privateDnsZoneResourceId: privateDnsZones.aiSearch
    }
    cosmosDbConfiguration: {
      privateDnsZoneResourceId: privateDnsZones.cosmosDb
    }
    storageAccountConfiguration: {
      blobPrivateDnsZoneResourceId: privateDnsZones.storageBlob
    }
    privateEndpointSubnetResourceId: privateEndpointSubnetResourceId
    includeAssociatedResources: true
    location: location
    tags: union(tags, {
      'apex-component': 'foundry'
      'apex-variant': 'APEX-M'
    })
  }
}

@description('Foundry account resource id.')
output foundryAccountId string = foundry.outputs.accountResourceId

@description('Foundry project resource id.')
output foundryProjectId string = foundry.outputs.projectResourceId

@description('Foundry project endpoint URL — used by hosted agents at runtime.')
output foundryProjectEndpoint string = foundry.outputs.projectEndpoint
