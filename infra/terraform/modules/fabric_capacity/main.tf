# APEX Fabric Capacity Module
#
# Provisions one azurerm_fabric_capacity with APEX-canonical naming,
# tagging, and cost guardrails. Sprint 14 Task 14.1 (BL.P.91).
#
# Usage:
#   module "fabric_capacity_prod" {
#     source              = "../../modules/fabric_capacity"
#     name                = "apex-rc-prod"
#     resource_group_name = "rg-apex-rc-prod"
#     location            = "eastus2"
#     sku                 = "F64"
#     environment         = "prod"
#     practice            = "rc"
#     monthly_budget_usd  = 5500
#     capacity_admins     = ["apex-rc-admins@deloitte.com"]
#   }
#
# Source-of-truth references:
#   Sellers Guide §1.6 (canonical schema kernel) — Fabric is the data plane
#   Sellers Guide §6.13.7.4 — F-SKU sizing inflection points (F64 = Copilot)
#   Sellers Guide Appendix V — cost calculation deltas per F-SKU tier

terraform {
  required_version = ">= 1.7.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

# ---------------------------------------------------------------------------
# Variable validation guards
# ---------------------------------------------------------------------------

locals {
  # Canonical APEX F-SKU set (per Sellers Guide §6.13.7.4 inflection points)
  valid_skus = [
    "F2", "F4", "F8", "F16", "F32",
    "F64",   # Copilot threshold; minimum for Practice-grade workloads
    "F128", "F256", "F512", "F1024", "F2048"
  ]

  # Approximate USD list price per F-SKU per month (PAYGO; reservation
  # discounts apply downstream). Used to enforce the monthly_budget_usd
  # guardrail at plan time. Numbers are illustrative; final costs come
  # from Microsoft. See Sellers Guide Appendix V.
  sku_monthly_usd = {
    F2    = 263
    F4    = 525
    F8    = 1050
    F16   = 2100
    F32   = 4200
    F64   = 5475
    F128  = 10950
    F256  = 21900
    F512  = 43800
    F1024 = 87600
    F2048 = 175200
  }

  estimated_monthly_cost = local.sku_monthly_usd[var.sku]

  # APEX canonical naming: apex-<practice>-<environment>[-<suffix>]
  canonical_name = lower(
    var.name_override != null
    ? var.name_override
    : (
      var.suffix != null
      ? "apex-${var.practice}-${var.environment}-${var.suffix}"
      : "apex-${var.practice}-${var.environment}"
    )
  )

  # APEX-canonical tag set (every Fabric capacity carries these — used by
  # Purview classification policy + cost-attribution dashboards)
  canonical_tags = merge(
    {
      "apex:practice"        = var.practice
      "apex:environment"     = var.environment
      "apex:resource_class"  = "fabric-capacity"
      "apex:sku"             = var.sku
      "apex:cost_center"     = var.cost_center
      "apex:owner"           = var.owner
      "apex:purview_class"   = "Internal"
      "apex:managed_by"      = "terraform"
      "apex:module_version"  = "0.1.0"
    },
    var.tags
  )
}

# ---------------------------------------------------------------------------
# Cost guardrail: refuse to plan if estimated cost exceeds budget
# ---------------------------------------------------------------------------

resource "null_resource" "cost_guardrail" {
  count = local.estimated_monthly_cost > var.monthly_budget_usd ? 1 : 0

  triggers = {
    error = "BUDGET_EXCEEDED: ${var.sku} estimated USD ${local.estimated_monthly_cost}/month exceeds monthly_budget_usd=${var.monthly_budget_usd}. Either bump the budget, drop to a smaller SKU, or set var.allow_budget_breach=true with sign-off."
  }

  lifecycle {
    precondition {
      condition     = var.allow_budget_breach
      error_message = "BUDGET_EXCEEDED: ${var.sku} estimated USD ${local.estimated_monthly_cost}/month exceeds monthly_budget_usd=${var.monthly_budget_usd}. Either bump var.monthly_budget_usd, drop to a smaller SKU, or set var.allow_budget_breach=true with explicit Independence-reviewed sign-off."
    }
  }
}

# ---------------------------------------------------------------------------
# Fabric capacity
# ---------------------------------------------------------------------------

resource "azurerm_fabric_capacity" "this" {
  name                = local.canonical_name
  resource_group_name = var.resource_group_name
  location            = var.location

  sku {
    name = var.sku
    tier = "Fabric"
  }

  administration_members = var.capacity_admins

  tags = local.canonical_tags

  lifecycle {
    # Prevent accidental destroy of production capacity. Override with
    # `-target` if intentional decommission is approved.
    prevent_destroy = true

    precondition {
      condition     = contains(local.valid_skus, var.sku)
      error_message = "Invalid SKU '${var.sku}'. Allowed: ${join(", ", local.valid_skus)}."
    }

    precondition {
      condition = (
        var.environment != "prod"
        || contains(["F64", "F128", "F256", "F512", "F1024", "F2048"], var.sku)
      )
      error_message = "Production capacities must use F64 or larger. F2-F32 are dev/test tiers; for prod choose F64+ for Copilot eligibility."
    }

    precondition {
      condition     = length(var.capacity_admins) >= 1
      error_message = "At least one capacity_admin must be supplied (Entra group or UPN)."
    }
  }
}
