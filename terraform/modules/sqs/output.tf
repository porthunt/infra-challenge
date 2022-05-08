output "sqs_arn" {
  value = aws_sqs_queue.sqs_queue.arn
}

output "dlq_sqs_arn" {
  value = aws_sqs_queue.deadletter_queue.arn
}

output "sqs_name" {
  value = aws_sqs_queue.sqs_queue.name
}

output "dlq_name" {
  value = aws_sqs_queue.deadletter_queue.name
}
