@app.route('/reset', methods=['POST'])
def reset_database():
    """Reset the database (for testing only)"""
    global users_db, user_id_counter
    users_db.clear()
    user_id_counter = 1
    logger.info("Database reset successfully")
    return jsonify({"message": "Database reset successfully"}), 200
