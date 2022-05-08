### Lambda variables
variable "function_name" {
  type        = string
  description = "name of the lambda function"
}

variable "s3_bucket" {
  type        = string
  description = "bucket where the lambda function's code is stored"
  default     = "infra-challenge-lambda"
}

variable "zip_name" {
  type        = string
  description = "name of the lambda function zip on s3"
}

variable "handler" {
  type        = string
  description = "function handler"
  default     = "lambda_handler"
}

variable "runtime" {
  type        = string
  description = "lambda runtime"
  default     = "python3.8"
}

variable "timeout" {
  type        = number
  description = "timeout in second for the lambda function"
  default     = 3
}

variable "source_code_hash" {
  type        = string
  description = "the source code hash"
  default     = null
}

variable "api_execution_arn" {
  type        = string
  description = "The API Gateway execution ARN"
}

variable "env_variables" {
  type        = map(string)
  description = "Environment variables that should be set on the lambda function"
  default     = {}
}

variable "source_path" {
  type        = string
  description = "Path for the zip file that must be uploaded to s3"
}

variable "s3_key" {
  type        = string
  description = "Key for the file on s3"
}

variable "sqs_event" {
  type        = bool
  description = "Wether an SQS event source mapping should be created for the function"
  default     = false
}

variable "queue_arn" {
  type        = string
  description = "The ARN for the SQS queue"
  default     = null
}

variable "batch_size" {
  type        = number
  description = "The amount of messages that a lambda will receive at once"
  default     = 10
}

variable "maximum_batching_window_in_seconds" {
  type        = string
  description = "Maximum amount in seconds to get messages before invoking function"
  default     = 60
}
