// infra/bicep/platform/ledger.bicep
// Append-only audit-row ledger for every agent decision.
// Backed by Azure SQL with ledger tables (per Professional-APEX §13).

targetScope = 'resourceGroup'

param tenant string
param location string
param tags object = {}

@description('Key Vault name to store the connection string in.')
param keyVaultName string = 'kv-apex-${tenant}'

resource sqlServer 'Microsoft.Sql/servers@2023-08-01-preview' = {
  name: 'sql-apex-${tenant}-ledger'
  location: location
  tags: tags
  properties: {
    minimalTlsVersion: '1.2'
    publicNetworkAccess: 'Disabled'
  }
}

resource ledgerDb 'Microsoft.Sql/servers/databases@2023-08-01-preview' = {
  parent: sqlServer
  name: 'apex_ledger'
  location: location
  tags: tags
  sku: {
    name: 'GP_S_Gen5'
    tier: 'GeneralPurpose'
    family: 'Gen5'
    capacity: 2
  }
  properties: {
    isLedgerOn: true
  }
}

output sqlServerName string = sqlServer.name
output databaseName string = ledgerDb.name
output connectionStringSecretUri string = 'https://${keyVaultName}.vault.azure.net/secrets/apex-ledger-connection'
