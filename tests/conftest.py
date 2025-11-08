import pytest
import requests
from src.api.app import app as flask_app
import threading
import time
from config.config import TestingConfig


@pytest.fixture(scope='session')
def app():
    """Fixture to start Flask app for testing"""
    config = TestingConfig()

    def run_app():
        flask_app.run(port=5000, debug=False, use_reloader=False)

    # Start the app in a separate thread
    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()

    # Wait for app to start
    time.sleep(2)

    yield flask_app


@pytest.fixture
def client(app):
    """Test client fixture"""
    return app.test_client()


@pytest.fixture
def base_url():
    """Base URL for API requests"""
    return TestingConfig().API_BASE_URL


@pytest.fixture
def api_client(base_url):
    """API client for making requests"""
    session = requests.Session()
    session.timeout = TestingConfig().TIMEOUT

    def _make_request(method, endpoint, **kwargs):
        url = f"{base_url}{endpoint}"
        return session.request(method, url, **kwargs)

    return _make_request


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the database before each test"""
    from src.api.app import users_db, user_id_counter
    users_db.clear()
    user_id_counter = 1
