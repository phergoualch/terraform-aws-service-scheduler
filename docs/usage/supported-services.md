## EC2

Individual EC2 instances can be tagged for scheduling with the. During scheduling, instances will be stopped, retaining all data as they are not terminated.

## Autoscaling Groups

Autoscaling Groups can be programmed to shut down by configuring the MinSize and MaxSize values to 0.0 with the scheduler. This action terminates all instances within the ASG, resulting in data loss. To mitigate this, the scheduler stores the current Min and Max values in DynamoDB for restoration during the next startup event.

!!! note
    ASGs require explicit tagging, as they do not inherit provider default tags. Use the following HCL code to add tags:
    ``` hcl
    dynamic "tag" {
      for_each = var.scheduler_tags
      content {
        key                 = tag.key
        value               = tag.value
        propagate_at_launch = false
      }
    }
    ```

## RDS

RDS instances can be scheduled, ensuring data retention as instances are only stopped. However, be aware of the following limitations:

!!! warning
    RDS instances restart automatically after 7 days, this is a limitation of the service.

    Stopping an RDS for SQL Server DB instance in a multi-AZ deployment isn't supported.

    You can't stop a DB instance that has a read replica, or that is a read replica.

## Aurora

Aurora Clusters are supported by the scheduler, allowing for scheduled stops with data retention. Be mindful of the following restrictions:

!!! warning
    Aurora clusters restart automatically after 7 days, this is a limitation of the service.

    You can't stop and start a cluster that's part of an Aurora global database.

    You can't stop and start a cluster that has a cross-Region read replica.

    You can't stop and start a cluster that is part of a blue/green deployment.

    For a cluster that uses the Aurora parallel query feature, the minimum Aurora MySQL version is 2.09.0.

    You can't stop and start an Aurora Serverless v1 cluster.


## ECS

ECS services can be tagged for scheduling. When the scheduler initiates a stop, it automatically sets the Min, Max, and Desired tasks values to 0, effectively stopping all running tasks associated with the service.

## DocumentDB

DocumentDB clusters can be scheduled, retaining all data as instances are only stopped

## Lambda

Lambda functions can be scheduled for "stop" actions, where the scheduler sets the Concurrent Executions to 0. Exercise caution with this specific use case, as adjusting your cron may achieve similar results.

## AppRunner

AppRunner services can be scheduled.

## ElastiCache (Redis)

Elaticache clusters can't be stopped, but the scheduler can be used to resize the cluster nodes. The scheduler will resize the cluster to a desized node type.
The tags used to define the cluster node type are `scheduler:start-node-type` and `scheduler:stop-node-type`.

!!! warning
    The scheduler will not stop the cluster, but resize it to the desired node type.

    Memcached clusters are not supported.

    Redis in cluster mode enabled is not supported.

## Cloudwatch Alarms

Both metric and composite alarms can be scheduled. When the scheduler initiates a stop, it disables the alarm actions. The scheduler will re-enable the alarm actions when the service is started. This can be used in conjunction with scheduling a resource, to avoid unnecessary alarms during the scheduled downtime.

## SageMaker Endpoints

SageMaker Endpoints can be scheduled to scale to zero instances when stopped and scale back to the original instance count when started. The scheduler stores the current instance count in DynamoDB to restore it during startup.

!!! warning
    Multi-variant endpoints are supported but only the first production variant's instance count is managed.

    Serverless endpoints are not supported as they manage their own auto-scaling.

## SageMaker Notebook Instances

SageMaker Notebook Instances can be scheduled for automatic start and stop. When stopped, the ML compute instance is terminated while preserving the ML storage volume. The instance is fully restored when started.

!!! note
    The notebook instance must be in "InService" state to be stopped and "Stopped" state to be started.

    All data on the ML storage volume is preserved during stop/start cycles.

## Neptune

Neptune DB clusters can be scheduled for automatic start and stop. All data is retained as clusters are only stopped, not deleted.

!!! warning
    Neptune clusters restart automatically after 7 days, this is a limitation of the service.

    You cannot stop a cluster that is part of a global database.

    You cannot stop a cluster that has cross-region read replicas.

## Redshift

Redshift clusters can be scheduled for automatic pause and resume. When paused, the cluster is not billed for compute resources. A snapshot is automatically created when pausing.

!!! warning
    Resuming a cluster can take several minutes to complete.

    Node IP addresses may change after resuming from a paused state.

    You cannot pause clusters deployed in EC2-Classic.

    You cannot pause clusters with HSM (Hardware Security Module) enabled.

    You cannot pause clusters with automated snapshots disabled.
