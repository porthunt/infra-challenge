variable "bucket_name" {
    type        = string
    description = "The bucket name"
}

variable "tags" {
  type        = map(string)
  default     = {}
}

variable "force_destroy" {
    type        = bool
    default     = false
    description = "Allows to destroy a bucket that is not empty"
}

variable "acl" {
    type        = string
    default     = "private"
    description = "ACL permission"
}
