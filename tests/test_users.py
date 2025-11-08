import pytest
import json


class TestUserCreation:
    """Test cases for POST /users endpoint"""

    def test_create_user_success(self, api_client):
        """Test successful user creation"""
        user_data = {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }

        response = api_client('POST', '/users', json=user_data)

        # Status code validation
        assert response.status_code == 201

        # Response body validation
        data = response.json()
        assert data['name'] == user_data['name']
        assert data['email'] == user_data['email']
        assert 'id' in data
        assert 'created_at' in data

    def test_create_user_missing_name(self, api_client):
        """Test user creation with missing name field"""
        user_data = {
            "email": "john.doe@example.com"
        }

        response = api_client('POST', '/users', json=user_data)

        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'name' in data['error'].lower()

    def test_create_user_missing_email(self, api_client):
        """Test user creation with missing email field"""
        user_data = {
            "name": "John Doe"
        }

        response = api_client('POST', '/users', json=user_data)

        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'email' in data['error'].lower()

    def test_create_user_invalid_email(self, api_client):
        """Test user creation with invalid email format"""
        user_data = {
            "name": "John Doe",
            "email": "invalid-email"
        }

        response = api_client('POST', '/users', json=user_data)

        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'email' in data['error'].lower()

    def test_create_user_duplicate_email(self, api_client):
        """Test user creation with duplicate email"""
        user_data = {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }

        # First request should succeed
        response1 = api_client('POST', '/users', json=user_data)
        assert response1.status_code == 201

        # Second request should fail
        response2 = api_client('POST', '/users', json=user_data)
        assert response2.status_code == 409
        data = response2.json()
        assert 'error' in data
        assert 'already exists' in data['error'].lower()

    def test_create_user_invalid_content_type(self, api_client):
        """Test user creation with invalid content type"""
        user_data = {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }

        response = api_client('POST', '/users', data=user_data)

        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'content-type' in data['error'].lower()


class TestGetUser:
    """Test cases for GET /users/{id} endpoint"""

    def test_get_user_success(self, api_client):
        """Test successful user retrieval"""
        # First create a user
        user_data = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com"
        }
        create_response = api_client('POST', '/users', json=user_data)
        user_id = create_response.json()['id']

        # Then retrieve the user
        response = api_client('GET', f'/users/{user_id}')

        assert response.status_code == 200
        data = response.json()
        assert data['id'] == user_id
        assert data['name'] == user_data['name']
        assert data['email'] == user_data['email']

    def test_get_user_not_found(self, api_client):
        """Test retrieving non-existent user"""
        response = api_client('GET', '/users/999')

        assert response.status_code == 404
        data = response.json()
        assert 'error' in data
        assert 'not found' in data['error'].lower()

    def test_get_user_invalid_id(self, api_client):
        """Test retrieving user with invalid ID"""
        response = api_client('GET', '/users/invalid')

        assert response.status_code == 404  # Flask converts to 404 for non-int IDs


class TestUserIntegration:
    """Integration test cases for user workflow"""

    def test_full_user_workflow(self, api_client):
        """Test complete user creation and retrieval workflow"""
        # Create user
        user_data = {
            "name": "Integration Test User",
            "email": "integration@example.com"
        }
        create_response = api_client('POST', '/users', json=user_data)
        assert create_response.status_code == 201

        created_user = create_response.json()
        user_id = created_user['id']

        # Retrieve user
        get_response = api_client('GET', f'/users/{user_id}')
        assert get_response.status_code == 200

        retrieved_user = get_response.json()

        # Verify data consistency
        assert created_user['id'] == retrieved_user['id']
        assert created_user['name'] == retrieved_user['name']
        assert created_user['email'] == retrieved_user['email']
        assert created_user['created_at'] == retrieved_user['created_at']
