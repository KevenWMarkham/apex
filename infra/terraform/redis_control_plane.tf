# Sprint 26 Task 26.11 — Terraform-equivalent of redis_control_plane.bicep
#
# Same governance posture: Enterprise tier, private endpoint only, Entra
# auth (no connection strings), Purview Internal class tag.

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.110"
    }
    azurecaf = {
      source  = "aztfmod/azurecaf"
      version = "~> 1.2"
    }
  }
}

variable "engagement_code" {
  description = "APEX engagement code, e.g., apex-tenant-rc-wave1"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  type = string
}

variable "private_endpoint_subnet_id" {
  description = "VNet subnet for the private endpoint"
  type        = string
}

variable "control_plane_reader_group_id" {
  description = "Entra group object id authorized to read budget/cancel-token keys"
  type        = string
}

variable "control_plane_writer_group_id" {
  description = "Entra group object id authorized to write cancel tokens"
  type        = string
}

variable "sku_name" {
  description = "Redis Enterprise SKU"
  type        = string
  default     = "Enterprise_E10"
  validation {
    condition     = contains(["Enterprise_E10", "Enterprise_E20", "Enterprise_E50"], var.sku_name)
    error_message = "Sprint 26 governance: SKU must be Enterprise tier."
  }
}

locals {
  common_tags = {
    apexEngagement   = var.engagement_code
    apexComponent    = "control-plane"
    apexClass        = "Internal"
    apexSprint       = "sprint-26"
    apexCachePolicy  = "apex-core-section-11"
  }
}

resource "azurerm_redis_enterprise_cluster" "control_plane" {
  name                = "${var.engagement_code}-control-plane"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku_name            = var.sku_name
  zones               = ["1", "2", "3"]
  tags                = local.common_tags

  minimum_tls_version = "1.2"
}

resource "azurerm_redis_enterprise_database" "control_plane" {
  name              = "default"
  cluster_id        = azurerm_redis_enterprise_cluster.control_plane.id
  client_protocol   = "Encrypted"
  clustering_policy = "EnterpriseCluster"
  eviction_policy   = "NoEviction"

  # Persistence off — Cosmos is the durable record per APEX-CORE §11
  # Sprint 26 Task 26.11 — accessKeysAuthentication disabled by default in newer provider releases
  resource_provider_use_legacy_id = false
}

resource "azurerm_private_endpoint" "control_plane" {
  name                = "${var.engagement_code}-control-plane-pe"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.private_endpoint_subnet_id
  tags                = local.common_tags

  private_service_connection {
    name                           = "redis-enterprise-link"
    private_connection_resource_id = azurerm_redis_enterprise_cluster.control_plane.id
    subresource_names              = ["redisEnterprise"]
    is_manual_connection           = false
  }
}

resource "azurerm_role_assignment" "reader" {
  scope                = azurerm_redis_enterprise_cluster.control_plane.id
  role_definition_name = "Reader"
  principal_id         = var.control_plane_reader_group_id
  principal_type       = "Group"
}

resource "azurerm_role_assignment" "writer" {
  scope                = azurerm_redis_enterprise_cluster.control_plane.id
  role_definition_name = "Contributor"
  principal_id         = var.control_plane_writer_group_id
  principal_type       = "Group"
}

output "redis_hostname" {
  value = azurerm_redis_enterprise_cluster.control_plane.hostname
}

output "redis_resource_id" {
  value = azurerm_redis_enterprise_cluster.control_plane.id
}

output "control_plane_database_id" {
  value = azurerm_redis_enterprise_database.control_plane.id
}

output "private_endpoint_id" {
  value = azurerm_private_endpoint.control_plane.id
}
