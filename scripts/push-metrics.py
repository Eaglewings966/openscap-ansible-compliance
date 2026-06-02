#!/usr/bin/env python3
"""
Compliance Metrics Publisher
Reads compliance scan results from JSON summary files and publishes
them to AWS CloudWatch custom metrics.

Usage:
    python3 scripts/push-metrics.py \
        --reports-dir reports \
        --region us-east-1
"""

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

try:
    import defusedxml.ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET  # noqa: S405

NAMESPACE = "ComplianceScanner"
NS = {"xccdf": "http://checklists.nist.gov/xccdf/1.2"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Push compliance metrics to CloudWatch"
    )
    parser.add_argument("--reports-dir", default="reports",
                        help="Directory containing compliance JSON reports")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    parser.add_argument("--namespace", default=NAMESPACE,
                        help="CloudWatch metric namespace")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print metrics without publishing to CloudWatch")
    return parser.parse_args()


def load_json_reports(reports_dir):
    reports = []
    for path in glob.glob(
        os.path.join(reports_dir, "**", "compliance-summary.json"), recursive=True
    ):
        try:
            with open(path) as fh:
                report = json.load(fh)
                report["_source_file"] = path
                reports.append(report)
                print(f"  Loaded: {path}")
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  WARNING: could not load {path}: {exc}")
    return reports


def score_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    rules = root.findall(".//xccdf:rule-result", namespaces=NS)
    if not rules:
        return 0.0
    passed = sum(
        1 for r in rules
        if r.findtext("xccdf:result", namespaces=NS) == "pass"
    )
    return round(passed / len(rules) * 100, 2)


def build_metrics(report):
    now = datetime.now(timezone.utc)
    instance_id = report.get("instance_id", report.get("hostname", "unknown"))
    os_name = report.get("os", "unknown")
    metrics = []

    if "cis_level1_score" in report:
        metrics.append({
            "MetricName": "ComplianceScore",
            "Dimensions": [
                {"Name": "InstanceId", "Value": instance_id},
                {"Name": "Profile", "Value": "cis-level1"},
                {"Name": "OS", "Value": os_name},
            ],
            "Timestamp": now,
            "Value": float(report["cis_level1_score"]),
            "Unit": "Percent",
        })

    if "cis_level2_score" in report:
        metrics.append({
            "MetricName": "ComplianceScore",
            "Dimensions": [
                {"Name": "InstanceId", "Value": instance_id},
                {"Name": "Profile", "Value": "cis-level2"},
                {"Name": "OS", "Value": os_name},
            ],
            "Timestamp": now,
            "Value": float(report["cis_level2_score"]),
            "Unit": "Percent",
        })

    for metric_name, key in [
        ("CriticalFindings", "critical_findings"),
        ("HighFindings", "high_findings"),
        ("MediumFindings", "medium_findings"),
    ]:
        if key in report:
            metrics.append({
                "MetricName": metric_name,
                "Dimensions": [{"Name": "InstanceId", "Value": instance_id}],
                "Timestamp": now,
                "Value": int(report[key]),
                "Unit": "Count",
            })

    return metrics


def publish(cloudwatch, namespace, metric_data, dry_run):
    total = 0
    for i in range(0, len(metric_data), 20):
        batch = metric_data[i:i + 20]
        if dry_run:
            print(f"  [DRY RUN] Would publish {len(batch)} metrics:")
            for m in batch:
                dims = ", ".join(f"{d['Name']}={d['Value']}" for d in m["Dimensions"])
                print(f"    {m['MetricName']}: {m['Value']} {m['Unit']} [{dims}]")
        else:
            try:
                cloudwatch.put_metric_data(Namespace=namespace, MetricData=batch)
                print(f"  Published batch of {len(batch)} metrics.")
            except ClientError as exc:
                print(f"  ERROR publishing metrics: {exc}")
                sys.exit(1)
        total += len(batch)
    return total


def main():
    args = parse_args()

    print("=" * 60)
    print("Compliance Metrics Publisher")
    print("=" * 60)
    print(f"Reports directory: {args.reports_dir}")
    print(f"Namespace:         {args.namespace}")
    print(f"Region:            {args.region}")
    print(f"Dry run:           {args.dry_run}")
    print()

    print("Loading compliance reports...")
    reports = load_json_reports(args.reports_dir)

    if not reports:
        print(f"WARNING: No compliance-summary.json files found in '{args.reports_dir}'.")
        sys.exit(0)

    print(f"Loaded {len(reports)} report(s).\n")

    all_metrics = []
    for r in reports:
        hostname = r.get("hostname", "unknown")
        print(f"Processing: {hostname}")
        print(f"  CIS L1: {r.get('cis_level1_score', 'N/A')}%")
        print(f"  CIS L2: {r.get('cis_level2_score', 'N/A')}%")
        print(f"  Critical: {r.get('critical_findings', 0)}")
        print(f"  High:     {r.get('high_findings', 0)}")
        all_metrics.extend(build_metrics(r))

    print(f"\nBuilt {len(all_metrics)} metrics total.")

    cw = boto3.client("cloudwatch", region_name=args.region)
    print("\nPublishing to CloudWatch...")
    total = publish(cw, args.namespace, all_metrics, args.dry_run)

    print()
    print("=" * 60)
    print(f"Published {total} metrics to namespace '{args.namespace}'.")
    print("=" * 60)


if __name__ == "__main__":
    main()
