resource "aws_ssm_parameter" "param" {
  name        = var.name
  type        = var.type
  value       = var.value
  description = var.description
  tags        = var.tags
}
