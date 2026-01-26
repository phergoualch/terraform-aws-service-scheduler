data "aws_region" "current" {}

locals {
  region            = data.aws_region.current.region
  region_short_name = format("%s%s%s", split("-", local.region)[0], substr(split("-", local.region)[1], 0, 1), split("-", local.region)[2])
}

data "aws_caller_identity" "current" {}

resource "aws_ssm_document" "manual" {
  name            = "${var.app_name}-manual"
  document_type   = "Automation"
  document_format = "JSON"

  content = jsonencode({
    "description" : "Manually invoke the service scheduler",
    "schemaVersion" : "0.3",
    "parameters" : {
      "tags" : {
        "type" : "String",
        "default" : "all",
        "description" : "The tags to select the resources, in a key=value format, default to all"
      },
      "services" : {
        "type" : "String",
        "default" : "all",
        "description" : "The services to execute the action on, default to all"
      },
      "delay" : {
        "type" : "String",
        "default" : "0",
        "description" : "The delay in minutes before starting the action"
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
          "input" : "{\"selectors\": [{\"tags\": \"{{ tags }}\", \"services\": \"{{ services }}\", \"delay\": {{ delay }} }]}",
          "stateMachineArn" : "arn:aws:states:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:stateMachine:${var.app_name}-{{ action }}"
        }
      }
    ]
  })
}
