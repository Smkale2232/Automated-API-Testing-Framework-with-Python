import pytest
import requests
import subprocess
import time
import os
import signal
from threading import Thread

# Global variable to track the server process
server_process = None


def start_flask_app():
    """Start the Flask app in a separate process"""
    global server_process
    env = os.environ.copy()
    env['FLASK_DEBUG'] = 'False'
    env['FLASK_PORT'] = '5000'

    server_process = subprocess.Popen(
        [os.sys.executable, 'src/api/app.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for server to start
    time.sleep(3)


def stop_flask_app():
    """Stop the Flask app process"""
    global server_process
    if server_process:
        server_process.terminate()
        server_process.wait()


def is_server_running():
    """Check if the server is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        return response.status_code == 200
    except:
        return False


@pytest.fixture(scope='session', autouse=True)
def flask_server():
    """Start and stop Flask server for tests"""
    # Start server
    print("Starting Flask server...")
    start_flask_app()

    # Wait for server to be ready
    max_attempts = 10
    for i in range(max_attempts):
        if is_server_running():
            print("Flask server is ready!")
            break
        print(f"Waiting for server... attempt {i+1}/{max_attempts}")
        time.sleep(1)
    else:
        raise Exception("Flask server failed to start")

    yield

    # Stop server
    print("Stopping Flask server...")
    stop_flask_app()


@pytest.fixture
def base_url():
    """Base URL for API requests"""
    return 'http://localhost:5000'


@pytest.fixture
def api_client(base_url):
    """API client for making requests"""
    session = requests.Session()
    session.timeout = 10

    def _make_request(method, endpoint, **kwargs):
        url = f"{base_url}{endpoint}"
        print(f"Making {method} request to {url}")
        response = session.request(method, url, **kwargs)
        print(f"Response status: {response.status_code}")
        return response

    return _make_request


@pytest.fixture
def unique_user_data():
    """Generate unique user data for each test"""
    import time
    timestamp = int(time.time() * 1000)
    return {
        "name": f"Test User {timestamp}",
        "email": f"test{timestamp}@example.com"
    }


@pytest.fixture(autouse=True)
def reset_database(api_client):
    """Reset the database before each test"""
    try:
        # Try to reset the database before each test
        response = api_client('POST', '/reset')
        if response.status_code == 200:
            print("Database reset successfully")
    except Exception as e:
        # If reset endpoint doesn't exist or fails, continue with unique data approach
        print(f"Reset endpoint not available: {e}")
    yield
