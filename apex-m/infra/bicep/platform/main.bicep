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

output identityId string = identity.outputs.managedIdentityId
output identityClientId string = identity.outputs.managedIdentityClientId
output ledgerConnectionStringSecretUri string = ledger.outputs.connectionStringSecretUri
output logAnalyticsWorkspaceId string = monitoring.outputs.workspaceId
output appInsightsConnectionString string = monitoring.outputs.appInsightsConnectionString
