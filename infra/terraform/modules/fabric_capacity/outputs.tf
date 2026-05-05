output "id" {
  description = "Resource ID of the provisioned Fabric capacity."
  value       = azurerm_fabric_capacity.this.id
}

output "name" {
  description = "Canonical name of the provisioned capacity."
  value       = azurerm_fabric_capacity.this.name
}

output "sku" {
  description = "F-SKU tier provisioned."
  value       = var.sku
}

output "estimated_monthly_cost_usd" {
  description = "Approximate USD/month list-price estimate. Reservation discounts (1-yr / 3-yr) are applied downstream."
  value       = local.estimated_monthly_cost
}

output "tags" {
  description = "Canonical APEX tag set applied to the capacity."
  value       = local.canonical_tags
}

output "canonical_naming_pattern" {
  description = "The naming pattern used: apex-{practice}-{environment}[-{suffix}]."
  value       = local.canonical_name
}
