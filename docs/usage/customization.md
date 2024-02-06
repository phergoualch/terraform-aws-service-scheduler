# Customization

You can customize the scheduler in multiple ways :

* Deploy only for specific services
* Change the default timezone
* Change the resources names prefix
* Change the tags prefix
* Change the tags prefix

## Custom tags

The scheduler uses tags to identify the resources to start and stop. You can customize the tags used by the scheduler by using the `tags_mapping` parameter in the module.

You can also use the `tags_prefix` parameter to change the prefix used for the tags.

``` tf
module "service_scheduler" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 2.0.0"

  ...

  tags_mapping = {
    active-days = "days",
  }

  tags_prefix = "my-scheduler"
}
```

Using the above example, the scheduler will use the `start-days` and `stop-days` tags instead of the default `start-active-days` and `stop-active-days` tags. The prefix used for the tags will be `my-scheduler` instead of the default `scheduler`.
So the tags will be `my-scheduler:start-days` and `my-scheduler:stop-days` instead of `scheduler:start-active-days` and `scheduler:stop-active-days`.

## Resouces names

The scheduler uses the `app_name` parameter to prefix all the AWS resources created by the module. You can change the prefix used for the resources names by using the `app_name` parameter in the module.

``` tf
module "service_scheduler" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 2.0.0"

  ...

  app_name = "my-scheduler"
}
```

Using the above example, the resources names will be prefixed with `my-scheduler` instead of the default `service-scheduler`.
