<div align="center">

# Automated SOC2/CIS Compliance Pipeline

[![OpenSCAP](https://img.shields.io/badge/OpenSCAP-CIS_L1%2FL2-CC0000?style=for-the-badge)](https://www.open-scap.org/)
[![Ansible](https://img.shields.io/badge/Ansible-Auto--Remediation-EE0000?style=for-the-badge&logo=ansible&logoColor=white)](https://www.ansible.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD_Gate-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

> **An automated compliance pipeline that scans EC2 instances against CIS Level 1 and CIS Level 2 benchmarks using OpenSCAP, auto-remediates fixable findings with Ansible, blocks CI/CD deployments when the compliance score drops below 85%, and publishes trends to a CloudWatch dashboard.**

[📖 Full Technical Article](https://emmanuelubani.hashnode.dev) • [📖 Human Story on Medium](https://medium.com/@emmaubani966) • [💼 LinkedIn](https://linkedin.com/in/ubaniemmanuel) • [🐙 GitHub](https://github.com/Eaglewings966) • [🌐 Portfolio](https://ops-run.lovable.app)

</div>

---

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

In 2022, a fintech startup in Berlin failed their SOC2 Type II audit after an auditor discovered that 34 of their 41 EC2 instances had root login enabled over SSH, no audit logging configured, and world-writable files in production directories. The findings were not the result of an attack. They were the result of nobody ever checking.

The compliance team spent four months manually remediating instances one by one. The audit delay cost them a $3.2 million enterprise contract that went to a competitor who could show a clean compliance report immediately.

Compliance is not a one-time event. It is an ongoing state that must be continuously monitored and maintained. Every new instance provisioned, every OS update applied, every configuration change made can introduce compliance drift. Manual audits catch drift weeks or months after it happens. This pipeline catches it within hours and remediates it automatically.

---

## What This Pipeline Does

- Scans EC2 instances (Amazon Linux 2023 and Ubuntu 22.04) using OpenSCAP against CIS Level 1 and Level 2.
- Extracts compliance scores and findings into HTML and JSON reports.
- Runs Ansible auto-remediation when the overall score falls below the configured threshold.
- Pushes compliance metrics to AWS CloudWatch for dashboards and historical visibility.
- Evaluates a compliance gate in CI/CD and blocks deployments when the score is below threshold.
- Generates auditor-friendly evidence for continuous compliance.

---

## Architecture Overview

Pipeline trigger: push / pull request / scheduled run / manual run.

- Infrastructure provisioning: Terraform
- Scan orchestration: Ansible playbooks and roles
- Metrics and gate logic: Python scripts with boto3
- CI/CD: GitHub Actions
- Monitoring: AWS CloudWatch Metrics and dashboards

---

## Pipeline Stages

| Stage | Tool(s) | Purpose |
| --- | --- | --- |
| IaC Scan | Checkov | Scan Terraform and Ansible for misconfigurations |
| Compliance Scan | OpenSCAP + Ansible | Run CIS Level 1 and Level 2 scans on target EC2 instances |
| Auto Remediation | Ansible | Apply fixable CIS controls automatically |
| Generate Report | Python | Consolidate scan results into HTML and JSON |
| Push Metrics | Python + boto3 | Publish compliance score and severity counts to CloudWatch |
| Compliance Gate | Python | Fail pipeline if score is below threshold or critical findings exist |
| Deploy | GitHub Actions | Continue only when the gate passes |

---

## Compliance Coverage

### Amazon Linux 2023

- SSH hardening and cipher configuration
- Password policy enforcement and PAM settings
- Auditd rules for process, login, and privilege escalation auditing
- Sysctl and network hardening
- File permission and ownership checks
- Service hardening for unnecessary daemons
- Security banners and login notices

### Ubuntu 22.04

- SSH hardening and secure authentication settings
- UFW firewall validation and policy checks
- AppArmor status and profile validation
- PAM password quality enforcement
- Auditd rule validation and logging verification
- AIDE file integrity monitoring initialization

---

## DevOps Toolchain

| Tool | Purpose |
| --- | --- |
| OpenSCAP | CIS Level 1 and Level 2 scanning |
| SCAP Security Guide | Provides benchmark profiles for supported OS versions |
| Ansible | Orchestrates scans and remediation |
| Python + boto3 | Publishes metrics, evaluates thresholds, generates reports |
| GitHub Actions | Automates pipeline execution and compliance gating |
| Terraform | Provisions EC2, IAM, SNS, CloudWatch, and supporting AWS resources |
| CloudWatch / SNS | Stores metrics, dashboards, and alerts |

---

## Project Structure

```
openscap-ansible-compliance/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── versions.tf
├── ansible/
│   ├── inventory/
│   │   ├── aws_ec2.yml
│   │   └── hosts.ini
│   ├── roles/
│   │   ├── cis-hardening/
│   │   ├── cis-remediation/
│   │   └── openscap-scan/
│   ├── scan.yml
│   ├── remediate.yml
│   └── site.yml
├── scripts/
│   ├── compliance-gate.py
│   ├── generate-report.py
│   ├── push-metrics.py
│   ├── provision-instances.sh
│   └── destroy-instances.sh
├── reports/
│   ├── consolidated-report.html
│   ├── amazon-linux/
│   └── ubuntu/
├── .github/workflows/
│   └── compliance-pipeline.yml
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

Install Python dependencies:

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

- Use AWS Systems Manager for large fleet discovery and inventory.
- Consider staged remediation to reduce blast radius.
- Publish reports to S3 and CloudFront for auditor access.
- Store long-term compliance history in searchable storage.
- Integrate SNS, Slack, or PagerDuty for critical alerts.

---

## Key Lessons Learned

- OpenSCAP exit code 2 indicates findings, not failure.
- Validate `sshd_config` with `sshd -t` before restarting SSH.
- Fresh AMIs often start with lower CIS Level 2 scores.
- Dynamic inventory requires `boto3` on the control machine.
- Compliance gates are only as strong as the configured thresholds and severity mappings.

---

## Destroy Everything

```bash
cd terraform
terraform destroy --auto-approve
rm -f compliance-key.pem
```

> Verify in AWS console: EC2 instances, key pair, security group, IAM role, SNS topic, CloudWatch dashboard, and alarm are all removed.

---

## Author

<div align="center">
**Emmanuel Ubani**  
Cloud and DevOps Engineer — Lagos, Nigeria

*From zoo volunteer to Cloud and DevOps Engineer.*  
*Building production-grade infrastructure in public.*

[LinkedIn](https://linkedin.com/in/ubaniemmanuel) • [GitHub](https://github.com/Eaglewings966) • [Hashnode](https://emmanuelubani.hashnode.dev) • [Medium](https://medium.com/@emmaubani966) • [Docker Hub](https://hub.docker.com/u/eaglewings6) • [Portfolio](https://ops-run.lovable.app)

### Featured Repositories

1. [AWS IAM Multi-Account Setup](https://github.com/Eaglewings966/aws-iam-multi-account-setup)
2. [GitHub Actions CI/CD Pipeline](https://github.com/Eaglewings966/github-actions-cicd-pipeline)
3. [Kubernetes EKS Deployment](https://github.com/Eaglewings966/eks-kubernetes-deployment)
4. [GitOps Platform with Argo CD](https://github.com/Eaglewings966/argocd-gitops-platform)
5. [AWS Cost Optimization Engine](https://github.com/Eaglewings966/aws-cost-optimization)
6. [AWS Multi-Account Landing Zone](https://github.com/Eaglewings966/aws-multi-account-landing-zone)
7. [Enterprise DevSecOps Pipeline](https://github.com/Eaglewings966/aws-devsecops-pipeline)
8. [HashiCorp Vault HA Cluster](https://github.com/Eaglewings966/hashicorp-vault-eks)
9. [Container Image Supply Chain](https://github.com/Eaglewings966/cosign-image-supply-chain)
10. [Zero-Trust Kubernetes Platform](https://github.com/Eaglewings966/istio-zero-trust-eks)
11. [Automated Compliance Pipeline](https://github.com/Eaglewings966/openscap-ansible-compliance)

</div>
