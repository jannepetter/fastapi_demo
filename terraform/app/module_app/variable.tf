variable "subscription_id" {
  type      = string
  sensitive = true
}
variable "app_name" {
  type      = string
  sensitive = false
}

variable "environment" {
  type      = string
  sensitive = false
}

variable "cpu" {
  type      = number
  sensitive = false
}
variable "memory" {
  type      = string
  sensitive = false
}

variable "min_replicas" {
  type      = number
  sensitive = false
}

variable "max_replicas" {
  type      = number
  sensitive = false
}

variable "location" {
  type      = string
  sensitive = true
}

variable "PORT" {
  type      = number
  sensitive = true
}

variable "app_env" {
  type      = string
  sensitive = true
}

variable "redis_image" {
  type        = string
  description = "Docker image for Redis sidecar"
  default     = "redis:alpine"
}

variable "redis_cpu" {
  type        = number
  description = "CPU allocated to the Redis sidecar container"
  default     = 0.25
}

variable "redis_memory" {
  type        = string
  description = "Memory allocated to the Redis sidecar container"
  default     = "0.5Gi"
}
variable "cloudflare_tunnel_token" {
  type      = string
  sensitive = true
}
variable "redis_password" {
  type      = string
  sensitive = true
}