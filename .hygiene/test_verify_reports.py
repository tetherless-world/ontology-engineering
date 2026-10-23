"""Check the pass/fail contract used by the GitHub Actions job."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("verify_reports.py")
PASS = '<testsuite><testcase name="labels"/></testsuite>'


class ReportValidationTests(unittest.TestCase):
    def check_reports(self, files, expected):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for relative, content in files.items():
                report = directory / relative
                report.parent.mkdir(parents=True, exist_ok=True)
                report.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(directory)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_clean_dev_report_passes(self):
        self.check_reports({"branch/latest/hygiene_test.dev.xml": PASS}, 0)

    def test_junit_failures_and_errors_fail(self):
        reports = [
            '<testsuite><testcase><failure message="missing label"/></testcase></testsuite>',
            '<testsuite><testcase><error>query failed</error></testcase></testsuite>',
            '<testsuite failures="1"><testcase/></testsuite>',
            '<testsuite errors="1"><testcase/></testsuite>',
        ]
        for report in reports:
            with self.subTest(report=report):
                self.check_reports({"hygiene_test.dev.xml": report}, 1)

    def test_missing_dev_report_fails_even_with_passing_prod(self):
        self.check_reports({}, 1)
        self.check_reports({"hygiene_test.prod.xml": PASS}, 1)

    def test_empty_or_invalid_report_fails(self):
        for report in ["<testsuite/>", "<testsuite>", "<document><testcase/></document>"]:
            with self.subTest(report=report):
                self.check_reports({"hygiene_test.dev.xml": report}, 1)

    def test_all_dev_reports_are_checked(self):
        self.check_reports(
            {
                "a/hygiene_test.dev.xml": PASS,
                "b/hygiene_test.dev.xml": '<testsuite><testcase><failure/></testcase></testsuite>',
            },
            1,
        )

    def test_namespaced_junit_is_supported(self):
        self.check_reports(
            {"hygiene_test.dev.xml": '<testsuites xmlns="urn:junit"><testsuite><testcase/></testsuite></testsuites>'},
            0,
        )


if __name__ == "__main__":
    unittest.main()
