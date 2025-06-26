variable "app_name" {
  description = "The name of the application"
  type        = string
  default     = "fastapidemo"
}

variable "environments" {
  description = "List of environment configurations with all required values"
  type = list(object({
    environment  = string
    location     = string
    cpu          = number
    memory       = string
    min_replicas = number
    max_replicas = number
  }))
  default = [
    {
      environment  = "testing"
      location     = "northeurope"
      cpu          = 0.25
      memory       = "0.5Gi"
      min_replicas = 1
      max_replicas = 2
    }
  ]
}
module "infra" {
  for_each        = { for env in var.environments : env.environment => env }
  source          = "../module_infra"
  SUBSCRIPTION_ID = var.SUBSCRIPTION_ID
  location        = each.value.location
  app_name        = var.app_name
  environment     = each.value.environment
}

module "app" {
  for_each        = { for env in var.environments : env.environment => env }
  source          = "../module_app"
  SUBSCRIPTION_ID = var.SUBSCRIPTION_ID
  resource_group  = module.infra[each.key].resource_group
  app_name        = var.app_name
  environment     = each.value.environment
  cpu             = each.value.cpu
  memory          = each.value.memory
  min_replicas    = each.value.min_replicas
  max_replicas    = each.value.max_replicas
  depends_on      = [module.infra]
}

output "app_urls" {
  value = {
    for env_key, app in module.app :
    env_key => app.container_app_url
  }
}