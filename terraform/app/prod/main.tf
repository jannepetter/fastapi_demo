variable "app_name" {
  description = "The name of the application"
  type        = string
  default     = "mytestprj"
}
variable "app_env" {
  description = "The app environment"
  type        = string
  default     = "PROD"
}

variable "port" {
  description = "The default port for app"
  default     = 8000
}

variable "environments" {
  description = "List of environment configurations with all required values"
  type = list(object({
    environment        = string
    location           = string
    cpu                = number
    memory             = string
    min_replicas       = number
    max_replicas       = number
    cae_subnet_address = string
  }))
  default = [
    {
      environment        = "prod"
      location           = "swedencentral"
      cpu                = 0.25
      memory             = "0.5Gi"
      min_replicas       = 1
      max_replicas       = 2
      cae_subnet_address = "10.0.8.0/21"
    }
  ]
}
module "infra" {
  for_each           = { for env in var.environments : env.environment => env }
  source             = "../module_infra"
  subscription_id    = var.PROD_SUBSCRIPTION_ID
  location           = each.value.location
  app_name           = var.app_name
  environment        = each.value.environment
  cae_subnet_address = each.value.cae_subnet_address
}

module "app" {
  for_each        = { for env in var.environments : env.environment => env }
  source          = "../module_app"
  app_env         = var.app_env
  PORT            = var.port
  subscription_id = var.PROD_SUBSCRIPTION_ID
  app_name        = var.app_name
  environment     = each.value.environment
  cpu             = each.value.cpu
  memory          = each.value.memory
  min_replicas    = each.value.min_replicas
  max_replicas    = each.value.max_replicas
  location        = each.value.location
  depends_on      = [module.infra]
}

output "app_urls" {
  value = {
    for env_key, app in module.app :
    env_key => app.container_app_url
  }
}
