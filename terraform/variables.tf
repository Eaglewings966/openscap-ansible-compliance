variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix for all resources"
  type        = string
  default     = "compliance"
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "dev"
}

variable "owner" {
  description = "Owner tag"
  type        = string
  default     = "emmanuel-ubani"
}

variable "instance_type" {
  description = "EC2 instance type for compliance targets"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "EC2 key pair name for Ansible SSH access"
  type        = string
  default     = "compliance-key"
}

variable "alert_email" {
  description = "Email address for compliance alert notifications"
  type        = string
  default     = "devops-alerts@example.com"
}

variable "compliance_threshold" {
  description = "Minimum compliance score percentage to pass the CI/CD gate"
  type        = number
  default     = 85
}
