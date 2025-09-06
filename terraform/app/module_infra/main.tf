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
}
