variable "default_timezone" {
  description = "The default timezone used by the lambda function"
  type        = string
  default     = "UTC"
}

variable "enabled_services" {
  description = "The list of services to enable"
  type        = list(string)
  default     = ["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner", "aurora", "elasticache"]

  validation {
    condition     = !contains([for s in var.enabled_services : contains(["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner", "aurora", "elasticache"], s)], false)
    error_message = "The list of enabled services must be a subset of [\"ec2\", \"asg\", \"ecs\", \"rds\", \"documentdb\", \"lambda\", \"apprunner\", \"aurora\", \"elasticache\"]"
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

variable "logs_retention_days" {
  description = "The number of days to retain the lambda logs"
  type        = number
  default     = 7

  validation {
    condition     = var.logs_retention_days >= 1 && var.logs_retention_days <= 365
    error_message = "The logs retention days must be between 1 and 365 days"
  }
}

variable "tags_prefix" {
  description = "The prefix to use for the tags"
  type        = string
  default     = "scheduler"

  validation {
    condition     = strcontains(var.tags_prefix, ":") == false
    error_message = "The tags prefix cannot contain the character :"
  }
}

variable "tags_mapping" {
  description = "The mapping of tags used if custom tags are needed"
  type = object({
    enabled              = optional(string, "enabled")
    time                 = optional(string, "time")
    timezone             = optional(string, "timezone")
    active-days          = optional(string, "active-days")
    active-days-of-month = optional(string, "active-days-of-month")
    active-weeks         = optional(string, "active-weeks")
    active-months        = optional(string, "active-months")
    parameter            = optional(string, "parameter")
  })
  default = {}

  validation {
    condition     = !contains([for k in keys(var.tags_mapping) : strcontains(k, ":") == false], false)
    error_message = "The tags mapping cannot contain the character : in any of the keys."
  }
}

variable "deploy_multiple_regions" {
  description = "If true, the IAM roles will be named with the region short name to allow deployment in multiple regions"
  type        = bool
  default     = false
}
