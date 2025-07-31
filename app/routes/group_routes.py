from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import IntegrityError

group_bp = Blueprint('group', __name__)

# ------------------ GET ALL GROUPS ------------------ #
@group_bp.route('/groups', methods=['GET'])
def get_groups():
    """Get all groups with basic information"""
    groups = Group.query.all()
    
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
    result = []
    # Try to get current user id if JWT is present
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except Exception:
        user_id = None

    for group in groups:
        current_user_is_admin = False
        current_user_is_member = False
        if user_id:
            member = next((m for m in group.members if m.user_id == int(user_id)), None)
            current_user_is_member = bool(member)
            current_user_is_admin = bool(member and member.is_admin)
        result.append({
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "created_at": group.created_at,
            "member_count": len(group.members),
            "current_user_is_admin": current_user_is_admin,
            "current_user_is_member": current_user_is_member
        })
    return jsonify(result), 200

# ------------------ CREATE GROUP ------------------ #
@group_bp.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    """Create a new group with the current user as admin"""
    user_id = int(get_jwt_identity())
    data = request.get_json()

    # Validate required fields
    required_fields = ['name']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Create the group
        new_group = Group(
            name=data['name'],
            description=data.get('description', '')
        )

        db.session.add(new_group)
        db.session.flush()  

        # Add creator as admin member
        admin_member = GroupMember(
            user_id=user_id,
            group_id=new_group.id,
            is_admin=True
        )

        db.session.add(admin_member)
        db.session.commit()

        return jsonify({
            "message": "Group created successfully",
            "group_id": new_group.id,
            "group": new_group.to_dict()
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Group name might already exist"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ------------------ GET SINGLE GROUP ------------------ #
@group_bp.route('/groups/<int:group_id>', methods=['GET'])
def get_single_group(group_id):
    """Get detailed information about a specific group"""
    group = Group.query.get_or_404(group_id)

    # Get user info if JWT provided
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except Exception:
        user_id = None

    current_user_is_admin = False
    current_user_is_member = False
    if user_id:
        member = next((m for m in group.members if m.user_id == int(user_id)), None)
        current_user_is_member = bool(member)
        current_user_is_admin = bool(member and member.is_admin)

    members = []
    for member in group.members:
        members.append({
            "user_id": member.user_id,
            "username": member.user.username,
            "is_admin": member.is_admin,
            "joined_at": member.joined_at
        })

    return jsonify({
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "created_at": group.created_at,
        "member_count": len(group.members),
        "members": members,
        "current_user_is_member": current_user_is_member,
        "current_user_is_admin": current_user_is_admin
    }), 200

# ------------------ UPDATE GROUP ------------------ #
@group_bp.route('/groups/<int:group_id>', methods=['PUT'])
@jwt_required()
def update_group(group_id):
    """Update group information (admin only)"""
    user_id = int(get_jwt_identity())
    group = Group.query.get_or_404(group_id)

    # Check if user is admin of this group
    member = GroupMember.query.filter_by(
        user_id=user_id, 
        group_id=group_id, 
        is_admin=True
    ).first()
    
    if not member:
        return jsonify({"error": "Unauthorized - Admin access required"}), 403

    data = request.get_json()
    
    # Update group fields
    if 'name' in data:
        group.name = data['name']
    if 'description' in data:
        group.description = data['description']

    try:
        db.session.commit()
        return jsonify({
            "message": "Group updated successfully",
            "group": group.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ------------------ DELETE GROUP ------------------ #
@group_bp.route('/groups/<int:group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    """Delete a group (admin only)"""
    user_id = int(get_jwt_identity())
    group = Group.query.get_or_404(group_id)

    # Check if user is admin of this group
    member = GroupMember.query.filter_by(
        user_id=user_id, 
        group_id=group_id, 
        is_admin=True
    ).first()
    
    if not member:
        return jsonify({"error": "Unauthorized - Admin access required"}), 403

    try:
        db.session.delete(group)
        db.session.commit()
        return jsonify({"message": "Group deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ------------------ JOIN GROUP ------------------ #
@group_bp.route('/groups/<int:group_id>/join', methods=['POST'])
@jwt_required()
def join_group(group_id):
    """Join a group as a regular member"""
    user_id = int(get_jwt_identity())
    group = Group.query.get_or_404(group_id)

    # Check if user is already a member
    existing_member = GroupMember.query.filter_by(
        user_id=user_id, 
        group_id=group_id
    ).first()
    
    if existing_member:
        return jsonify({"error": "You are already a member of this group"}), 400

    try:
        new_member = GroupMember(
            user_id=user_id,
            group_id=group_id,
            is_admin=False
        )

        db.session.add(new_member)
        db.session.commit()

        return jsonify({
            "message": "Successfully joined the group",
            "membership": new_member.to_dict()
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "You are already a member of this group"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ------------------ LEAVE GROUP ------------------ #
@group_bp.route('/groups/<int:group_id>/leave', methods=['DELETE'])
@jwt_required()
def leave_group(group_id):
    """Leave a group"""
    user_id = int(get_jwt_identity())
    
    member = GroupMember.query.filter_by(
        user_id=user_id, 
        group_id=group_id
    ).first()
    
    if not member:
        return jsonify({"error": "You are not a member of this group"}), 400

    try:
        db.session.delete(member)
        db.session.commit()
        return jsonify({"message": "Successfully left the group"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ------------------ MANAGE MEMBER ADMIN STATUS ------------------ #
@group_bp.route('/groups/<int:group_id>/members/<int:member_user_id>/admin', methods=['PUT'])
@jwt_required()
def toggle_admin_status(group_id, member_user_id):
    """Promote/demote a member to/from admin (admin only)"""
    user_id = int(get_jwt_identity())
    
    # Check if current user is admin of this group
    admin_member = GroupMember.query.filter_by(
        user_id=user_id, 
        group_id=group_id, 
        is_admin=True
    ).first()
    
    if not admin_member:
        return jsonify({"error": "Unauthorized - Admin access required"}), 403

    # Find the member to modify
    target_member = GroupMember.query.filter_by(
        user_id=member_user_id, 
        group_id=group_id
    ).first()
    
    if not target_member:
        return jsonify({"error": "User is not a member of this group"}), 404

    data = request.get_json()
    is_admin = data.get('is_admin', False)

    try:
        target_member.is_admin = is_admin
        db.session.commit()
        
        action = "promoted to admin" if is_admin else "demoted from admin"
        return jsonify({
            "message": f"Member {action} successfully",
            "membership": target_member.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ------------------ REMOVE MEMBER FROM GROUP ------------------ #
@group_bp.route('/groups/<int:group_id>/members/<int:member_user_id>', methods=['DELETE'])
@jwt_required()
def remove_member(group_id, member_user_id):
    """Remove a member from the group (admin only)"""
    user_id = int(get_jwt_identity())
    
    # Check if current user is admin of this group
    admin_member = GroupMember.query.filter_by(
        user_id=user_id, 
        group_id=group_id, 
        is_admin=True
    ).first()
    
    if not admin_member:
        return jsonify({"error": "Unauthorized - Admin access required"}), 403

    # Find the member to remove
    target_member = GroupMember.query.filter_by(
        user_id=member_user_id, 
        group_id=group_id
    ).first()
    
    if not target_member:
        return jsonify({"error": "User is not a member of this group"}), 404

    # Prevent admin from removing themselves (they should leave instead)
    if user_id == member_user_id:
        return jsonify({"error": "Use leave endpoint to remove yourself from the group"}), 400

    try:
        db.session.delete(target_member)
        db.session.commit()
        return jsonify({"message": "Member removed from group successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ------------------ GET USER'S GROUPS ------------------ #
@group_bp.route('/my-groups', methods=['GET'])
@jwt_required()
def get_my_groups():
    """Get all groups that the current user is a member of"""
    user_id = int(get_jwt_identity())
    
    memberships = GroupMember.query.filter_by(user_id=user_id).all()
    
    result = []
    for membership in memberships:
        group = membership.group
        result.append({
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "created_at": group.created_at,
            "member_count": len(group.members),
            "is_admin": membership.is_admin,
            "joined_at": membership.joined_at
        })
    
    return jsonify(result), 200