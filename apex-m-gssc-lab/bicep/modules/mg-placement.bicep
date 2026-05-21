// modules/mg-placement.bicep
// Places (or asserts placement of) an existing subscription under the target
// management group. Per Microsoft's reference:
//   https://learn.microsoft.com/en-us/azure/templates/microsoft.management/managementgroups/subscriptions
// this resource type deploys only at tenant scope.
//
// Idempotency: PUT-style association. Re-running against the same MG is a
// no-op; if the subscription is currently under a different MG it will be
// moved (idempotent on target state, not source).

targetScope = 'tenant'

@description('Target management group name (e.g., mg-apex-m-lab per Appendix A).')
param managementGroupName string

@description('Subscription GUID (no /subscriptions/ prefix).')
param subscriptionId string

resource mg 'Microsoft.Management/managementGroups@2023-04-01' existing = {
  scope: tenant()
  name: managementGroupName
}

resource placement 'Microsoft.Management/managementGroups/subscriptions@2023-04-01' = {
  parent: mg
  name: subscriptionId
}
