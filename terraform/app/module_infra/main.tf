locals {
  tags = {
    environment = var.environment
    project     = var.app_name
  }
}

data "azurerm_subscription" "current" {
  subscription_id = var.subscription_id
}

data "azurerm_resource_group" "env_rg" {
  name = "rg-${var.app_name}-${var.environment}-${var.location}"
}
data "azurerm_resource_group" "base_rg" {
  name = "rg-${var.app_name}-base-${var.location}"
}

data "azurerm_virtual_network" "vnet" {
  name                = "vnet-${var.app_name}-${var.environment}-${var.location}"
  resource_group_name = data.azurerm_resource_group.env_rg.name
}
data "azurerm_subnet" "pe_subnet" {
  name                 = "snet-pe-${var.environment}"
  resource_group_name  = data.azurerm_resource_group.env_rg.name
  virtual_network_name = data.azurerm_virtual_network.vnet.name
}


data "azurerm_key_vault" "kv" {
  name                = "kv-${var.app_name}-${var.environment}"
  resource_group_name = data.azurerm_resource_group.base_rg.name
}

resource "azurerm_subnet" "cae_subnet" {
  name                 = "snet-cae-${var.app_name}-${var.environment}"
  resource_group_name  = data.azurerm_resource_group.env_rg.name
  virtual_network_name = data.azurerm_virtual_network.vnet.name
  address_prefixes     = [var.cae_subnet_address]

  delegation {
    name = "delegation"

    service_delegation {
      name = "Microsoft.App/environments"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action",
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ]
    }
  }
}

data "azurerm_private_dns_zone" "kv_dns" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = data.azurerm_resource_group.base_rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "kv" {
  name                  = "pdnslink-kv-${var.app_name}-${var.environment}"
  resource_group_name   = data.azurerm_resource_group.base_rg.name
  private_dns_zone_name = data.azurerm_private_dns_zone.kv_dns.name
  virtual_network_id    = data.azurerm_virtual_network.vnet.id
  registration_enabled  = false
  tags                  = local.tags
}

resource "azurerm_private_endpoint" "kv_pe" {
  name                = "pe-kv-${var.app_name}-${var.environment}-${var.location}"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.env_rg.name
  subnet_id           = data.azurerm_subnet.pe_subnet.id

  private_service_connection {
    name                           = "psc-kv-${var.app_name}-${var.environment}"
    private_connection_resource_id = data.azurerm_key_vault.kv.id
    subresource_names              = ["vault"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "pdnszg-kv-${var.app_name}-${var.environment}"
    private_dns_zone_ids = [data.azurerm_private_dns_zone.kv_dns.id]
  }
  tags = local.tags
}
