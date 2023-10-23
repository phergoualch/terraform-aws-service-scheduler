# Service Scheduler Terraform module

The Service Scheduler is an open-source project developed to help scheduling resources on development and test environments to save money.

It is based on 2 services, Lambda and Step Function. The architecture is as follows:

![Architecture](https://raw.githubusercontent.com/phergoualch/terraform-aws-service-scheduler/main/docs/architecture.png)

An EventBridge rule starts every 6 hours (by default) 2 Step Functions state machines, one to start resources and one to stop them. These two state machines will invoke a Lambda for each supported service, which lists all the resources in the account and determines whether they should be started or stopped within the next 6 hours. If not, they are ignored; if they are, the exact timestamp is calculated and passed to a ParallelMap. The map will act as a for loop, with a Wait block waiting for the calculated timestamp. Once the time has arrived, the correct API call is made to start or stop the resource.

The states machines and IAM roles are generated dynamically depending on the enabled_services variable. The Lambda and Step Function will be authorized to make API calls on these enabled services only. 

> [!NOTE]
> This solution is able to start and stop resources only in the region where it’s deployed

## Usage

```hcl
module "service_scheduler" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 1.0.0"

  enabled_services   =  ["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner"] # List of services to enable in the scheduler
  default_timezone   = "Europe/Paris" # Default timezone used to calculate the start and stop times
  app_name           = "service-scheduler" # Name of the application, used to generate the resources names
  execution_interval = 6 # Interval between each execution of the state machine
}
```

## Tagging

To add a resource to the scheduler, multiple tags need to be added to the resource you want to schedule.

| Key                            | Description                                                                                                                           | Examples                                                                                                                      |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| finops:enabled                 | **Required**: Can be true or false, if not present or different than false, the resource will not be scheduled                        | `true` or `false`                                                                                                             |
| finops:active-days             | *Optional*: The days of the week that you want the scheduler to schedule this resource (Default to MON-SUN)                           | `MON-FRI` <br> `MON`  <br> `MON,WED,FRI` <br> `MON,WED-FRI,SUN`                                                               |
| finops:start-active-days       | *Optional*: The days of the week that you want the scheduler to start this resource (Overwrite active-days if both specified)         | Same as active-days                                                                                                           |
| finops:stop-active-days        | *Optional*: The days of the week that you want the scheduler to stop this resource (Overwrite active-days if both specified)          | Same as active-days                                                                                                           |
| finops:active-days-month       | *Optional*: The days of the month that you want the scheduler to schedule this resource (Default to 1-31)                             | `1-31` <br> `15`  <br> `1,7,14,21,28` <br> `1-6,14,17-25`                                                                     |
| finops:start-active-days-month | *Optional*: The days of the month that you want the scheduler to start this resource (Overwrite active-days-number if both specified) | Same as active-days-month                                                                                                     |
| finops:stop-active-days-month  | *Optional*: The days of the month that you want the scheduler to stop this resource (Overwrite active-days-number if both specified)  | Same as active-days-month                                                                                                     |
| finops:active-weeks            | *Optional*: The days of the week that you want the scheduler to schedule this resource (Default to 1-53)                              | `10-40` <br> `5`  <br> `10-20,30-40` <br> `5,30-50,53`                                                                        |
| finops:start-active-weeks      | *Optional*: The days of the week that you want the scheduler to start this resource (Overwrite active-weeks if both specified)        | Same as active-weeks                                                                                                          |
| finops:stop-active-weeks       | *Optional*: The days of the week that you want the scheduler to stop this resource (Overwrite active-weeks if both specified)         | Same as active-weeks                                                                                                          |
| finops:active-months           | *Optional*: The months of the year that you want the scheduler to schedule this resource (Default to JAN-DEC)                         | `APR-JUL` <br> `AUG`  <br> `JAN,APR,MAY,SEP` <br> `FEB-JUN,SEP-DEC`                                                           |
| finops:start-active-months     | *Optional*: The months of the year that you want the scheduler to start this resource (Overwrite active-months if both specified)     | Same as active-months                                                                                                         |
| finops:stop-active-months      | *Optional*: The months of the year that you want the scheduler to stop this resource (Overwrite active-months if both specified)      | Same as active-months                                                                                                         |
| finops:start-time              | *Optional*: The time of the day that you want to start your resource                                                                  | `18:00` <br> `07:48`                                                                                                          |
| finops:stop-time               | *Optional*: The time of the day that you want to stop your resource                                                                   | Same as start-time                                                                                                            |
| finops:timezone                | *Optional*: The timezone used to calculate the times. If not specified, the default timezone set in Terraform is used                 | `Europe/Paris` <br> `America/New_York` <br> [List of timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

## Supported Services

### EC2

You can tag individual EC2 instances to be scheduled with the scheduler, all data will be retained as the instances will be stopped and not terminated.

### Autoscaling Groups

The Autoscaling Groups can be programmed to shut down, with the scheduler setting the MinSize and MaxSize values to 0.0, thus terminating all instances of the ASG and losing all data.

The Scheduler is able to store the current Min and Max values in order to restore them at the next start-up event.

ASGs are not tagged the same way as other resources and don't inherit of provider default tags. They must be added explicitly on the resource.

```hcl
dynamic "tag" {
  for_each = var.scheduler_tags
  content {
    key                 = tag.key
    value               = tag.value
    propagate_at_launch = false
  }
}
```

### RDS and Aurora

Both RDS instances and Aurora Clusters can be scheduled, all data will be retained as the instances are only stopped.

### ECS

You can tag both ECS clusters and the services to be scheduled. If a cluster is tagged, all services dependent on it will be scheduled using the cluster's tags. You can overwrite a specific service in the tagging if required. In most cases, services will be tagged individually.

The scheduler is able to store the current DesiredTasks values in order to restore them at the next startup.

### DocumentDB

DocumentDB Clusters can be scheduled, all data will be retained as the instances are only stopped.

### Lambda

Lambda functions can be "scheduled"; when they are stopped, the scheduler sets the Concurrent Executions to 0 and remove it on startup. This is a specific use case and should be used with caution. Most of the time, adjusting your cron will have the same result.

### AppRunner

AppRunner can be scheduled, all data present in the container will be lost as the containers are stopped.

## Examples

1. Resources that must be active every day from Monday to Friday, from 8 to 18.

```hcl
tags = {
  "finops:enabled"     = true
  "finops:active-days" = "MON-FRI"
  "finops:start-time"  = "08:00"
  "finops:stop-time"   = "18:00"
}
```

2. Resources to be shut down every day at 19:30 if they have been started manually.

```hcl
tags = {
  "finops:enabled"     = true
  "finops:active-days" = "MON-SUN"
  "finops:stop-time"   = "19:30"
}
```

3. Resources to be shut down only at weekends

```hcl
tags = {
  "finops:enabled"           = true
  "finops:start-active-days" = "MON"
  "finops:start-time"        = "08:00"
  "finops:stop-active-days"  = "FRI"
  "finops:stop-time"         = "18:00"
}
```

4. Resources to be started and stopped on Mondays and Fridays in the New York time zone.

```hcl
tags = {
  "finops:enabled"     = true
  "finops:active-days" = "MON,FRI"
  "finops:start-time"  = "08:00"
  "finops:stop-time"   = "18:00"
  "finops:timezone"    = "America/New_York"
}
```

5. Resources to be started the 1st monday of the 10th week and stopped the 1st friday of the 20th week.

```hcl
tags = {
  "finops:enabled"            = true
  "finops:start-active-days"  = "MON"
  "finops:start-active-weeks" = "10"
  "finops:stop-active-days"   = "FRI"
  "finops:stop-active-weeks"  = "20"
  "finops:start-time"         = "08:00"
  "finops:stop-time"          = "18:00"
}
```

## Manual execution

You can manually start and stop resources on an account. To do this, an SSM automation document is deployed on each account and can be used to manually trigger the step function.

To perform the action, you need to go to the System Manager Document console, choose the Owned by you, select the service-scheduler-manual document and then click on Execute Automation. You will then be prompted to enter the parameters as explained below.

> [!NOTE]
> The service scheduler is account-specific, so if you want to manually start or stop multiple applications deployed on multiple accounts, you'll need to execute automation on each account.

### Parameters

**action**: `start` or `stop`

**selector**: `all` by default, can be used to select specific resources to start or stop. It is based on resource tags. It must be a comma-delimited string (key=value). The same key can be present several times.

*Example: environment=dev,application=test,application=test2*

**services**: `all` by default, can be used to select specific services to start or stop. It must be a comma-delimited string containing the short names of the services. 

*Example: asg,rds*

## Manual execution from the API

The scheduler can also be run manually from the AWS API, for example using aws cli :

```bash
aws stepfunctions start-execution \
--state-machine-arn arn:aws:states:<region>:<accountId>:stateMachine:service-scheduler-start \
--input "{\"action\": \"start\", \"services\":\"all\",\"selector\":\"all\"}"
```

## Authors
Module is maintained by [Pereg Hergoualc'h](https://github.com/phergoualch).

## License
GNU GPLv3 Licensed. See [LICENSE](https://github.com/phergoualch/terraform-aws-service-scheduler/blob/main/LICENSE) for full details.