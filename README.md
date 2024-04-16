# AWS Service Scheduler Terraform module

> [!NOTE]
> Full documentation can be found here: [scheduler.pereg.cloud](https://scheduler.pereg.cloud/)

The Service Scheduler is an open-source project developed to help scheduling AWS resources, primarily for cost-saving purposes. It is designed to be deployed in multiple accounts and regions, and to be able to start and stop resources based on their tags.

It is based on 2 services, Lambda and Step Function. The architecture is as follows:

![Architecture](https://raw.githubusercontent.com/phergoualch/terraform-aws-service-scheduler/main/docs/img/diagram-background.png)


## Usage

```hcl
module "service_scheduler" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 2.0.0"

  enabled_services   =  ["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner", "aurora", "elasticache"]
  default_timezone   = "Europe/Paris"
  app_name           = "service-scheduler"
  execution_interval = 6
}
```

## Authors
Module is maintained by [Pereg Hergoualc'h](https://github.com/phergoualch).

## License
GNU GPLv3 Licensed. See [LICENSE](https://github.com/phergoualch/terraform-aws-service-scheduler/blob/main/LICENSE) for full details.
