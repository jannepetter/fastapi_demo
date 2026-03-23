data "azurerm_resource_group" "common_rg" {
  name = "rg-common-${var.app_name}"
}

data "azurerm_key_vault" "fav" {
  name                = "kv-fastapidemo"
  resource_group_name = data.azurerm_resource_group.common_rg.name
}

data "azurerm_subscription" "current" {
  subscription_id = var.SUBSCRIPTION_ID
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.app_name}-${var.environment}-${var.location}"
  location = var.location
}

resource "azurerm_virtual_network" "vnet_a" {
  name                = "rg-${var.app_name}-${var.environment}-${var.location}-vnet"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  address_space       = ["10.1.0.0/16"]
}

resource "azurerm_subnet" "cae_subnet" {
  name                 = "cae-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet_a.name
  address_prefixes     = ["10.1.0.0/22"]
    delegation {
    name = "containerappsdelegation"

    service_delegation {
      name = "Microsoft.App/environments"

      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action"
      ]
    }
  }
}

resource "azurerm_subnet" "default" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet_a.name
  address_prefixes     = ["10.1.4.0/24"]
}

resource "azurerm_private_dns_zone" "my_dns_zone" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "dns_link" {
  name                  = "dnslink"
  resource_group_name   = azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.my_dns_zone.name
  virtual_network_id    = azurerm_virtual_network.vnet_a.id
}

resource "azurerm_private_endpoint" "example" {
  name                = "pe-kv"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.default.id
  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [azurerm_private_dns_zone.my_dns_zone.id]
  }
    private_service_connection {
    name                              = "pe-kv"
    private_connection_resource_id    = data.azurerm_key_vault.fav.id
    subresource_names                 = ["vault"]
    is_manual_connection              = false
  }
}