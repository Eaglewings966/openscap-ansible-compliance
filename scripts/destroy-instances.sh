#!/bin/bash
# Destroy all resources created by this project
# Run this after collecting screenshots

set -euo pipefail

echo "================================================"
echo "Destroying All Compliance Infrastructure"
echo "================================================"
echo ""
echo "This will destroy:"
echo "  - Amazon Linux 2023 EC2 instance"
echo "  - Ubuntu 22.04 EC2 instance"
echo "  - EC2 key pair"
echo "  - Security group"
echo "  - IAM role and instance profile"
echo "  - SNS topic and subscription"
echo "  - CloudWatch dashboard and alarm"
echo ""
read -r -p "Are you sure? Type 'yes' to confirm: " CONFIRM

if [ "${CONFIRM}" != "yes" ]; then
  echo "Destroy cancelled."
  exit 0
fi

cd "$(dirname "$0")/../terraform"
terraform destroy --auto-approve

# Remove local key file
KEY_FILE="$(dirname "$0")/../compliance-key.pem"
if [ -f "${KEY_FILE}" ]; then
  rm -f "${KEY_FILE}"
  echo "Removed local key file: ${KEY_FILE}"
fi

# Verify
echo ""
echo "Verifying cleanup..."
REGION="${AWS_REGION:-us-east-1}"
aws ec2 describe-instances \
  --filters "Name=tag:Project,Values=compliance" \
            "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].InstanceId' \
  --output text \
  --region "${REGION}" || true

echo ""
echo "================================================"
echo "Destroy complete."
echo "Verify in the AWS console that all resources are gone."
echo "================================================"
