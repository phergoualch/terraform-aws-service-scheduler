# Manual Execution

You can manually start and stop resources on an account. To do this, an SSM automation document is deployed on each account and can be used to manually trigger the step function.

To perform the action, you need to go to the System Manager Document console, choose the Owned by you, select the service-scheduler-manual document and then click on Execute Automation. You will then be prompted to enter the parameters as explained below.

> [!NOTE]
> The service scheduler is account-specific, so if you want to manually start or stop multiple applications deployed on multiple accounts, you'll need to execute automation on each account.

### Parameters

* **action**: `start` or `stop`

* **selectors**: List of selector item, each item consist of a tags, services and delay attributes.

    * **tags**: `all` by default, can be used to select specific resources to start or stop. It is based on resource tags. It must be a comma-delimited string (key=value). The same key can be present several times.

        *Example: environment=dev,application=test,application=test2*
        <br><br>

    * **services**: `all` by default, can be used to select specific services to start or stop. It must be a comma-delimited string containing the short names of the services.

        *Example: asg,rds*
        <br><br>

    * **delay**: `0` by default, can be used to delay the execution of one action to the next. It must be a number of seconds. Could be used to start a database before the application that depends on it. Or start an application before another one.

        *Example: 300* (5 minutes)

## Manual execution from the API

The scheduler can also be run manually from the AWS API, for example using aws cli :

```bash
aws stepfunctions start-execution \
--state-machine-arn arn:aws:states:<region>:<accountId>:stateMachine:service-scheduler-start \
--input "{\"selectors\": [{\"services\":\"all\",\"tags\":\"all\",\"delay\":0}]}"
```

You can submit multiple selectors in the input parameter to start or stop multiple resources or services with a delay between each action.

```bash
aws stepfunctions start-execution \
--state-machine-arn arn:aws:states:<region>:<accountId>:stateMachine:service-scheduler-start \
--input "{\"selectors\": [{\"services\":\"rds\",\"tags\":\"all\",\"delay\":0},{\"services\":\"ec2\",\"tags\":\"all\",\"delay\":30}]}"
```
