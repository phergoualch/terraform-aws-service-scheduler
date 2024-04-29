The scheduler utilizes tags to identify resources for starting and stopping. Tags can be added via the AWS console, CLI, or any Infrastructure as Code (IaC) tool.

Each tag consists of three parts: the prefix, the action, and the optional iterator. The prefix identifies the tag as a scheduler tag, the action defines the operation, and the iterator allows for multiple schedules on the same resource.

!!! example
    ```
    scheduler:start-time
    scheduler:stop-time
    scheduler:active-days
    scheduler:active-days:1
    scheduler:stop-time:1
    ```

* The `prefix` part can be customized, for more information see the [Custom Tags](customization.md) section.
* For more information about the `iterator`, explore the [Multiple Schedules](multiple-schedules.md) section.

The following section describes different tags that can be added to a resource.

## Enabled

The `enabled` tag enables or disables the scheduler. Use `true` to enable and `false` to disable.

If no tag is defined, the scheduler will use `false` as the default value.

This tag plays a crucial role in the operation of the Step Functions state machine. When the enabled value is set to false, the state machine is unable to make any API calls on the associated resources. This restriction is enforced through an IAM policy condition, ensuring that the scheduler's actions align with the specified enablement status.

!!! example
    ```
    enabled = "true"
    enabled = "false"
    ```

## Time

The tags `start-time` and `stop-time` are used to define the start and stop times of the resources. The format is `HH:MM` (24h format).

These are the only required tags to use the scheduler as they have no default value.

!!! example
    ```
    start-time = "08:00"
    stop-time  = "18:00"
    ```

!!! note
    Use only one of the tags if needed, e.g., starting resources manually but stopping them automatically.

## Timezone

The `timezone` tag defines the timezone for calculating start and stop times.

If undefined, the scheduler defaults to `UTC`.

View available timezone values [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

!!! example
    ```
    timezone = "Europe/Paris"
    timezone = "America/New_York"
    ```

## Active Days

The tags `active-days`, `start-active-days` and `stop-active-days` are used to define the range of days when the resources should be scheduled. The format can support multiple values separated by a comma (`,`) and ranges separated by a dash (`-`).

If no tag is defined, the scheduler will use `MON-FRI` as the default value.

!!! example
    ```
    active-days = "MON-FRI"
    active-days = "MON,FRI,SUN"
    active-days = "THU,SUN-TUE"
    active-days = "MON-FRI,SUN-TUE"
    ```
If both `active-days` and `start-active-days`/`stop-active-days` are defined, the scheduler will use the least specific value. For example, if `active-days` is defined to `MON-FRI` and `start-active-days` is defined to `MON`, the scheduler will use `MON`.

This allows to define different values for the start and stop actions.

!!! example
    This will start the resources on Monday and stop them on Friday:
    ```
    start-active-days = "MON"
    stop-active-days = "FRI"
    ```

## Active Days of Month

The tags `active-days-of-month`, `start-active-days-of-month` and `stop-active-days-of-month` are used to define the range of days of the month when the resources should be scheduled. The format can support multiple values separated by a comma (`,`) and ranges separated by a dash (`-`).

If no tag is defined, the scheduler will use `1-31` as the default value.

!!! example
    ```
    active-days-of-month = "8"
    active-days-of-month = "1-31"
    active-days-of-month = "1,7,14,21,28"
    active-days-of-month = "1-15,20-31"
    ```

## Active Weeks

The tags `active-weeks`, `start-active-weeks` and `stop-active-weeks` are used to define the range of weeks when the resources should be scheduled. The format can support multiple values separated by a comma (`,`) and ranges separated by a dash (`-`).

If no tag is defined, the scheduler will use `1-53` as the default value.

!!! example
    ```
    active-weeks = "1"
    active-weeks = "1-53"
    active-weeks = "1,7,14,21,28"
    active-weeks = "1-15,20-53"
    ```

## Active Months

The tags `active-months`, `start-active-months` and `stop-active-months` are used to define the range of months when the resources should be scheduled. The format can support multiple values separated by a comma (`,`) and ranges separated by a dash (`-`).

If no tag is defined, the scheduler will use `1-12` as the default value.

!!! example
    ```
    active-months = "1"
    active-months = "1-12"
    active-months = "1,7,12"
    active-months = "1-6,8-12"
    ```

## Parameter

The tag `parameter` is used to to define scheduler parameters in a parameter store parameter instead of using tags. For more information, see the [Parameter Store](parameter-store.md) section.

!!! example
    ```
    parameter = "/scheduler/parameter"
    ```

## Node type

Some services, like ElastiCache, can't be stopped but can be resized. The scheduler can resize the cluster to a desired node type. The tags used to define the cluster node type are `scheduler:start-node-type` and `scheduler:stop-node-type`.

!!! example
    ```
    scheduler:start-node-type = "cache.t4g.medium"
    scheduler:stop-node-type = "cache.t4g.micro"
    ```
