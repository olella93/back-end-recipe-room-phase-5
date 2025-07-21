from app.extensions import db

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default = db.func.current_timestamp())

    # Relationships
    members = db.relationship('GroupMember', backref='group', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'member_count': len(self.members) if self.members else 0
        }