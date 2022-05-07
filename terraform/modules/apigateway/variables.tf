### APIGateway variables
variable "api_name" {
  type        = string
  description = "Name of the REST API"
}

variable "openapi_file" {
  type        = string
  description = "Location of the openapi.json file"

  validation {
    condition     = can(regex("\\.json$", var.openapi_file))
    error_message = "The OpenAPI file must be a json."
  }
}

variable "template_vars" {
  type        = any
  description = "All the variables that should be replaced on the template"
}

variable "stage" {
  type        = string
  description = "The stage name"
  default     = "dev"
}

variable "log_retention" {
  type        = number
  description = "Cloudwatch API Gateway logs retention period"
  default     = 3
}
