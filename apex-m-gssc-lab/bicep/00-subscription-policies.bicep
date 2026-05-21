// 00-subscription-policies.bicep
// APEX-M GSSC Lab — Day-0 subscription placement, tags, and diagnostic
// settings. Per APEX-M GSSC Lab Infrastructure Deployment v2.0 Chapter 3 +
// Chapter 4 + Appendix A.
//
// Maps to WI 12713 (Feature F1.1 / Story S1.1.1):
//   "Provision sub-apex-m-gssc-lab subscription under mg-apex-m-lab"
//
// The subscription itself is allocated by Azure central provisioning out of
// band (§3.1 — "Subscription ID: (allocated by Azure central provisioning)").
// This template only CONFIGURES the pre-existing subscription:
//   1. Asserts placement under mg-apex-m-lab (idempotent PUT).
//   2. Applies the six §3.3 tags at subscription scope.
//   3. Routes the Activity Log to log-apex-m-gssc-eus2.
//
// Re-running is a no-op once configured. See Microsoft's subscription-vending
// guidance for the broader landing-zone pattern:
//   https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending

targetScope = 'managementGroup'

@description('Subscription GUID of sub-apex-m-gssc-lab (allocated by Azure central provisioning per §3.1).')
param subscriptionId string

@description('Owner email for the owner tag (§3.3).')
param ownerEmail string

@description('Pack-tenant tag value per §22.2 — one of the seven pack tenants the lab supports.')
@allowed([
  'shared'
  'merch'
  'finance'
  'risk'
  'manufacturing'
  'cxp'
  'esg'
])
param packTenant string = 'shared'

@description('Auto-shutdown eligibility tag (§3.3). Subscription-scope value is informational and inherited by child RGs.')
param autoStop bool = false

@description('Full ARM resource ID of log-apex-m-gssc-eus2 Log Analytics workspace (Appendix A).')
param logAnalyticsWorkspaceId string

// Step 1 — assert subscription is under this management group.
// mg-placement is tenant-scoped; we pass our deployment MG name explicitly so
// the module is reusable from any caller scope.
module placement 'modules/mg-placement.bicep' = {
  scope: tenant()
  name: 'place-${subscriptionId}'
  params: {
    managementGroupName: managementGroup().name
    subscriptionId: subscriptionId
  }
}

// Step 2 — compute the §3.3 tag set (no resources; just an output).
module tagSet 'modules/tags.bicep' = {
  name: 'tags-${subscriptionId}'
  scope: subscription(subscriptionId)
  params: {
    ownerEmail: ownerEmail
    packTenant: packTenant
    autoStop: autoStop
  }
}

// Step 3 — apply the §3.3 tags at subscription scope.
module subTags 'modules/tags-apply.bicep' = {
  name: 'apply-tags-${subscriptionId}'
  scope: subscription(subscriptionId)
  params: {
    tags: tagSet.outputs.tags
  }
  dependsOn: [
    placement
  ]
}

// Step 4 — route subscription Activity Log to log-apex-m-gssc-eus2.
module activityLog 'modules/activity-log-diagnostics.bicep' = {
  name: 'activity-log-${subscriptionId}'
  scope: subscription(subscriptionId)
  params: {
    logAnalyticsWorkspaceId: logAnalyticsWorkspaceId
  }
  dependsOn: [
    placement
  ]
}

output subscriptionId string = subscriptionId
output managementGroupName string = managementGroup().name
