resource "aws_dynamodb_table" "this" {
  #checkov:skip=CKV_AWS_28: "Ensure Dynamodb point in time recovery (backup) is enabled"
  #checkov:skip=CKV_AWS_119: "Ensure DynamoDB Tables are encrypted using a KMS Customer Managed CMK"
  count = local.create_dynamodb ? 1 : 0

  name         = local.full_deployment_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "resourceArn"
  range_key    = "service"

  attribute {
    name = "resourceArn"
    type = "S"
  }

  attribute {
    name = "service"
    type = "S"
  }

  ttl {
    attribute_name = "resourceTtl"
    enabled        = true
  }
}
