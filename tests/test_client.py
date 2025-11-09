"""
Test client configuration for CI environments
"""
import pytest
from src.api.app import app


@pytest.fixture
def test_client():
    """Provide test client for CI environment"""
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers():
    """Provide authentication headers if needed"""
    return {'Content-Type': 'application/json'}
