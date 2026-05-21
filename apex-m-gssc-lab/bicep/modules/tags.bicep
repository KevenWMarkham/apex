// modules/tags.bicep
// APEX-M GSSC Lab tag schema per §3.3 of the deployment doc.
// Six required tags: apex-m, env, owner, pack-tenant, auto-stop, cost-center.
// pack-tenant allowed values come from §22.2 (FinOps showback): the seven
// pack tenants the lab supports.
//
// This module emits the tag set as an output object; it creates no resources.

targetScope = 'subscription'

@description('Owner email — who manages the resource (apex-m §3.3).')
param ownerEmail string

@description('Pack-tenant value per §22.2 (shared, merch, finance, risk, manufacturing, cxp, esg).')
@allowed([
  'shared'
  'merch'
  'finance'
  'risk'
  'manufacturing'
  'cxp'
  'esg'
])
param packTenant string

@description('Auto-shutdown eligibility tag value (§3.3 — true | false).')
param autoStop bool

var baseTags = {
  'apex-m': 'lab'
  env: 'gssc-lab'
  owner: ownerEmail
  'cost-center': 'DMTSP-APEX-M-LAB'
  'pack-tenant': packTenant
  'auto-stop': autoStop ? 'true' : 'false'
}

output tags object = baseTags
