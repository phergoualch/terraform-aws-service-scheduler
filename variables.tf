variable "default_timezone" {
  description = "The default timezone used by the lambda function"
  type        = string
  default     = "UTC"
}

variable "enabled_services" {
  description = "The list of services to enable"
  type        = list(string)
  default     = ["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner"]

  validation {
    condition     = !contains([for s in var.enabled_services : contains(["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner"], s)], false)
    error_message = "The list of enabled services must be a subset of [\"ec2\", \"asg\", \"ecs\", \"rds\", \"documentdb\", \"lambda\", \"apprunner\"]"
  }
}

variable "app_name" {
  description = "The name of the application"
  type        = string
  default     = "service-scheduler"
}

variable "execution_interval" {
  description = "The execution interval of the state machine in hours"
  type        = number
  default     = 6

  validation {
    condition     = var.execution_interval >= 1 && var.execution_interval <= 24
    error_message = "The execution interval must be between 1 and 24 hours"
  }
}
