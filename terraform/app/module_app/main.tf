
data "azurerm_resource_group" "env_rg" {
  name = "rg-${var.app_name}-${var.environment}-${var.location}"
}
data "azurerm_container_registry" "acr" {
  name                = "acr${var.app_name}123"
  resource_group_name = data.azurerm_resource_group.env_rg.name
}
data "azurerm_subscription" "current" {
  subscription_id = var.subscription_id
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
  name                           = "cae-${var.app_name}-${var.environment}-${var.location}"
  location                       = var.location
  resource_group_name            = data.azurerm_resource_group.env_rg.name
  infrastructure_subnet_id       = data.azurerm_subnet.cae_subnet.id
  internal_load_balancer_enabled = true
  public_network_access          = "Disabled"
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

resource "azurerm_container_app" "ca" {
  name                         = "ca-${var.app_name}-${var.environment}"
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

  secret {
    name  = "redis-password"
    value = var.redis_password
  }

  secret {
    name  = "cloudflare-tunnel-token"
    value = var.cloudflare_tunnel_token
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
      env {
        name  = "REDIS_HOST"
        value = "localhost"
      }
      env {
        name  = "REDIS_PORT"
        value = "6379"
      }
      env {
        name        = "REDIS_PASSWORD"
        secret_name = "redis-password"
      }
    }

    container {
      name   = "redis"
      image  = var.redis_image
      cpu    = var.redis_cpu
      memory = var.redis_memory

      command = ["/bin/sh", "-c"]
      args = [
        "redis-server --requirepass $REDIS_PASSWORD"
      ]

      env {
        name        = "REDIS_PASSWORD"
        secret_name = "redis-password"
      }
    }
    container {
      name   = "cloudflared"
      image  = "cloudflare/cloudflared:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name        = "TUNNEL_TOKEN"
        secret_name = "cloudflare-tunnel-token"
      }

      command = ["cloudflared"]
      args = [
        "tunnel",
        "--no-autoupdate",
        "run",
        "--token",
        "$(TUNNEL_TOKEN)"
      ]
    }
    min_replicas = var.min_replicas
    max_replicas = var.max_replicas
  }
  depends_on = [
    azurerm_user_assigned_identity.containerapp,
    azurerm_role_assignment.containerapp,
  ]
  ingress {
    external_enabled = false
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
