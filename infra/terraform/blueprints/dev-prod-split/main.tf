# Blueprint: Dev/Prod Split
#
# Sprint 14 Task 14.3 (BL.P.93). Two F-SKU capacities — one smaller
# capacity for dev/test (typically F16 or F32) and one production-grade
# capacity (F64 or larger). Right for Wave 2 engagements where dev
# iteration must not contend with production workloads.

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

variable "dev_sku" {
  type    = string
  default = "F16"
}

variable "prod_sku" {
  description = "Production capacity. Must be F64 or larger."
  type        = string
  default     = "F64"
}

variable "dev_admins" {
  type = list(string)
}

variable "prod_admins" {
  type = list(string)
}

variable "monthly_budget_usd_dev" {
  type    = number
  default = 2200
}

variable "monthly_budget_usd_prod" {
  type    = number
  default = 6000
}

variable "cost_center" {
  type = string
}

# ---------------------------------------------------------------------------
# Two resource groups (clean cost-attribution boundary)
# ---------------------------------------------------------------------------

resource "azurerm_resource_group" "dev" {
  name     = "rg-apex-${var.practice}-dev"
  location = var.location
  tags = {
    "apex:practice"    = var.practice
    "apex:environment" = "dev"
    "apex:blueprint"   = "dev-prod-split"
    "apex:cost_center" = var.cost_center
  }
}

resource "azurerm_resource_group" "prod" {
  name     = "rg-apex-${var.practice}-prod"
  location = var.location
  tags = {
    "apex:practice"    = var.practice
    "apex:environment" = "prod"
    "apex:blueprint"   = "dev-prod-split"
    "apex:cost_center" = var.cost_center
  }
}

# ---------------------------------------------------------------------------
# Two capacities
# ---------------------------------------------------------------------------

module "capacity_dev" {
  source = "../../modules/fabric_capacity"

  resource_group_name = azurerm_resource_group.dev.name
  location            = var.location
  practice            = var.practice
  environment         = "dev"
  sku                 = var.dev_sku
  capacity_admins     = var.dev_admins
  monthly_budget_usd  = var.monthly_budget_usd_dev
  cost_center         = var.cost_center
  tags                = { "apex:blueprint" = "dev-prod-split" }
}

module "capacity_prod" {
  source = "../../modules/fabric_capacity"

  resource_group_name = azurerm_resource_group.prod.name
  location            = var.location
  practice            = var.practice
  environment         = "prod"
  sku                 = var.prod_sku
  capacity_admins     = var.prod_admins
  monthly_budget_usd  = var.monthly_budget_usd_prod
  cost_center         = var.cost_center
  tags                = { "apex:blueprint" = "dev-prod-split" }
}

output "dev_capacity_id" { value = module.capacity_dev.id }
output "prod_capacity_id" { value = module.capacity_prod.id }
output "estimated_monthly_total_usd" {
  value = module.capacity_dev.estimated_monthly_cost_usd + module.capacity_prod.estimated_monthly_cost_usd
}
output "blueprint" { value = "dev-prod-split" }
