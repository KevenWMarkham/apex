using '00-subscription-policies.bicep'

// sub-apex-m-gssc-lab subscription GUID, supplied by Azure central provisioning
// per APEX-M GSSC Lab Infrastructure Deployment v2.0 §3.1.
// Resolve from `az account subscription list --query "[?displayName=='sub-apex-m-gssc-lab'].subscriptionId" -o tsv`.
param subscriptionId = '<sub-apex-m-gssc-lab GUID>'

param ownerEmail = '<engineer-email>'

// One of: shared | merch | finance | risk | manufacturing | cxp | esg (§22.2).
// Subscription-scope tag is typically 'shared' since the sub itself is multi-tenant.
param packTenant = 'shared'

// Subscription-scope auto-stop tag is informational; child RGs/resources set their own.
param autoStop = false

// log-apex-m-gssc-eus2 resource ID. Resolve from
// `az monitor log-analytics workspace show -g rg-apex-m-gssc-observability -n log-apex-m-gssc-eus2 --query id -o tsv`
// once the observability platform is deployed (Feature F6.3).
param logAnalyticsWorkspaceId = '<full-ARM-id-of-log-apex-m-gssc-eus2>'
