locals {
  full_deployment_name = var.app_name
  create_dynamodb      = contains(var.enabled_services, "asg") || contains(var.enabled_services, "ecs")
}
