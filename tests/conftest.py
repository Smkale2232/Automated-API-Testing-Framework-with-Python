import pytest
import requests
import subprocess
import time
import os
import sys
from threading import Thread

# Global variable to track the server process
server_process = None


def start_flask_app():
    """Start the Flask app in a separate process"""
    global server_process
    try:
        env = os.environ.copy()
        env['FLASK_DEBUG'] = 'False'
        env['FLASK_PORT'] = '5000'
        env['PYTHONPATH'] = os.getcwd()

        server_process = subprocess.Popen(
            [sys.executable, 'src/api/app.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait for server to start
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Failed to start Flask app: {e}")
        return False


def stop_flask_app():
    """Stop the Flask app process"""
    global server_process
    if server_process:
        server_process.terminate()
        server_process.wait()
        server_process = None


def is_server_running(base_url='http://localhost:5000'):
    """Check if the server is running"""
    try:
        response = requests.get(f'{base_url}/health', timeout=2)
        return response.status_code == 200
    except:
        return False


@pytest.fixture(scope='session')
def flask_server():
    """Start and stop Flask server for tests - only if not in CI"""
    # In CI, we use the test client directly, no need for external server
    if os.getenv('CI') == 'true':
        print("Running in CI environment - using test client")
        yield
        return

    # Local development - start actual server
    print("Starting Flask server for local testing...")
    if not start_flask_app():
        pytest.skip("Could not start Flask server")

    # Wait for server to be ready
    max_attempts = 10
    for i in range(max_attempts):
        if is_server_running():
            print("Flask server is ready!")
            break
        print(f"Waiting for server... attempt {i+1}/{max_attempts}")
        time.sleep(1)
    else:
        pytest.skip("Flask server failed to start within timeout")

    yield

    print("Stopping Flask server...")
    stop_flask_app()


@pytest.fixture
def base_url():
    """Base URL for API requests"""
    if os.getenv('CI') == 'true':
        # In CI, we'll use the test client directly
        return 'http://testserver'
    return 'http://localhost:5000'


@pytest.fixture
def api_client(base_url):
    """API client for making requests"""
    if os.getenv('CI') == 'true':
        # In CI, use Flask test client
        from src.api.app import app
        with app.test_client() as client:
            def _make_request(method, endpoint, **kwargs):
                # Convert requests-like API to Flask test client API
                method = method.lower()
                flask_method = getattr(client, method)

                # Handle JSON data
                json_data = kwargs.get('json')
                if json_data:
                    response = flask_method(
                        endpoint,
                        json=json_data,
                        headers=kwargs.get('headers', {})
                    )
                else:
                    response = flask_method(
                        endpoint,
                        data=kwargs.get('data'),
                        headers=kwargs.get('headers', {})
                    )

                # Convert Flask response to requests-like response
                class ResponseWrapper:
                    def __init__(self, flask_response):
                        self.status_code = flask_response.status_code
                        self.headers = dict(flask_response.headers)
                        self._flask_response = flask_response

                    def json(self):
                        import json
                        return json.loads(self._flask_response.data.decode('utf-8'))

                    @property
                    def text(self):
                        return self._flask_response.data.decode('utf-8')

                return ResponseWrapper(response)

            yield _make_request
    else:
        # Local development - use requests
        session = requests.Session()
        session.timeout = 10

        def _make_request(method, endpoint, **kwargs):
            url = f"{base_url}{endpoint}"
            print(f"Making {method} request to {url}")
            response = session.request(method, url, **kwargs)
            print(f"Response status: {response.status_code}")
            return response

        yield _make_request


@pytest.fixture
def unique_user_data():
    """Generate unique user data for each test"""
    import time
    timestamp = int(time.time() * 1000)
    return {
        "name": f"Test User {timestamp}",
        "email": f"test{timestamp}@example.com"
    }
