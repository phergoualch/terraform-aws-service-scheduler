data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/src"
  output_path = "${path.module}/lambda/lambda.zip"
}

resource "aws_lambda_function" "list_resources" {
  #checkov:skip=CKV_AWS_115: "Ensure that AWS Lambda function is configured for function-level concurrent execution limit"
  #checkov:skip=CKV_AWS_173: "Check encryption settings for Lambda environmental variable"
  #checkov:skip=CKV_AWS_116: "Ensure that AWS Lambda function is configured for a Dead Letter Queue(DLQ)"
  #checkov:skip=CKV_AWS_117: "Ensure that AWS Lambda function is configured inside a VPC"
  #checkov:skip=CKV_AWS_50: "X-ray tracing is enabled for Lambda"
  #checkov:skip=CKV_AWS_272: "Ensure AWS Lambda function is configured to validate code-signing"
  function_name    = "${var.app_name}-list-resources"
  description      = "Used by the ${var.app_name} state machines to list all resources in the account"
  role             = aws_iam_role.list_resources.arn
  handler          = "handler.handler"
  runtime          = "python3.10"
  timeout          = 60
  filename         = data.archive_file.lambda.output_path
  architectures    = ["arm64"]
  source_code_hash = data.archive_file.lambda.output_base64sha256

  environment {
    variables = {
      DEFAULT_TIMEZONE   = var.default_timezone
      EXECUTION_INTERVAL = var.execution_interval
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.list_resources
  ]
}

resource "aws_cloudwatch_log_group" "list_resources" {
  #checkov:skip=CKV_AWS_158: "Ensure that CloudWatch Log Group is encrypted by KMS"
  #checkov:skip=CKV_AWS_338: "Ensure CloudWatch log groups retains logs for at least 1 year"
  name              = "/aws/lambda/${var.app_name}-list-resources"
  retention_in_days = 7
}

resource "aws_iam_role" "list_resources" {
  name = "${var.app_name}-list-resources"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  dynamic "inline_policy" {
    for_each = contains(var.enabled_services, "ec2") ? [1] : []
    content {
      name = "EC2"
      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Effect   = "Allow",
            Action   = "ec2:DescribeInstances"
            Resource = "*",
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
            Effect = "Allow",
            Action = [
              "ecs:List*",
              "ecs:Describe*",
            ],
            Resource = "*",
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
              "apprunner:ListServices",
              "apprunner:ListTagsForResource"
            ],
            Resource = "*",
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
              "rds:Describe*",
              "rds:ListTagsForResource",
            ],
            Resource = "*",
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
              "rds:Describe*",
              "rds:ListTagsForResource",
            ],
            Resource = "*",
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
            Effect   = "Allow",
            Action   = "lambda:List*",
            Resource = "*",
          }
        ]
      })
    }
  }

  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
}
