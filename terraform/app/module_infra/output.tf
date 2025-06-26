output "resource_group" {
  value = {
    location = azurerm_resource_group.rg.location
    name     = azurerm_resource_group.rg.name
  }
  sensitive = true
}