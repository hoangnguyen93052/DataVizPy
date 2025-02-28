import time
import jwt
from flask import Flask, request, jsonify, g
from functools import wraps
from flask_limiter import Limiter, RateLimitExceeded
from flask_cors import CORS
import logging
import traceback
from werkzeug.exceptions import Unauthorized

# Configuration
SECRET_KEY = 'your_secret_key'
JWT_EXPIRATION_DELTA = 3600  # token expiration time in seconds
LIMIT = "100/hour"  # rate limit configuration

# Initialize Flask app and extensions
app = Flask(__name__)
CORS(app)
limiter = Limiter(app, key_func=lambda: request.headers.get('X-API-KEY'))

# Set up logging
logging.basicConfig(level=logging.INFO)

# A dummy user database for example purposes
users_db = {
    "user1": "password1",
    "user2": "password2"
}

# Token generation
def generate_token(username):
    payload = {
        'sub': username,
        'exp': time.time() + JWT_EXPIRATION_DELTA
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Token verification
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired.")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token.")

# Rate limit error handler
@app.errorhandler(RateLimitExceeded)
def handle_rate_limit_error(e):
    return jsonify(error="Rate limit exceeded.", message=str(e.description)), 429

# Middleware for checking token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            raise Unauthorized("Token is missing.")
        try:
            username = verify_token(token.split(" ")[1])
        except Unauthorized as e:
            return jsonify(message=str(e)), 401
        g.username = username
        return f(*args, **kwargs)
    return decorated

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    auth_data = request.json
    username = auth_data.get('username')
    password = auth_data.get('password')

    if username in users_db and users_db[username] == password:
        token = generate_token(username)
        return jsonify(token=token), 200
    return jsonify(message="Invalid credentials."), 401

# Sample API endpoint
@app.route('/api/resource', methods=['GET'])
@token_required
@limiter.limit(LIMIT)
def protected_resource():
    return jsonify(message=f"Welcome {g.username}, here is your protected resource."), 200

# Error handler for internal server errors
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error("An error occurred: %s", traceback.format_exc())
    return jsonify(error="Internal Server Error", message=str(e)), 500

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)