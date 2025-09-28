data "azurerm_subscription" "current" {
  subscription_id = var.SUBSCRIPTION_ID
}

resource "azurerm_resource_group" "common_rg" {
  name     = "rg-common-${var.app_name}"
  location = var.location
}

resource "azurerm_container_registry" "acr" {
  name                = "fatestdemo"
  resource_group_name = azurerm_resource_group.common_rg.name
  location            = azurerm_resource_group.common_rg.location
  sku                 = "Basic"
  admin_enabled       = false
}

resource "azurerm_key_vault" "kv" {
  name                        = "kv-${var.app_name}"
  location                    = azurerm_resource_group.common_rg.location
  resource_group_name         = azurerm_resource_group.common_rg.name
  enabled_for_disk_encryption = false
  tenant_id                   = data.azurerm_subscription.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
  enable_rbac_authorization   = true

  sku_name = "standard"
}

resource "azurerm_storage_account" "storage" {
  name                     = "testistorageacco"
  resource_group_name      = azurerm_resource_group.common_rg.name
  location                 = azurerm_resource_group.common_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  public_network_access_enabled = false
}
