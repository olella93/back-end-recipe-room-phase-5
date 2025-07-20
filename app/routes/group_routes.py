from flask import Blueprint, jsonify, request
from app.models.group import Group
from app.models.group_member import GroupMember
from app.extensions import db

group_bp = Blueprint('group', __name__)

@group_bp.route('/groups', methods =['POST'])
def create_group():
    data = request.get_json()
    new_group = Group(
        name = data['name'],
        description = data.get('description', '')
    ) 

    db.session.add(new_group)
    db.session.commit()

    member = GroupMember(
        user_id=data['user_id'],
        group_id=new_group.id,
        is_admin = True
    )

    db.session.add(member)
    db.session.commit()

    return jsonify({"message": "Group created", "group_id": new_group.id}), 201