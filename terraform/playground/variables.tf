variable "aws_region" {
  description = "[DO NOT CHANGE] Region where to deploy the infrastructure"
  default     = "eu-west-1"
}

variable "username" {
  description = "Your username. Note that every ressource you create must be prepended by your username"
}
