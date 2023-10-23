resource "aws_sfn_state_machine" "main" {
  for_each = toset(["start", "stop"])
  #checkov:skip=CKV_AWS_285: "Ensure State Machine has execution history logging enabled"
  #checkov:skip=CKV_AWS_284: "Ensure State Machine has X-Ray tracing enabled"
  name     = "${var.app_name}-${each.key}"
  role_arn = aws_iam_role.state_machine.arn

  definition = templatefile("${path.module}/templates/main.tftpl", {
    branches = jsonencode([
      for service in var.enabled_services : jsondecode(templatefile("${path.module}/templates/${each.key}/${service}.tftpl", {
        list_resources_lambda_arn = aws_lambda_function.list_resources.arn,
        dynamodb_table_name       = local.create_dynamodb ? aws_dynamodb_table.this[0].name : null,
        }
      ))
    ])
  })
}

resource "aws_iam_role" "state_machine" {
  name = "${var.app_name}-state-machine"
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

  inline_policy {
    name = "InvokeLambda"
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

  dynamic "inline_policy" {
    for_each = local.create_dynamodb ? [1] : []
    content {
      name = "StoreDynamoDB"
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
  }

  dynamic "inline_policy" {
    for_each = contains(var.enabled_services, "ec2") ? [1] : []
    content {
      name = "EC2"
      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Action = [
              "ec2:StartInstances",
              "ec2:StopInstances"
            ],
            Effect   = "Allow",
            Resource = "*",
            Condition = {
              StringEquals = {
                "aws:ResourceTag/finops:enabled" = "true"
              }
            }
          }
        ]
      })
    }
  }

  dynamic "inline_policy" {
    for_each = contains(var.enabled_services, "ecs") ? [1] : []
    content {
      name = "ECS"
      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Effect   = "Allow",
            Action   = "ecs:DescribeServices",
            Resource = "*",
          },
          {
            Effect   = "Allow",
            Action   = "ecs:UpdateService",
            Resource = "*",
            Condition = {
              StringEquals = {
                "aws:ResourceTag/finops:enabled" = "true"
              }
            }
          }
        ]
      })
    }
  }

  dynamic "inline_policy" {
    for_each = contains(var.enabled_services, "asg") ? [1] : []
    content {
      name = "AutoScaling"
      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Effect   = "Allow",
            Action   = "autoscaling:DescribeAutoScalingGroups",
            Resource = "*",
          },
          {
            Effect   = "Allow",
            Action   = "autoscaling:UpdateAutoScalingGroup"
            Resource = "*",
            Condition = {
              StringEquals = {
                "aws:ResourceTag/finops:enabled" = "true"
              }
            }
          }
        ]
      })
    }
  }

  dynamic "inline_policy" {
    for_each = contains(var.enabled_services, "apprunner") ? [1] : []
    content {
      name = "AppRunner"
      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Effect = "Allow",
            Action = [
              "apprunner:PauseService",
              "apprunner:ResumeService"
            ],
            Resource = "*",
            Condition = {
              StringEquals = {
                "aws:ResourceTag/finops:enabled" = "true"
              }
            }
          }
        ]
      })
    }
  }

  dynamic "inline_policy" {
    for_each = contains(var.enabled_services, "rds") ? [1] : []
    content {
      name = "RDS"
      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Effect = "Allow",
            Action = [
              "rds:StartDBInstance",
              "rds:StopDBInstance",
              "rds:StopDBCluster",
              "rds:StartDBCluster"
            ],
            Resource = "*",
            Condition = {
              StringEquals = {
                "aws:ResourceTag/finops:enabled" = "true"
              }
            }
          }
        ]
      })
    }
  }

  dynamic "inline_policy" {
    for_each = contains(var.enabled_services, "documentdb") ? [1] : []
    content {
      name = "DocumentDB"
      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Effect = "Allow",
            Action = [
              "rds:StartDBCluster",
              "rds:StopDBCluster",
            ],
            Resource = "*",
            Condition = {
              StringEquals = {
                "aws:ResourceTag/finops:enabled" = "true"
              }
            }
          }
        ]
      })
    }
  }

  dynamic "inline_policy" {
    for_each = contains(var.enabled_services, "lambda") ? [1] : []
    content {
      name = "Lambda"
      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Effect = "Allow",
            Action = [
              "lambda:DeleteFunctionConcurrency",
              "lambda:PutFunctionConcurrency",
            ],
            Resource = "*",
            Condition = {
              StringEquals = {
                "aws:ResourceTag/finops:enabled" = "true"
              }
            }
          }
        ]
      })
    }
  }
}
