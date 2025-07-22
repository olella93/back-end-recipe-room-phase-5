from flask import Blueprint, jsonify, request  
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils.cloudinary_upload import upload_profile_image




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

# ------------------ UPLOAD PROFILE IMAGE ------------------ #
@auth_bp.route('/upload-profile-image', methods=['POST'])
@jwt_required()
def upload_user_profile_image():
    """Upload and update user's profile image"""
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    
    # Check if file is present in request
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if not file or file.filename == '':
        return jsonify({"error": "No image file selected"}), 400
    
    try:
        # Upload to Cloudinary
        success, result = upload_profile_image(file, user_id)
        
        if not success:
            return jsonify({"error": result}), 400
        
        # Update user's profile image URL
        user.profile_image = result['url']
        db.session.commit()
        
        return jsonify({
            "message": "Profile image uploaded successfully",
            "profile_image": result['url'],
            "upload_details": {
                "width": result.get('width'),
                "height": result.get('height'),
                "format": result.get('format'),
                "size_bytes": result.get('bytes')
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

# ------------------ UPDATE USER PROFILE ------------------ #
@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile information"""
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    
    # Update fields if provided
    if 'username' in data:
        # Check if username is already taken by another user
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"error": "Username already exists"}), 400
        user.username = data['username']
    
    if 'email' in data:
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"error": "Email already exists"}), 400
        user.email = data['email']
    
    if 'profile_image' in data:
        user.profile_image = data['profile_image']
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Profile updated successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_image": user.profile_image,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Update failed: {str(e)}"}), 500

# ------------------ GET USER PROFILE ------------------ #
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile information"""
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile_image": user.profile_image,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 200