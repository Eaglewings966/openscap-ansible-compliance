output "amazon_linux_instance_id" {
  description = "Amazon Linux 2023 instance ID"
  value       = aws_instance.amazon_linux.id
}

output "amazon_linux_public_ip" {
  description = "Amazon Linux 2023 public IP"
  value       = aws_instance.amazon_linux.public_ip
}

output "ubuntu_instance_id" {
  description = "Ubuntu 22.04 instance ID"
  value       = aws_instance.ubuntu.id
}

output "ubuntu_public_ip" {
  description = "Ubuntu 22.04 public IP"
  value       = aws_instance.ubuntu.public_ip
}

output "private_key_path" {
  description = "Path to the SSH private key for Ansible"
  value       = "${path.module}/../compliance-key.pem"
}

output "sns_topic_arn" {
  description = "SNS topic ARN for compliance alerts"
  value       = aws_sns_topic.compliance_alerts.arn
}

output "cloudwatch_dashboard_url" {
  description = "CloudWatch compliance dashboard URL"
  value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${aws_cloudwatch_dashboard.compliance.dashboard_name}"
}

output "ansible_inventory_vars" {
  description = "Values needed for Ansible dynamic inventory"
  value = {
    amazon_linux_ip = aws_instance.amazon_linux.public_ip
    ubuntu_ip       = aws_instance.ubuntu.public_ip
    key_path        = "${path.module}/../compliance-key.pem"
  }
}
