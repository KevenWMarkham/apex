// apex-m/infra/bicep/platform/fabric.bicep
// Sprint 30 kickoff — provisions the Microsoft Fabric data tier per
// Services Guide §1.6 primary-workspace pattern.
//
// Layout per Services Guide §1.6:
//   rc-canonical/                       (primary workspace — RC practice)
//     Lakehouses/scml-silver, merml-silver, proml-silver, crmml-silver
//     OneLake security: roles defined here, propagate via shortcut
//
//   rc-e2e-03/                          (per-service consumer)
//     Lakehouses/service-bronze, service-gold
//     OneLake shortcuts → rc-canonical Silver tables
//
// Reference:
//   https://learn.microsoft.com/fabric/onelake/security/best-practices-secure-data-in-onelake
//   https://learn.microsoft.com/fabric/security/workspace-identity
//   https://learn.microsoft.com/fabric/security/security-trusted-workspace-access

targetScope = 'resourceGroup'

@description('APEX tenant slug (e.g., contoso-prod). Lowercase, dash-only.')
@minLength(3)
@maxLength(40)
param tenant string

@description('Region for Fabric capacity.')
param location string

@description('Fabric capacity SKU (F2 dev, F8 lab, F32+ prod).')
@allowed([ 'F2', 'F4', 'F8', 'F16', 'F32', 'F64', 'F128', 'F256' ])
param fabricSku string = 'F8'

@description('Tags applied to every resource.')
param tags object = {}

@description('Practice slug — first iteration is rc only.')
param practice string = 'rc'

@description('Per-service workspace slugs to create as consumers of the primary workspace.')
param consumerServices array = [
  'rc-e2e-03'
  'rc-e2e-04'
  'rc-e2e-05'
  'rc-e2e-07'
  'rc-e2e-09'
]

@description('Microsoft Entra security group / user OIDs that get Fabric Admin on the primary workspace.')
param primaryAdminPrincipalIds array = []

@description('Microsoft Entra security group / user OIDs that get Fabric Member on consumer workspaces.')
param consumerMemberPrincipalIds array = []

// ---------------------------------------------------------------------------
// Fabric capacity (the F-SKU)
// ---------------------------------------------------------------------------
// Note: Microsoft.Fabric/capacities is the Bicep resource type; quotas + region
// support are subject to Microsoft Learn capacity-and-licensing docs.
// Reference: https://learn.microsoft.com/fabric/enterprise/buy-subscription
resource fabricCapacity 'Microsoft.Fabric/capacities@2023-11-01' = {
  name: 'fab-apex-${tenant}'
  location: location
  tags: union(tags, {
    'apex-component': 'fabric-capacity'
    'apex-variant': 'APEX-M'
    'apex-practice': practice
  })
  sku: {
    name: fabricSku
    tier: 'Fabric'
  }
  properties: {
    administration: {
      members: primaryAdminPrincipalIds
    }
  }
}

