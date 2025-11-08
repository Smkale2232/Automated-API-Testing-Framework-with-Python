import pytest
import time


@pytest.mark.integration
class TestUserWorkflowIntegration:
    """Integration tests for complete user workflows"""

    def test_complete_user_lifecycle(self, api_client, unique_user_data):
        """Test complete user lifecycle: create, retrieve, and validate data consistency"""
        print("\n=== Testing Complete User Lifecycle ===")

        # Step 1: Create a new user
        print("1. Creating user...")
        create_response = api_client('POST', '/users', json=unique_user_data)
        assert create_response.status_code == 201, f"User creation failed: {create_response.text}"

        created_user = create_response.json()
        user_id = created_user['id']
        print(f"   ✅ User created with ID: {user_id}")

        # Step 2: Retrieve the created user
        print("2. Retrieving user...")
        get_response = api_client('GET', f'/users/{user_id}')
        assert get_response.status_code == 200, f"User retrieval failed: {get_response.text}"

        retrieved_user = get_response.json()
        print(f"   ✅ User retrieved successfully")

        # Step 3: Validate data consistency
        print("3. Validating data consistency...")
        assert created_user['id'] == retrieved_user['id']
        assert created_user['name'] == retrieved_user['name']
        assert created_user['email'] == retrieved_user['email']
        assert created_user['created_at'] == retrieved_user['created_at']
        print("   ✅ Data consistency validated")

        # Step 4: Verify all required fields are present
        required_fields = ['id', 'name', 'email', 'created_at']
        for field in required_fields:
            assert field in retrieved_user, f"Missing field in response: {field}"

        print("=== User Lifecycle Test Completed Successfully ===\n")

    def test_multiple_user_operations(self, api_client):
        """Test operations with multiple users"""
        print("\n=== Testing Multiple User Operations ===")

        users_data = []

        # Create multiple users
        for i in range(3):
            user_data = {
                "name": f"Multi User {i}",
                "email": f"multi.user{i}_{int(time.time())}@example.com"
            }

            response = api_client('POST', '/users', json=user_data)
            assert response.status_code == 201, f"Failed to create user {i}: {response.text}"

            created_user = response.json()
            users_data.append(created_user)
            print(f"   ✅ Created user {i+1} with ID: {created_user['id']}")

        # Retrieve and validate each user
        for i, user_data in enumerate(users_data):
            user_id = user_data['id']
            response = api_client('GET', f'/users/{user_id}')
            assert response.status_code == 200, f"Failed to retrieve user {user_id}"

            retrieved_user = response.json()
            assert retrieved_user['id'] == user_data['id']
            assert retrieved_user['name'] == user_data['name']
            assert retrieved_user['email'] == user_data['email']
            print(f"   ✅ Verified user {i+1} data consistency")

        print("=== Multiple User Operations Test Completed Successfully ===\n")

    def test_error_scenarios_in_workflow(self, api_client, unique_user_data):
        """Test error scenarios within a workflow context"""
        print("\n=== Testing Error Scenarios in Workflow ===")

        # Step 1: Create a user successfully
        print("1. Creating initial user...")
        response1 = api_client('POST', '/users', json=unique_user_data)
        assert response1.status_code == 201
        user_id = response1.json()['id']
        print(f"   ✅ Initial user created with ID: {user_id}")

        # Step 2: Try to create user with duplicate email (should fail)
        print("2. Testing duplicate email rejection...")
        response2 = api_client('POST', '/users', json=unique_user_data)
        assert response2.status_code == 409
        assert 'already exists' in response2.json()['error'].lower()
        print("   ✅ Duplicate email correctly rejected")

        # Step 3: Try to retrieve non-existent user (should fail)
        print("3. Testing retrieval of non-existent user...")
        response3 = api_client('GET', '/users/9999')
        assert response3.status_code == 404
        assert 'not found' in response3.json()['error'].lower()
        print("   ✅ Non-existent user correctly handled")

        # Step 4: Verify original user still exists and is accessible
        print("4. Verifying original user accessibility...")
        response4 = api_client('GET', f'/users/{user_id}')
        assert response4.status_code == 200
        assert response4.json()['id'] == user_id
        print("   ✅ Original user remains accessible")

        print("=== Error Scenarios Test Completed Successfully ===\n")


@pytest.mark.integration
class TestAPIHealthIntegration:
    """Integration tests for API health and reliability"""

    def test_api_health_under_load(self, api_client):
        """Test API health endpoint under repeated requests"""
        print("\n=== Testing API Health Under Load ===")

        successful_requests = 0
        total_requests = 10

        for i in range(total_requests):
            try:
                response = api_client('GET', '/health')
                if response.status_code == 200:
                    successful_requests += 1
                    print(f"   ✅ Request {i+1}/{total_requests}: Success")
                else:
                    print(
                        f"   ❌ Request {i+1}/{total_requests}: Failed with status {response.status_code}")
            except Exception as e:
                print(f"   ❌ Request {i+1}/{total_requests}: Exception {e}")

            # Small delay between requests
            time.sleep(0.1)

        success_rate = (successful_requests / total_requests) * 100
        print(
            f"   📊 Success Rate: {success_rate:.1f}% ({successful_requests}/{total_requests})")

        # Allow for some failures in a demo environment
        assert success_rate >= 80.0, f"API reliability below 80%: {success_rate:.1f}%"

        print("=== API Health Under Load Test Completed Successfully ===\n")

    def test_concurrent_operations(self, api_client):
        """Test basic concurrent operations (simulated)"""
        print("\n=== Testing Concurrent Operations ===")

        # Create multiple users in sequence (simulating concurrent operations)
        user_ids = []

        for i in range(3):
            user_data = {
                "name": f"Concurrent User {i}",
                "email": f"concurrent.user{i}_{int(time.time()*1000)}@example.com"
            }

            response = api_client('POST', '/users', json=user_data)
            assert response.status_code == 201, f"Failed to create user in concurrent test: {response.text}"

            user_id = response.json()['id']
            user_ids.append(user_id)
            print(f"   ✅ Created user {i+1} with ID: {user_id}")

        # Verify all users can be retrieved
        for i, user_id in enumerate(user_ids):
            response = api_client('GET', f'/users/{user_id}')
            assert response.status_code == 200, f"Failed to retrieve user {user_id}"
            print(f"   ✅ Verified user {i+1} with ID: {user_id}")

        print("=== Concurrent Operations Test Completed Successfully ===\n")
