from app.extensions import db

class GroupMember(db.Model):
    __tablename__ = 'group_members'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable = False)
    is_admin = db.Column(db.Boolean, default = False)
    joined_at = db.Column(db.DateTime, default = db.func.current_timestamp())

    # Relationships
    user = db.relationship('User', backref='group_memberships')

    # Unique constraint to prevent duplicate memberships
    __table_args__ = (
        db.UniqueConstraint('user_id', 'group_id', name='unique_group_membership'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'is_admin': self.is_admin,
            'joined_at': self.joined_at,
            'username': self.user.username if self.user else None
        } 