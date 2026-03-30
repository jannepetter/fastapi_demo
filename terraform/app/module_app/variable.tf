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
