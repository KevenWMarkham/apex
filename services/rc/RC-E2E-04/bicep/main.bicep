// services/rc/RC-E2E-04/bicep/main.bicep
// Service-level deployment for RC-E2E-04 Customer Lifecycle & Loyalty.
// Composes the canonical agent-fleet module with service-specific schemas,
// personas, HITL policy, and the Tier-3 PII JIT unlock pattern.

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

@description('Sprint 34.3 — winback offer percent above which Maya Patel HITL fires.')
@minValue(0)
@maxValue(100)
param winbackOfferAbovePct int = 25

@description('Sprint 34.3 — cohort total offer cost USD above which HITL fires.')
@minValue(0)
param cohortTotalOfferCostAboveUsd int = 50000

@description('Sprint 34.3 — Tier-3 PII unlock required for percent_off / amount_off offers.')
param tier3PiiUnlockRequired bool = true

@description('Sprint 34.3 — max cohort size eligible for auto-clear (points/shipping only).')
@minValue(0)
param autoClearMaxCohortSize int = 200

var serviceCode = 'RC-E2E-04'

// -----------------------------------------------------------------------------
// Sprint 34.3 — HITL threshold + Tier-3 PII unlock policy in Key Vault
// -----------------------------------------------------------------------------
module hitl 'hitl.bicep' = {
  name: 'hitl-${serviceCode}'
  params: {
    tenant: tenant
    keyVaultName: keyVaultName
    agentIdentityId: agentIdentityId
    winbackOfferAbovePct: winbackOfferAbovePct
    cohortTotalOfferCostAboveUsd: cohortTotalOfferCostAboveUsd
    tier3PiiUnlockRequired: tier3PiiUnlockRequired
    autoClearMaxCohortSize: autoClearMaxCohortSize
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
