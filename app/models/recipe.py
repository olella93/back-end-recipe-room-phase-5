from app.extensions import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False)
    ingredients = db.Column(db.Text, nullable = False)
    instructions = db.Column(db.Text, nullable = False)
    country = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    serving_size = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default = db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())  

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True) 

    user = db.relationship('User', backref='recipes')
    group = db.relationship('Group', backref='recipes')
    bookmarks = db.relationship('Bookmark', back_populates='recipe', cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='recipe', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='recipe', cascade='all, delete-orphan')
