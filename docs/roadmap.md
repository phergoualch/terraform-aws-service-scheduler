---
hide:
  - navigation
---

## More supported services

### MQ

Add support for Amazon MQ brokers. The scheduler will be able to restart Amazon MQ brokers using the `ModifyBroker` API call.

### MemoryDB for Redis

Add support for MemoryDB for Redis clusters. The scheduler will be able to resize MemoryDB for Redis clusters using the `UpdateCluster` API call.

### RDS, Aurora and EC2 resizing

Add support for resizing RDS, Aurora and EC2 instances. The scheduler will be able to resize RDS, Aurora and EC2 instances using the `ModifyDBInstance`, `ModifyDBCluster` and `ModifyInstance` API calls.

## CDK support

The scheduler currently only supports Terraform. It would be interesting to add support for other IaC tools such as CDK.
Having the CDK support would allow to deploy the scheduler in an organization as CloudFormation StackSets.

## Google Cloud Platform support

All features could be ported to Google Cloud Platform. The GCP services could be used with the same logic as AWS

* Cloud Functions in replacement of Lambda
* Cloud Workflows in replacement of Step Functions
