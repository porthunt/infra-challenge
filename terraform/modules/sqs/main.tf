resource "aws_sqs_queue" "sqs_queue" {
  name                       = var.queue_name
  delay_seconds              = var.delay_seconds
  max_message_size           = var.max_message_size
  message_retention_seconds  = var.message_retention_seconds
  receive_wait_time_seconds  = var.receive_wait_time_seconds
  visibility_timeout_seconds = var.visibility_timeout_seconds
  fifo_queue                 = var.fifo_queue
  tags                       = var.tags
  redrive_policy = jsonencode({
    "deadLetterTargetArn" = aws_sqs_queue.deadletter_queue.arn,
    "maxReceiveCount"     = var.receive_count
  })
}

resource "aws_sqs_queue" "deadletter_queue" {
  name                       = "${var.queue_name}-DLQ"
  message_retention_seconds  = var.message_retention_seconds
  visibility_timeout_seconds = var.visibility_timeout_seconds
}