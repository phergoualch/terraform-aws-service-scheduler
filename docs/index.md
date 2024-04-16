---
hide:
  - navigation
---

# AWS Service Scheduler

The **AWS Service Scheduler** is an open-source project developed to help scheduling **AWS resources**. It is based on AWS Step Functions and Lambda, and can be deployed in any AWS account.

It's main feature is to start and stop resources on a schedule, mainly for finops purposes but can also be used for other use cases.

The key features are:

* :fontawesome-solid-play: **Easy to use:** The only thing to do is to add tags to your resources, the scheduler will do the rest.
* :fontawesome-solid-bolt: **Easy to deploy:** Deploy in minutes, simply add the module to your Terraform code.
* :material-wrench: **Customizable:** You want custom tags ? No problem, you can customize the tags used by the scheduler.
* :material-security: **Secure:** The scheduler will only be able to start and stop resources identified by the tags you specified.
* :fontawesome-solid-sack-dollar: **Cost-effective:** The scheduler is serverless, based on Step Functions and Lambda.
* :material-forum: **Open-source:** The code is available on GitHub, feel free to contribute !


## Usage
``` tf
module "service_scheduler" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 2.0.0"

  enabled_services   =  ["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner", "aurora", "elasticache"] #(1)!
  default_timezone   = "Europe/Paris" #(2)!
  app_name           = "service-scheduler" #(3)!
  execution_interval = 6 #(4)!
}
```

1. List of services to enable in the scheduler
2. Default timezone used to calculate the start and stop times
3. Name of the application, used to generate the resources names
4. Interval between each execution of the state machine

## Supported services

<div class="grid cards" markdown>

- **[EC2](usage/supported-services.md#ec2)**
- **[ECS](usage/supported-services.md#ecs)**
- **[Auto Scaling Groups](usage/supported-services.md#auto-scaling-groups)**
- **[RDS](usage/supported-services.md#rds)**
- **[DocumentDB](usage/supported-services.md#documentdb)**
- **[Lambda](usage/supported-services.md#lambda)**
- **[App Runner](usage/supported-services.md#app-runner)**
- **[Aurora](usage/supported-services.md#aurora)**
- **[ElastiCache (Redis)](usage/supported-services.md#elasticache-redis)**

</div>
