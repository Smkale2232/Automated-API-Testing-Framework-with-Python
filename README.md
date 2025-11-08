Automated API Testing Framework
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Flask-2.3.3-green
https://img.shields.io/badge/pytest-Testing%2520Framework-orange
https://img.shields.io/badge/CI%252FCD-GitHub%2520Actions-brightgreen

A comprehensive, professional API testing framework built with Python, Flask, and pytest. Demonstrates industry best practices for API testing and automation.

📋 Table of Contents
Features

Project Structure

Quick Start

Installation

API Documentation

Testing Guide

CI/CD Pipeline

Configuration

Best Practices

Resume Highlights

🚀 Features
✅ REST API Implementation - Flask-based API with 3 key endpoints

✅ Comprehensive Test Suite - Positive/negative test cases, status code validation, response validation

✅ Test Reporting - HTML and JUnit XML reports with detailed analytics

✅ CI/CD Integration - GitHub Actions for automated testing across multiple Python versions

✅ Environment Configuration - Multiple environment support (dev, test, prod)

✅ Professional Structure - Modular, maintainable codebase following industry standards

✅ Error Handling - Comprehensive negative testing and edge cases

✅ Performance Monitoring - Response time validation and performance metrics

📁 Project Structure
text
api-testing-framework/
│
├── src/
│ └── api/
│ ├── **init**.py
│ └── app.py # Flask API implementation
│
├── tests/
│ ├── **init**.py
│ ├── conftest.py # Pytest configuration and fixtures
│ ├── test_health.py # Health endpoint tests
│ ├── test_users.py # User endpoint tests
│ └── integration/
│ └── test_integration.py # Integration tests
│
├── config/
│ ├── **init**.py
│ ├── config.py # Configuration management
│ └── environments.py # Environment settings
│
├── utils/
│ ├── **init**.py
│ └── report_generator.py # HTML report generation
│
├── test-reports/ # Generated test reports (auto-created)
├── .github/
│ └── workflows/
│ └── python-tests.yml # CI/CD pipeline
│
├── requirements.txt # Python dependencies
├── pytest.ini # Pytest configuration
├── run_tests.py # Test runner script
├── .env.example # Environment variables template
└── README.md # This file
🚦 Quick Start
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Git

5-Minute Setup
Clone and setup:

bash

# Clone the repository

git clone https://github.com/Smkale2232/api-testing-framework.git
cd api-testing-framework

# Create virtual environment

python -m venv venv

# Activate virtual environment

# On Windows:

venv\Scripts\activate

# On macOS/Linux:

source venv/bin/activate

# Install dependencies

pip install -r requirements.txt
Start the API (Terminal 1):

bash
python src/api/app.py
API will run at: http://localhost:5000

Run tests (Terminal 2):

bash

# Run all tests with HTML report

python run_tests.py
View reports: Check test-reports/ directory for detailed HTML reports.

🛠️ Installation & Setup
Detailed Installation Steps
Environment Setup:

bash

# Clone repository

git clone https://github.com/Smkale2232/api-testing-framework.git
cd api-testing-framework

# Create and activate virtual environment

python -m venv venv

# Windows

venv\Scripts\activate

# macOS/Linux

source venv/bin/activate

# Install dependencies

pip install -r requirements.txt
Configuration:

bash

# Copy environment template

cp .env.example .env

# Edit .env file with your settings

# ENVIRONMENT=development

# API_BASE_URL=http://localhost:5000

# REQUEST_TIMEOUT=10

Verify Installation:

bash

# Start API server

python src/api/app.py

# In another terminal, test health endpoint

curl http://localhost:5000/health
Running the Framework
Start API Server:

bash
python src/api/app.py
Run Test Commands:

bash

# Run all tests with full reporting

python run_tests.py

# Run smoke tests (quick validation)

python run_tests.py --type smoke

# Run unit tests only

python run_tests.py --type unit

# Run integration tests

python run_tests.py --type integration

# Run without HTML report

python run_tests.py --no-html

# Run with specific Python module

python -m pytest tests/test_health.py -v
🔧 API Documentation
Endpoint Summary
Method Endpoint Description Success Code Error Codes
GET /health API health check 200 -
POST /users Create new user 201 400, 409
GET /users/{id} Get user by ID 200 404
Detailed Endpoint Specifications
Health Check
http
GET /health
Response (200):

json
{
"status": "healthy",
"timestamp": "2023-10-15T10:30:00.000Z",
"version": "1.0.0"
}
Create User
http
POST /users
Content-Type: application/json

{
"name": "John Doe",
"email": "john.doe@example.com"
}
Success Response (201):

json
{
"id": 1,
"name": "John Doe",
"email": "john.doe@example.com",
"created_at": "2023-10-15T10:30:00.000Z"
}
Error Responses:

