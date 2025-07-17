from app.db import db

class GroupMember(db.Model):
    __tablename__ = 'group_members'

    id = db.Colunm(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable = False)
    is_admin = db.Column(db.Boolean, default = False)
    joined_at = db.Column(db.Datetime, default = db.func.current_timestamp()) 