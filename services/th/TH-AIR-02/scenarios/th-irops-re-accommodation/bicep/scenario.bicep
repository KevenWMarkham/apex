// services/th/TH-AIR-02/scenarios/th-irops-re-accommodation/bicep/scenario.bicep
// Scenario-level overlay — only define if the scenario needs more than the
// service-default agent fleet (e.g., custom MCP server, custom data fusion).

targetScope = 'resourceGroup'

@description('Tenant slug.')
param tenant string

// Scenario-specific resources go here. Empty by default.
