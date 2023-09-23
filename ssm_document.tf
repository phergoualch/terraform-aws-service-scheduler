data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

resource "aws_ssm_document" "manual" {
  name            = "${local.full_deployment_name}-manual"
  document_type   = "Automation"
  document_format = "YAML"

  content = <<DOC
description: ''
schemaVersion: '0.3'
parameters:
  action:
     type: String
     allowedValues:
       - start
       - stop
     description: "The action to execute, either start or stop"
  selector:
    type: String
    default: "all"
    description: "The tags to select the resources, in a key=value format, default to all"
  services:
    type: String
    default: "all"
    description: "The services to execute the action on, default to all"
mainSteps:
 - name: InvokeStateMachine
   action: aws:executeStateMachine
   inputs:
     stateMachineArn: arn:aws:states:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:stateMachine:service-scheduler-{{ action }}
     input: '{"selector": "{{ selector }}", "action": "{{ action }}", "services": "{{ services }}"}'
DOC
}
