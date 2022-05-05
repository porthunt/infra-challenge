variable "pool_name" {
    type = string
    description = "The Cognito pool name"
}

variable "client_name" {
    type = string
    description = "Name of the client that will connect to the pool"
}

variable "attributes" {
    type = list(any)
    description = "List of attributes that users must have"
}

variable "tags" {
  type        = map(string)
  default     = {}
}
