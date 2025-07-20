from flask import Blueprint, jsonify, request  
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token
# from app.schemas.user_schema import UserSchema  # Temporarily commented out
# user_schema = UserSchema()  # Temporarily commented out



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    required = ['username', 'email', 'password']
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username = data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    if User.query.filter_by(email = data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    user = User(
        username = data['username'],
        email = data['email']  
    )

    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile_image": user.profile_image,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 201

@auth_bp.route('/login' , methods =['POST'] )
def login():
    data = request.get_json()
    required = ['username', 'password']
    if not all(field in data for field in required):
     return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username = data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Incorect username or password"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile_image": user.profile_image,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }), 200