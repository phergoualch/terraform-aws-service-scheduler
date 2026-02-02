resource "aws_cloudwatch_event_rule" "this" {
  name                = var.app_name
  description         = "Trigger ${var.app_name} state machines every ${var.execution_interval} ${var.execution_interval == 1 ? "hour" : "hours"}"
  schedule_expression = "rate(${var.execution_interval} ${var.execution_interval == 1 ? "hour" : "hours"})"
}

resource "aws_cloudwatch_event_target" "main" {
  for_each  = aws_sfn_state_machine.main
  target_id = each.value.name
  rule      = aws_cloudwatch_event_rule.this.name
  arn       = each.value.arn
  role_arn  = aws_iam_role.eventbridge.arn
}

resource "aws_iam_role" "eventbridge" {
  name = var.deploy_multiple_regions ? "${var.app_name}-eventbridge-${local.region_short_name}" : "${var.app_name}-eventbridge"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "eventbridge_stepfunctions" {
  name = "StepFunctions"
  role = aws_iam_role.eventbridge.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "states:StartExecution"
        Effect   = "Allow"
        Resource = [for state_machine in aws_sfn_state_machine.main : state_machine.arn]
      }
    ]
  })
}
