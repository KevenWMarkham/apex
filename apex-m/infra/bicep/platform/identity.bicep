// apex-m/infra/bicep/platform/identity.bicep
// APEX-M identity layer (Phase I.1).
//
// Provisions:
//   1. User-assigned managed identity (UAMI) used by every agent Container
//      App + Foundry hosted agent for Azure resource access (Cosmos DB,
//      Storage, Key Vault, Fabric).
//   2. Microsoft Entra Agent ID tenant root blueprint (GA April 2026).
//   3. Per-service blueprint placeholder pattern (operator drives via
//      Microsoft Graph after Bicep deploy — see deploymentScripts block).
//
// Reference: docs/APEX - Design and Build/agent-identity-blueprints.md
// Reference: https://learn.microsoft.com/entra/agent-id/what-is-microsoft-entra-agent-id
//
// IMPORTANT: Entra Agent ID resources are not yet exposed via native ARM
// resource types as of April 2026 GA. Provisioning happens via Microsoft
// Graph API. Bicep here provisions the UAMI + a deployment script that
// invokes the Graph endpoints. When Microsoft.Graph/agentIdentities
// resource type lands, swap the deployment script for native resources.

targetScope = 'resourceGroup'

@description('APEX tenant slug, used in resource names.')
param tenant string

@description('Region for the managed identity.')
param location string

@description('Tags applied to every resource.')
param tags object = {}

@description('APEX service codes to create blueprints for (e.g., ["RC-E2E-03","RC-E2E-04"]).')
param serviceCodes array = []

@description('Conditional Access policy ids attached to the tenant root blueprint.')
param tenantRootCaPolicyIds array = []

// ---------------------------------------------------------------------------
// Layer 1 — User-assigned managed identity for the agent runtime
// ---------------------------------------------------------------------------
resource agentIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-apex-${tenant}-agent'
  location: location
  tags: union(tags, {
    'apex-component': 'agent-runtime-identity'
    'apex-variant': 'APEX-M'
  })
}

// ---------------------------------------------------------------------------
// Layer 1 — Entra Agent ID tenant root blueprint (provisioned post-deploy)
//
// The deployment script runs as a *deployment-time* step, calling Microsoft
// Graph as the deployment principal. It must have Application.ReadWrite.All
// + AgentIdentity.ReadWrite.All on Microsoft Graph.
//
// Naming convention from agent-identity-blueprints.md §3:
//   tenant root        : apex-m-tenant-root
//   per-service        : apex-m-{service-code-lowercase}-blueprint
// ---------------------------------------------------------------------------
resource entraBlueprintProvisioner 'Microsoft.Resources/deploymentScripts@2023-08-01' = {
  name: 'ds-apex-${tenant}-entra-blueprints'
  location: location
  kind: 'AzurePowerShell'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${agentIdentity.id}': {}
    }
  }
  properties: {
    azPowerShellVersion: '11.0'
    retentionInterval: 'P1D'
    cleanupPreference: 'OnSuccess'
    arguments: '-Tenant ${tenant} -ServiceCodes "${join(serviceCodes, ',')}" -CaPolicies "${join(tenantRootCaPolicyIds, ',')}"'
    scriptContent: '''
param([string]$Tenant, [string]$ServiceCodes, [string]$CaPolicies)

# Acquire Graph token via this script's UAMI (must hold AgentIdentity.ReadWrite.All).
$token = (Get-AzAccessToken -ResourceUrl "https://graph.microsoft.com").Token
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }

# 1. Tenant root blueprint
$rootId = "apex-m-tenant-root"
$rootBody = @{
    id = $rootId
    displayName = "APEX-M Tenant Root ($Tenant)"
    parentBlueprintId = $null
    conditionalAccessPolicyIds = @($CaPolicies -split "," | Where-Object { $_ })
    lifecyclePolicy = @{ autoRevokeOnTenantDecommission = $true }
    notes = "APEX-M Phase I.1 — see docs/APEX - Design and Build/agent-identity-blueprints.md §4.1"
} | ConvertTo-Json -Depth 5

# Idempotent upsert
try {
    Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/agentIdentities/blueprints/$rootId" -Method GET -Headers $headers
    Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/agentIdentities/blueprints/$rootId" -Method PATCH -Headers $headers -Body $rootBody
    Write-Output "[apex-m] tenant root blueprint UPDATED: $rootId"
} catch {
    Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/agentIdentities/blueprints" -Method POST -Headers $headers -Body $rootBody
    Write-Output "[apex-m] tenant root blueprint CREATED: $rootId"
}

# 2. Per-service blueprints
$codes = $ServiceCodes -split "," | Where-Object { $_ }
foreach ($code in $codes) {
    $svcId = "apex-m-$($code.ToLower())-blueprint"
    $svcBody = @{
        id = $svcId
        displayName = "APEX-M $code"
        parentBlueprintId = $rootId
        notes = "APEX-M Phase I.1 — service blueprint for $code; see agent-identity-blueprints.md §4.2"
    } | ConvertTo-Json -Depth 5
    try {
        Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/agentIdentities/blueprints/$svcId" -Method GET -Headers $headers
        Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/agentIdentities/blueprints/$svcId" -Method PATCH -Headers $headers -Body $svcBody
        Write-Output "[apex-m] service blueprint UPDATED: $svcId"
    } catch {
        Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/agentIdentities/blueprints" -Method POST -Headers $headers -Body $svcBody
        Write-Output "[apex-m] service blueprint CREATED: $svcId"
    }
}

# Output for Bicep consumption
$DeploymentScriptOutputs = @{
    tenantRootBlueprintId = $rootId
    serviceBlueprintIds   = $codes | ForEach-Object { "apex-m-$($_.ToLower())-blueprint" }
}
'''
  }
  dependsOn: [
    agentIdentity
  ]
}

// ---------------------------------------------------------------------------
// Outputs — consumed by service Bicep modules + the wizard render endpoint
// ---------------------------------------------------------------------------
output managedIdentityId string = agentIdentity.id
output managedIdentityClientId string = agentIdentity.properties.clientId
output managedIdentityPrincipalId string = agentIdentity.properties.principalId

@description('APEX-M Entra Agent ID tenant root blueprint id (per agent-identity-blueprints.md §3).')
output tenantRootBlueprintId string = entraBlueprintProvisioner.properties.outputs.tenantRootBlueprintId

@description('Per-service blueprint ids created from `serviceCodes` parameter.')
output serviceBlueprintIds array = entraBlueprintProvisioner.properties.outputs.serviceBlueprintIds