400 Bad Request - Missing required fields or invalid email format

409 Conflict - Email address already exists

Get User
http
GET /users/1
Success Response (200):

json
{
"id": 1,
"name": "John Doe",
"email": "john.doe@example.com",
"created_at": "2023-10-15T10:30:00.000Z"
}
Error Response:

404 Not Found - User with specified ID not found

🧪 Testing Guide
Test Categories

1. Unit Tests
   Individual endpoint testing

Isolated functionality validation

Mocked dependencies when needed

2. Integration Tests
   Multi-endpoint workflow testing

Data consistency across operations

End-to-end user scenarios

3. Positive Testing
   Valid request scenarios

Happy path validation

Success response verification

4. Negative Testing
   Invalid input handling

Error response validation

Edge case coverage

Test Examples
Positive Test Cases:

Health check returns 200 status

User creation with valid data returns 201

User retrieval returns correct user data

Data persistence across operations

Negative Test Cases:

User creation with missing name/email

User creation with invalid email format

Duplicate email registration attempt

Retrieving non-existent user

Invalid HTTP methods

Malformed JSON payloads

Running Specific Tests
bash

# Run specific test file

python -m pytest tests/test_health.py -v

# Run specific test class

python -m pytest tests/test_users.py::TestUserCreation -v

# Run specific test method

python -m pytest tests/test_users.py::TestUserCreation::test_create_user_success -v

# Run tests with markers

python -m pytest -m smoke -v

# Run tests excluding slow ones

python -m pytest -m "not slow" -v
Test Reports
After test execution, you'll find:

HTML Report (test-reports/test*report*\*.html):

Executive summary dashboard

Test execution statistics

Duration metrics

Failure analysis

JUnit XML (test-reports/junit-report.xml):

CI/CD integration format

Test execution data

Failure details

Console Output:

Real-time test progress

Immediate failure feedback

Summary statistics

🔄 CI/CD Pipeline
GitHub Actions Workflow
The framework includes automated CI/CD with GitHub Actions:

Trigger Events:

Push to main/develop branches

Pull requests to main branch

Manual triggers

Pipeline Stages:

Setup: Python environment setup

Dependencies: Package installation

API Server: Start test server

Testing: Execute test suite

Reporting: Generate and upload reports

Security: Security scanning (Bandit, Safety)

Supported Python Versions:

3.8

3.9

3.10

Pipeline Configuration
yaml

# .github/workflows/python-tests.yml

name: Python API Tests
on: [push, pull_request]
jobs:
test:
runs-on: ubuntu-latest
strategy:
matrix:
python-version: [3.8, 3.9, 3.10]
steps: - uses: actions/checkout@v3 - name: Set up Python
uses: actions/setup-python@v3
with:
python-version: ${{ matrix.python-version }} - name: Install dependencies
run: pip install -r requirements.txt - name: Start API Server
run: python src/api/app.py & - name: Run tests
run: python run_tests.py
⚙️ Configuration
Environment Management
The framework supports multiple environments:

Development (ENVIRONMENT=development):

Debug mode enabled

Localhost API URL

Detailed logging

Testing (ENVIRONMENT=testing):

Test-specific configurations

Isolated test database

CI/CD optimized settings

Production (ENVIRONMENT=production):

Production API URLs

Optimized performance settings

Security-focused configuration

Environment Variables
Create a .env file:

env

# Application Environment

ENVIRONMENT=development

# API Configuration

API_BASE_URL=http://localhost:5000
REQUEST_TIMEOUT=10

# Testing Configuration

TEST_DATABASE_URL=sqlite:///test.db
LOG_LEVEL=INFO
Configuration Files
config/config.py:

Base configuration class

Environment-specific overrides

Configuration validation

pytest.ini:

Pytest configuration

Test markers definition

Execution options

💡 Best Practices Implemented

1. Testing Best Practices
   Test Isolation: Database reset between tests

Comprehensive Coverage: Positive and negative test cases

Data Validation: Response structure and content verification

Error Handling: Proper error response testing

Performance Checks: Response time validation

2. Code Quality
   Modular Design: Separated concerns and reusable components

Documentation: Comprehensive docstrings and comments

Type Hints: Python type annotations for better code clarity

Logging: Structured logging for debugging and monitoring

3. Automation & CI/CD
   Automated Testing: Zero manual intervention required

Multi-Environment: Support for different deployment environments

Quality Gates: Automated quality checks in pipeline

Artifact Management: Test report storage and accessibility

4. Security
   Input Validation: Comprehensive request validation

Error Handling: Secure error messages without information leakage

Dependency Scanning: Automated security vulnerability checks

