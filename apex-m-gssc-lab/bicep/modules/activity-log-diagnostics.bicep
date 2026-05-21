// modules/activity-log-diagnostics.bicep
// Routes the subscription Activity Log to the lab Log Analytics workspace.
// Per APEX-M GSSC Lab Infrastructure Deployment §3 (observability).
//
// Idempotency: PUT on a named diagnosticSettings resource. Re-runs with the
// same name + workspaceId are no-ops; changes to logs[] reconcile to the
// declared set.
//
// API 2021-05-01-preview is the latest available per Microsoft Learn (May
// 2026); no GA release exists for this resource type:
//   https://learn.microsoft.com/en-us/azure/templates/microsoft.insights/diagnosticsettings

targetScope = 'subscription'

@description('Full ARM resource ID of the destination Log Analytics workspace (e.g., log-apex-m-gssc-eus2 in the GSSC Lab).')
param logAnalyticsWorkspaceId string

resource activityLog 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'send-activity-log-to-loganalytics'
  properties: {
    workspaceId: logAnalyticsWorkspaceId
    logs: [
      { category: 'Administrative', enabled: true }
      { category: 'Security', enabled: true }
      { category: 'ServiceHealth', enabled: true }
      { category: 'Alert', enabled: true }
      { category: 'Recommendation', enabled: true }
      { category: 'Policy', enabled: true }
      { category: 'Autoscale', enabled: true }
      { category: 'ResourceHealth', enabled: true }
    ]
  }
}
