from flask import Flask, request, jsonify
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory storage for demo purposes
users_db = {}
user_id_counter = 1


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }), 200


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    global user_id_counter

    logger.info("Create user endpoint called")

    # Validate request content type
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Validate email format
    if '@' not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400

    # Check if email already exists
    for user in users_db.values():
        if user['email'] == data['email']:
            return jsonify({"error": "Email already exists"}), 409

    # Create user
    user_id = user_id_counter
    users_db[user_id] = {
        'id': user_id,
        'name': data['name'],
        'email': data['email'],
        'created_at': datetime.utcnow().isoformat()
    }

    user_id_counter += 1

    logger.info(f"User created with ID: {user_id}")
    return jsonify(users_db[user_id]), 201


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details by ID"""
    logger.info(f"Get user endpoint called for ID: {user_id}")

    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404

    return jsonify(users_db[user_id]), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
