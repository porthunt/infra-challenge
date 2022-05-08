### APIGateway module

data "template_file" "openapi" {
  template = file(var.openapi_file)
  vars     = var.template_vars
}

resource "aws_api_gateway_rest_api" "api" {
  name = var.api_name
  body = data.template_file.openapi.rendered
}

resource "aws_api_gateway_api_key" "api_key" {
  name  = var.api_key_name
  value = var.api_key_value
}

resource "aws_api_gateway_usage_plan" "usage_plan" {
  count = var.usage_plan ? 1 : 0
  name  = var.usage_plan_name

  api_stages {
    api_id = aws_api_gateway_rest_api.api.id
    stage  = aws_api_gateway_stage.stage.stage_name
  }

  quota_settings {
    limit  = var.quota_settings_data.limit
    offset = var.quota_settings_data.offset
    period = var.quota_settings_data.period
  }

  throttle_settings {
    burst_limit = var.throttle_settings_data.burst_limit
    rate_limit  = var.throttle_settings_data.rate_limit
  }
}

resource "aws_api_gateway_usage_plan_key" "usage_plan_key" {
  count         = var.usage_plan ? 1 : 0
  key_id        = aws_api_gateway_api_key.api_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.usage_plan[0].id
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
