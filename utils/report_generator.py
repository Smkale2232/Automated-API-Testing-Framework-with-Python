import json
import os
from datetime import datetime
import html


class HTMLReportGenerator:
    """Generate HTML test reports"""

    def __init__(self, report_dir="test-reports"):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)

    def generate_report(self, test_results, duration):
        """Generate HTML test report"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = os.path.join(
            self.report_dir, f"test_report_{timestamp}.html")

        total_tests = len(test_results)
        passed_tests = sum(
            1 for result in test_results if result['status'] == 'passed')
        failed_tests = sum(
            1 for result in test_results if result['status'] == 'failed')
        skipped_tests = sum(
            1 for result in test_results if result['status'] == 'skipped')

        html_content = self._generate_html_content(
            test_results, total_tests, passed_tests, failed_tests,
            skipped_tests, duration, timestamp
        )

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return report_file

    def _generate_html_content(self, test_results, total, passed, failed, skipped, duration, timestamp):
        """Generate HTML content for the report"""

        status_color = {
            'passed': 'success',
            'failed': 'danger',
            'skipped': 'warning'
        }

        test_rows = ""
        for i, result in enumerate(test_results, 1):
            test_rows += f"""
            <tr class="table-{status_color[result['status']]}">
                <td>{i}</td>
                <td>{html.escape(result['name'])}</td>
                <td><span class="badge bg-{status_color[result['status']]}">{result['status'].upper()}</span></td>
                <td>{result['duration']:.2f}s</td>
                <td>{html.escape(result.get('error', ''))}</td>
            </tr>
            """

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>API Test Report</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                .summary-card {{ transition: transform 0.2s; }}
                .summary-card:hover {{ transform: translateY(-5px); }}
                .test-table {{ font-size: 0.9rem; }}
            </style>
        </head>
        <body>
            <div class="container-fluid py-4">
                <div class="row">
                    <div class="col-12">
                        <h1 class="text-center mb-4">API Test Automation Report</h1>
                        
                        <!-- Summary Cards -->
                        <div class="row mb-4">
                            <div class="col-md-3">
                                <div class="card summary-card text-white bg-primary">
                                    <div class="card-body text-center">
                                        <h4>{total}</h4>
                                        <p>Total Tests</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card summary-card text-white bg-success">
                                    <div class="card-body text-center">
                                        <h4>{passed}</h4>
                                        <p>Passed</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card summary-card text-white bg-danger">
                                    <div class="card-body text-center">
                                        <h4>{failed}</h4>
                                        <p>Failed</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card summary-card text-white bg-warning">
                                    <div class="card-body text-center">
                                        <h4>{skipped}</h4>
                                        <p>Skipped</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Test Results -->
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title mb-0">Test Results</h5>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped test-table">
                                        <thead>
                                            <tr>
                                                <th>#</th>
                                                <th>Test Name</th>
                                                <th>Status</th>
                                                <th>Duration</th>
                                                <th>Error Message</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {test_rows}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Footer -->
                        <div class="mt-4 text-muted text-center">
                            <p>Generated on: {timestamp}</p>
                            <p>Total Duration: {duration:.2f} seconds</p>
                            <p>Success Rate: {(passed/total*100 if total > 0 else 0):.1f}%</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """


def pytest_sessionfinish(session, exitstatus):
    """Pytest hook to generate report after test session"""
    try:
        from utils.report_generator import HTMLReportGenerator

        # Collect test results
        test_results = []
        for item in session.items:
            test_duration = getattr(item, 'execution_duration', 0) or 0
            test_status = 'passed'
            error_msg = ''

            if hasattr(item, 'rep_call'):
                if item.rep_call.failed:
                    test_status = 'failed'
                    if hasattr(item.rep_call, 'longrepr'):
                        error_msg = str(item.rep_call.longrepr)
                elif item.rep_call.skipped:
                    test_status = 'skipped'

            test_results.append({
                'name': item.nodeid,
                'status': test_status,
                'duration': test_duration,
                'error': error_msg
            })

        # Generate report
        generator = HTMLReportGenerator()
        report_file = generator.generate_report(test_results, session.duration)
        print(f"\n📊 HTML Test Report generated: {report_file}")

    except Exception as e:
        print(f"Warning: Could not generate HTML report: {e}")
