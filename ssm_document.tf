data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

resource "aws_ssm_document" "manual" {
  name            = "${var.app_name}-manual"
  document_type   = "Automation"
  document_format = "JSON"

  content = jsonencode({
    "description" : "Manually invoke the service scheduler",
    "schemaVersion" : "0.3",
    "parameters" : {
      "selector" : {
        "type" : "String",
        "default" : "all",
        "description" : "The tags to select the resources, in a key=value format, default to all"
      },
      "services" : {
        "type" : "String",
        "default" : "all",
        "description" : "The services to execute the action on, default to all"
      },
      "action" : {
        "type" : "String",
        "allowedValues" : [
          "start",
          "stop"
        ],
        "description" : "The action to execute, either start or stop"
      }
    },
    "mainSteps" : [
      {
        "name" : "InvokeStateMachine",
        "action" : "aws:executeStateMachine",
        "isEnd" : true,
        "inputs" : {
          "input" : "{\"selector\": \"{{ selector }}\", \"action\": \"{{ action }}\", \"services\": \"{{ services }}\"}",
          "stateMachineArn" : "arn:aws:states:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:stateMachine:${var.app_name}-{{ action }}"
        }
      }
    ]
  })
}
