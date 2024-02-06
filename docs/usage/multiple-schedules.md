# Multiple Schedules

Enhance the flexibility of scheduling by incorporating multiple schedules for a single resource. This functionality proves beneficial when distinct schedules are required for various days of the week or specific time intervals.

To implement this, utilize an iterator appended to the scheduler tag, denoted by a numerical value.

!!! example
    ```
    scheduler:start-time:1
    scheduler:stop-time:1
    scheduler:active-days:1
    ```

The scheduler will evaluate each iterator, starting from none to the highest, seeking the first schedule that aligns with the current time.

If certain parameters are unspecified for a particular iterator, the scheduler defaults to the general values.

!!! example
    ```
    scheduler:start-time = "08:00"
    scheduler:stop-time = "18:00"
    scheduler:stop-time:1 = "20:00"
    scheduler:active-days:1 = "SAT-SUN"
    ```

    In this example, the resource will start at 08:00 and stop at 18:00 from Monday to Friday. It will stop at 20:00 on Saturday and Sunday.
    On Saturday and Sunday, the scheduler will use the schedule with the iterator `1` because it is the most specific schedule. The scheduler will use the default value for the start time because it is not defined for the iterator `1`.
