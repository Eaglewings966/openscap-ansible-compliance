#!/bin/bash
# Run compliance pipeline from WSL
# Usage: wsl bash scripts/wsl-run.sh [scan|remediate|site|gate|metrics|report|all]

set -euo pipefail

# -------------------------------------------------------
# PATHS — translate Windows project root to WSL path
# -------------------------------------------------------
PROJECT_WIN="c:\Projects\openscap-ansible-compliance"
PROJECT_WSL="/mnt/c/Projects/openscap-ansible-compliance"
KEY_WIN="${PROJECT_WIN}\compliance-key.pem"
KEY_WSL="${PROJECT_WSL}/compliance-key.pem"
THRESHOLD=85

cd "${PROJECT_WSL}"

# -------------------------------------------------------
# INSTALL DEPENDENCIES (idempotent)
# -------------------------------------------------------
install_deps() {
  echo "==> Checking dependencies..."
  if ! command -v ansible-playbook &>/dev/null; then
    echo "Installing Ansible..."
    sudo apt-get update -qq
    sudo apt-get install -y python3-pip python3-boto3 openssh-client
    pip3 install --quiet ansible ansible-core boto3 botocore defusedxml
    ansible-galaxy collection install amazon.aws community.general --force-with-deps
  fi

  if ! pip3 show defusedxml &>/dev/null; then
    pip3 install --quiet defusedxml
  fi

  echo "==> Dependencies OK"
}

# -------------------------------------------------------
# FIX KEY PERMISSIONS (WSL needs 600, Windows NTFS ignores it)
# -------------------------------------------------------
setup_key() {
  echo "==> Setting up SSH key..."
  mkdir -p ~/.ssh
  cp "${KEY_WSL}" ~/.ssh/compliance-key.pem
  chmod 600 ~/.ssh/compliance-key.pem
  KEY="~/.ssh/compliance-key.pem"
  echo "==> Key ready at ~/.ssh/compliance-key.pem"
}

# -------------------------------------------------------
# ANSIBLE COMMON ARGS
# -------------------------------------------------------
ANSIBLE_ARGS="-i ansible/inventory/aws_ec2.yml \
  --private-key ~/.ssh/compliance-key.pem \
  --ssh-extra-args='-o StrictHostKeyChecking=no' \
  -v"

# -------------------------------------------------------
# COMMANDS
# -------------------------------------------------------
run_scan() {
  local phase="${1:-initial}"
  echo ""
  echo "================================================"
  echo "Running OpenSCAP Compliance Scan (phase: ${phase})"
  echo "================================================"
  mkdir -p reports
  ansible-playbook ansible/scan.yml \
    -i ansible/inventory/aws_ec2.yml \
    --private-key ~/.ssh/compliance-key.pem \
    --ssh-extra-args="-o StrictHostKeyChecking=no" \
    -e "scan_phase=${phase}" \
    -v
}

run_remediate() {
  echo ""
  echo "================================================"
  echo "Running CIS Auto-Remediation"
  echo "================================================"
  ansible-playbook ansible/remediate.yml \
    -i ansible/inventory/aws_ec2.yml \
    --private-key ~/.ssh/compliance-key.pem \
    --ssh-extra-args="-o StrictHostKeyChecking=no" \
    -v
}

run_gate() {
  echo ""
  echo "================================================"
  echo "Running Compliance Gate (threshold: ${THRESHOLD}%)"
  echo "================================================"
  python3 scripts/compliance-gate.py \
    --threshold "${THRESHOLD}" \
    --reports-dir reports \
    --profile cis-level2 \
    --fail-on-critical
}

run_metrics() {
  echo ""
  echo "================================================"
  echo "Pushing Metrics to CloudWatch"
  echo "================================================"
  python3 scripts/push-metrics.py \
    --reports-dir reports \
    --region us-east-1
}

run_report() {
  echo ""
  echo "================================================"
  echo "Generating HTML Report"
  echo "================================================"
  python3 scripts/generate-report.py \
    --reports-dir reports \
    --output reports/consolidated-report.html \
    --threshold "${THRESHOLD}"
  echo "Report: ${PROJECT_WSL}/reports/consolidated-report.html"
  echo "Open:   file:///mnt/c/Projects/openscap-ansible-compliance/reports/consolidated-report.html"
}

# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
COMMAND="${1:-all}"

install_deps
setup_key

export AWS_DEFAULT_REGION="us-east-1"

case "${COMMAND}" in
  scan)
    run_scan initial
    ;;
  remediate)
    run_remediate
    ;;
  post-scan)
    run_scan post_remediation
    ;;
  gate)
    run_gate
    ;;
  metrics)
    run_metrics
    ;;
  report)
    run_report
    ;;
  all)
    run_scan initial
    run_remediate
    run_scan post_remediation
    run_gate
    run_metrics
    run_report
    ;;
  *)
    echo "Usage: $0 [scan|remediate|post-scan|gate|metrics|report|all]"
    exit 1
    ;;
esac
