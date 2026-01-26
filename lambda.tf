data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/src"
  output_path = "${path.module}/lambda/lambda.zip"
  excludes    = ["tests"]
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
  runtime          = "python3.14"
  timeout          = 60
  filename         = data.archive_file.lambda.output_path
  architectures    = ["arm64"]
  source_code_hash = data.archive_file.lambda.output_base64sha256

  environment {
    variables = {
      DEFAULT_TIMEZONE      = var.default_timezone
      EXECUTION_INTERVAL    = var.execution_interval
      TAGS_MAPPING          = jsonencode(var.tags_mapping)
      TAGS_PREFIX           = var.tags_prefix
      SCHEDULE_WITHOUT_TAGS = jsonencode(var.schedule_without_tags)
      DEFAULT_SCHEDULE      = jsonencode(var.default_schedule)
    }
  }

  logging_config {
    log_format            = "JSON"
    log_group             = aws_cloudwatch_log_group.list_resources.name
    system_log_level      = "WARN"
    application_log_level = "INFO"
  }
}

resource "aws_cloudwatch_log_group" "list_resources" {
  #checkov:skip=CKV_AWS_158: "Ensure that CloudWatch Log Group is encrypted by KMS"
  #checkov:skip=CKV_AWS_338: "Ensure CloudWatch log groups retains logs for at least 1 year"
  name              = "/aws/lambda/${var.app_name}-list-resources"
  retention_in_days = var.logs_retention_days
}

resource "aws_iam_role" "list_resources" {
  name = var.deploy_multiple_regions ? "${var.app_name}-list-resources-${local.region_short_name}" : "${var.app_name}-list-resources"
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
}

resource "aws_iam_role_policy" "list_resources_get_parameters" {
  name = "GetParameters"
  role = aws_iam_role.list_resources.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow",
        Action   = "ssm:GetParameter",
        Resource = "arn:aws:ssm:*:*:parameter/${var.app_name}/*",
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "list_resources_managed" {
  role       = aws_iam_role.list_resources.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "list_resources_services" {
  dynamic "statement" {
    for_each = {
      for service, permissions in local.list_resources_permissions :
      service => permissions if contains(var.enabled_services, service)
    }

    content {
      effect    = "Allow"
      actions   = statement.value
      resources = ["*"]
    }
  }
}

resource "aws_iam_role_policy" "list_resources_services" {
  name   = "ServicesAccess"
  role   = aws_iam_role.list_resources.name
  policy = data.aws_iam_policy_document.list_resources_services.json
}
