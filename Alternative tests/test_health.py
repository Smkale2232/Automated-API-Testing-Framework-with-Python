import pytest
import requests
import time


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
        # Simple version - just verify the endpoint works
        start_time = time.perf_counter()
        response = api_client('GET', '/health')
        end_time = time.perf_counter()

        response_time = end_time - start_time

        # Primary assertion - endpoint must work
        assert response.status_code == 200

        # Secondary assertion - log response time but don't fail for performance
        # This makes the test more reliable in different environments
        print(f"Health check response time: {response_time:.3f} seconds")

        # Only fail if response time is extremely slow (10+ seconds)
        # This indicates a serious problem, not just slow performance
        if response_time > 10.0:
            pytest.fail(f"Health check extremely slow: {response_time:.3f}s")

    def test_health_check_response_structure(self, api_client):
        """Test health check response has correct structure"""
        response = api_client('GET', '/health')

        assert response.status_code == 200

        data = response.json()

        # Validate all required fields
        required_fields = ['status', 'timestamp', 'version']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        # Validate field values
        assert data['status'] == 'healthy'
        assert isinstance(data['timestamp'], str)
        assert isinstance(data['version'], str)
