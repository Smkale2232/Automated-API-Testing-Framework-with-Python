import pytest
import requests


class TestHealthEndpoint:
    """Test cases for /health endpoint"""

    def test_health_check_success(self, api_client):
        """Test health check returns 200 and correct structure"""
        response = api_client('GET', '/health')

        # Status code validation
        assert response.status_code == 200

        # Response body validation
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'version' in data

    def test_health_check_method_not_allowed(self, api_client):
        """Test POST method not allowed for health endpoint"""
        response = api_client('POST', '/health')
        assert response.status_code == 405

    def test_health_check_response_time(self, api_client):
        """Test health check response time is acceptable"""
        import time
        start_time = time.time()
        response = api_client('GET', '/health')
        end_time = time.time()

        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Response within 1 second
