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

resource "azurerm_key_vault" "example" {
  name                        = "kv-${var.app_name}"
  location                    = azurerm_resource_group.common_rg.location
  resource_group_name         = azurerm_resource_group.common_rg.name
  enabled_for_disk_encryption = false
  tenant_id                   = data.azurerm_subscription.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"
}


resource "azurerm_virtual_network" "example" {
  name                = "vn-example"
  location            = azurerm_resource_group.common_rg.location
  resource_group_name = azurerm_resource_group.common_rg.name
  address_space       = ["10.5.0.0/16"]
}

resource "azurerm_subnet" "vm_sn" {
  name                 = "vm-sn"
  resource_group_name  = azurerm_resource_group.common_rg.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.5.3.0/24"]
}

resource "azurerm_public_ip" "example" {
  name                = "vm-public-ip"
  location            = azurerm_resource_group.common_rg.location
  resource_group_name = azurerm_resource_group.common_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
  zones               = ["3"]
}

resource "azurerm_network_security_group" "example" {
  name                = "jooTestSecurityGroup"
  location            = azurerm_resource_group.common_rg.location
  resource_group_name = azurerm_resource_group.common_rg.name

  security_rule {
    name                       = "test123"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {}
}

resource "azurerm_network_interface" "example" {
  name                = "example-nic"
  location            = azurerm_resource_group.common_rg.location
  resource_group_name = azurerm_resource_group.common_rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.vm_sn.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.example.id
  }
}

resource "azurerm_network_interface_security_group_association" "nsg_assoc" {
  network_interface_id      = azurerm_network_interface.example.id
  network_security_group_id = azurerm_network_security_group.example.id
}

resource "azurerm_virtual_machine" "vm" {
  name                  = "testi-vm"
  location              = azurerm_resource_group.common_rg.location
  resource_group_name   = azurerm_resource_group.common_rg.name
  network_interface_ids = [azurerm_network_interface.example.id]
  vm_size               = "Standard_B1s"
  zones                 = ["3"]

  delete_os_disk_on_termination    = true
  delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "hostname"
    admin_username = "testadmin"
    admin_password = "testpass"
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
  tags = {}
}

resource "azurerm_subnet" "example" {
  name                 = "sn-db"
  resource_group_name  = azurerm_resource_group.common_rg.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.5.2.0/24"]
  service_endpoints    = ["Microsoft.Storage"]
  delegation {
    name = "fs"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}
resource "azurerm_private_dns_zone" "example" {
  name                = "example.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.common_rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "example" {
  name                  = "exampleVnetZone.com"
  private_dns_zone_name = azurerm_private_dns_zone.example.name
  virtual_network_id    = azurerm_virtual_network.example.id
  resource_group_name   = azurerm_resource_group.common_rg.name
  depends_on            = [azurerm_subnet.example]
}

resource "azurerm_postgresql_flexible_server" "example" {
  name                          = "ex-serv-hommat"
  resource_group_name           = azurerm_resource_group.common_rg.name
  location                      = azurerm_resource_group.common_rg.location
  version                       = "16"
  delegated_subnet_id           = azurerm_subnet.example.id
  private_dns_zone_id           = azurerm_private_dns_zone.example.id
  public_network_access_enabled = false
  administrator_login           = "testadmin"
  administrator_password        = "testpass"
  zone                          = "1"

  storage_mb   = 32768
  storage_tier = "P4"

  sku_name   = "B_Standard_B1ms"
  depends_on = [azurerm_private_dns_zone_virtual_network_link.example]

}