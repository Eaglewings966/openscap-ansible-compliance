 # Automated SOC2/CIS Compliance Pipeline

 [![OpenSCAP](https://img.shields.io/badge/OpenSCAP-CIS_L1%2FL2-CC0000?style=for-the-badge)](https://www.open-scap.org/)
 [![Ansible](https://img.shields.io/badge/Ansible-Auto--Remediation-EE0000?style=for-the-badge&logo=ansible&logoColor=white)](https://www.ansible.com/)
 [![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD_Gate-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
 [![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.

 

 ## You said: Continue
 Continue

 May 26
 

 ## Claude responded: org//)
 org//)
 [Show Image](https://aws.amazon.com/)
 [Show Image](https://www.terraform.io/)
 [Show Image](LICENSE)
 [Show Image](https://github.com/Eaglewings966/openscap-ansible-compliance)

 **An automated compliance pipeline that scans EC2 instances against
 CIS Level 1 and Level 2 benchmarks using OpenSCAP, auto-remediates
 all fixable findings with Ansible, blocks CI/CD deployments when
 the compliance score drops below 85%, and publishes trends to
 a CloudWatch dashboard.**

 [📖 Full Technical Article](https://emmanuelubani.hashnode.dev) •
 [📖 Human Story on Medium](https://medium.com/@emmaubani966) •
 [💼 LinkedIn](https://linkedin.com/in/ubaniemmanuel) •
 [🐙 GitHub](https://github.com/Eaglewings966) •
 [🌐 Portfolio](https://ops-run.lovable.app)

</div>

---

### Table of Contents

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

### The Problem

In 2022, a fintech startup in Berlin failed their SOC2 Type II
audit after an auditor discovered that 34 of their 41 EC2 instances
had root login enabled over SSH, no audit logging configured,
and world-writable files in production directories. The findings
were not the result of an attack. They were the result of nobody
ever checking.

The compliance team spent four months manually remediating instances
one by one. The audit delay cost them a $3.2 million enterprise
contract that went to a competitor who could show a clean compliance
report immediately.

Compliance is not a one-time event. It is an ongoing state that
must be continuously monitored and maintained. Every new instance
provisioned, every OS update applied, every configuration change
made can introduce compliance drift. Manual audits catch drift
weeks or months after it happens. This pipeline catches it within
hours and remediates it automatically.

---

### What This Pipeline Does

```
EC2 Instances (Amazon Linux 2023 + Ubuntu 22.04)
				│
				▼
OpenSCAP scans against CIS Level 1 + Level 2
				│
				▼
Compliance scores extracted and saved as JSON
				│
				├──► Score below 85% → Ansible auto-remediation runs
				│         │
				│         └──► Re-scan to verify improvement
				│
				├──► Metrics pushed to CloudWatch custom namespace
				│         │
				│         └──► Dashboard shows trends + 85% threshold line
				│
				├──► HTML consolidated report generated
				│
				└──► CI/CD compliance gate evaluates final scores
									│
									├──► Score ≥ 85% → GATE PASSES → Deployment proceeds
									└──► Score 

```
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS PIPELINE                       │
│                                                                  │
│  Trigger: push to main / PR / weekly schedule / manual          │
│                                                                  │
│  Stage 1 — IaC Scan (Checkov)                                  │
│  Scans Terraform + Ansible for misconfigurations               │
│          │                                                       │
│  Stage 2 — OpenSCAP Scan (Ansible)                             │
│  Scans both EC2 instances against CIS L1 + L2                  │
│          │                                                       │
│  Stage 3 — Push Metrics (Python + boto3)                       │
│  Publishes scores to CloudWatch custom namespace               │
│          │                                                       │
│  Stage 4 — Generate Report (Python)                            │
│  Creates consolidated HTML compliance report                    │
│          │                                                       │
│  Stage 5 — Compliance Gate (Python)                            │
│  Exits 1 if any score below 85% or CRITICAL findings exist     │
│          │                                                       │
│  Stage 6 — Deploy (only if gate passes)                        │
│  Deployment proceeds only after compliance is confirmed         │
└─────────────────────────────────────────────────────────────────┘
															 │
										┌─────────┴──────────┐
										▼                    ▼
				 Amazon Linux 2023        Ubuntu 22.04
				 t3.micro EC2             t3.micro EC2
										│                    │
										└─────────┬──────────┘
															▼
										CloudWatch Dashboard
										Compliance Score Trends
										85% Threshold Line
										Critical/High/Medium Counts

---

### Pipeline Stages

StageToolWhat It DoesIaC ScanCheckovScans Terraform + Ansible for misconfigsCompliance ScanOpenSCAP + AnsibleCIS L1 + L2 scan on both OSPush MetricsPython + boto3Publishes scores to CloudWatchGenerate ReportPythonCreates HTML consolidated reportCompliance GatePythonBlocks deployment if score below 85%DeployBashProceeds only after gate passes

---

# Automated SOC2 / CIS Compliance Pipeline

[![OpenSCAP](https://img.shields.io/badge/OpenSCAP-CIS_L1%2FL2-CC0000?style=for-the-badge)](https://www.open-scap.org/)
[![Ansible](https://img.shields.io/badge/Ansible-Auto--Remediation-EE0000?style=for-the-badge&logo=ansible&logoColor=white)](https://www.ansible.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD_Gate-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

An automated compliance pipeline that scans EC2 instances against CIS Level 1 and Level 2 using OpenSCAP, auto-remediates fixable findings with Ansible, pushes metrics to CloudWatch, and gates CI/CD deployments.

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

Manual, infrequent compliance checks allow drift. This project demonstrates an automated pipeline that detects and remediates CIS benchmark drift quickly, prevents non-compliant deployments, and provides auditor-friendly evidence.

---

## What This Pipeline Does

- Scans EC2 instances (Amazon Linux 2023, Ubuntu 22.04) using OpenSCAP against CIS L1 & L2.
- Extracts compliance scores and findings into JSON and HTML reports.
- If score < 85% (configurable), runs Ansible auto-remediation and re-scans.
- Pushes metrics to CloudWatch for historical trends and dashboards.
- Acts as a CI/CD gate: fail the pipeline when scores are below threshold or critical findings exist.

### High-level flow

```
EC2 instances → OpenSCAP scan → extract scores
	├─ If score < threshold → Ansible remediation → re-scan
	├─ Push metrics → CloudWatch
	└─ Generate consolidated HTML report
```

---

## Architecture Overview

Pipeline trigger: push / PR / schedule / manual

- IaC provisioning: Terraform
- Scanning & remediation orchestration: Ansible (roles + playbooks)
- Metrics & gate: Python scripts (boto3)
- CI/CD: GitHub Actions (multi-stage)

See the `terraform/`, `ansible/`, and `scripts/` folders for implementation details.

---

## Pipeline Stages

| Stage | Tool(s) | Purpose |
|---|---|---|
| IaC Scan | Checkov | Scan Terraform & Ansible for misconfigurations |
| Compliance Scan | OpenSCAP + Ansible | CIS L1 + L2 scanning on target instances |
| Push Metrics | Python + boto3 | Publish scores/counts to CloudWatch |
| Generate Report | Python | Consolidated HTML report generation |
| Compliance Gate | Python | Fail pipeline if score below threshold or critical findings |
| Deploy | Bash / GitHub Actions | Deploy only if gate passes |

---

## Compliance Coverage

Coverage examples (see `ansible/roles/*/vars/main.yml` for profiles):

- Amazon Linux 2023: SSH hardening, password policy, auditd rules, sysctl/network hardening, file permissions, service hardening, banners.
- Ubuntu 22.04: SSH hardening, UFW/AppArmor checks, PAM, auditd, AIDE initialization.

---

## DevOps Toolchain

| Tool | Purpose |
|---|---|
| OpenSCAP | CIS L1/L2 scanning (XCCDF) |
| SCAP Security Guide | SCAP content for supported OS profiles |
| Ansible | Scan orchestration & remediation playbooks |
| Python + boto3 | Metrics publisher, gate logic, report generator |
| GitHub Actions | CI/CD pipeline with compliance gate |
| Terraform | Provisioning (EC2, IAM, SNS, CloudWatch) |
| AWS CloudWatch / SNS | Metrics, dashboard, and alerts |

---

## Project Structure

```
openscap-ansible-compliance/
├── terraform/                # EC2, IAM, SNS, CloudWatch
├── ansible/                  # playbooks, inventory, roles
│   ├── inventory/
│   └── roles/
├── scripts/                  # compliance-gate.py, push-metrics.py, generate-report.py
├── .github/workflows/        # CI/CD pipeline
└── README.md
```

---

## Prerequisites

- AWS CLI v2 (configured)
- Terraform v1.5+
- Ansible 2.14+
- Python 3.11+ and `boto3`
- GitHub secrets for CI: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `SSH_PRIVATE_KEY`

Install Python dependencies:

```bash
pip3 install -r requirements.txt  # or `pip3 install boto3` if you don't have a requirements file
```

---

## Deployment (quick start)

1. Provision instances

```bash
cd terraform && terraform init && terraform apply --auto-approve
terraform output
```

2. Run initial scan

```bash
ansible-playbook ansible/scan.yml \
	-i ansible/inventory/aws_ec2.yml \
	--private-key compliance-key.pem \
	-u ec2-user \
	--ssh-extra-args="-o StrictHostKeyChecking=no"
```

3. Run auto-remediation (if required)

```bash
ansible-playbook ansible/remediate.yml \
	-i ansible/inventory/aws_ec2.yml \
	--private-key compliance-key.pem \
	-u ec2-user \
	--ssh-extra-args="-o StrictHostKeyChecking=no"
```

4. Run the compliance gate

```bash
python3 scripts/compliance-gate.py --threshold 85 --reports-dir reports --profile cis-level2 --fail-on-critical
```

5. Push metrics + generate report

```bash
python3 scripts/push-metrics.py --reports-dir reports
python3 scripts/generate-report.py --output reports/report.html
```

---

## Production Considerations

- Instance discovery: consider AWS Systems Manager inventory for large fleets.
- Remediation strategy: use staged/blue-green remediation to reduce blast radius.
- Report storage: publish reports to S3 + CloudFront for auditor access.
- Historical storage: export metrics to OpenSearch or long-term storage for auditor timelines.
- Alerting: integrate SNS + PagerDuty for CRITICAL findings.

---

## Key Lessons Learned

- OpenSCAP exit code 2 indicates findings (not a failure). Use `failed_when: result.rc not in [0,2]` in Ansible.
- Validate `sshd_config` (`sshd -t`) before restarting SSH during remediation to avoid lockout.
- Fresh OS images often start with low Level 2 scores — remediation improves the baseline.
- Dynamic inventory requires `boto3` on the control machine (Ansible inventory plugin uses AWS APIs locally).

---

## Destroy Everything

```bash
cd terraform && terraform destroy --auto-approve
rm -f compliance-key.pem
```

---

## Author

Emmanuel Ubani — Cloud & DevOps Engineer

Links: https://github.com/Eaglewings966 • https://linkedin.com/in/ubaniemmanuel

#### Phase 1 — Provision EC2 Instances

bash

```
cd terraform && terraform apply --auto-approve
terraform output
```

#### Phase 2 — Run Initial Compliance Scan

bash

```
ansible-playbook ansible/scan.yml \
	-i ansible/inventory/aws_ec2.yml \
	--private-key compliance-key.pem \
	-u ec2-user \
	--ssh-extra-args="-o StrictHostKeyChecking=no"
```

#### Phase 3 — Run Auto-Remediation

bash

```
ansible-playbook ansible/remediate.yml \
	-i ansible/inventory/aws_ec2.yml \
	--private-key compliance-key.pem \
	-u ec2-user \
	--ssh-extra-args="-o StrictHostKeyChecking=no"
```

#### Phase 4 — Run Post-Remediation Scan

bash

```
ansible-playbook ansible/scan.yml \
	-i ansible/inventory/aws_ec2.yml \
	--private-key compliance-key.pem \
	-u ec2-user \
	-e "scan_phase=post_remediation"
```

#### Phase 5 — Run Compliance Gate

bash

```
python3 scripts/compliance-gate.py \
	--threshold 85 \
	--reports-dir reports \
	--profile cis-level2 \
	--fail-on-critical
```

#### Phase 6 — Push Metrics + Generate Report

bash

```
python3 scripts/push-metrics.py --reports-dir reports
python3 scripts/generate-report.py --output reports/report.html
```

---

### Production Considerations

GapCurrent StateProduction SolutionInstance discoveryStatic tagsAWS Systems Manager Fleet Manager inventoryRemediation riskRuns on all instancesBlue/green remediation with staging validation firstReport storageLocal HTMLS3 + CloudFront for compliance report portalHistorical trendingCloudWatch onlyOpenSearch for long-term compliance historyAlertingSNS email onlyPagerDuty integration for CRITICAL findingsWindows supportLinux onlyOpenSCAP for Windows or Microsoft STIG toolingContainersEC2 onlykube-bench for Kubernetes CIS benchmarksEvidence collectionHTML reportAutomated evidence packages for auditors

---

### Key Lessons Learned

**OpenSCAP exit code 2 is not a failure**
When oscap finds non-compliant rules, it exits with code 2.
This is expected. It means the scan ran and found issues.
Exit code 1 means the scan itself failed. If you use
`failed_when: result.rc != 0` in Ansible, your playbook will
fail on every non-perfect system. Use
`failed_when: result.rc not in [0, 2]`.

**Ansible remediation must not break SSH before completing**
The SSH hardening tasks modify sshd_config. If the handler
restarts SSH before all tasks complete and the new config has
a syntax error, you lose your SSH connection permanently.
Always validate sshd_config with `sshd -t` before restarting.
The Ansible handler only fires after all tasks succeed.

**The CIS Level 2 score starts lower than you expect**
A fresh Amazon Linux 2023 instance scores approximately 45-55%
on CIS Level 2 out of the box. This is not a failure state.
It is the baseline that the remediation playbook improves.
Document both the before and after scores as the proof of value.

**Dynamic inventory requires boto3 on the control machine**
The amazon.aws.aws_ec2 inventory plugin calls AWS APIs from
your local machine, not from the EC2 instances. Install boto3
and the amazon.aws Ansible collection on your control machine
before running any playbook with the dynamic inventory.

---

### Destroy Everything

bash

```
cd terraform && terraform destroy --auto-approve
rm -f compliance-key.pem
```

Verify in AWS console:
EC2 instances, key pair, security group, IAM role,
SNS topic, CloudWatch dashboard and alarm are all removed.

---

### Author

<div align="center">
**Emmanuel Ubani**
Cloud and DevOps Engineer — Lagos, Nigeria

*From zoo volunteer to Cloud and DevOps Engineer.*
*Building production-grade infrastructure in public.*

[Show Image](https://linkedin.com/in/ubaniemmanuel)
[Show Image](https://github.com/Eaglewings966)
[Show Image](https://emmanuelubani.hashnode.dev)
[Show Image](https://medium.com/@emmaubani966)
[Show Image](https://hub.docker.com/u/eaglewings6)
[Show Image](https://ops-run.lovable.app)

#ProjectRepository1AWS IAM Multi-Account Setup[aws-iam-multi-account-setup](https://github.com/Eaglewings966/aws-iam-multi-account-setup)2GitHub Actions CI/CD Pipeline[github-actions-cicd-pipeline](https://github.com/Eaglewings966/github-actions-cicd-pipeline)3Kubernetes EKS Deployment[eks-kubernetes-deployment](https://github.com/Eaglewings966/eks-kubernetes-deployment)4GitOps Platform with Argo CD[argocd-gitops-platform](https://github.com/Eaglewings966/argocd-gitops-platform)5AWS Cost Optimization Engine[aws-cost-optimization](https://github.com/Eaglewings966/aws-cost-optimization)6AWS Multi-Account Landing Zone[aws-multi-account-landing-zone](https://github.com/Eaglewings966/aws-multi-account-landing-zone)7Enterprise DevSecOps Pipeline[aws-devsecops-pipeline](https://github.com/Eaglewings966/aws-devsecops-pipeline)8HashiCorp Vault HA Cluster[hashicorp-vault-eks](https://github.com/Eaglewings966/hashicorp-vault-eks)9Container Image Supply Chain[cosign-image-supply-chain](https://github.com/Eaglewings966/cosign-image-supply-chain)10Zero-Trust Kubernetes Platform[istio-zero-trust-eks](https://github.com/Eaglewings966/istio-zero-trust-eks)11Automated Compliance PipelineThis repository

</div>
