### APIGateway module

data "template_file" "openapi" {
  template = file(var.openapi_file)
  vars     = var.template_vars
}

resource "aws_api_gateway_rest_api" "api" {
  name = var.api_name
  body = data.template_file.openapi.rendered
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.api.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = var.stage
  depends_on    = [aws_cloudwatch_log_group.log]
}

resource "aws_cloudwatch_log_group" "log" {
  name              = "API-Gateway-Execution-Logs_${aws_api_gateway_rest_api.api.id}/${var.stage}"
  retention_in_days = var.log_retention
}
