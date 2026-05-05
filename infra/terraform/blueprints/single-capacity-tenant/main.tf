# Blueprint: Single Capacity per Tenant
#
# Sprint 14 Task 14.3 (BL.P.93). One F-SKU capacity hosting every
# medallion role (Bronze, Silver, Gold, Governance, Runtime, Sandbox).
# Right for Wave 1 pilots and most mid-size Wave 2 engagements.
#
# Cost profile (illustrative): F16 ≈ $2,100/mo, F32 ≈ $4,200/mo,
# F64 ≈ $5,475/mo (Copilot threshold). Reservation pricing reduces 20%
# (1-year) or 40% (3-year) — apply downstream of this module.

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

# ---------------------------------------------------------------------------
# Inputs (override via terraform.tfvars or -var)
# ---------------------------------------------------------------------------

variable "practice" {
  description = "APEX Practice (rc / hls / er / axle / tmt / th / ice / core)."
  type        = string
}

variable "environment" {
  description = "Environment tier (dev / test / stage / prod)."
  type        = string
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "eastus2"
}

variable "sku" {
  description = "F-SKU. F16 minimum; production must use F64+."
  type        = string
  default     = "F16"
}

variable "capacity_admins" {
  description = "Entra group IDs or UPNs administering the capacity."
  type        = list(string)
}

variable "monthly_budget_usd" {
  description = "Soft monthly budget guardrail."
  type        = number
  default     = 6000
}

variable "cost_center" {
  description = "Finance cost-center code for chargeback."
  type        = string
}

# ---------------------------------------------------------------------------
# Resource group
# ---------------------------------------------------------------------------

resource "azurerm_resource_group" "this" {
  name     = "rg-apex-${var.practice}-${var.environment}"
  location = var.location

  tags = {
    "apex:practice"    = var.practice
    "apex:environment" = var.environment
    "apex:blueprint"   = "single-capacity-tenant"
    "apex:cost_center" = var.cost_center
  }
}

# ---------------------------------------------------------------------------
# One capacity, one role pattern
# ---------------------------------------------------------------------------

module "capacity" {
  source = "../../modules/fabric_capacity"

  resource_group_name = azurerm_resource_group.this.name
  location            = var.location
  practice            = var.practice
  environment         = var.environment
  sku                 = var.sku
  capacity_admins     = var.capacity_admins
  monthly_budget_usd  = var.monthly_budget_usd
  cost_center         = var.cost_center

  tags = {
    "apex:blueprint" = "single-capacity-tenant"
  }
}

# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------

output "capacity_id" {
  value = module.capacity.id
}

output "capacity_name" {
  value = module.capacity.name
}

output "estimated_monthly_cost_usd" {
  value = module.capacity.estimated_monthly_cost_usd
}

output "blueprint" {
  value = "single-capacity-tenant"
}
