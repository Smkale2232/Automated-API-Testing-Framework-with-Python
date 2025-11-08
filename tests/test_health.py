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
        # Measure multiple requests and take the average
        response_times = []

        for i in range(3):  # Take 3 measurements
            start_time = time.perf_counter()
            response = api_client('GET', '/health')
            end_time = time.perf_counter()

            assert response.status_code == 200
            response_time = end_time - start_time
            response_times.append(response_time)
            time.sleep(0.1)  # Small delay between requests

        average_response_time = sum(response_times) / len(response_times)
        print(f"Response times: {response_times}")
        print(f"Average response time: {average_response_time:.3f} seconds")

        # Use a more realistic threshold - 3 seconds for local development
        assert average_response_time < 3.0, f"Average response time {average_response_time:.3f}s exceeds 3.0s threshold"

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

        # Validate timestamp format (ISO 8601)
        try:
            from datetime import datetime
            datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {data['timestamp']}")
