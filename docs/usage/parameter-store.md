# Parameter Store

If you need to centralize the configuration of the scheduler, you can use the parameter store to define the scheduler parameters. The scheduler will read the parameters from the parameter store and merge them with tags defined on the resources.

Using parameters can also be used for cases when the quota of tags per resource is reached (50 tags per resource).

You are free to name your parameter as you want, but the parameter should start with `/scheduler-scheduler/` by default. You can modify this prefix by changing the `app_name` Terraform variable when deploying the module.

!!! example
    ```
    /scheduler-scheduler/weekday-8-18
    /scheduler-scheduler/stop-weekend
    ```

The parameter should be a JSON object with the tag names as keys and the tag values as values.

!!! example
    ``` json
    {
        "start-time": "08:00",
        "stop-time": "18:00",
        "active-days": "MON-FRI"
    }
    ```
