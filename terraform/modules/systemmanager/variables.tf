variable "name" {
  type        = string
  description = "The name for the system parameter"
}

variable "type" {
  type        = string
  description = "The type for the parameter"
  default     = "SecureString"
}

variable "value" {
  type        = string
  description = "The parameter that should be stored"
}

variable "description" {
  type        = string
  description = "A description for the item that is being stored"
  default     = null
}

variable "tags" {
  type    = map(string)
  default = {}
}
