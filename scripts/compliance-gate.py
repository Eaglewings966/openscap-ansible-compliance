#!/usr/bin/env python3
"""
Compliance CI/CD Gate
Reads compliance scores from JSON summary files produced by the Ansible scan role.
Exits with code 1 if any score is below the threshold or critical findings exist.
Used in GitHub Actions to block deployments.

Usage:
    python3 scripts/compliance-gate.py \
        --threshold 85 \
        --reports-dir reports \
        --profile cis-level2 \
        --fail-on-critical
"""

import argparse
import glob
import json
import os
import sys

try:
    import defusedxml.ElementTree as ET
except ImportError:
    # Fallback: standard library — safe here because we only read
    # local files produced by our own Ansible role, not untrusted input.
    import xml.etree.ElementTree as ET  # noqa: S405


NS = {"xccdf": "http://checklists.nist.gov/xccdf/1.2"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compliance CI/CD gate — blocks deploy if score is low"
    )
    parser.add_argument("--threshold", type=float, default=85.0,
                        help="Minimum compliance score percentage (default: 85)")
    parser.add_argument("--reports-dir", default="reports",
                        help="Directory containing compliance reports")
    parser.add_argument("--profile", default="cis-level2",
                        choices=["cis-level1", "cis-level2"],
                        help="CIS profile score to evaluate (default: cis-level2)")
    parser.add_argument("--fail-on-critical", action="store_true",
                        help="Always fail if any CRITICAL findings exist")
    return parser.parse_args()


def load_json_reports(reports_dir):
    """Load compliance-summary.json files written by the Ansible openscap-scan role."""
    reports = []
    for path in glob.glob(
        os.path.join(reports_dir, "**", "compliance-summary.json"), recursive=True
    ):
        try:
            with open(path) as fh:
                reports.append(json.load(fh))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"WARNING: could not load {path}: {exc}")
    return reports


def score_from_xml(xml_file):
    """Compute pass% from an XCCDF results XML (fallback when no JSON available)."""
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


def load_xml_reports(reports_dir, profile):
    """Fallback: derive reports from raw XML result files."""
    suffix = "level1" if profile == "cis-level1" else "level2"
    reports = []
    for path in glob.glob(
        os.path.join(reports_dir, "**", f"cis_{suffix}_results.xml"), recursive=True
    ):
        hostname = os.path.basename(os.path.dirname(path))
        s = score_from_xml(path)
        reports.append({
            "hostname": hostname,
            "os": "unknown",
            "cis_level1_score": s if suffix == "level1" else 0,
            "cis_level2_score": s if suffix == "level2" else 0,
            "critical_findings": 0,
            "high_findings": 0,
            "medium_findings": 0,
        })
    return reports


def evaluate(reports, threshold, profile, fail_on_critical):
    score_key = f"{profile.replace('-', '_')}_score"
    results = []
    all_passed = True

    for r in reports:
        score = float(r.get(score_key, 0))
        critical = int(r.get("critical_findings", 0))
        high = int(r.get("high_findings", 0))
        medium = int(r.get("medium_findings", 0))

        pass_score = score >= threshold
        block_critical = fail_on_critical and critical > 0
        passed = pass_score and not block_critical

        results.append({
            "hostname": r.get("hostname", "unknown"),
            "os": r.get("os", "unknown"),
            "score": score,
            "threshold": threshold,
            "profile": profile,
            "critical_findings": critical,
            "high_findings": high,
            "medium_findings": medium,
            "passed": passed,
            "blocked_by_score": not pass_score,
            "blocked_by_critical": block_critical,
        })

        if not passed:
            all_passed = False

    return all_passed, results


def print_report(results, all_passed):
    print()
    print("=" * 70)
    print("COMPLIANCE CI/CD GATE REPORT")
    print("=" * 70)

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"\n  Host:    {r['hostname']}")
        print(f"  OS:      {r['os']}")
        print(f"  Profile: {r['profile'].upper()}")
        print(f"  Score:   {r['score']:.1f}% (threshold: {r['threshold']:.0f}%)")
        print(f"  Critical findings: {r['critical_findings']}")
        print(f"  High findings:     {r['high_findings']}")
        print(f"  Medium findings:   {r['medium_findings']}")
        print(f"  Gate status: {status}")

        if r["blocked_by_score"]:
            deficit = r["threshold"] - r["score"]
            print(f"  Score is {deficit:.1f}% below threshold.")
            print("  Run: ansible-playbook ansible/remediate.yml")

        if r["blocked_by_critical"]:
            print(f"  {r['critical_findings']} CRITICAL finding(s) must be resolved.")

    print()
    print("=" * 70)
    if all_passed:
        print("GATE PASSED — All instances meet compliance requirements.")
        print("Deployment is approved to proceed.")
    else:
        print("GATE FAILED — One or more instances below compliance threshold.")
        print("Deployment is BLOCKED.")
        print()
        print("To fix:")
        print("  1. ansible-playbook ansible/remediate.yml")
        print("  2. ansible-playbook ansible/scan.yml")
        print("  3. Re-run this gate check.")
    print("=" * 70)
    print()


def set_github_outputs(all_passed, results):
    output_file = os.environ.get("GITHUB_OUTPUT", "")
    if not output_file:
        return
    min_score = min(r["score"] for r in results) if results else 0
    avg_score = sum(r["score"] for r in results) / len(results) if results else 0
    total_critical = sum(r["critical_findings"] for r in results)
    with open(output_file, "a") as fh:
        fh.write(f"gate_passed={'true' if all_passed else 'false'}\n")
        fh.write(f"min_score={min_score:.1f}\n")
        fh.write(f"avg_score={avg_score:.1f}\n")
        fh.write(f"total_critical={total_critical}\n")


def main():
    args = parse_args()

    print("=" * 70)
    print("COMPLIANCE CI/CD GATE")
    print("=" * 70)
    print(f"Threshold:         {args.threshold}%")
    print(f"Profile:           {args.profile}")
    print(f"Reports directory: {args.reports_dir}")
    print(f"Fail on critical:  {args.fail_on_critical}")

    reports = load_json_reports(args.reports_dir)

    if not reports:
        print("\nNo JSON summary files found — falling back to XML result files...")
        reports = load_xml_reports(args.reports_dir, args.profile)

    if not reports:
        print(f"\nERROR: No compliance reports found in '{args.reports_dir}'.")
        print("Run the compliance scan first:")
        print("  ansible-playbook ansible/scan.yml")
        sys.exit(1)

    print(f"Found {len(reports)} compliance report(s).")

    all_passed, results = evaluate(
        reports, args.threshold, args.profile, args.fail_on_critical
    )
    print_report(results, all_passed)
    set_github_outputs(all_passed, results)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
