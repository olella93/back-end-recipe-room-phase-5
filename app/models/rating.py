from app.extensions import db

class Rating(db.Model):
    __tablename__ = 'ratings' 

    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable = False)
    created_at = db.Column(db.DateTime, default = db.func.current_timestamp())