resource "aws_cloudwatch_event_rule" "this" {
  name                = local.full_deployment_name
  description         = "Trigger ${local.full_deployment_name} state machines"
  schedule_expression = "rate(${var.execution_interval} hours)"
}

resource "aws_cloudwatch_event_target" "main" {
  for_each  = toset(["start", "stop"])
  target_id = aws_sfn_state_machine.main[each.key].name
  rule      = aws_cloudwatch_event_rule.this.name
  arn       = aws_sfn_state_machine.main[each.key].arn
  role_arn  = aws_iam_role.eventbridge.arn
  input = jsonencode({
    "action" = each.key
  })
}

resource "aws_iam_role" "eventbridge" {
  name = "${local.full_deployment_name}-eventbridge"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "StepFunctions"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "states:StartExecution",
          ]
          Effect   = "Allow"
          Resource = [for state_machine in aws_sfn_state_machine.main : state_machine.arn]
        },
      ]
    })
  }
}
