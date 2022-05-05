output "function" {
  value = aws_lambda_function.lambda
}

output "lambda_arn" {
  value = aws_lambda_function.lambda.arn
}

output "invoke_arn" {
  value = aws_lambda_function.lambda.invoke_arn
}
