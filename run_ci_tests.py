#!/usr/bin/env python3
"""
CI Test Runner - Simplified version for GitHub Actions
"""
import subprocess
import sys
import os


def run_ci_tests():
    """Run tests in CI environment"""
    # Set CI environment
    env = os.environ.copy()
    env['CI'] = 'true'

    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--html=test-reports/pytest_report.html",
        "--self-contained-html",
        "--junit-xml=test-reports/junit-report.xml",
        "--tb=short",
        "-p", "no:warnings"
    ]

    print(f"Running CI tests: {' '.join(cmd)}")

    result = subprocess.run(cmd, env=env, capture_output=True, text=True)

    print("STDOUT:")
    print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    return result.returncode


if __name__ == "__main__":
    # Create test-reports directory
    os.makedirs("test-reports", exist_ok=True)

    return_code = run_ci_tests()
    sys.exit(return_code)
