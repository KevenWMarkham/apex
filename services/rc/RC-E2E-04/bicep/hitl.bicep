// services/rc/RC-E2E-04/bicep/hitl.bicep
//
// Sprint 34 item 34.3. Materialises RC-E2E-04 HITL threshold + Tier-3 PII
// unlock policy from `services/rc/RC-E2E-04/config/hitl-thresholds.yaml` as
// Azure Key Vault secrets.
//
// The Decide agent reads thresholds at runtime via Managed Identity + RBAC
// (Key Vault Secrets User role). The tokenizer-mcp bulk_detokenize webhook
// secret is also stored here — Decide invokes it ONLY post-HITL approval
// per the JIT PII unlock pattern (Deployment Guide §5.2.2).

targetScope = 'resourceGroup'

@description('APEX tenant slug — keyvault secret prefix.')
param tenant string

@description('Existing Key Vault name in the platform RG.')
param keyVaultName string

@description('Resource ID of the agent runtime managed identity (granted Get permission).')
param agentIdentityId string

@description('Winback offer depth percent above which HITL is required.')
@minValue(0)
@maxValue(100)
param winbackOfferAbovePct int = 25

@description('Cohort total offer cost USD above which HITL is required.')
@minValue(0)
param cohortTotalOfferCostAboveUsd int = 50000

@description('Whether Tier-3 PII unlock requires HITL approval. NOT RECOMMENDED to disable.')
param tier3PiiUnlockRequired bool = true

@description('Max cohort size eligible for auto-clear (bonus_points / free_shipping only).')
@minValue(0)
param autoClearMaxCohortSize int = 200

@description('Tokenizer-mcp bulk_detokenize webhook URL.')
@secure()
param tokenizerBulkDetokenizeWebhookUrl string

@description('Teams webhook URL for HITL Adaptive Cards.')
@secure()
param teamsWebhookUrl string

var serviceCode = 'rc-e2e-04'
var secretPrefix = 'apex-hitl-${tenant}-${serviceCode}'

resource kv 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}

// -----------------------------------------------------------------------------
// Threshold secrets
// -----------------------------------------------------------------------------
resource secWinbackOfferAbove 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--winback-offer-above-pct'
  properties: {
    value: string(winbackOfferAbovePct)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=percent'
  }
}

resource secCohortCostAbove 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--cohort-total-offer-cost-above-usd'
  properties: {
    value: string(cohortTotalOfferCostAboveUsd)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=usd'
  }
}

resource secTier3Required 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--tier-3-pii-unlock-required'
  properties: {
    value: string(tier3PiiUnlockRequired)
    contentType: 'application/x-apex-hitl-threshold; type=boolean'
  }
}

resource secAutoClearMaxCohort 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: '${secretPrefix}--auto-clear-max-cohort-size'
  properties: {
    value: string(autoClearMaxCohortSize)
    contentType: 'application/x-apex-hitl-threshold; type=number; units=count'
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
// RBAC — agent runtime identity gets Key Vault Secrets User on these secrets
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
  winbackOfferAbovePct: secWinbackOfferAbove.id
  cohortTotalOfferCostAboveUsd: secCohortCostAbove.id
  tier3PiiUnlockRequired: secTier3Required.id
  autoClearMaxCohortSize: secAutoClearMaxCohort.id
  tokenizerBulkDetokenizeWebhook: secTokenizerWebhook.id
  teamsWebhook: secTeamsWebhook.id
}

output secretPrefix string = secretPrefix
