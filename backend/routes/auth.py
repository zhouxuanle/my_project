from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import uuid
import logging
from database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_id = f"{uuid.uuid4()}_{username}"

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check if user exists
            cursor.execute("SELECT id FROM app_users WHERE username = %s", (username,))
            if cursor.fetchone():
                return jsonify({"msg": "Username already exists"}), 400
            # Create user
            password_hash = generate_password_hash(password)
            cursor.execute("INSERT INTO app_users (user_id, username, password_hash) VALUES (%s, %s, %s)", (user_id, username, password_hash))
            connection.commit()

        return jsonify({"msg": "User created successfully"}), 201
    except Exception as e:
        logging.error(f"Register error: {str(e)}")
        return jsonify({"msg": "Error creating user"}), 500
    finally:
        if connection:
            connection.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, password_hash FROM app_users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password_hash'], password):
                # Identity must be a string for flask-jwt-extended
                access_token = create_access_token(identity=str(user['user_id']))
                refresh_token = create_refresh_token(identity=str(user['user_id']))
                return jsonify(access_token=access_token, refresh_token=refresh_token, user_id=user['user_id']), 200
            else:
                return jsonify({"msg": "Invalid username or password"}), 401
    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({"msg": "Login error"}), 500
    finally:
        if connection:
            connection.close()


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh endpoint: accepts a refresh token and returns a new access token."""
    try:
        identity = get_jwt_identity()
        new_access = create_access_token(identity=identity)
        return jsonify(access_token=new_access), 200
    except Exception as e:
        logging.error(f"Refresh token error: {str(e)}")
        return jsonify({"msg": "Token refresh failed"}), 401
