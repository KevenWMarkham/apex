// apps/deploy-wizard/bicep/main.bicep
// Wraps infra/bicep/control-plane/main.bicep so the wizard can be deployed
// from inside its own folder with a one-liner:
//   az deployment group create -g rg-apex-... -f apps/deploy-wizard/bicep/main.bicep -p ...

targetScope = 'resourceGroup'

param tenant string
param containerAppsEnvId string
param wizardApiImage string
param wizardWebImage string

module cp '../../../infra/bicep/control-plane/main.bicep' = {
  name: 'apex-control-plane'
  params: {
    tenant: tenant
    containerAppsEnvId: containerAppsEnvId
    wizardApiImage: wizardApiImage
    wizardWebImage: wizardWebImage
  }
}

output controlPlaneApiFqdn string = cp.outputs.controlPlaneApiFqdn
output controlPlaneWebFqdn string = cp.outputs.controlPlaneWebFqdn
