## Basic examples

1. Resources that must be active every day from Monday to Friday, from 8 to 18.

    ``` json
    {
        "scheduler:enabled"     = "true"
        "scheduler:active-days" = "MON-FRI"
        "scheduler:start-time"  = "08:00"
        "scheduler:stop-time"   = "18:00"
    }
    ```

2. Resources to be shut down every day at 19:30 if they have been started manually.

    ``` json
    {
        "scheduler:enabled"     = "true"
        "scheduler:stop-time"   = "19:30"
    }
    ```

3. Resources to be shut down only at weekends

    ``` json
    {
        "scheduler:enabled"           = "true"
        "scheduler:start-active-days" = "MON"
        "scheduler:start-time"        = "08:00"
        "scheduler:stop-active-days"  = "FRI"
        "scheduler:stop-time"         = "18:00"
    }
    ```

4. Resources to be started and stopped on Mondays and Fridays in the New York time zone.

    ``` json
    {
        "scheduler:enabled"     = "true"
        "scheduler:active-days" = "MON,FRI"
        "scheduler:start-time"  = "08:00"
        "scheduler:stop-time"   = "18:00"
        "scheduler:timezone"    = "America/New_York"
    }
    ```

## Advanced examples

1. Resources to be started and stopped at different times on weekdays and weekends.

    ``` json
    {
        "scheduler:enabled"        = "true"
        "scheduler:start-time"     = "08:00"
        "scheduler:stop-time"      = "18:00"
        "scheduler:active-days"    = "MON-FRI"
        "scheduler:start-time:1"   = "10:00"
        "scheduler:stop-time:1"    = "16:00"
        "scheduler:active-days:1"  = "SAT-SUN"
    }
    ```

2. Resources to be started and stopped from April to September, from 8 to 18. Ensure that RDS instances are stopped if restarted automatically.

    ``` json
    {
        "scheduler:enabled"              = "true"
        "scheduler:start-time"           = "08:00"
        "scheduler:stop-time"            = "18:00"
        "scheduler:start-active-months"  = "APR-SEP"
        "scheduler:stop-active-months"   = "JAN-DEC"
    }
    ```
