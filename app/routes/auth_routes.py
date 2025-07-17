from flask import Blueprint, jsonify, request  
from app.models.user import User
from app.db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
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

    return jsonify({"message": "User created", "user_id": user.id}), 201

@auth_bp.route('/login' , methods =['POST'] )
def login():
    data = request.get_json()
    user = User.query.filter_by(username = data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Incorect username or password"}), 401
    
    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    })