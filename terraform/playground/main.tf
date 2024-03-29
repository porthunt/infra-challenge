terraform {
  cloud {
    organization = "infra-challenge"

    workspaces {
      name = "infra-demo"
    }
  }
}

### AWS as default provider
provider "aws" {
  region = var.aws_region
}

### Build the populate Lambda function
module "populate_lambda" {
  source            = "../modules/lambda"
  function_name     = "${var.username}-populate"
  zip_name          = "api.zip"
  s3_bucket         = module.s3.bucket_name
  handler           = "app.populate_table"
  api_execution_arn = module.apigateway.api_execution_arn
  source_path       = "../../api/api.zip"
  s3_key            = "api.zip"
  env_variables = {
    "USERNAME" : var.username,
    "TRANSACTION_TABLE" : module.dynamodb.table_name
  }
  source_code_hash  = base64sha256("./api.zip")
  api_gateway_event = true
}

## Build the transaction Lambda function
module "transaction_lambda" {
  source            = "../modules/lambda"
  function_name     = "${var.username}-transactions"
  zip_name          = "api.zip"
  s3_bucket         = module.s3.bucket_name
  handler           = "app.transactions"
  api_execution_arn = module.apigateway.api_execution_arn
  source_path       = "../../api/api.zip"
  s3_key            = "api.zip"
  env_variables = {
    "USERNAME" : var.username,
    "TRANSACTION_TABLE" : module.dynamodb.table_name
  }
  source_code_hash  = base64sha256("./api.zip")
  api_gateway_event = true
}

## Build the add transaction Lambda function
module "add_transaction_lambda" {
  source            = "../modules/lambda"
  function_name     = "${var.username}-add-transaction"
  zip_name          = "api.zip"
  s3_bucket         = module.s3.bucket_name
  handler           = "app.add_transaction"
  api_execution_arn = module.apigateway.api_execution_arn
  source_path       = "../../api/api.zip"
  s3_key            = "api.zip"
  env_variables = {
    "USERNAME" : var.username,
    "TRANSACTION_TABLE" : module.dynamodb.table_name,
    "TRANSACTION_DLQ" : module.sqs.dlq_name
  }
  source_code_hash = base64sha256("./api.zip")
  sqs_event        = true
  queue_arn        = module.sqs.sqs_arn
}

### Create the dynamodb table
module "dynamodb" {
  source       = "../modules/dynamodb"
  table_name   = "${var.username}-transaction-challenge"
  hash_key     = "transaction_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    {
      name = "transaction_id"
      type = "S"
    },
    {
      name = "merchant"
      type = "S"
    }
  ]

  global_secondary_indexes = [
    {
      name            = "MerchantIndex"
      hash_key        = "merchant"
      projection_type = "ALL"
    }
  ]

  tags = {
    "Service" = "primer-challenge"
  }
}

### Add the API gateway
module "apigateway" {
  source          = "../modules/apigateway"
  api_name        = "${var.username}-transaction-api"
  openapi_file    = "../../api/openapi.json"
  api_key_name    = "${var.username}-transaction-api-key"
  api_key_value   = var.api_key
  usage_plan_name = "${var.username}-transaction-api-usage-plan"
  template_vars = {
    region                  = var.aws_region
    transactions_lambda_arn = module.transaction_lambda.invoke_arn
    populate_lambda_arn     = module.populate_lambda.invoke_arn
    lambda_timeout          = 10000
  }
}

### Add the SQS queue
module "sqs" {
  source     = "../modules/sqs"
  queue_name = "${var.username}-infra-challenge-queue"
}


### Add S3 bucket to host lambda code
module "s3" {
  source        = "../modules/s3"
  bucket_name   = "infra-challenge-lambda-deployment-a32w0a"
  force_destroy = true
}

# Add API Key parameter to System Manager
# This resource will be used by the alternative
# API that was created using Serverless Framework
module "systemmanager" {
  source      = "../modules/systemmanager"
  name        = "infra-challenge-api-key"
  description = "API key for the API (Serverless Framework)"
  value       = "${var.api_key}2"
}
