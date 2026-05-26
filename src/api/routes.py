from flask import request, jsonify, Blueprint
from api.models import db, User
from api.utils import create_token, verify_token

api = Blueprint('api', __name__)

@api.route('/signup', methods=['POST'])
def signup():
    try:
        body = request.get_json()
        
        if not body or 'email' not in body or 'password' not in body:
            return jsonify({"error": "Email and password are required"}), 400
        
        email = body.get('email')
        password = body.get('password')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 400
        
        new_user = User(email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        token = create_token(new_user.id, new_user.email)
        
        return jsonify({
            "message": "User created successfully",
            "token": token,
            "user": new_user.serialize()
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/login', methods=['POST'])
def login():
    try:
        body = request.get_json()
        
        if not body or 'email' not in body or 'password' not in body:
            return jsonify({"error": "Email and password are required"}), 400
        
        email = body.get('email')
        password = body.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        token = create_token(user.id, user.email)
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": user.serialize()
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/private', methods=['GET'])
def private():
    try:
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid token"}), 401
        
        token = auth_header.split(' ')[1]
        user_data = verify_token(token)
        
        if not user_data:
            return jsonify({"error": "Invalid token"}), 401
        
        user = User.query.get(user_data.get('user_id'))
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "message": "Access granted to private area",
            "user": user.serialize()
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
