// modules/tags-apply.bicep
// Applies a tag object at subscription scope. API 2025-04-01 is the latest
// stable per Microsoft Learn (May 2026):
//   https://learn.microsoft.com/en-us/azure/templates/microsoft.resources/tags

targetScope = 'subscription'

@description('Tag object emitted by modules/tags.bicep.')
param tags object

resource subTags 'Microsoft.Resources/tags@2025-04-01' = {
  name: 'default'
  properties: {
    tags: tags
  }
}
