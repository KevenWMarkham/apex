variable "name_override" {
  description = "If set, used verbatim as the capacity name. Otherwise the canonical name 'apex-<practice>-<environment>[-<suffix>]' is generated."
  type        = string
  default     = null
}

variable "name" {
  description = "Backward-compat alias for name_override. Prefer name_override."
  type        = string
  default     = null
}

variable "resource_group_name" {
  description = "Azure resource group that will own the capacity."
  type        = string
}

variable "location" {
  description = "Azure region (e.g. eastus2, westeurope)."
  type        = string
}

variable "sku" {
  description = "Fabric F-SKU tier. F64 is the Copilot eligibility threshold and the minimum for production Practice workloads."
  type        = string
  validation {
    condition = contains(
      ["F2", "F4", "F8", "F16", "F32", "F64", "F128", "F256", "F512", "F1024", "F2048"],
      var.sku
    )
    error_message = "Allowed SKUs: F2, F4, F8, F16, F32, F64, F128, F256, F512, F1024, F2048."
  }
}

variable "environment" {
  description = "APEX environment tier."
  type        = string
  validation {
    condition     = contains(["dev", "test", "stage", "prod"], var.environment)
    error_message = "Environment must be one of: dev, test, stage, prod."
  }
}

variable "practice" {
  description = "APEX Practice code (rc, hls, er, axle, tmt, th, ice)."
  type        = string
  validation {
    condition     = contains(["rc", "hls", "er", "axle", "tmt", "th", "ice", "core"], var.practice)
    error_message = "Practice must be one of: rc, hls, er, axle, tmt, th, ice, core."
  }
}

variable "suffix" {
  description = "Optional suffix appended to the canonical name (e.g., 'eu' for the European capacity in a multi-region tenant)."
  type        = string
  default     = null
}

variable "capacity_admins" {
  description = "List of UPNs or Entra group IDs that administer the capacity. Must contain at least one entry."
  type        = list(string)
  validation {
    condition     = length(var.capacity_admins) >= 1
    error_message = "Provide at least one capacity admin."
  }
}

variable "monthly_budget_usd" {
  description = "Soft monthly budget in USD. The module fails plan if the estimated cost of the chosen SKU exceeds this value, unless allow_budget_breach is set."
  type        = number
  default     = 999999  # Effectively no guardrail unless overridden
}

variable "allow_budget_breach" {
  description = "Set to true to permit a plan when the estimated cost exceeds monthly_budget_usd. Should require Independence-Office sign-off via PR review."
  type        = bool
  default     = false
}

variable "cost_center" {
  description = "Finance cost-center code for chargeback. Stamped into 'apex:cost_center' tag."
  type        = string
  default     = "TBD"
}

variable "owner" {
  description = "Engagement owner UPN or team alias. Stamped into 'apex:owner' tag."
  type        = string
  default     = "deloitte-apex-team"
}

variable "tags" {
  description = "Additional tags merged onto the canonical APEX tag set."
  type        = map(string)
  default     = {}
}
