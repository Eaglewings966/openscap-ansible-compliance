# Automated SOC2 / CIS Compliance Pipeline

[![OpenSCAP](https://img.shields.io/badge/OpenSCAP-CIS_L1%2FL2-CC0000?style=for-the-badge)](https://www.open-scap.org/)
[![Ansible](https://img.shields.io/badge/Ansible-Auto--Remediation-EE0000?style=for-the-badge&logo=ansible&logoColor=white)](https://www.ansible.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD_Gate-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

An automated compliance pipeline that scans EC2 instances against CIS Level 1 and CIS Level 2 benchmarks using OpenSCAP, auto-remediates all fixable findings with Ansible, blocks CI/CD deployments when the compliance score drops below 85%, and publishes trends to a CloudWatch dashboard.

## Table of Contents

- [The Problem](#the-problem)
- [What This Pipeline Does](#what-this-pipeline-does)
- [Architecture Overview](#architecture-overview)
- [Pipeline Stages](#pipeline-stages)
- [Compliance Coverage](#compliance-coverage)
- [DevOps Toolchain](#devops-toolchain)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Deployment](#deployment)
- [Production Considerations](#production-considerations)
- [Key Lessons Learned](#key-lessons-learned)
- [Destroy Everything](#destroy-everything)
- [Author](#author)

---

## The Problem

Manual, infrequent compliance checks allow drift. This repository demonstrates an automated pipeline to detect and remediate CIS benchmark drift, prevent non-compliant deployments, and create auditor-friendly evidence.

---

## What This Pipeline Does

- Scans EC2 instances (Amazon Linux 2023, Ubuntu 22.04) using OpenSCAP against CIS Level 1 and Level 2.
- Extracts compliance scores and findings into JSON and HTML reports.
- Runs Ansible auto-remediation when score falls below the configured threshold.
- Pushes metrics to CloudWatch for dashboards and historical visibility.
- Acts as a CI/CD gate to block deployments when compliance is below threshold.

---

## Architecture Overview

Pipeline trigger: push / PR / scheduled run / manual run.

- IaC provisioning: Terraform
- Scan orchestration: Ansible playbooks and roles
- Metrics and gate logic: Python scripts with boto3
- CI/CD: GitHub Actions
- Monitoring: AWS CloudWatch Metrics and dashboards

---

## Pipeline Stages

| Stage | Tool(s) | Purpose |
| --- | --- | --- |
| IaC Scan | Checkov | Scan Terraform and Ansible for misconfigurations |
| Compliance Scan | OpenSCAP + Ansible | CIS Level 1 and Level 2 scan on target instances |
| Push Metrics | Python + boto3 | Publish compliance metrics to CloudWatch |
| Generate Report | Python | Build consolidated HTML compliance report |
| Compliance Gate | Python | Fail pipeline if threshold not met or critical findings exist |
| Deploy | GitHub Actions | Deploy only if the gate passes |

---

## Compliance Coverage

### Amazon Linux 2023

- SSH hardening
- Password policy enforcement
- Auditd rules and logging
- Sysctl/network hardening
- File permission checks
- Service hardening
- Security banners

### Ubuntu 22.04

- SSH hardening
- UFW firewall validation
- AppArmor status checks
- PAM password quality
- Auditd rules and logging
- AIDE file integrity initialization

---

## DevOps Toolchain

| Tool | Purpose |
| --- | --- |
| OpenSCAP | CIS Level 1 + Level 2 scanning |
| SCAP Security Guide | SCAP content and benchmark profiles |
| Ansible | Scan orchestration and remediation |
| Python + boto3 | Metrics export, gate evaluation, report generation |
| GitHub Actions | CI/CD pipeline automation |
| Terraform | Provisioning EC2, IAM, SNS, CloudWatch resources |
| AWS CloudWatch / SNS | Metrics, dashboards, alerts |

---

## Project Structure

```
openscap-ansible-compliance/
├── terraform/
├── ansible/
│   ├── inventory/
│   └── roles/
├── scripts/
├── .github/workflows/
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

---

## Prerequisites

- AWS CLI v2
- Terraform v1.5+
- Ansible 2.14+
- Python 3.11+
- boto3

Install dependencies:

```bash
pip3 install boto3
```

---

## Deployment

### Phase 1 — Provision EC2 Instances

```bash
cd terraform
terraform init
terraform apply --auto-approve
terraform output
```

### Phase 2 — Run Initial Compliance Scan

```bash
ansible-playbook ansible/scan.yml \
  -i ansible/inventory/aws_ec2.yml \
  --private-key compliance-key.pem \
  -u ec2-user \
  --ssh-extra-args="-o StrictHostKeyChecking=no"
```

### Phase 3 — Run Auto-Remediation

```bash
ansible-playbook ansible/remediate.yml \
  -i ansible/inventory/aws_ec2.yml \
  --private-key compliance-key.pem \
  -u ec2-user \
  --ssh-extra-args="-o StrictHostKeyChecking=no"
```

### Phase 4 — Run Post-Remediation Scan

```bash
ansible-playbook ansible/scan.yml \
  -i ansible/inventory/aws_ec2.yml \
  --private-key compliance-key.pem \
  -u ec2-user \
  -e "scan_phase=post_remediation"
```

### Phase 5 — Run Compliance Gate

```bash
python3 scripts/compliance-gate.py --threshold 85 --reports-dir reports --fail-on-critical
```

### Phase 6 — Push Metrics + Generate Report

```bash
python3 scripts/push-metrics.py --reports-dir reports
python3 scripts/generate-report.py --output reports/report.html
```

---

## Production Considerations

- Use AWS Systems Manager for large fleet discovery.
- Consider staged remediation to reduce risk.
- Publish reports to S3 + CloudFront for auditor access.
- Store long-term compliance history in searchable storage.
- Integrate SNS + PagerDuty for critical alerts.

---

## Key Lessons Learned

- OpenSCAP exit code 2 indicates findings, not failure.
- Validate `sshd_config` with `sshd -t` before restarting SSH.
- Fresh images often start with lower CIS Level 2 scores.
- Dynamic inventory requires `boto3` on the control machine.

---

## Destroy Everything

```bash
cd terraform
terraform destroy --auto-approve
rm -f compliance-key.pem
```

---

## Author

Emmanuel Ubani — Cloud & DevOps Engineer

GitHub: https://github.com/Eaglewings966
