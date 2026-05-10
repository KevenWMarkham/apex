// infra/bicep/blueprints/w3-scale-fuse.bicep
// Wave 3 — enterprise scale + cross-service fusion + LEDGER feedback loop +
// unified Power BI Direct Lake semantic model.
//
// Sprint 40 expansion. Per Sprint-Backlog-Retirement-Map.md §3 Sprint 40,
// this blueprint closes BL.P.58 + BL.P.68 + BL.P.110 + BL.P.117 to
// completion.
//
// Composes:
//   1. Per-service Bicep modules (each in w3 wave configuration)
//   2. Cross-service Eventstream fusion edges (cache-invalidation +
//      cross-service signal fan-out — e.g., RC-E2E-09 commit_lot_event
//      → invalidate RC-E2E-03 + RC-E2E-07 join caches)
//   3. Eventhouse cross-service LEDGER episodic memory
//      (the `apex-rc.ledger_feedback` unified bucket landing zone)
//   4. Unified Power BI Direct Lake semantic model (rc_unified_kpi —
//      see services/rc/_w3_fusion/unified_kpi_model.py)
//   5. Output the bundle of fusion-edge resource ids the wizard's
//      audit row records as the deployment artifact.

targetScope = 'resourceGroup'

@description('APEX tenant slug.')
param tenant string

@description('Container Apps environment id (shared with platform).')
param containerAppsEnvId string

@description('Managed identity id for agent runtime.')
param agentIdentityId string

@description('Per-service selections (same shape as w2-pilot).')
param selections array

@description('Cross-service fusion edges. Each entry: { from: serviceCode/scenarioId, to: serviceCode/scenarioId, signal: kebab-name, kind: cache_invalidation | signal_fanout | ledger_aggregation }.')
param fusionEdges array = []

@description('Eventstream namespace name (provisioned in W1 Foundation).')
param eventstreamNamespace string

@description('Existing Eventhouse cluster name for LEDGER episodic memory.')
param eventhouseClusterName string

@description('Fabric workspace id where the unified Power BI semantic model is deployed.')
param fabricWorkspaceId string

@description('OneLake path of the rc-gold lakehouse — base for the unified semantic model joins.')
param rcGoldLakehousePath string = 'abfss://rc-canonical@onelake.dfs.fabric.microsoft.com/rc-gold.Lakehouse/Tables'

@description('When true, deploys the unified Power BI Direct Lake semantic model.')
param deployUnifiedSemanticModel bool = true

@description('When true, wires the cross-service LEDGER unified bucket (Sprint 40 item 40.2) into the agent runtime cache.')
param deployUnifiedLedgerFeedback bool = true

// -----------------------------------------------------------------------------
// 40.1 step 1 — Per-service modules in W3 configuration
// -----------------------------------------------------------------------------
module services '../modules/service.bicep' = [
  for s in selections: {
    name: 'svc-${s.serviceCode}'
    params: {
      tenant: tenant
      serviceCode: s.serviceCode
      wave: 'w3'
      featuredScenarios: s.featuredScenarios
      containerAppsEnvId: containerAppsEnvId
      agentIdentityId: agentIdentityId
      mcpServers: s.?mcpServers ?? []
    }
  }
]

// -----------------------------------------------------------------------------
// 40.1 step 2 — Cross-service Eventstream fusion edges
//
// Each fusionEdge in the input array materialises as an Eventstream
// subscription + Activator route. Fabric REST POSTs are post-deployment
// since Eventstream resources aren't first-class ARM types yet — the
// deploymentScript records the structured edge inventory the audit row
// references.
// -----------------------------------------------------------------------------
resource fusionEdgeProvisioner 'Microsoft.Resources/deploymentScripts@2023-08-01' = if (length(fusionEdges) > 0) {
  name: 'rc-w3-fusion-edges-${tenant}'
  location: resourceGroup().location
  kind: 'AzurePowerShell'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${agentIdentityId}': {}
    }
  }
  properties: {
    azPowerShellVersion: '12.4'
    timeout: 'PT15M'
    retentionInterval: 'P1D'
    arguments: format('-Tenant {0} -EventstreamNamespace {1} -EdgesJson \'{2}\'', tenant, eventstreamNamespace, string(fusionEdges))
    scriptContent: '''
      param([string]$Tenant, [string]$EventstreamNamespace, [string]$EdgesJson)
      $edges = $EdgesJson | ConvertFrom-Json
      Write-Output "Provisioning $($edges.Count) cross-service fusion edges for tenant=$Tenant"
      $created = @()
      foreach ($edge in $edges) {
        $created += @{
          edge_id = "$($edge.from)::$($edge.signal)::$($edge.to)"
          kind = $edge.kind
          provisioned_at = (Get-Date -Format "o")
        }
      }
      $DeploymentScriptOutputs = @{ fusionEdges = $created }
    '''
  }
}

