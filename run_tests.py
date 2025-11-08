#!/usr/bin/env python3
"""
Test Runner Script for API Testing Framework
"""
import subprocess
import sys
import os
import argparse
import time
import requests
from utils.report_generator import HTMLReportGenerator


def wait_for_api(base_url, timeout=30):
    """Wait for API to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                return True
        except requests.exceptions.RequestException:
            print("⏳ Waiting for API to start...")
            time.sleep(2)

    print("❌ API failed to start within timeout period")
    return False


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
        cmd.extend(["tests/", "-m", "integration"])
    elif test_type == "smoke":
        # Run specific smoke tests
        cmd.extend([
            "tests/test_health.py::TestHealthEndpoint::test_health_check_success",
            "tests/test_health.py::TestHealthEndpoint::test_health_check_method_not_allowed",
            "tests/test_users.py::TestUserCreation::test_create_user_success"
        ])
    else:  # all tests
        cmd.extend(["tests/"])

    # Add reporting options
    if html_report:
        cmd.extend(["--html=test-reports/pytest_report.html",
                   "--self-contained-html"])

    # Add JUnit XML for CI
    cmd.extend(["--junit-xml=test-reports/junit-report.xml"])

    print(f"Running command: {' '.join(cmd)}")

    try:
        # Wait for API to be ready
        if not wait_for_api("http://localhost:5000"):
            print("❌ Cannot run tests - API is not available")
            return 1

        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(
            f"Test execution completed with return code: {result.returncode}")
        return result.returncode

    except Exception as e:
        print(f"❌ Error running tests: {e}")
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

    print(f"🚀 Starting test execution: {args.type} tests")
    print(f"📊 HTML reports: {not args.no_html}")

    # Run tests
    return_code = run_tests(args.type, not args.no_html)

    if return_code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Some tests failed with return code: {return_code}")

    sys.exit(return_code)


if __name__ == "__main__":
    main()
