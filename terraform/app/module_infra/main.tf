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
