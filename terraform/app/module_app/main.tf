data "azurerm_container_registry" "acr" {
  name                = "acr${var.app_name}"
  resource_group_name = "rg-${var.app_name}-base-${var.location}"
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


data "azurerm_subnet" "cae_subnet" {
  name                 = "snet-cae-${var.app_name}-${var.environment}"
  virtual_network_name = data.azurerm_virtual_network.vnet.name
  resource_group_name  = data.azurerm_resource_group.env_rg.name
}


resource "azurerm_container_app_environment" "cont_app_env" {
  name                       = "cae-${var.app_name}-${var.environment}-${var.location}"
  location                   = var.location
  resource_group_name        = data.azurerm_resource_group.env_rg.name
  infrastructure_subnet_id   = data.azurerm_subnet.cae_subnet.id
  workload_profile {
    name                  = "Consumption"
    workload_profile_type = "Consumption"
    maximum_count         = 4
    minimum_count         = 0
  }
  lifecycle {
    ignore_changes = [infrastructure_resource_group_name, infrastructure_subnet_id]
  }
}

# data "azurerm_key_vault" "kv" {
#   name                = "kv-${var.app_name}-${var.environment}"
#   resource_group_name = data.azurerm_resource_group.base_rg.name
# }

resource "azurerm_user_assigned_identity" "containerapp" {
  location            = data.azurerm_resource_group.env_rg.location
  name                = "containerappidentity-${var.app_name}-${var.environment}-${var.location}"
  resource_group_name = data.azurerm_resource_group.env_rg.name
}
resource "azurerm_role_assignment" "containerapp" {
  scope                = data.azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.containerapp.principal_id
  depends_on           = [azurerm_user_assigned_identity.containerapp]
}

# resource "azurerm_role_assignment" "primary_keyvault_access" {
#   scope                = data.azurerm_key_vault.kv.id
#   role_definition_name = "Key Vault Secrets User"
#   principal_id         = azurerm_user_assigned_identity.containerapp.principal_id
# }

resource "azurerm_container_app" "ca" {
  name                         = "ca-${var.app_name}-${var.environment}-${var.location}"
  container_app_environment_id = azurerm_container_app_environment.cont_app_env.id
  resource_group_name          = data.azurerm_resource_group.env_rg.name
  revision_mode                = "Single"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.containerapp.id]
  }

  registry {
    server   = data.azurerm_container_registry.acr.login_server
    identity = azurerm_user_assigned_identity.containerapp.id
  }

  template {
    container {
      name   = "${var.app_name}-${var.environment}-${var.location}"
      image  = "${data.azurerm_container_registry.acr.login_server}/${var.app_name}:latest-${var.environment}"
      cpu    = var.cpu
      memory = var.memory
      env {
        name  = "ENV"
        value = var.app_env
      }
      env {
        name  = "AZURE_CLIENT_ID"
        value = azurerm_user_assigned_identity.containerapp.client_id
      }
    }
    min_replicas = var.min_replicas
    max_replicas = var.max_replicas
  }
  depends_on = [
    azurerm_user_assigned_identity.containerapp,
    azurerm_role_assignment.containerapp,
    # azurerm_role_assignment.primary_keyvault_access
  ]
  ingress {
    external_enabled = true
    target_port      = var.PORT
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

output "container_app_url" {
  value       = azurerm_container_app.ca.ingress[0].fqdn
  description = "The URL of the Azure Container App"
}

resource "azuread_application" "my_app" {
  display_name     = "app-${var.app_name}-${var.environment}-${var.location}"
  sign_in_audience = "AzureADMyOrg"
  web {
    redirect_uris = compact([
      "https://${azurerm_container_app.ca.ingress[0].fqdn}/.auth/login/aad/callback",
      # var.extra_redirect_uri,
    ])

    implicit_grant {
      access_token_issuance_enabled = false
      id_token_issuance_enabled     = true
    }
  }
  depends_on = [azurerm_container_app.ca]
}

resource "azapi_resource_action" "my_app_auth" {
  type        = "Microsoft.App/containerApps/authConfigs@2024-03-01"
  resource_id = "${azurerm_container_app.ca.id}/authConfigs/current"
  method      = "PUT"
  body = {
    location = var.location
    properties = {
      globalValidation = {
        redirectToProvider          = "azureactivedirectory"
        unauthenticatedClientAction = "RedirectToLoginPage"
      }
      identityProviders = {
        azureActiveDirectory = {
          registration = {
            clientId     = azuread_application.my_app.client_id
            openIdIssuer = "https://sts.windows.net/${data.azurerm_subscription.current.tenant_id}/v2.0"
          }
          validation = {
            defaultAuthorizationPolicy = {
              allowedApplications = [
                azuread_application.my_app.client_id
              ]
            }
          }
        }
      }
      platform = {
        enabled = true
      }
    }
  }
}
