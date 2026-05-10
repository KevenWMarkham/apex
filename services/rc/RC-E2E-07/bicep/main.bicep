// services/rc/RC-E2E-07/bicep/main.bicep
// Service-level deployment for RC-E2E-07 Returns & Refund Integrity. Composes
// the canonical agent-fleet module with the Concurrent canonical pattern,
// adaptive HITL thresholds, and Tier-3 PII unlock policy (Sprint 37.3).

targetScope = 'resourceGroup'

@description('APEX tenant slug (e.g., contoso-prod).')
param tenant string

@description('Wave being deployed: w1 | w2 | w3.')
@allowed([ 'w1', 'w2', 'w3' ])
param wave string

@description('Featured scenario IDs to deploy in this wave.')
param featuredScenarios array = []

@description('Container Apps environment resource ID.')
param containerAppsEnvId string

@description('Managed identity resource ID for agent runtime.')
param agentIdentityId string

@description('Existing Key Vault name in the platform RG (HITL secrets land here).')
param keyVaultName string

@description('Tokenizer-mcp bulk_detokenize webhook URL (Tier-3 PII unlock).')
@secure()
param tokenizerBulkDetokenizeWebhookUrl string

@description('Tenant Teams webhook for HITL Adaptive Cards.')
@secure()
param teamsWebhookUrl string

@description('Sprint 37.3 — auto-clear band ceiling (×100; 40 = 0.40).')
@minValue(0)
@maxValue(100)
param autoClearMaxFraudScore int = 40

@description('Sprint 37.3 — HITL review band floor (×100; 40 = 0.40).')
@minValue(0)
@maxValue(100)
param hitlReviewMinFraudScore int = 40

@description('Sprint 37.3 — escalate band floor (×100; 70 = 0.70).')
@minValue(0)
@maxValue(100)
param escalateMinFraudScore int = 70

@description('Sprint 37.3 — refund USD above which low-score returns still HITL.')
@minValue(0)
param autoClearMaxRefundValueUsd int = 100

@description('Sprint 37.3 — ring_indicator==true forces escalate.')
param ringIndicatorForceEscalate bool = true

@description('Sprint 37.3 — hold decisions require Tier-3 PII unlock.')
param holdRequiresTier3PiiUnlock bool = true

var serviceCode = 'RC-E2E-07'

// -----------------------------------------------------------------------------
// Sprint 37.3 — adaptive HITL thresholds + Tier-3 PII unlock in Key Vault
// -----------------------------------------------------------------------------
module hitl 'hitl.bicep' = {
  name: 'hitl-${serviceCode}'
  params: {
    tenant: tenant
    keyVaultName: keyVaultName
    agentIdentityId: agentIdentityId
    autoClearMaxFraudScore: autoClearMaxFraudScore
    hitlReviewMinFraudScore: hitlReviewMinFraudScore
    escalateMinFraudScore: escalateMinFraudScore
    autoClearMaxRefundValueUsd: autoClearMaxRefundValueUsd
    ringIndicatorForceEscalate: ringIndicatorForceEscalate
    holdRequiresTier3PiiUnlock: holdRequiresTier3PiiUnlock
    tokenizerBulkDetokenizeWebhookUrl: tokenizerBulkDetokenizeWebhookUrl
    teamsWebhookUrl: teamsWebhookUrl
  }
}

module fleet '../../../../apex-m/infra/bicep/modules/agent-fleet.bicep' = [
  for sid in featuredScenarios: {
    name: 'fleet-${sid}'
    params: {
      tenant: tenant
      serviceCode: serviceCode
      scenarioId: sid
      wave: wave
      containerAppsEnvId: containerAppsEnvId
      agentIdentityId: agentIdentityId
    }
  }
]

output serviceCode string = serviceCode
output deployedScenarios array = featuredScenarios
output hitlSecretIds object = hitl.outputs.hitlSecretIds
output hitlSecretPrefix string = hitl.outputs.secretPrefix
