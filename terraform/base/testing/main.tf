
variable "app_name" {
  description = "The name of the application"
  type        = string
  default     = "fastapidemo"
}

variable "environments" {
  description = "List of environment configurations with all required values"
  type = list(object({
    environment = string
    location    = string
  }))
  default = [
    {
      environment = "testing"
      location    = "northeurope"
    }
  ]
}
module "base" {
  for_each        = { for env in var.environments : env.environment => env }
  source          = "../module_base"
  SUBSCRIPTION_ID = var.SUBSCRIPTION_ID
  location        = each.value.location
  app_name        = var.app_name
  environment     = each.value.environment
}