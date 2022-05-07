variable "queue_name" {
  type        = string
  description = "The queue name"
}

variable "delay_seconds" {
  type    = number
  default = null
}

variable "max_message_size" {
  type    = number
  default = null
}

variable "message_retention_seconds" {
  type    = number
  default = null
}

variable "receive_wait_time_seconds" {
  type    = number
  default = null
}

variable "visibility_timeout_seconds" {
  type    = number
  default = null
}

variable "fifo_queue" {
  type    = bool
  default = false
}

variable "tags" {
  type    = map(string)
  default = {}
}
