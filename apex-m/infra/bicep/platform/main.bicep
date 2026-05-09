// infra/bicep/platform/main.bicep
// Tenant-level platform infra. Run this once per APEX tenant before any
// service modules. Idempotent.

targetScope = 'resourceGroup'

@description('APEX tenant slug (e.g., contoso-prod). Lowercase, dash-only.')
@minLength(3)
@maxLength(40)
param tenant string

@description('Azure region for tenant resources.')
param location string = resourceGroup().location

@description('Tags applied to every resource for drift detection.')
param tags object = {
  'apex-tenant': tenant
  'apex-component': 'platform'
}

module identity 'identity.bicep' = {
  name: 'apex-identity-${tenant}'
  params: {
    tenant: tenant
    location: location
    tags: tags
  }
}

module ledger 'ledger.bicep' = {
  name: 'apex-ledger-${tenant}'
  params: {
    tenant: tenant
    location: location
    tags: tags
  }
}

module monitoring 'monitoring.bicep' = {
  name: 'apex-monitoring-${tenant}'
  params: {
    tenant: tenant
    location: location
    tags: tags
  }
}

// Microsoft Foundry account + project (Standard Setup with Private Networking).
// Required for production substrates per Pre-deployment Security Gate item #13.
// BYO resources (Storage / AI Search / Cosmos DB) and networking subnets
// MUST be provisioned upstream and passed in as resource ids — they cannot
// be added to a Foundry account after creation for hosted agents.
@description('Whether to provision Foundry. Set false for non-agent tenants.')
param provisionFoundry bool = true

@description('BYO Storage Account resource id (required if provisionFoundry=true).')
param byoStorageAccountId string = ''

@description('BYO Azure AI Search resource id.')
param byoSearchServiceId string = ''

@description('BYO Cosmos DB account resource id.')
param byoCosmosAccountId string = ''

@description('Delegated subnet (/27 or larger, delegated to Microsoft.App/environments).')
param agentSubnetResourceId string = ''

@description('Private endpoint subnet.')
param privateEndpointSubnetResourceId string = ''

@description('Private DNS zone resource ids for Foundry-attached services.')
param privateDnsZones object = {}

module foundry 'foundry.bicep' = if (provisionFoundry) {
  name: 'apex-foundry-${tenant}'
  params: {
    tenant: tenant
    location: location
    tags: tags
    agentIdentityPrincipalId: identity.outputs.managedIdentityPrincipalId
    byoStorageAccountId: byoStorageAccountId
    byoSearchServiceId: byoSearchServiceId
    byoCosmosAccountId: byoCosmosAccountId
    agentSubnetResourceId: agentSubnetResourceId
    privateEndpointSubnetResourceId: privateEndpointSubnetResourceId
    privateDnsZones: privateDnsZones
  }
}

output identityId string = identity.outputs.managedIdentityId
output identityClientId string = identity.outputs.managedIdentityClientId
output ledgerConnectionStringSecretUri string = ledger.outputs.connectionStringSecretUri
output logAnalyticsWorkspaceId string = monitoring.outputs.workspaceId
output appInsightsConnectionString string = monitoring.outputs.appInsightsConnectionString
output foundryAccountId string = provisionFoundry ? foundry.outputs.foundryAccountId : ''
output foundryProjectId string = provisionFoundry ? foundry.outputs.foundryProjectId : ''
output foundryProjectEndpoint string = provisionFoundry ? foundry.outputs.foundryProjectEndpoint : ''
