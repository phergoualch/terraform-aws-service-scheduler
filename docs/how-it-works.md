---
hide:
  - navigation
---

# How it works

The AWS Service Scheduler is a serverless solution based on AWS Step Functions and Lambda. It is designed to start and stop resources on a schedule, mainly for finops purposes but can also be used for other scheduling needs.


<figure markdown>
  ![Architecture](./img/diagram-darkmode.png#only-dark){ width="600" }
  ![Architecture](./img/diagram-lightmode.png#only-light){ width="600" }
</figure>

An EventBridge rule starts every X hours (6 by default) two Step Functions state machines, one to start resources and one to stop them. These two state machines will invoke a Lambda for each supported service in parallel, which lists all the resources in the account and determines whether they should be started or stopped within the next X hours. If not, they are ignored; if they are, the exact timestamp is calculated and passed to a Parallel Map. The map will act as a for loop, with a Wait block waiting for the calculated timestamp. Once the time has arrived, the correct API call is made to start or stop the resource.

The states machines and IAM policies are generated dynamically depending on the enabled_services variable. The Lambda and Step Function will be authorized to make API calls on these enabled services only.
