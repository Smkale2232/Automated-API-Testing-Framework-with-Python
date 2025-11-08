#!/usr/bin/env python3
"""
Test Runner Script for API Testing Framework
"""
import subprocess
import sys
import os
import argparse
from utils.report_generator import HTMLReportGenerator


def run_tests(test_type="all", html_report=True):
    """Run tests with specified configuration"""

    # Set environment for testing
    env = os.environ.copy()
    env['ENVIRONMENT'] = 'testing'

    # Base pytest command
    cmd = [sys.executable, "-m", "pytest", "-v"]

    # Add options based on test type
    if test_type == "unit":
        cmd.extend(["tests/", "-m", "not integration"])
    elif test_type == "integration":
        cmd.extend(["tests/integration/", "-m", "integration"])
    elif test_type == "smoke":
        cmd.extend(["tests/test_health.py",
                   "tests/test_users.py::TestUserCreation::test_create_user_success"])
    else:  # all tests
        cmd.extend(["tests/"])

    # Add coverage if requested
    if html_report:
        cmd.extend(["--html=test-reports/pytest_report.html",
                   "--self-contained-html"])

    # Add JUnit XML for CI
    cmd.extend(["--junit-xml=test-reports/junit-report.xml"])

    print(f"Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        return result.returncode

    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="API Test Runner")
    parser.add_argument("--type", choices=["all", "unit", "integration", "smoke"],
                        default="all", help="Type of tests to run")
    parser.add_argument("--no-html", action="store_true",
                        help="Disable HTML report")

    args = parser.parse_args()

    # Create test-reports directory
    os.makedirs("test-reports", exist_ok=True)

    # Run tests
    return_code = run_tests(args.type, not args.no_html)

    sys.exit(return_code)


if __name__ == "__main__":
    main()
