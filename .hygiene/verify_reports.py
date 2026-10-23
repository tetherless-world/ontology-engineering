#!/usr/bin/env python3
"""Fail CI for missing/empty/malformed DEV reports or JUnit failures/errors."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def local_name(element):
    return element.tag.rsplit("}", 1)[-1]


def main():
    if len(sys.argv) != 2:
        print("Usage: verify_reports.py REPORT_DIRECTORY", file=sys.stderr)
        return 2

    reports = sorted(Path(sys.argv[1]).rglob("hygiene_test.dev.xml"))
    if not reports:
        print("ERROR: no hygiene_test.dev.xml report was produced.", file=sys.stderr)
        return 1

    failed = False
    for report in reports:
        print(f"Checking {report}", flush=True)
        try:
            root = ET.parse(report).getroot()
            if local_name(root) not in {"testsuite", "testsuites"}:
                raise ValueError("expected a JUnit testsuite/testsuites root")
            elements = list(root.iter())
            cases = [e for e in elements if local_name(e) == "testcase"]
            problems = [e for e in elements if local_name(e) in {"failure", "error"}]
            suites = [e for e in elements if local_name(e) in {"testsuite", "testsuites"}]
            declared_failure = any(
                int(e.get("failures", "0")) > 0 or int(e.get("errors", "0")) > 0
                for e in suites
            )
            if not cases:
                print("ERROR: report contains no test cases.")
                failed = True
            if problems or declared_failure:
                print(f"ERROR: failures/errors in a report with {len(cases)} test cases.")
                for problem in problems:
                    print(problem.get("message", ""))
                    print("".join(problem.itertext()).strip())
                failed = True
            elif cases:
                print(f"PASS: {len(cases)} test cases, no JUnit failures/errors.")
        except (OSError, ET.ParseError, ValueError) as exc:
            print(f"ERROR: cannot validate report: {exc}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
