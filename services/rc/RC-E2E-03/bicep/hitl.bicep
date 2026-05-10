// services/rc/RC-E2E-03/bicep/hitl.bicep
//
// Sprint 32 item 32.10. Materialises the RC-E2E-03 HITL threshold policy
// from `services/rc/RC-E2E-03/config/hitl-thresholds.yaml` as Azure Key
// Vault secrets. The Decide agent reads them at runtime via Managed
// Identity + RBAC (Key Vault Secrets User role assigned to agent identity).
//
// Tenant overrides come from the use-case `hitl_thresholds` block;
// defaults below match the framework hitl-thresholds.yaml.

targetScope = 'resourceGroup'

@description('APEX tenant slug — keyvault secret prefix.')
param tenant string

@description('Existing Key Vault name in the platform RG.')
param keyVaultName string

@description('Resource ID of the agent runtime managed identity (granted Get permission).')
param agentIdentityId string

@description('Markdown percent above which Operations Lead HITL is required.')
@minValue(0)
@maxValue(100)
param markdownPctAbove int = 30

@description('Whether destroy decisions require HITL: any / none / critical_only.')
@allowed([ 'any', 'none', 'critical_only' ])
param destroyDecision string = 'any'

@description('Refund USD above which HITL is required (cross-service framework field).')
@minValue(0)
param refundUsdAbove int = 500

@description('Max seconds a Pricer recommendation may be cached before stale.')
@minValue(60)
@maxValue(86400)
param pricingRecommendationAgeMaxSeconds int = 1800

@description('Markdown percent above which dual-control (Marisol + Daniel) is required.')
@minValue(0)
@maxValue(100)
param requiresDualControlAbovePct int = 60

@description('Teams webhook URL (will be stored as secret `apex-hitl-<tenant>-rc-e2e-03--teams-webhook`).')
@secure()
param teamsWebhookUrl string

var serviceCode = 'rc-e2e-03'
var secretPrefix = 'apex-hitl-${tenant}-${serviceCode}'

// -----------------------------------------------------------------------------
// Existing Key Vault reference
// -----------------------------------------------------------------------------
resource kv 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}

// -----------------------------------------------------------------------------
// Threshold secrets
// -----------------------------------------------------------------------------
resource secMarkdownPctAbove 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--markdown-pct-above'
  properties: {
    value: string(markdownPctAbove)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=percent'
  }
}

resource secDestroyDecision 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--destroy-decision'
  properties: {
    value: destroyDecision
    contentType: 'application/x-apex-hitl-threshold; type=enum'
  }
}

resource secRefundUsdAbove 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--refund-usd-above'
  properties: {
    value: string(refundUsdAbove)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=usd'
  }
}

resource secPricingAgeMax 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--pricing-recommendation-age-max-seconds'
  properties: {
    value: string(pricingRecommendationAgeMaxSeconds)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=seconds'
  }
}

resource secDualControlAbove 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--requires-dual-control-above-pct'
  properties: {
    value: string(requiresDualControlAbovePct)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=percent'
  }
}

resource secTeamsWebhook 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--teams-webhook'
  properties: {
    value: teamsWebhookUrl
    contentType: 'application/x-apex-hitl-webhook; channel=teams'
  }
}

// -----------------------------------------------------------------------------
// RBAC — agent runtime identity gets Key Vault Secrets User on these secrets
// (Key Vault Secrets User role definition GUID is stable per Azure docs.)
// -----------------------------------------------------------------------------
var keyVaultSecretsUserRoleId = '4633458b-17de-408a-b874-0445c86b69e6'

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: kv
  name: guid(kv.id, agentIdentityId, keyVaultSecretsUserRoleId, serviceCode)
  properties: {
    principalId: agentIdentityId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      keyVaultSecretsUserRoleId
    )
  }
}

// -----------------------------------------------------------------------------
// Outputs — referenced by agent.yaml manifest stamps + the wizard's
// security-gate page (Sprint 46) so an operator can see which HITL
// secrets are wired before the deploy button enables.
// -----------------------------------------------------------------------------
output hitlSecretIds object = {
  markdownPctAbove: secMarkdownPctAbove.id
  destroyDecision: secDestroyDecision.id
  refundUsdAbove: secRefundUsdAbove.id
  pricingRecommendationAgeMaxSeconds: secPricingAgeMax.id
  requiresDualControlAbovePct: secDualControlAbove.id
  teamsWebhook: secTeamsWebhook.id
}

output secretPrefix string = secretPrefix
