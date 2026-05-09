// infra/bicep/control-plane/main.bicep
// Deploys the deploy-wizard control-plane itself: an API Container App
// + a static web frontend + Cosmos for state + a managed identity that
// can read services/_registry.json from the repo (or from blob storage
// after publish).

targetScope = 'resourceGroup'

param tenant string
param location string = resourceGroup().location
param containerAppsEnvId string
param wizardApiImage string
param wizardWebImage string

resource cpIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-apex-${tenant}-control-plane'
  location: location
}

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: 'cosmos-apex-${tenant}-cp'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [ { locationName: location, failoverPriority: 0 } ]
  }
}

resource api 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'ca-apex-${tenant}-cp-api'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${cpIdentity.id}': {} }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvId
    configuration: {
      ingress: { external: true, targetPort: 8000 }
    }
    template: {
      containers: [
        {
          name: 'api'
          image: wizardApiImage
          env: [
            { name: 'APEX_TENANT', value: tenant }
            { name: 'COSMOS_ENDPOINT', value: cosmos.properties.documentEndpoint }
          ]
          resources: { cpu: json('1.0'), memory: '2Gi' }
        }
      ]
      scale: { minReplicas: 1, maxReplicas: 3 }
    }
  }
}

resource web 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'ca-apex-${tenant}-cp-web'
  location: location
  properties: {
    managedEnvironmentId: containerAppsEnvId
    configuration: {
      ingress: { external: true, targetPort: 80 }
    }
    template: {
      containers: [
        {
          name: 'web'
          image: wizardWebImage
          env: [
            { name: 'API_URL', value: 'https://${api.properties.configuration.ingress.fqdn}' }
          ]
          resources: { cpu: json('0.25'), memory: '0.5Gi' }
        }
      ]
      scale: { minReplicas: 1, maxReplicas: 2 }
    }
  }
}

output controlPlaneApiFqdn string = api.properties.configuration.ingress.fqdn
output controlPlaneWebFqdn string = web.properties.configuration.ingress.fqdn
output controlPlaneIdentityId string = cpIdentity.id
