terraform {
  # backend "azurerm" {
  #   resource_group_name  = "rg-mytestprj-base-swedencentral"
  #   storage_account_name = "sttfbemytestprj"
  #   container_name       = "terraform-state"
  #   key                  = "prod-terraform.tfstate"
  #   use_azuread_auth     = true
  # }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.62.1"
    }
    azapi = {
      source  = "azure/azapi"
      version = "=2.3.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "=3.3.0"
    }
  }
}
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
  subscription_id = var.PROD_SUBSCRIPTION_ID
}

provider "azapi" {
}

provider "azuread" {
}