🎯 Resume Highlights
Technical Skills Demonstrated
API Development & Testing
✅ RESTful API design and implementation with Flask

✅ Comprehensive API testing strategies

✅ HTTP protocol understanding (status codes, methods, headers)

✅ Request/response validation and error handling

Test Automation
✅ pytest framework mastery

✅ Automated test execution and reporting

✅ Positive and negative test case design

✅ Integration and unit testing methodologies

CI/CD & DevOps
✅ GitHub Actions pipeline implementation

✅ Automated testing across multiple Python versions

✅ Test report generation and artifact management

✅ Environment configuration management

Software Engineering
✅ Professional code structure and organization

✅ Configuration management best practices

✅ Documentation and code quality standards

✅ Version control with Git

Project Impact Statements for Resume
Bullet Point Examples:

"Designed and implemented automated API testing framework achieving 95%+ test coverage"

"Built comprehensive test suites with 30+ test cases including positive/negative scenarios"

"Implemented CI/CD pipeline reducing manual testing effort by 80%"

"Created professional test reporting system improving test result visibility by 60%"

"Applied software engineering best practices ensuring maintainable and scalable codebase"

Interview Talking Points
Testing Strategy: "I implemented a multi-layered testing approach covering unit, integration, and negative testing scenarios..."

Automation Benefits: "The framework reduces manual testing time from hours to minutes while improving test consistency..."

CI/CD Impact: "Automated testing in the pipeline catches regressions immediately, improving code quality and deployment confidence..."

Best Practices: "I followed industry standards like test isolation, comprehensive validation, and professional reporting..."

🚀 Advanced Usage
Extending the Framework
Adding New Endpoints:

Add endpoint to src/api/app.py

Create test file in tests/

Implement positive and negative test cases

Update documentation

Custom Test Fixtures:

python
@pytest.fixture
def auth_headers():
return {'Authorization': 'Bearer token123'}

@pytest.fixture
def sample_payload():
return {
"name": "Test User",
"email": "test@example.com"
}
Performance Testing:

python
def test_response_performance(api_client):
start_time = time.time()
response = api_client('GET', '/health')
end_time = time.time()

    assert response.status_code == 200
    assert (end_time - start_time) < 0.5  # 500ms threshold

Integration with Other Tools
Test Management:

Integrate with TestRail, Zephyr, or similar tools

Export test results for external reporting

Track test execution history

Monitoring:

Integrate with Prometheus/Grafana for metrics

Add performance monitoring

Implement alerting for test failures

🐛 Troubleshooting
Common Issues
API Not Starting:

bash

# Check if port 5000 is available

netstat -an | grep 5000

# Use different port

python src/api/app.py --port 5001
Test Failures:

bash

# Run with detailed output

python -m pytest -v --tb=long

# Debug specific test

python -m pytest tests/test_users.py -v -s
Dependency Issues:

bash

# Clear cache and reinstall

pip cache purge
pip install -r requirements.txt --force-reinstall
Getting Help
Check existing issues on GitHub

Review test reports for detailed error information

Enable debug logging in configuration

Use Python debugger for complex issues

📈 Performance Metrics
Key Metrics Tracked
Test Execution Time: Individual and total test duration

Success Rate: Percentage of passing tests

API Response Time: Endpoint performance under test

Test Coverage: Code and scenario coverage metrics

Optimization Tips
Parallel Testing: Use pytest-xdist for parallel test execution

Test Data Management: Optimize test data setup and teardown

Selective Testing: Run only affected tests using markers

Caching: Implement caching for expensive test operations

🤝 Contributing
We welcome contributions! Please see our contributing guidelines:

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

Contribution Areas
New test scenarios and endpoints

Enhanced reporting features

Additional CI/CD integrations

Performance optimizations

Documentation improvements

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🛠️ Built With
Python - Programming language

Flask - Web framework

pytest - Testing framework

Requests - HTTP library

GitHub Actions - CI/CD platform

📞 Support
Documentation: GitHub Wiki

Issues: GitHub Issues

Discussions: GitHub Discussions

🎓 Learning Resources
Related Topics to Explore
REST API design principles

Test-driven development (TDD)

Continuous integration/deployment

Software testing methodologies

Python testing frameworks

Next Steps
Add database integration with SQLAlchemy

Implement authentication and authorization testing

Add performance and load testing

Integrate with API documentation tools (Swagger/OpenAPI)

Expand to microservices testing

⭐ If this project helped you, please give it a star on GitHub!

📧 Contact: your.email@example.com

🐦 Twitter: @yourhandle

💼 LinkedIn: Your Profile

<div align="center">
🚀 Ready to automate your API testing?
Get started in 5 minutes with our quick start guide above!

</div>
