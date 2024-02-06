---
hide:
  - navigation
---

## More supported services

### Redshift

Add support for Redshift clusters. The scheduler will be able to start and stop Redshift clusters using the `PauseCluster` and `ResumeCluster` API calls.

### SageMaker Notebooks

Add support for SageMaker Notebooks. The scheduler will be able to start and stop SageMaker Notebooks using the `StartNotebookInstance` and `StopNotebookInstance` API calls.

### Neptune

Add support for Neptune clusters. The scheduler will be able to start and stop Neptune clusters using the `StopDBCluster` and `StartDBCluster` API calls.

## Resizing support

The scheduler currently only allows to stop and start resources. Some AWS services do not support stopping and starting, but support resizing. The scheduler could be extended to support resizing of resources. This would be interesting for cost optimization purposes.

This feature would allow to resize the following services:
* Elaticache
* Amazon MQ
* MemoryDB for Redis

It would also allow to resize the following services that can currently be stopped and started:
* RDS
* DocumentDB
* Aurora

## More Infrastructure as Code support

The scheduler currently only supports Terraform. It would be interesting to add support for other IaC tools such as CloudFormation and CDK.
Having the CloudFormation support would allow to deploy the scheduler in an organization using StackSets.

## Google Cloud Platform support

All features could be ported to Google Cloud Platform. The GCP services could be used with the same logix as AWS
* Cloud Functions in replacement of Lambda
* Cloud Workflows in replacement of Step Functions