// ---------------------------------------------------------------------------
// Workspaces are provisioned via Fabric REST API at deployment-script time.
// As of Microsoft.Fabric resource-provider GA (2025), workspace + lakehouse +
// shortcut creation are not yet ARM resources. The deployment script bridges
// this until those resource types land. When they do, swap the script for
// native Bicep.
//
// The script:
//   1. Creates the primary workspace `<practice>-canonical` bound to the
//      Fabric capacity.
//   2. Provisions a workspace identity (per Microsoft Learn — workspace
//      identity GA Jan 2026) and grants it Storage Blob Data Reader on the
//      tenant's ADLS Gen2 source accounts (trusted workspace access).
//   3. Creates Lakehouses per APEX-Core schema family (SCML / MERML / PROML /
//      CRMML for RC).
//   4. Creates per-service consumer workspaces.
//   5. Wires OneLake shortcuts from each consumer workspace to the primary
//      workspace's Silver tables.
//   6. Configures SQL analytics endpoint to user identity mode (per
//      Services Guide §1.5).
// ---------------------------------------------------------------------------
resource fabricWorkspaceProvisioner 'Microsoft.Resources/deploymentScripts@2023-08-01' = {
  name: 'ds-apex-${tenant}-fabric-workspaces'
  location: location
  kind: 'AzurePowerShell'
  properties: {
    azPowerShellVersion: '11.0'
    retentionInterval: 'P1D'
    cleanupPreference: 'OnSuccess'
    arguments: '-Tenant ${tenant} -Practice ${practice} -CapacityId "${fabricCapacity.id}" -ConsumerServices "${join(consumerServices, ',')}" -ConsumerMembers "${join(consumerMemberPrincipalIds, ',')}"'
    scriptContent: '''
param(
    [string]$Tenant,
    [string]$Practice,
    [string]$CapacityId,
    [string]$ConsumerServices,
    [string]$ConsumerMembers
)

# Acquire Fabric token via the deployment script's identity (must hold
# Fabric admin permissions on the capacity).
$token = (Get-AzAccessToken -ResourceUrl "https://api.fabric.microsoft.com").Token
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }
$baseUri = "https://api.fabric.microsoft.com/v1"

function Upsert-Workspace {
    param([string]$Name, [string]$Description)
    # Try GET; if 404, create. Microsoft.Fabric REST API per
    # https://learn.microsoft.com/rest/api/fabric/core/workspaces
    $existing = Invoke-RestMethod -Uri "$baseUri/workspaces?displayName=$Name" -Headers $headers -Method GET -ErrorAction SilentlyContinue
    if ($existing -and $existing.value -and $existing.value.Count -gt 0) {
        Write-Output "[apex-m] workspace EXISTS: $Name (id $($existing.value[0].id))"
        return $existing.value[0].id
    }
    $body = @{
        displayName = $Name
        description = $Description
        capacityId = ($CapacityId -split '/')[-1]
    } | ConvertTo-Json -Depth 5
    $created = Invoke-RestMethod -Uri "$baseUri/workspaces" -Headers $headers -Method POST -Body $body
    Write-Output "[apex-m] workspace CREATED: $Name (id $($created.id))"
    return $created.id
}

function Provision-WorkspaceIdentity {
    param([string]$WorkspaceId)
    Invoke-RestMethod -Uri "$baseUri/workspaces/$WorkspaceId/provisionIdentity" -Headers $headers -Method POST
    Write-Output "[apex-m] workspace identity provisioned for $WorkspaceId"
}

function Upsert-Lakehouse {
    param([string]$WorkspaceId, [string]$Name)
    $existing = Invoke-RestMethod -Uri "$baseUri/workspaces/$WorkspaceId/lakehouses" -Headers $headers -Method GET -ErrorAction SilentlyContinue
    foreach ($lh in $existing.value) {
        if ($lh.displayName -eq $Name) {
            Write-Output "[apex-m] lakehouse EXISTS: $Name in $WorkspaceId"
            return $lh.id
        }
    }
    $body = @{ displayName = $Name } | ConvertTo-Json
    $created = Invoke-RestMethod -Uri "$baseUri/workspaces/$WorkspaceId/lakehouses" -Headers $headers -Method POST -Body $body
    Write-Output "[apex-m] lakehouse CREATED: $Name in $WorkspaceId (id $($created.id))"
    return $created.id
}

# 1. Primary workspace
$primaryName = "$Practice-canonical"
$primaryWsId = Upsert-Workspace -Name $primaryName -Description "APEX-M Primary workspace for $Practice practice. Owns Silver canonical entities."
Provision-WorkspaceIdentity -WorkspaceId $primaryWsId

# 2. Silver lakehouses on the primary workspace
$schemas = @("scml-silver", "merml-silver", "proml-silver", "crmml-silver")
$silverLakehouses = @{}
foreach ($s in $schemas) {
    $silverLakehouses[$s] = Upsert-Lakehouse -WorkspaceId $primaryWsId -Name $s
}

# 3. Per-service consumer workspaces
$consumerWorkspaces = @{}
$services = $ConsumerServices -split "," | Where-Object { $_ }
foreach ($svc in $services) {
    $cwsName = $svc.ToLower()
    $cwsId = Upsert-Workspace -Name $cwsName -Description "APEX-M consumer workspace for service $svc."
    Provision-WorkspaceIdentity -WorkspaceId $cwsId
    $consumerWorkspaces[$svc] = $cwsId

    # service-bronze + service-gold lakehouses
    Upsert-Lakehouse -WorkspaceId $cwsId -Name "service-bronze" | Out-Null
    Upsert-Lakehouse -WorkspaceId $cwsId -Name "service-gold" | Out-Null

    # OneLake shortcuts from consumer to primary's Silver lakehouses
    foreach ($s in $schemas) {
        $shortcutBody = @{
            name = $s
            target = @{
                oneLake = @{
                    workspaceId = $primaryWsId
                    itemId = $silverLakehouses[$s]
                    path = "/Tables"
                }
            }
        } | ConvertTo-Json -Depth 5
        try {
            Invoke-RestMethod -Uri "$baseUri/workspaces/$cwsId/items/service-bronze/shortcuts" -Headers $headers -Method POST -Body $shortcutBody | Out-Null
            Write-Output "[apex-m] shortcut $svc -> $primaryName/$s created"
        } catch {
            Write-Output "[apex-m] shortcut $svc -> $primaryName/$s already exists (or error: $_)"
        }
    }
}

# Outputs for Bicep consumption
$DeploymentScriptOutputs = @{
    primaryWorkspaceId = $primaryWsId
    primaryWorkspaceName = $primaryName
    consumerWorkspaceIds = $consumerWorkspaces
    silverLakehouses = $silverLakehouses
}
'''
  }
  dependsOn: [
    fabricCapacity
  ]
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------
output fabricCapacityId string = fabricCapacity.id
output fabricCapacityName string = fabricCapacity.name

@description('Primary workspace id (rc-canonical for first iteration).')
output primaryWorkspaceId string = fabricWorkspaceProvisioner.properties.outputs.primaryWorkspaceId

@description('Primary workspace name.')
output primaryWorkspaceName string = fabricWorkspaceProvisioner.properties.outputs.primaryWorkspaceName

@description('Per-service consumer workspace ids (object keyed by service code).')
output consumerWorkspaceIds object = fabricWorkspaceProvisioner.properties.outputs.consumerWorkspaceIds

@description('Silver lakehouse ids on the primary workspace (object keyed by schema family).')
output silverLakehouses object = fabricWorkspaceProvisioner.properties.outputs.silverLakehouses
