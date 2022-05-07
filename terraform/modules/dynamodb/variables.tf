### DynamoDB variables
variable "table_name" {
  type        = string
  description = "Table name"
}

variable "hash_key" {
  type        = string
  description = "Hash (partition) key"
}

variable "range_key" {
  type        = string
  description = "Sort key"
  default     = null
}

variable "billing_mode" {
  type        = string
  default     = "PROVISIONED"
  description = "Billing mode that should be used (PROVISIONED/PAY_PER_REQUEST)"
}

variable "read_capacity" {
  type        = number
  default     = null
  description = "Number of read units. Must be set if PROVISIONED billing mode is set"
}

variable "write_capacity" {
  type        = number
  default     = null
  description = "Number of read units. Must be set if PROVISIONED billing mode is set"
}

variable "attributes" {
  type        = list(map(string))
  default     = []
  description = "List of all attributes that are used on hash/range keys or global/local indexes"
}

variable "global_secondary_indexes" {
  type        = list(any)
  default     = []
  description = "Global secondary indexes used to scan using other attributes"
}

variable "local_secondary_indexes" {
  type        = list(any)
  default     = []
  description = "Local secondary indexes used to scan using other attributes"
}

variable "tags" {
  type    = map(string)
  default = {}
}