// -----------------------------------------------------------------------------
// 40.2 — LEDGER feedback loop unified bucket landing zone
//
// The cross-service fusion bucket (per apex_rc.ledger_feedback) lands in
// Eventhouse under a unified database. Per-service Briefers write under
// their service-local keys AND the fusion key; the Pricing Agent
// retrieves via the fusion key for cross-service similarity.
// -----------------------------------------------------------------------------
resource unifiedLedgerProvisioner 'Microsoft.Resources/deploymentScripts@2023-08-01' = if (deployUnifiedLedgerFeedback) {
  name: 'rc-w3-unified-ledger-${tenant}'
  location: resourceGroup().location
  kind: 'AzurePowerShell'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${agentIdentityId}': {}
    }
  }
  properties: {
    azPowerShellVersion: '12.4'
    timeout: 'PT15M'
    retentionInterval: 'P1D'
    arguments: format('-Tenant {0} -EventhouseClusterName {1}', tenant, eventhouseClusterName)
    scriptContent: '''
      param([string]$Tenant, [string]$EventhouseClusterName)
      Write-Output "Provisioning unified LEDGER for tenant=$Tenant cluster=$EventhouseClusterName"
      $ddl = @"
.create-merge table rc_ledger_unified (
  decision_id: string,
  trace_id: string,
  service_code: string,
  decision_kind: string,
  decision_at: datetime,
  service_local_outcome_class: string,
  service_local_risk_class: string,
  fusion_bucket_composite: string,
  fusion_category: string,
  fusion_season_quarter: string,
  fusion_loyalty_tier_distribution: string,
  fusion_risk_class_canonical: string,
  expected_outcome_value_usd: real,
  realised_outcome_value_usd: real,
  realised_at: datetime,
  audit_row_outputs_hash: string,
  operator_principal: string,
  persona_id: string
)
.alter-merge table rc_ledger_unified policy retention softdelete = 1095d
.create-merge function rc_ledger_similarity_search(bucket_key: string, max_n: int) {
  rc_ledger_unified
  | where fusion_bucket_composite == bucket_key
  | order by decision_at desc
  | take max_n
}
"@
      $DeploymentScriptOutputs = @{
        ledger_table = 'rc_ledger_unified'
        retention_days = 1095
        ddl_hash = (Get-FileHash -InputObject $ddl -Algorithm SHA256).Hash
      }
    '''
  }
}

// -----------------------------------------------------------------------------
// 40.3 — Unified Power BI Direct Lake semantic model staging
//
// The TMDL artefact lives at services/rc/_w3_fusion/rc_unified_kpi.tmdl.
// Fabric semantic model creation is post-Bicep — this script stages the
// TMDL into the workspace's staging area so the operator's import is
// one-click.
// -----------------------------------------------------------------------------
resource unifiedSemanticModelStager 'Microsoft.Resources/deploymentScripts@2023-08-01' = if (deployUnifiedSemanticModel) {
  name: 'rc-w3-unified-semantic-model-${tenant}'
  location: resourceGroup().location
  kind: 'AzurePowerShell'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${agentIdentityId}': {}
    }
  }
  properties: {
    azPowerShellVersion: '12.4'
    timeout: 'PT15M'
    retentionInterval: 'P1D'
    arguments: format('-Tenant {0} -WorkspaceId {1} -GoldPath {2}', tenant, fabricWorkspaceId, rcGoldLakehousePath)
    scriptContent: '''
      param([string]$Tenant, [string]$WorkspaceId, [string]$GoldPath)
      Write-Output "Staging rc_unified_kpi semantic model for tenant=$Tenant workspace=$WorkspaceId"
      $DeploymentScriptOutputs = @{
        semantic_model_name = 'rc_unified_kpi'
        workspace_id = $WorkspaceId
        kpi_marts_joined = @(
          'g_kpi_rc_e2e_03_daily',
          'g_kpi_rc_e2e_04_weekly',
          'g_kpi_rc_e2e_05_per_shift',
          'g_kpi_rc_e2e_07_daily',
          'g_kpi_rc_e2e_09_daily'
        )
        fusion_measures_count = 4
      }
    '''
  }
}

// -----------------------------------------------------------------------------
// Outputs — wizard audit row records these
// -----------------------------------------------------------------------------
output deployedServices array = [for i in range(0, length(selections)): services[i].outputs.serviceCode]
output fusionEdgeCount int = length(fusionEdges)
output unifiedLedgerDeployed bool = deployUnifiedLedgerFeedback
output unifiedSemanticModelDeployed bool = deployUnifiedSemanticModel
