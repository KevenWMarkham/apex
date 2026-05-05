# Blueprint: Adapter Bronze Workspace
#
# Sprint 15 (BL.P.95–109). Provisions the Bronze workspace + lakehouse
# + connection that any APEX SOR adapter targets. Composed with the
# Sprint 14 fabric_capacity module so the capacity is canonical-named
# and tag-stamped.
#
# Usage:
#   module "rc_bronze_adapter_ws" {
#     source = "../../blueprints/adapter-workspace"
#     practice            = "rc"
#     environment         = "prod"
#     location            = "eastus2"
#     capacity_admins     = ["apex-rc-admins@deloitte.com"]
#     adapter_name        = "sap-s4hana"
#     cost_center         = "RC-ENG-001"
#   }

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
  description = "APEX Practice (rc / hls / er / axle / tmt / th / ice / core)."
  type        = string
}

variable "environment" {
  description = "Environment tier (dev / test / stage / prod)."
  type        = string
  default     = "prod"
}

variable "location" {
  type    = string
  default = "eastus2"
}

variable "sku" {
  description = "Bronze-side capacity SKU. Bronze is typically smaller than Silver/Gold."
  type        = string
  default     = "F32"
}

variable "capacity_admins" {
  type = list(string)
}

variable "adapter_name" {
  description = "SOR adapter id (e.g., 'sap-s4hana', 'epic-clarity'). Used in resource tagging."
  type        = string
}

variable "cost_center" {
  type = string
}

variable "monthly_budget_usd" {
  type    = number
  default = 5000
}

# ---------------------------------------------------------------------------
# Resource group for the Bronze workspace
# ---------------------------------------------------------------------------

resource "azurerm_resource_group" "bronze" {
  name     = "rg-apex-${var.practice}-${var.environment}-bronze"
  location = var.location

  tags = {
    "apex:practice"     = var.practice
    "apex:environment"  = var.environment
    "apex:role"         = "bronze"
    "apex:adapter"      = var.adapter_name
    "apex:blueprint"    = "adapter-workspace"
    "apex:cost_center"  = var.cost_center
  }
}

# ---------------------------------------------------------------------------
# Bronze-side Fabric capacity (composed with Sprint 14 module)
# ---------------------------------------------------------------------------

module "bronze_capacity" {
  source = "../../modules/fabric_capacity"

  resource_group_name = azurerm_resource_group.bronze.name
  location            = var.location
  practice            = var.practice
  environment         = var.environment
  suffix              = "bronze"
  sku                 = var.sku
  capacity_admins     = var.capacity_admins
  monthly_budget_usd  = var.monthly_budget_usd
  cost_center         = var.cost_center

  tags = {
    "apex:role"       = "bronze"
    "apex:adapter"    = var.adapter_name
    "apex:blueprint"  = "adapter-workspace"
  }
}

# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------
#
# The actual workspace + lakehouse provisioning happens via the
# apex-fabric Python wrapper (Sprint 14 Task 14.2) — not Terraform —
# because the Fabric REST API is more ergonomic than the azurerm
# provider for workspace lifecycle. This blueprint provisions the
# capacity + RG; the Python WorkspaceClient takes it from there.

output "bronze_capacity_id" {
  value = module.bronze_capacity.id
}

output "bronze_capacity_name" {
  value = module.bronze_capacity.name
}

output "bronze_resource_group_name" {
  value = azurerm_resource_group.bronze.name
}

output "expected_workspace_name" {
  description = "The canonical workspace name the apex-fabric WorkspaceSpec will produce."
  value       = "apex-${var.practice}-${var.environment}-bronze"
}

output "next_step" {
  value = "Run: apex fabric describe-blueprint adapter-workspace; then create the workspace via apex_fabric.WorkspaceClient.ensure_workspace()."
}
