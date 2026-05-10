// services/rc/RC-E2E-07/bicep/hitl.bicep
//
// Sprint 37.3. Materialises RC-E2E-07 adaptive-HITL thresholds + Tier-3 PII
// unlock policy from `services/rc/RC-E2E-07/config/hitl-thresholds.yaml`
// as Azure Key Vault secrets. The Decide agent reads thresholds at runtime
// via Managed Identity + Key Vault Secrets User RBAC.

targetScope = 'resourceGroup'

@description('APEX tenant slug — keyvault secret prefix.')
param tenant string

@description('Existing Key Vault name in the platform RG.')
param keyVaultName string

@description('Resource ID of the agent runtime managed identity (granted Get permission).')
param agentIdentityId string

@description('Auto-clear band ceiling — fraud_score < this auto-clears.')
@minValue(0)
@maxValue(1)
param autoClearMaxFraudScore int = 40   // 0.40 stored as int×100; Decide divides by 100

@description('HITL review band floor — fraud_score >= this triggers Adaptive Card.')
@minValue(0)
@maxValue(1)
param hitlReviewMinFraudScore int = 40

@description('Escalate band floor — fraud_score >= this triggers Tier-3 PII unlock.')
@minValue(0)
@maxValue(1)
param escalateMinFraudScore int = 70

@description('Refund USD above which low-score refunds still HITL.')
@minValue(0)
param autoClearMaxRefundValueUsd int = 100

@description('Whether ring_indicator==true forces escalate regardless of score.')
param ringIndicatorForceEscalate bool = true

@description('Whether hold decisions require Tier-3 PII unlock via tokenizer-mcp.')
param holdRequiresTier3PiiUnlock bool = true

@description('Tokenizer-mcp bulk_detokenize webhook URL.')
@secure()
param tokenizerBulkDetokenizeWebhookUrl string

@description('Teams webhook URL for HITL Adaptive Cards.')
@secure()
param teamsWebhookUrl string

var serviceCode = 'rc-e2e-07'
var secretPrefix = 'apex-hitl-${tenant}-${serviceCode}'

resource kv 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}

// -----------------------------------------------------------------------------
// Adaptive HITL threshold secrets — values are stored ×100 (Decide divides) so
// Bicep param can stay int-typed; tenant operators tune via the wizard which
// renders the 0.00–1.00 form.
// -----------------------------------------------------------------------------
resource secAutoClearMax 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--auto-clear-max-fraud-score'
  properties: {
    value: string(autoClearMaxFraudScore)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=score_x100'
  }
}

resource secHitlReviewMin 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--hitl-review-min-fraud-score'
  properties: {
    value: string(hitlReviewMinFraudScore)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=score_x100'
  }
}

resource secEscalateMin 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--escalate-min-fraud-score'
  properties: {
    value: string(escalateMinFraudScore)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=score_x100'
  }
}

resource secAutoClearRefundUsd 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--auto-clear-max-refund-value-usd'
  properties: {
    value: string(autoClearMaxRefundValueUsd)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=usd'
  }
}

resource secRingForce 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--ring-indicator-force-escalate'
  properties: {
    value: string(ringIndicatorForceEscalate)
    contentType: 'application/x-apex-hitl-threshold; type=boolean'
  }
}

resource secHoldRequiresUnlock 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--hold-requires-tier-3-pii-unlock'
  properties: {
    value: string(holdRequiresTier3PiiUnlock)
    contentType: 'application/x-apex-hitl-threshold; type=boolean'
  }
}

// -----------------------------------------------------------------------------
// Tier-3 PII unlock — tokenizer bulk_detokenize webhook
// -----------------------------------------------------------------------------
resource secTokenizerWebhook 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--tokenizer-bulk-detokenize-webhook'
  properties: {
    value: tokenizerBulkDetokenizeWebhookUrl
    contentType: 'application/x-apex-tier3-pii-unlock; ttl_seconds=60'
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
// RBAC — agent runtime identity gets Key Vault Secrets User
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
// Outputs
// -----------------------------------------------------------------------------
output hitlSecretIds object = {
  autoClearMaxFraudScore: secAutoClearMax.id
  hitlReviewMinFraudScore: secHitlReviewMin.id
  escalateMinFraudScore: secEscalateMin.id
  autoClearMaxRefundValueUsd: secAutoClearRefundUsd.id
  ringIndicatorForceEscalate: secRingForce.id
  holdRequiresTier3PiiUnlock: secHoldRequiresUnlock.id
  tokenizerBulkDetokenizeWebhook: secTokenizerWebhook.id
  teamsWebhook: secTeamsWebhook.id
}

output secretPrefix string = secretPrefix
