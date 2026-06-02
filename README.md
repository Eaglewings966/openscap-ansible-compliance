# OpenSCAP Ansible Compliance

Automated CIS benchmark compliance scanning and remediation pipeline using OpenSCAP, Ansible, Terraform, and GitHub Actions on AWS.

## Architecture

```
GitHub Actions → Terraform (EC2) → Ansible (OpenSCAP scan) → Compliance Gate → CloudWatch Metrics
```

## Components

| Path | Purpose |
|------|---------|
| `terraform/` | Provisions RHEL 9 EC2 instances |
| `ansible/roles/openscap-scan/` | Runs OpenSCAP CIS scan |
| `ansible/roles/cis-hardening/` | Applies CIS Level 1 hardening |
| `ansible/roles/cis-remediation/` | Auto-remediates via `oscap --remediate` |
| `scripts/compliance-gate.py` | Fails pipeline if score < threshold |
| `scripts/push-metrics.py` | Sends scores to CloudWatch |
| `scripts/generate-report.py` | Builds consolidated HTML report |
| `.github/workflows/` | Full CI/CD pipeline |

## Prerequisites

- AWS account with credentials configured
- EC2 key pair named `compliance-key` (or set `key_name` in `terraform.tfvars`)
- S3 bucket for Terraform state (update `terraform/main.tf` backend config)
- GitHub secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `SSH_PRIVATE_KEY`

## Usage

### Manual run

```bash
# 1. Provision instances
bash scripts/provision-instances.sh

# 2. Run scan
ansible-playbook ansible/scan.yml -i ansible/inventory/aws_ec2.yml

# 3. Check compliance gate (default threshold: 80%)
python scripts/compliance-gate.py --threshold 80

# 4. Generate report
python scripts/generate-report.py

# 5. Push metrics to CloudWatch
python scripts/push-metrics.py

# 6. Destroy instances
bash scripts/destroy-instances.sh
```

### CI/CD

Push to `main` triggers the full pipeline automatically. Results are available as GitHub Actions artifacts.

## Configuration

- **Scan profile**: `openscap_profile` in `ansible/roles/openscap-scan/vars/main.yml`
- **Compliance threshold**: `COMPLIANCE_THRESHOLD` env var in `.github/workflows/compliance-pipeline.yml`
- **Instance count/type**: `terraform/terraform.tfvars`
