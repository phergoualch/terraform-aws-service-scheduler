# Installation

## Requirements

* :simple-terraform: Terraform >= 1.5.0
* :simple-amazonaws: AWS Provider >= 5.32.0

## Usage

The module is published to Terraform Registry, you can find it [here](https://registry.terraform.io/modules/phergoualch/service-scheduler/aws).

To deploy it on your account, simply add the following code to your Terraform configuration:

``` tf
module "service_scheduler" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 2.0.0"

  enabled_services   =  ["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner", "aurora", "elasticache"]
  default_timezone   = "Europe/Paris"
  app_name           = "service-scheduler"
  execution_interval = 6
}
```

## Parameters

These are the parameters you can use to customize the scheduler:

* `enabled_services` (required): List of services to enable in the scheduler, possible values are `ec2`, `asg`, `ecs`, `rds`, `documentdb`, `lambda`, `apprunner`, `aurora`, `elasticache`. Enabling only the services you need will reduce the number of Lambda invocations and the cost of the scheduler. Default is all the services.
* `default_timezone` (required): Default timezone used to calculate the start and stop times, possible values can be found [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Default is `UTC`.
* `app_name` (required): Name of the application, used to prefix all the AWS resources created by the module.
* `execution_interval` (required): Interval between each execution of the state machine, in hours between 1 and 24. Default is `6`.
* `tags_prefix` (optional): Prefix used for the tags. Default is `scheduler`.
* `tags_mapping` (optional): Map of tags if you want to customize the tags used by the scheduler. Default is `{}`.
* `logs_retention_days` (optional): Number of days to retain the logs of the Lambda function. Default is `7`.
* `deploy_multiple_regions` (optional): If true, the IAM roles will be named with the region short name to allow deployment in multiple regions on the same account. Default is `false`.

## Multi regions deployment

If you want to deploy the scheduler in multiple regions on the same account, you can use the `deploy_multiple_regions` parameter. This will allow you to deploy the scheduler in multiple regions without any conflict.

The `deploy_multiple_regions` parameter is a boolean, if set to `true`, the IAM roles will be named with the region short name to allow deployment in multiple regions on the same account. (eg. `service-scheduler-list-resources-euw1` and `service-scheduler-list-resources-euw3`).

Here is an example of how to deploy the scheduler in `eu-west-1` and `eu-west-3`:

``` tf
module "service_scheduler_euw1" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 2.0.0"

  providers = {
    aws = aws.eu-west-1
  }

  enabled_services        =  ["ec2", "asg", "ecs"]
  default_timezone        = "UTC"
  app_name                = "service-scheduler"
  execution_interval      = 6
  deploy_multiple_regions = true
}

module "service_scheduler_euw3" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 2.0.0"

  providers = {
    aws = aws.eu-west-3
  }

  enabled_services        =  ["ec2", "asg", "ecs"]
  default_timezone        = "Europe/Paris"
  app_name                = "service-scheduler"
  execution_interval      = 6
  deploy_multiple_regions = true
}
```
