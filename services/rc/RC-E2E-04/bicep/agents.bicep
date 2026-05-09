// services/rc/RC-E2E-04/bicep/agents.bicep
// Override hook for service-specific agent configuration.
// Default agent-fleet behavior is in apex-m/infra/bicep/modules/agent-fleet.bicep.
// Add only the deltas (custom tools, custom prompts, custom HITL gates) here.

targetScope = 'resourceGroup'

@description('Tenant slug.')
param tenant string

@description('Scenario id this override applies to.')
param scenarioId string

// Add scenario-specific overrides below. Empty by default.
