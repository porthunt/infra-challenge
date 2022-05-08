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

variable "api_key_name" {
  type        = string
  description = "The API Key name"
}

variable "api_key_value" {
  type        = string
  description = "The API Key value"
  default     = null
}

variable "usage_plan" {
  type        = bool
  description = "If a usage plan must be created"
  default     = true
}

variable "usage_plan_name" {
  type        = string
  description = "Name of the usage plan"
}

variable "quota_settings_data" {
  type        = map(any)
  description = "The quota setting attributes"
  default = {
    limit : 100
    offset : 2
    period : "WEEK"
  }
}

variable "throttle_settings_data" {
  type        = map(any)
  description = "The throttle setting attributes"
  default = {
    burst_limit : 5
    rate_limit : 10
  }
}
