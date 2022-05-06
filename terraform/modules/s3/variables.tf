variable "bucket_name" {
    type        = string
    description = "The bucket name"
}

variable "tags" {
  type        = map(string)
  default     = {}
}

variable "acl" {
    type        = string
    default     = "private"
    description = "ACL permission"
}