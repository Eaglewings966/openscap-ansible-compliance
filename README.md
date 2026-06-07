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
