resource "aws_iam_role" "lambda_role" {
  name = "${var.function_name}-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "${var.function_name}-policy"
  roles      = [aws_iam_role.lambda_role.id]
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "${var.function_name}-policy"
  description = "Permissions that are required for lambda"
  policy      = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:*"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "sqs:*"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
POLICY
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 3
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "${var.function_name}-logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_lambda_permission" "lambda_permission" {
  count         = var.api_gateway_event ? 1 : 0
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*/*"
}

resource "aws_s3_bucket_object" "file_upload" {
  bucket = var.s3_bucket
  key    = var.s3_key
  source = var.source_path
}

resource "aws_lambda_function" "lambda" {
  function_name    = var.function_name
  s3_bucket        = var.s3_bucket
  s3_key           = var.zip_name
  handler          = var.handler
  runtime          = var.runtime
  timeout          = var.timeout
  role             = aws_iam_role.lambda_role.arn
  source_code_hash = var.source_code_hash
  environment {
    variables = var.env_variables
  }
  depends_on = [
    aws_s3_bucket_object.file_upload,
  ]
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  depends_on                         = [aws_lambda_function.lambda]
  count                              = var.sqs_event ? 1 : 0
  event_source_arn                   = var.queue_arn
  enabled                            = true
  function_name                      = var.function_name
  batch_size                         = var.batch_size
  maximum_batching_window_in_seconds = var.maximum_batching_window_in_seconds
}
