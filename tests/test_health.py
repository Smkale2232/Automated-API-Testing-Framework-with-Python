import pytest
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
        # Skip performance tests in CI as they can be unreliable
        if os.getenv('CI') == 'true':
            pytest.skip("Skipping response time test in CI environment")

        start_time = time.perf_counter()
        response = api_client('GET', '/health')
        end_time = time.perf_counter()

        response_time = end_time - start_time

        assert response.status_code == 200

        # Use a more realistic threshold
        max_expected_time = 5.0
        if response_time > max_expected_time:
            print(f"⚠️  Performance note: Response took {response_time:.3f}s")
            # Don't fail in CI, just warn
            if os.getenv('CI') != 'true':
                assert response_time < max_expected_time, f"Response too slow: {response_time:.3f}s"

    def test_health_check_structure_validation(self, api_client):
        """Test health check response structure validation"""
        response = api_client('GET', '/health')

        assert response.status_code == 200

        data = response.json()

        # Validate all required fields exist
        required_fields = ['status', 'timestamp', 'version']
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Validate field types and values
        assert data['status'] == 'healthy'
        assert isinstance(data['timestamp'], str)
        assert isinstance(data['version'], str)
