from app.db import db

class Rating(db.Model):
    _tablename__ = 'ratings' 

    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    recipe_id = id.Column(db.Integer, db.ForeignKey('recipes.id'), nullable = False)
    created_at = id.Column(db.Datetime, default = db.func.current_timestamp())