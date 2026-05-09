// infra/bicep/blueprints/w1-foundation.bicep
// Wave 1 — SOR connect + medallion + canonical. Bootstraps the tenant.
// Assumes Terraform has already provisioned: Fabric capacity, Key Vault,
// Container App env, Purview (per Professional-APEX §10).

targetScope = 'resourceGroup'

@description('Tenant slug.')
param tenant string

@description('Region.')
param location string = resourceGroup().location

module platform '../platform/main.bicep' = {
  name: 'platform-${tenant}'
  params: {
    tenant: tenant
    location: location
  }
}

output identityId string = platform.outputs.identityId
output identityClientId string = platform.outputs.identityClientId
output workspaceId string = platform.outputs.logAnalyticsWorkspaceId
