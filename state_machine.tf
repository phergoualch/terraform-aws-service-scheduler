resource "aws_sfn_state_machine" "main" {
  for_each = toset(["start", "stop"])
  #checkov:skip=CKV_AWS_285: "Ensure State Machine has execution history logging enabled"
  #checkov:skip=CKV_AWS_284: "Ensure State Machine has X-Ray tracing enabled"
  name     = "${var.app_name}-${each.key}"
  role_arn = aws_iam_role.state_machine.arn

  definition = templatefile("${path.module}/templates/main.json", {
    action = each.key
    branches = jsonencode([
      for service in var.enabled_services : jsondecode(templatefile("${path.module}/templates/${each.key}/${service}.json", {
        list_resources_lambda_arn = aws_lambda_function.list_resources.arn,
        dynamodb_table_name       = local.create_dynamodb ? aws_dynamodb_table.this[0].name : null,
        }
      ))
    ])
  })
}

resource "aws_iam_role" "state_machine" {
  name = var.deploy_multiple_regions ? "${var.app_name}-state-machine-${local.region_short_name}" : "${var.app_name}-state-machine"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "states.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "state_machine_invoke_lambda" {
  name = "InvokeLambda"
  role = aws_iam_role.state_machine.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "lambda:InvokeFunction"
        ],
        Resource = aws_lambda_function.list_resources.arn,
      }
    ]
  })
}

resource "aws_iam_role_policy" "state_machine_dynamodb" {
  count = local.create_dynamodb ? 1 : 0
  name  = "DynamoDBAccess"
  role  = aws_iam_role.state_machine.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:UpdateItem",
          "dynamodb:PutItem",
          "dynamodb:GetItem"
        ]
        Resource = aws_dynamodb_table.this[0].arn,
      }
    ]
  })
}

data "aws_iam_policy_document" "state_machine_services" {
  # Describe statements (without condition)
  dynamic "statement" {
    for_each = {
      for service, permissions in local.state_machine_services_permissions :
      service => permissions.describe if contains(var.enabled_services, service) && try(length(permissions.describe) > 0, false)
    }

    content {
      effect    = "Allow"
      actions   = statement.value
      resources = ["*"]
    }
  }

  # Update statements (with condition)
  dynamic "statement" {
    for_each = {
      for service, permissions in local.state_machine_services_permissions :
      service => permissions.update if contains(var.enabled_services, service) && try(length(permissions.update) > 0, false)
    }

    content {
      effect    = "Allow"
      actions   = statement.value
      resources = ["*"]

      dynamic "condition" {
        for_each = var.schedule_without_tags ? ["StringNotEquals"] : ["StringEquals"]

        content {
          test     = condition.value
          variable = "aws:ResourceTag/${var.tags_prefix}:${var.tags_mapping["enabled"]}"
          values   = var.schedule_without_tags ? ["false"] : ["true"]
        }
      }
    }
  }
}

resource "aws_iam_role_policy" "state_machine_services" {
  name   = "ServicesAccess"
  role   = aws_iam_role.state_machine.name
  policy = data.aws_iam_policy_document.state_machine_services.json
}