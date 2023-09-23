output "state_machine_arns" {
  description = "The ARNs of the state machines"
  value = {
    for key, value in aws_sfn_state_machine.main : key => value.arn
  }
}

output "list_resources_lambda_arn" {
  description = "The ARN of the list resources lambda"
  value       = aws_lambda_function.list_resources.arn
}

output "ssm_document_arn" {
  description = "The arn of the SSM document"
  value       = aws_ssm_document.manual.arn
}

output "ssm_document_name" {
  description = "The name of the SSM document"
  value       = aws_ssm_document.manual.name
}

output "state_machine_role_arn" {
  description = "The ARN of the state machine role"
  value       = aws_iam_role.state_machine.arn
}

output "list_resources_lambda_role_arn" {
  description = "The ARN of the list resources lambda role"
  value       = aws_iam_role.list_resources.arn
}
