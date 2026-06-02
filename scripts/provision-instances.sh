#!/bin/bash
# Provision EC2 compliance target instances via Terraform
# Run this before running Ansible

set -euo pipefail

echo "================================================"
echo "Provisioning Compliance Target Instances"
echo "================================================"

cd "$(dirname "$0")/../terraform"

terraform init -upgrade
terraform fmt
terraform validate
terraform plan -out=tfplan
terraform apply tfplan

echo ""
echo "Instances provisioned. Waiting for SSH to be available..."

AMAZON_IP=$(terraform output -raw amazon_linux_public_ip)
UBUNTU_IP=$(terraform output -raw ubuntu_public_ip)
KEY_PATH=$(terraform output -raw private_key_path)

echo "Amazon Linux 2023 IP: ${AMAZON_IP}"
echo "Ubuntu 22.04 IP:      ${UBUNTU_IP}"
echo "Key path:             ${KEY_PATH}"

# Wait for SSH — Amazon Linux uses ec2-user, Ubuntu uses ubuntu
declare -A INSTANCE_USERS
INSTANCE_USERS["${AMAZON_IP}"]="ec2-user"
INSTANCE_USERS["${UBUNTU_IP}"]="ubuntu"

for IP in "${AMAZON_IP}" "${UBUNTU_IP}"; do
  USER="${INSTANCE_USERS[$IP]}"
  echo ""
  echo "Waiting for SSH on ${IP} (user: ${USER})..."
  for i in $(seq 1 30); do
    if ssh -o StrictHostKeyChecking=no \
           -o ConnectTimeout=5 \
           -i "${KEY_PATH}" \
           "${USER}@${IP}" "echo connected" 2>/dev/null; then
      echo "  SSH ready on ${IP}"
      break
    fi
    echo "  Attempt ${i}/30 — waiting 10 seconds..."
    sleep 10
  done
done

echo ""
echo "================================================"
echo "Instances are ready for compliance scanning."
echo ""
echo "Run the compliance pipeline:"
echo "  ansible-playbook ansible/site.yml \\"
echo "    -i ansible/inventory/aws_ec2.yml \\"
echo "    --private-key ${KEY_PATH}"
echo "================================================"
