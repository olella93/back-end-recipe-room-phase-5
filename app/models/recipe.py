from app.db import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False)
    ingredients = db.Column(db.Text, nullable = False)
    instructions = db.Column(db.Text, nullable = False)
    country = db.Column(db.String(50))
    serving_size = db.Column(db.Integer)
    created_at = db.Column(db.Datetime, default = db.func.current_timestamp())
    updated_at = db.Column(db.Datetime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())  

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))