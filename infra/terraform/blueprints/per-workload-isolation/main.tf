# Blueprint: Per-Workload Isolation
#
# Sprint 14 Task 14.3 (BL.P.93). Multiple production capacities, each
# scoped to a workload class. Right for Wave 3 enterprise scale and
# clients with compliance boundaries between workloads (e.g., HLS where
# clinical workloads must be isolated from operational analytics).
#
# Default capacity layout:
#   - Warehouse capacity (F128) — Silver/Gold T-SQL workloads
#   - Real-time capacity   (F64)  — Eventhouse / KQL streaming
#   - Governance capacity  (F64)  — Purview, classification, lineage tools
#
# Total minimum cost ~ F256-equivalent. Use only when workload isolation
# is a contractual requirement.

terraform {
  required_version = ">= 1.7.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "practice" {
  type = string
}

variable "location" {
  type    = string
  default = "eastus2"
}

variable "warehouse_sku" {
  type    = string
  default = "F128"
}

variable "realtime_sku" {
  type    = string
  default = "F64"
}

variable "governance_sku" {
  type    = string
  default = "F64"
}

variable "warehouse_admins" {
  type = list(string)
}

variable "realtime_admins" {
  type = list(string)
}

variable "governance_admins" {
  type = list(string)
}

variable "cost_center" {
  type = string
}

# ---------------------------------------------------------------------------
# One resource group per workload class
# ---------------------------------------------------------------------------

resource "azurerm_resource_group" "warehouse" {
  name     = "rg-apex-${var.practice}-prod-warehouse"
  location = var.location
  tags = {
    "apex:practice"      = var.practice
    "apex:environment"   = "prod"
    "apex:workload"      = "warehouse"
    "apex:blueprint"     = "per-workload-isolation"
    "apex:cost_center"   = var.cost_center
  }
}

resource "azurerm_resource_group" "realtime" {
  name     = "rg-apex-${var.practice}-prod-realtime"
  location = var.location
  tags = {
    "apex:practice"      = var.practice
    "apex:environment"   = "prod"
    "apex:workload"      = "realtime"
    "apex:blueprint"     = "per-workload-isolation"
    "apex:cost_center"   = var.cost_center
  }
}

resource "azurerm_resource_group" "governance" {
  name     = "rg-apex-${var.practice}-prod-governance"
  location = var.location
  tags = {
    "apex:practice"      = var.practice
    "apex:environment"   = "prod"
    "apex:workload"      = "governance"
    "apex:blueprint"     = "per-workload-isolation"
    "apex:cost_center"   = var.cost_center
  }
}

# ---------------------------------------------------------------------------
# Three capacities
# ---------------------------------------------------------------------------

module "warehouse_capacity" {
  source              = "../../modules/fabric_capacity"
  resource_group_name = azurerm_resource_group.warehouse.name
  location            = var.location
  practice            = var.practice
  environment         = "prod"
  suffix              = "warehouse"
  sku                 = var.warehouse_sku
  capacity_admins     = var.warehouse_admins
  cost_center         = var.cost_center
  tags                = { "apex:blueprint" = "per-workload-isolation", "apex:workload" = "warehouse" }
}

module "realtime_capacity" {
  source              = "../../modules/fabric_capacity"
  resource_group_name = azurerm_resource_group.realtime.name
  location            = var.location
  practice            = var.practice
  environment         = "prod"
  suffix              = "realtime"
  sku                 = var.realtime_sku
  capacity_admins     = var.realtime_admins
  cost_center         = var.cost_center
  tags                = { "apex:blueprint" = "per-workload-isolation", "apex:workload" = "realtime" }
}

module "governance_capacity" {
  source              = "../../modules/fabric_capacity"
  resource_group_name = azurerm_resource_group.governance.name
  location            = var.location
  practice            = var.practice
  environment         = "prod"
  suffix              = "governance"
  sku                 = var.governance_sku
  capacity_admins     = var.governance_admins
  cost_center         = var.cost_center
  tags                = { "apex:blueprint" = "per-workload-isolation", "apex:workload" = "governance" }
}

output "warehouse_capacity_id" { value = module.warehouse_capacity.id }
output "realtime_capacity_id" { value = module.realtime_capacity.id }
output "governance_capacity_id" { value = module.governance_capacity.id }
output "estimated_monthly_total_usd" {
  value = (
    module.warehouse_capacity.estimated_monthly_cost_usd
    + module.realtime_capacity.estimated_monthly_cost_usd
    + module.governance_capacity.estimated_monthly_cost_usd
  )
}
output "blueprint" { value = "per-workload-isolation" }
