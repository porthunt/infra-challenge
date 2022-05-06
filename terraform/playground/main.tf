### AWS as default provider
provider "aws" {
  region  = var.aws_region
}

### Build the populate Lambda function
module "populate_lambda" {
  source            = "../modules/lambda"
  function_name     = "${var.username}-populate"
  zip_name          = "primer-api.zip"
  s3_bucket         = "primer-challenge-lambda-deployment"
  handler           = "app.populate_table"
  api_execution_arn = module.apigateway.api_execution_arn
  env_variables     = {"USERNAME": var.username}
}

### Build the transaction Lambda function
module "transaction_lambda" {
  source            = "../modules/lambda"
  function_name     = "${var.username}-transactions"
  zip_name          = "primer-api.zip"
  s3_bucket         = "primer-challenge-lambda-deployment"
  handler           = "app.transactions"
  api_execution_arn = module.apigateway.api_execution_arn
  env_variables     = {"USERNAME": var.username}
}

### Create the dynamodb table
module "dynamodb" {
  source        = "../modules/dynamodb"
  table_name    = "${var.username}-transaction-challenge"
  hash_key      = "transaction_id"
  billing_mode  = "PAY_PER_REQUEST"

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
      name               = "MerchantIndex"
      hash_key           = "merchant"
      projection_type    = "ALL"
    }
  ]

  tags = {
    "Service" = "primer-challenge"
  }
}

### Add the API gateway
module "apigateway" {
  source           = "../modules/apigateway"
  api_name         = "${var.username}-transaction-api"
  openapi_file     = "../../primer-api/openapi.json"
  template_vars    = {
    region = var.aws_region
    transactions_lambda_arn = module.transaction_lambda.invoke_arn
    populate_lambda_arn     = module.populate_lambda.invoke_arn
    lambda_timeout          = 3000
  }
}

### Add the Cognito User Pool
module "cognito" {
  source        = "../modules/cognito"
  pool_name     = "${var.username}-primer-challenge"
  client_name   = "${var.username}-primer-api"
  attributes    = [
    {
      name     = "role"
      type     = "String"
      mutable  = true
    }
  ]
}

### Add the SQS queue
module "sqs" {
  source        = "../modules/sqs"
  queue_name    = "${var.username}-primer-challenge-queue"
}


### Add S3 bucket to host lambda code
module "s3" {
  source        = "../modules/s3"
  bucket_name   = "primer-challenge-lambda-deployment-a32w0a"
  force_destroy = true
}
